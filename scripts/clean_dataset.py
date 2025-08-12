# Cleans a password dataset (sample)
import os
inp = "data/sample.txt"
out = "data/cleaned.txt"
if not os.path.exists(inp):
    print("Place your sample passwords in data/sample.txt, one per line.")
    raise SystemExit(1)
with open(inp, "r", encoding="latin-1") as f:
    pwds = [l.strip() for l in f if l.strip()]
# Remove duplicates, long entries, whitespace-only
pwds = list(dict.fromkeys([p for p in pwds if len(p)<=20 and p.strip()!='']))
with open(out, "w", encoding="utf-8") as f:
    for p in pwds:
        f.write(p+"\n")
print(f"Cleaned {len(pwds)} passwords to {out}")
