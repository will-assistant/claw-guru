#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from collections import Counter
from pathlib import Path
SIG=[(r"Application command names must be unique","Discord command collision"),(r"Gateway start blocked: set gateway\.mode=local","Set gateway.mode=local"),(r"refusing to bind gateway .* without auth","Configure gateway auth"),(r"another gateway instance is already listening|EADDRINUSE","Port conflict")]
def latest():
    d=Path.home()/'.openclaw'/'logs'
    if not d.exists(): return None
    xs=sorted(d.glob('openclaw*.log'), key=lambda p:p.stat().st_mtime, reverse=True)
    return xs[0] if xs else None
if len(sys.argv)>1: lines=Path(sys.argv[1]).expanduser().read_text(encoding='utf-8',errors='replace').splitlines()
elif not sys.stdin.isatty(): lines=sys.stdin.read().splitlines()
else:
    p=latest(); lines=p.read_text(encoding='utf-8',errors='replace').splitlines() if p else []
if not lines: print('No log input.'); raise SystemExit(1)
c=Counter()
for ln in lines:
    for pat,h in SIG:
        if re.search(pat,ln,re.I): c[h]+=1
for h,n in c.most_common(): print(f'{n}x {h}')
