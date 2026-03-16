#!/usr/bin/env python3
"""baseconv - Number base converter (bin, oct, dec, hex, base36, base64, roman). Zero deps."""
import sys, string, base64

DIGITS = string.digits + string.ascii_lowercase

def to_base(n, base):
    if n == 0: return "0"
    neg = n < 0
    n = abs(n)
    result = []
    while n:
        result.append(DIGITS[n % base])
        n //= base
    if neg: result.append("-")
    return "".join(reversed(result))

def from_base(s, base):
    return int(s, base)

def to_roman(n):
    if n <= 0 or n > 3999: return "N/A"
    vals = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
            (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    result = ""
    for v, s in vals:
        while n >= v: result += s; n -= v
    return result

def from_roman(s):
    vals = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    total = 0
    s = s.upper()
    for i, c in enumerate(s):
        if i+1 < len(s) and vals.get(c,0) < vals.get(s[i+1],0):
            total -= vals[c]
        else:
            total += vals.get(c, 0)
    return total

def detect_base(s):
    s = s.strip().lower()
    if s.startswith("0x"): return 16, s[2:]
    if s.startswith("0b"): return 2, s[2:]
    if s.startswith("0o"): return 8, s[2:]
    if all(c in "ivxlcdm" for c in s.lower()) and len(s) <= 15: return "roman", s
    if all(c in "01" for c in s) and len(s) > 3: return 2, s
    return 10, s

def cmd_convert(args):
    if not args:
        print("Usage: baseconv <number> [--to base] [--from base]")
        sys.exit(1)
    
    to = None; frm = None
    num_str = args[0]
    for i, a in enumerate(args):
        if a == "--to" and i+1 < len(args): to = args[i+1]
        if a == "--from" and i+1 < len(args): frm = args[i+1]
    
    # Auto-detect input
    if frm:
        if frm == "roman":
            decimal = from_roman(num_str)
        else:
            decimal = from_base(num_str, int(frm))
    else:
        detected, cleaned = detect_base(num_str)
        if detected == "roman":
            decimal = from_roman(cleaned)
        else:
            decimal = from_base(cleaned, detected)
    
    if to:
        if to == "roman":
            print(to_roman(decimal))
        elif to == "all":
            show_all(decimal)
        else:
            print(to_base(decimal, int(to)))
    else:
        show_all(decimal)

def show_all(n):
    print(f"  Decimal:  {n}")
    print(f"  Hex:      0x{to_base(n, 16)}")
    print(f"  Binary:   0b{to_base(n, 2)}")
    print(f"  Octal:    0o{to_base(n, 8)}")
    print(f"  Base36:   {to_base(n, 36)}")
    if 0 < n <= 3999:
        print(f"  Roman:    {to_roman(n)}")
    print(f"  ASCII:    {chr(n) if 32 <= n <= 126 else 'N/A'}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("baseconv - Number base converter")
        print("Usage: baseconv <number> [--to base|all|roman] [--from base|roman]")
        print("Auto-detects: 0x (hex), 0b (bin), 0o (oct), roman numerals")
        sys.exit(0)
    cmd_convert(args)
