#!/usr/bin/env python3
import argparse
import json
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET


SECTION_HEADINGS = [
    "Education",
    "Research Experience",
    "Publications",
    "Presentations",
    "Public Datasets / Data Resources",
    "Leadership & Activities",
    "Skills & Interests",
    "Additional Academic Service",
    "Grants",
    "References",
]

MONTH_MAP = {
    "jan": "Jan", "january": "Jan",
    "feb": "Feb", "february": "Feb",
    "mar": "Mar", "march": "Mar",
    "apr": "Apr", "april": "Apr",
    "may": "May",
    "jun": "Jun", "june": "Jun",
    "jul": "Jul", "july": "Jul",
    "aug": "Aug", "august": "Aug",
    "sep": "Sep", "sept": "Sep", "september": "Sep",
    "oct": "Oct", "october": "Oct",
    "nov": "Nov", "november": "Nov",
    "dec": "Dec", "december": "Dec",
}


def clean(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def read_docx_paragraphs(path):
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lines = []
    for paragraph in root.findall(".//w:p", ns):
        parts = [node.text or "" for node in paragraph.findall(".//w:t", ns)]
        text = clean("".join(parts))
        if text:
            lines.append(text)
    return lines


def find_cv_path(data, repo_root):
    raw = clean(data.get("hero", {}).get("cv", ""))
    if raw and not re.match(r"^https?://", raw, flags=re.I):
        candidate = repo_root / raw.lstrip("./")
        if candidate.exists():
            return candidate

    candidates = []
    for pattern in ("media/files/*CV*.docx", "media/files/*cv*.docx", "*CV*.docx", "*cv*.docx"):
        candidates.extend(repo_root.glob(pattern))

    unique = []
    seen = set()
    for item in candidates:
        key = str(item.resolve())
        if key not in seen:
            unique.append(item)
            seen.add(key)

    if unique:
        return unique[0]
    return None


def section(lines, heading):
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []

    stop = len(lines)
    for next_heading in SECTION_HEADINGS:
        if next_heading == heading:
            continue
        try:
            idx = lines.index(next_heading, start)
            stop = min(stop, idx)
        except ValueError:
            pass
    return lines[start:stop]


def remove_author_prefix(text):
    return re.sub(r"^Hwang K,\s*et al\.\s*", "", clean(text), flags=re.I)


def normalize_meta(meta):
    value = clean(meta)
    value = re.sub(r"\s*;\s*", " · ", value)
    value = re.sub(r"\.\s*(Oral presentation|Poster presentation)\.?$", r" · \1", value, flags=re.I)
    value = re.sub(r"\s{2,}", " ", value)
    return value.rstrip(". ")


def parse_presentations(lines):
    entries = []
    markers = [
        "Korean Urological Association",
        "KUA Annual Meeting",
        "Urological Research Society",
        "URS Annual Meeting",
        "AACR Annual Meeting",
    ]

    for idx, raw in enumerate(section(lines, "Presentations")):
        text = remove_author_prefix(raw)
        positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
        if not positions:
            continue
        split_at = min(positions)
        title = text[:split_at].strip()
        meta = text[split_at:].strip()
        title = title.rstrip()
        if title and not title.endswith("."):
            title += "."
        year_match = re.search(r"\b(20\d{2})\b", meta)
        year = int(year_match.group(1)) if year_match else 0
        entries.append({
            "title": title,
            "meta": normalize_meta(meta),
            "_year": year,
            "_idx": idx,
        })

    entries.sort(key=lambda x: (x["_year"], x["_idx"]), reverse=True)
    return [{"title": x["title"], "meta": x["meta"]} for x in entries]


def parse_toolkit(lines):
    skill_lines = section(lines, "Skills & Interests")
    if not skill_lines:
        return []

    output = []
    mode = None
    for i, line in enumerate(skill_lines):
        if line == "Technical":
            mode = "technical"
            continue
        if line == "Programming":
            mode = "programming"
            continue
        if line in {"Certification"}:
            break

        if mode == "technical" and ":" in line:
            output.append(line)
        elif mode == "programming" and line:
            output.append(f"Programming: {line}")
            mode = None

    return output


def parse_publication(lines):
    pubs = section(lines, "Publications")
    if not pubs:
        return None

    raw = clean(pubs[0])
    year_match = re.search(r"\b(20\d{2})\b", raw)
    year = year_match.group(1) if year_match else ""

    status_match = re.search(
        r"\b(Under revision at|Under review at|Accepted at|In press at|Published in|Preprint at)\s+(.+?)(?:,\s*20\d{2})?\.?$",
        raw,
        flags=re.I,
    )

    if status_match:
        status_phrase = clean(status_match.group(1))
        journal = clean(status_match.group(2)).rstrip("., ")
        citation = raw[:status_match.start()].rstrip()
        if citation and not citation.endswith("."):
            citation += "."
        if status_phrase.lower() == "under revision at":
            journal_text = f"Manuscript under revision at {journal}."
            status = f"Under revision · {journal}"
        elif status_phrase.lower() == "under review at":
            journal_text = f"Manuscript under review at {journal}."
            status = f"Under review · {journal}"
        else:
            journal_text = f"{status_phrase} {journal}."
            status = f"{status_phrase} · {journal}"
    else:
        citation = raw
        journal_text = ""
        status = ""

    return {
        "citation": citation,
        "year": year,
        "journalText": journal_text,
        "status": status,
    }


def parse_resources(lines, existing):
    resource_lines = section(lines, "Public Datasets / Data Resources")
    result = deepcopy(existing or [])

    geo_text = " ".join(resource_lines)
    geo_match = re.search(r"\b(GSE\d+)\b", geo_text, flags=re.I)
    doi_match = re.search(r"https?://doi\.org/(10\.\d{4,9}/[^\s,\]]+)", geo_text, flags=re.I)
    if not doi_match:
        doi_match = re.search(r"\b(10\.\d{4,9}/[^\s,\]]+)", geo_text, flags=re.I)

    def get_or_add(label, defaults):
        for item in result:
            if clean(item.get("label", "")).lower() == label.lower():
                return item
        item = dict(defaults)
        result.append(item)
        return item

    if geo_match:
        accession = geo_match.group(1).upper()
        item = get_or_add("GEO", {
            "label": "GEO",
            "title": accession,
            "text": "Public dataset listed in the current CV.",
            "url": "",
            "button": "View GEO record",
        })
        item["title"] = accession
        item["url"] = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}"

    if doi_match:
        doi = doi_match.group(1).rstrip(".,")
        item = get_or_add("Zenodo", {
            "label": "Zenodo",
            "title": "Research data resource",
            "text": "Public data resource listed in the current CV.",
            "url": "",
            "button": "View Zenodo record",
        })
        item["url"] = f"https://doi.org/{doi}"

    return result


def month_token(value):
    key = clean(value).lower().rstrip(".")
    return MONTH_MAP.get(key, value.title().rstrip("."))


def normalize_date_span(text):
    text = clean(text).replace("–", "-").replace("—", "-")
    summer = re.search(r"\b(Summer|Spring|Fall|Winter)\s+(20\d{2})\b", text, flags=re.I)
    if summer:
        return f"{summer.group(1).title()} {summer.group(2)}"

    pattern = re.compile(
        r"\b("
        r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
        r")\.?\s*(20\d{2})"
        r"(?:\s*-\s*("
        r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|current|present"
        r")\.?\s*(20\d{2})?)?",
        flags=re.I,
    )
    match = pattern.search(text)
    if not match:
        return ""

    start = f"{month_token(match.group(1))} {match.group(2)}"
    end_token = match.group(3)
    end_year = match.group(4)
    if not end_token:
        return start

    if end_token.lower() in {"current", "present"}:
        end = "Present"
    else:
        end = month_token(end_token)
        if end_year:
            end += f" {end_year}"
    return f"{start} — {end}"


def find_date_near(lines, phrase, lookahead=2):
    phrase_lower = phrase.lower()
    for idx, line in enumerate(lines):
        if phrase_lower in line.lower():
            candidates = [line] + lines[idx + 1:idx + 1 + lookahead]
            for candidate in candidates:
                date = normalize_date_span(candidate)
                if date:
                    return date
    return ""


def update_trajectory_dates(lines, existing):
    result = deepcopy(existing or [])
    education = section(lines, "Education")
    research = section(lines, "Research Experience")

    dates = {
        "city of hope": find_date_near(education, "City of Hope", 3),
        "unc lineberger": find_date_near(research, "University of North Carolina", 1),
        "saihst": find_date_near(education, "Samsung Advanced Institute", 2),
        "korea university": find_date_near(research, "Korea University College of Medicine", 1),
        "kyung hee": find_date_near(education, "Kyunghee University", 2),
    }

    for item in result:
        title = clean(item.get("title", "")).lower()
        target = ""
        if "city of hope" in title:
            target = dates["city of hope"]
        elif "unc" in title or "lineberger" in title:
            target = dates["unc lineberger"]
        elif "saihst" in title or "sungkyunkwan" in title:
            target = dates["saihst"]
        elif "korea university" in title:
            target = dates["korea university"]
        elif "kyung hee" in title or "kyunghee" in title:
            target = dates["kyung hee"]
        if target:
            item["when"] = target

    return result, dates


def parse_email(lines):
    joined = " ".join(lines[:8])
    match = re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", joined, flags=re.I)
    return match.group(0) if match else ""


def summarize_changes(before, after):
    changed = []
    for key in ["hero", "selectedWork", "trajectory", "presentations", "toolkit", "resources"]:
        if before.get(key) != after.get(key):
            changed.append(key)
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data.json")
    parser.add_argument("--report", default="/tmp/cv-sync-report.md")
    args = parser.parse_args()

    repo_root = Path.cwd()
    data_path = repo_root / args.data
    if not data_path.exists():
        raise SystemExit(f"Missing {args.data}")

    before = json.loads(data_path.read_text(encoding="utf-8"))
    after = deepcopy(before)

    cv_path = find_cv_path(after, repo_root)
    if cv_path is None:
        raise SystemExit("Could not locate a CV file. Check hero.cv in data.json.")
    if cv_path.suffix.lower() != ".docx":
        raise SystemExit(
            f"CV sync currently supports DOCX. The configured CV is: {cv_path.as_posix()}"
        )

    lines = read_docx_paragraphs(cv_path)

    email = parse_email(lines)
    if email:
        after.setdefault("hero", {})["email"] = email

    presentations = parse_presentations(lines)
    if presentations:
        after["presentations"] = presentations

    toolkit = parse_toolkit(lines)
    if toolkit:
        after["toolkit"] = toolkit

    publication = parse_publication(lines)
    if publication:
        selected = after.setdefault("selectedWork", {})
        for field in ["citation", "year", "journalText", "status"]:
            if publication.get(field):
                selected[field] = publication[field]

    after["resources"] = parse_resources(lines, after.get("resources", []))
    trajectory, detected_dates = update_trajectory_dates(lines, after.get("trajectory", []))
    after["trajectory"] = trajectory

    changed = summarize_changes(before, after)
    data_path.write_text(json.dumps(after, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = [
        "# CV → website sync review",
        "",
        f"CV parsed: `{cv_path.as_posix()}`",
        "",
        "## Structured fields considered",
        "",
        "- Email",
        "- Current manuscript citation/status/year",
        "- Presentation list",
        "- Computational toolkit",
        "- GEO / Zenodo identifiers and links",
        "- Date ranges for matching trajectory entries",
        "",
        "## Intentionally not synced",
        "",
        "- Phone number and street/postal address",
        "- References and their contact information",
        "- Leadership / military service",
        "- Grants and academic service",
        "- About text, research-theme prose, and other manually curated narrative sections",
        "",
        "## Result",
        "",
    ]

    if changed:
        report.append("The following top-level website fields changed: " + ", ".join(f"`{x}`" for x in changed) + ".")
    else:
        report.append("No structured website fields changed.")

    detected = [f"- {key}: {value}" for key, value in detected_dates.items() if value]
    if detected:
        report.extend(["", "## Detected trajectory dates", "", *detected])

    report.extend([
        "",
        "Review the `data.json` diff before merging this Pull Request. If any extraction is wrong, close the PR and edit the website manually in Pages CMS.",
        "",
    ])

    Path(args.report).write_text("\n".join(report), encoding="utf-8")
    print(f"Parsed {cv_path}")
    print("Changed fields:", ", ".join(changed) if changed else "none")


if __name__ == "__main__":
    main()
