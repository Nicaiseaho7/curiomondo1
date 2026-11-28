#!/usr/bin/env python3
"""Build an optional 640w homepage-only rendition from an existing local 800w WebP."""
import hashlib
from io import BytesIO
import os
from pathlib import Path
import re
import sys
import tempfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAT = re.compile(r"/assets/images/editorial-auto/([a-zA-Z0-9_-]+)-800\.webp\Z")

def run(url):
    m = PAT.fullmatch(url)
    if not m:
        return
    parent = ROOT / "assets/images/editorial-auto"
    source = ROOT / url.lstrip("/")
    if not source.is_file() or source.is_symlink() or source.resolve().parent != parent.resolve():
        return
    raw = source.read_bytes()
    sig = hashlib.sha256(raw).hexdigest()[:10]
    target = parent / f"{m[1]}-home-{sig}-640.webp"
    if target.is_file() and not target.is_symlink():
        with Image.open(target) as icon:
            if icon.format == "WEBP" and icon.width == 640 and target.stat().st_size < len(raw) * .85:
                icon.verify()
                print("/" + target.relative_to(ROOT).as_posix())
                return
    with Image.open(BytesIO(raw)) as source_image:
        if source_image.format != "WEBP" or source_image.width != 800 or source_image.is_animated:
            return
        img = source_image.convert("RGB").resize(
            (640, round(source_image.height * 640 / source_image.width)), Image.Resampling.LANCZOS
        )
        data = BytesIO()
        kwargs = {"icc_profile": source_image.info["icc_profile"]} if "icc_profile" in source_image.info else {}
        img.save(data, "WEBP", quality=81, method=6, **kwargs)
    if data.tell() >= len(raw) * .85:
        return
    with tempfile.NamedTemporaryFile(dir=parent,prefix=".home-thumb-",delete=False) as f:
        try:
            f.write(data.getvalue())
            f.flush()
            os.chmod(f.name, 0o644)
            os.replace(f.name,target)
        finally:
            if os.path.exists(f.name):
                os.unlink(f.name)
    print("/" + target.relative_to(ROOT).as_posix())

if __name__ == "__main__":
    # An unavailable or unsupported source is deliberately not fatal to publishing.
    if len(sys.argv) == 2:
        run(sys.argv[1])
