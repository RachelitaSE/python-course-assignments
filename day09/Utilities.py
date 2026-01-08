import re
from datetime import datetime, timezone
from dataclasses import dataclass
from urllib.request import urlopen


# ----------------------------
# Datetime helpers
# ----------------------------

def parse_deadline(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M").replace(tzinfo=timezone.utc)

def parse_iso_z(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ----------------------------
# Data model
# ----------------------------

@dataclass
class Submission:
    student: str
    assignment: str
    submitted_at: datetime
    subject: str


# ----------------------------
# Regex patterns
# ----------------------------

ASSIGNMENT_RE = re.compile(
    r'(?P<assign>Day\s*\d+|Final\s+Project\s+proposal)\s+by\s+(?P<student>.+)',
    re.IGNORECASE
)

DEADLINE_RE = re.compile(
    r'Dead-line:\s*(\d{4}\.\d{2}\.\d{2})\s+(\d{2}:\d{2})',
    re.IGNORECASE
)

PROJECT_RE = re.compile(
    r'(Project proposal|Project submission)\s+dead-line:\s*(\d{4}\.\d{2}\.\d{2})\s+(\d{2}:\d{2})',
    re.IGNORECASE
)

DAY_HEADER_RE = re.compile(r'^Day\s+(\d+)$', re.IGNORECASE)


# ----------------------------
# Network helper (stdlib only)
# ----------------------------

def read_text_from_url(url: str) -> str:
    with urlopen(url) as r:
        return r.read().decode("utf-8")


# ----------------------------
# README parsing
# ----------------------------

def extract_deadlines(readme_text: str) -> dict[str, datetime]:
    deadlines = {}
    current_day = None

    for line in readme_text.splitlines():
        line = line.strip()

        m_day = DAY_HEADER_RE.match(line)
        if m_day:
            current_day = f"Day{int(m_day.group(1)):02d}"
            continue

        m_proj = PROJECT_RE.search(line)
        if m_proj:
            key = m_proj.group(1)
            deadlines[key] = parse_deadline(
                f"{m_proj.group(2)} {m_proj.group(3)}"
            )
            continue

        m_dl = DEADLINE_RE.search(line)
        if m_dl and current_day and current_day not in deadlines:
            deadlines[current_day] = parse_deadline(
                f"{m_dl.group(1)} {m_dl.group(2)}"
            )

    return deadlines


# ----------------------------
# subjects.txt parsing
# ----------------------------

def normalize_assignment(s: str) -> str:
    if s.lower().startswith("day"):
        num = re.sub(r"\D+", "", s)
        return f"Day{int(num):02d}"
    return "Project proposal"


def parse_subjects_from_text(text: str) -> list[Submission]:
    submissions = []

    for line in text.splitlines():
        parts = line.strip().split("\t")
        if len(parts) < 5:
            continue

        subject = parts[2]
        submitted_at = parse_iso_z(parts[4])

        m = ASSIGNMENT_RE.search(subject)
        if not m:
            continue

        submissions.append(
            Submission(
                student=m.group("student").strip(),
                assignment=normalize_assignment(m.group("assign")),
                submitted_at=submitted_at,
                subject=subject,
            )
        )

    return submissions


# ----------------------------
# Time utilities
# ----------------------------

def hours_diff(submitted: datetime, deadline: datetime) -> float:
    return (submitted - deadline).total_seconds() / 3600.0

def time_bin(hours: float) -> str:
    if hours <= -24:
        return "< -24h"
    if hours <= 0:
        return "-24h..0h"
    if hours <= 24:
        return "0h..+24h"
    return "> +24h"
