"""Everyday Wonder — one sentence of everyday wonder.

Writes exactly one sentence to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

Rules enforced here (matching the bounty gate):
- UTF-8 text, 1-200 characters, not whitespace-only, a single line.
- No trailing newline is added: the file holds the sentence and nothing else.

Python 3.13 standard library only. Fully deterministic: the same input
always produces the same bytes.
"""

import os
from pathlib import Path

ENTRY = (
    "The lift doors opened on a stranger humming my dead grandmother's song, "
    "and for one floor I lived in a building where she was still upstairs."
)

MIN_LENGTH = 1
MAX_LENGTH = 200
LIMIT = (MIN_LENGTH, MAX_LENGTH)

OUTPUT_FILENAME = "entry.txt"


def ensure_one_sentence(text: str) -> str:
    """Reject anything that is not exactly one line of text."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline characters)")
    return text


def validate_entry(text: str) -> str:
    """Validate the entry against the bounty gate and return it unchanged."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    text.encode("utf-8")  # raises UnicodeEncodeError on non-UTF-8-encodable input
    low, high = LIMIT
    if not low <= len(text) <= high:
        raise ValueError(
            f"entry must be {low}-{high} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be whitespace-only")
    return ensure_one_sentence(text)


def output_path() -> Path:
    """Resolve the output file from the environment."""
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    return Path(out_dir) / OUTPUT_FILENAME


def main() -> None:
    entry = validate_entry(ENTRY)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(entry, encoding="utf-8")


if __name__ == "__main__":
    main()
