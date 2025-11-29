# Copilot instructions for this course repo

- Prioritize readability and testability over cleverness.
- Favor Python standard library; do **not** add dependencies unless explicitly requested.
- Write implementation **after** stubbing tests and docstrings.
- Don’t generate entire solutions in one go. Prefer small, reviewable changes.
- If the prompt is ambiguous, propose 2–3 concrete options and ask which to pursue.
- Avoid producing files outside the current exercise folder (e.g., `day05/`).
- Assume `pytest` for tests.
- Provide unit tests for pure functions first; then add minimal CLI tests.
- Keep functions small with clear inputs/outputs. Use type hints and docstrings.
- Keep line length ≤ 100; prefer f-strings.
- Don’t invent external APIs or network calls.
- Don’t add frameworks or GUI libs.
- Don’t change public behavior without updating tests and README.
