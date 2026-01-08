from collections import defaultdict, Counter

from Utilities import (read_text_from_url,extract_deadlines,parse_subjects_from_text,hours_diff,time_bin,)


README_URL = (
    "https://raw.githubusercontent.com/"
    "Code-Maven/wis-python-course-2025-10/main/README.md"
)

SUBJECTS_URL = (
    "https://raw.githubusercontent.com/"
    "Code-Maven/wis-python-course-2025-10/main/day09/subjects.txt"
)


def main() -> None:
    print("WIS Python Course — Assignment Submission Report")
    print("-" * 70)

    readme_text = read_text_from_url(README_URL)
    subjects_text = read_text_from_url(SUBJECTS_URL)

    deadlines = extract_deadlines(readme_text)
    submissions = parse_subjects_from_text(subjects_text)

    students = {s.student for s in submissions}

    by_assignment = defaultdict(dict)
    for s in submissions:
        prev = by_assignment[s.assignment].get(s.student)
        if not prev or s.submitted_at < prev.submitted_at:
            by_assignment[s.assignment][s.student] = s

    # ----------------------------
    # Late submissions
    # ----------------------------

    print("\n=== Late submissions ===")
    dist = Counter()

    for assignment, deadline in deadlines.items():
        if assignment not in by_assignment:
            continue

        for s in by_assignment[assignment].values():
            h = hours_diff(s.submitted_at, deadline)
            dist[time_bin(h)] += 1

            if h > 0:
                print(
                    f"{s.student:30} "
                    f"{assignment:12} "
                    f"{h:6.1f} hours late"
                )

    # ----------------------------
    # Missing submissions
    # ----------------------------

    print("\n=== Missing submissions ===")
    for assignment in deadlines:
        missing = students - set(by_assignment.get(assignment, {}))
        if missing:
            print(f"\n{assignment}:")
            for m in sorted(missing):
                print(" ", m)

    # ----------------------------
    # Distribution
    # ----------------------------

    print("\n=== Distribution relative to deadline ===")
    for k in ["< -24h", "-24h..0h", "0h..+24h", "> +24h"]:
        print(f"{k:10} : {dist[k]}")

    # ----------------------------
    # Popularity
    # ----------------------------

    print("\n=== Assignment popularity ===")
    counts = Counter(s.assignment for s in submissions)
    for assignment, count in counts.most_common():
        print(f"{assignment:12} {count}")


if __name__ == "__main__":
    main()
