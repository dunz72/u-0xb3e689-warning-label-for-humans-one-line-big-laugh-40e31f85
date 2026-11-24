"""Warning Label for Humans: One Line, Big Laugh entry.

Writes a single original funny line — a safety warning label that
should be printed on every human — to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the variable
is not set). The line is 1-160 characters (the sealed gate's range),
UTF-8, a single line, not only whitespace.
"""

import os

LINE = (
    "WARNING: Operates on coffee, spite, and 4 hours of sleep. "
    "Says 'I'm fine' while visibly on fire. Do not shake."
)


def main():
    text = LINE.strip()
    if not 1 <= len(text) <= 160:
        raise ValueError(
            f"entry must be 1-160 characters, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main()
