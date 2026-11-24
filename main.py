"""Warning Label for Humans: One Line, Big Laugh entry.

Writes a single original funny line — a safety warning label that
should be printed on every human — to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the variable
is not set).

The sealed gate requires the entry to be 1-160 characters, UTF-8, a
single line, and not only whitespace. This module keeps the line in
one place, checks it in another, and only then writes it out, so a
bad line fails loudly before any file is touched.
"""

import os
import sys

# Gate limits for the judged entry (single line, 1-160 chars).
MIN_CHARS = 1
MAX_CHARS = 160

# Fallback output directory when MAKEFUN_OUTPUT_DIR is not set.
DEFAULT_OUTPUT_DIR = "/output"

OUTPUT_FILENAME = "entry.txt"


def warning_line():
    """Return the judged entry line, exactly as it must be written."""
    return (
        "WARNING: Operates on coffee, spite, and 4 hours of sleep. "
        "Says 'I'm fine' while visibly on fire. Do not shake."
    )


def validate_line(text):
    """Check one candidate line against the sealed gate's rules.

    Returns the stripped line when it passes. Raises ValueError with
    a specific reason when it does not, so a bad line never reaches
    the output file.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("entry must not be empty or only whitespace")
    if len(cleaned) < MIN_CHARS or len(cleaned) > MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(cleaned))
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in cleaned):
        raise ValueError("entry must not contain control characters")
    return cleaned


def resolve_output_dir():
    """Resolve where entry.txt goes, creating the directory if needed."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, OUTPUT_FILENAME)


def write_entry(path, text):
    """Write the validated line to path as UTF-8, one line + newline."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")


def main(argv=None):
    """Build, validate, and write the entry. Returns 0 on success."""
    del argv  # no command-line arguments are accepted
    try:
        text = validate_line(warning_line())
        write_entry(resolve_output_dir(), text)
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
