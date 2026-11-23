#!/usr/bin/env python3
"""Entry for news-image-20261123: copy the baked poster to /output/entry.png.

The poster (entry.png, 1024x1024, baked at build time) sums up Monday
23 November 2026 in 50 sourced stories. Standard library only; no network.
Runs deterministically: repeated runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
