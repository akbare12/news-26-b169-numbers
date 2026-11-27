#!/usr/bin/env python3
"""news-image-20261126 entry (V165): copy the pre-rendered entry.png to MAKEFUN_OUTPUT_DIR.
Standard library only: os, shutil. The image is rendered build-time by gen.py (PIL)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png")

if not os.path.isfile(SRC):
    sys.exit("entry.png missing next to main.py")
os.makedirs(os.path.dirname(DST) or ".", exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote %s (%d bytes)" % (DST, os.path.getsize(DST)))
