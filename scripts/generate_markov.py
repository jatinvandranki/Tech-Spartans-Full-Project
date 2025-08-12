# Build a simple character Markov model (order=2) and generate candidates
import os, random, json
inp = "data/cleaned.txt"
out = "candidates/markov_top.txt"
order = 2
chains = {}
total = 0
with open(inp, "r", encoding="utf-8") as f:
    for line in f:
        pwd = line.strip()
        if len(pwd)==0: continue
        padded = "~"*order + pwd + "$"
        for i in range(len(padded)-order):
            key = padded[i:i+order]
            nxt = padded[i+order]
            chains.setdefault(key, []).append(nxt)
        total += 1

def generate_word(maxlen=16):
    key = "~"*order
    out = ""
    for _ in range(maxlen):
        if key not in chains: break
        nxt = random.choice(chains[key])
        if nxt == "$": break
        out += nxt
        key = key[1:] + nxt
    return out

# generate many and score by frequency from generation
gen = []
for _ in range(50000):
    gen.append(generate_word())

# simple frequency
from collections import Counter
cnt = Counter([g for g in gen if g])
most = [p for p,_ in cnt.most_common(50000)]
with open(out, "w", encoding="utf-8") as f:
    for p in most:
        f.write(p+"\n")
print("Markov candidates saved to", out)
