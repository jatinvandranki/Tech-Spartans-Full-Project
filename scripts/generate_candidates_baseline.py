# Generate candidates by frequency (baseline)
from collections import Counter
inp = "data/cleaned.txt"
out = "candidates/top100k.txt"
with open(inp, "r", encoding="utf-8") as f:
    pwds = [l.strip() for l in f if l.strip()]
c = Counter(pwds)
most = [p for p,_ in c.most_common(100000)]
with open(out, "w", encoding="utf-8") as f:
    for p in most:
        f.write(p+"\n")
print("Saved", len(most), "candidates to", out)
