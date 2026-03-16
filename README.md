# baseconv

Number base converter with auto-detection. Zero dependencies.

## Usage

```bash
baseconv 255                    # Show all bases
baseconv 0xff                   # Auto-detect hex
baseconv 0b11111111             # Auto-detect binary
baseconv 2026 --to roman        # To Roman numerals
baseconv MMXXVI                 # Auto-detect Roman
baseconv 42 --to 2              # To specific base
baseconv ff --from 16 --to 2    # Between bases
```

## Formats

Decimal, hex, binary, octal, base36, Roman numerals, ASCII

## Requirements

- Python 3.6+ (stdlib only)
