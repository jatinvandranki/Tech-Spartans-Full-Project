# Simple MD5 cracker using a candidate wordlist
import hashlib, sys, os
hashfile = sys.argv[1] if len(sys.argv)>1 else "hashes/sample_md5.txt"
candfile = sys.argv[2] if len(sys.argv)>2 else "candidates/top100k.txt"
if not os.path.exists(hashfile):
    print("Hash file not found:", hashfile); sys.exit(1)
if not os.path.exists(candfile):
    print("Candidate wordlist not found:", candfile); sys.exit(1)
with open(hashfile,"r",encoding="utf-8") as f:
    hashes = [l.strip().split(":",1)[0].strip() for l in f if l.strip()]
with open(candfile,"r",encoding="utf-8") as f:
    cands = [l.strip() for l in f if l.strip()]
md5map = {}
for pwd in cands:
    md5map[hashlib.md5(pwd.encode("utf-8",errors="ignore")).hexdigest()] = pwd
cracked = []
for h in hashes:
    cracked.append((h, md5map.get(h, None)))
for h,p in cracked:
    print(h, "=>", p)
