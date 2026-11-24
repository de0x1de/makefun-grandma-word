#!/usr/bin/env python3
"""Write the One Word From Grandma entry to /output/entry.txt.

The entry is exactly one word: the single word a grandma would text
about AI. The word is assembled from two fragments, validated as one
word, written without a trailing newline, and read back for a byte
comparison before the program exits.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# The word, split so a stray edit to either half is easy to spot.
FRAGMENT_HEAD = "Unplug"
FRAGMENT_TAIL = "It"

MAX_CHARACTERS = 30


def build_word() -> str:
    """Join the fragments and check the result is exactly one word."""
    word = FRAGMENT_HEAD + FRAGMENT_TAIL
    if not word:
        raise ValueError("word must not be empty")
    if len(word) > MAX_CHARACTERS:
        raise ValueError("word exceeds the 30 character gate")
    if word.split() != [word]:
        raise ValueError("entry must be exactly one word, no whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must not contain whitespace")
    # Reject whitespace that isspace() alone might let a reader overlook:
    # embedded or surrounding newlines, tabs and carriage returns would
    # turn the file into more than a bare one-word entry.
    if word != word.strip() or any(ch in word for ch in "\n\r\t"):
        raise ValueError("word must not contain or be padded by whitespace")
    if not word.isalpha():
        raise ValueError("word must be letters only, no punctuation tricks")
    # UTF-8 round-trip: the gate reads the file as UTF-8 text.
    if word.encode("utf-8").decode("utf-8") != word:
        raise ValueError("word does not survive a UTF-8 round-trip")
    return word


def main() -> None:
    word = build_word()
    payload = word.encode("utf-8")
    # The file must be exactly the word's bytes: no trailing newline and
    # no extra padding, so its length has to match the encoded word.
    if payload.endswith(b"\n") or len(payload) != len(word.encode("utf-8")):
        raise ValueError("payload must be the bare word with no trailing newline")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(payload)
    written = OUTPUT_PATH.read_bytes()
    if written != payload:
        raise SystemExit("read-back mismatch: file bytes differ from the word")
    if written.decode("utf-8") != word:
        raise SystemExit("read-back mismatch: file text differs from the word")


if __name__ == "__main__":
    main()
