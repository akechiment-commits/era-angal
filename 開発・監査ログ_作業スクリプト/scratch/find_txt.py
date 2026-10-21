# -*- coding: utf-8 -*-
import os, sys, glob

files = glob.glob(r'tools/output/*.txt')
for f in files:
    bn = os.path.basename(f)
    if 'つゆり' in bn or '八朔' in bn or 'なつみ' in bn or 'さあや' in bn:
        print(f"Found: {bn} (len={os.path.getsize(f)})")
