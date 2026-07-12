#!/usr/bin/env python3
"""
screenshot_sites.py — capture REAL screenshots of businesses' current websites
for the "current site" preview tiles on the operator dashboard.

WHY THIS APPROACH (learned the hard way):
- The remote Browserbase browser CAPTURES a screenshot but BrowserSaveScreenshot
  frequently errors "No screenshot to save", so it can't be persisted/embedded.
- Google PageSpeed's screenshot API is quota-blocked without an API key.
- thum.io is keyless and reliable from the container via curl (curl honors the
  sandbox HTTPS_PROXY). It renders ASYNC: the first request returns a loading
  GIF, so we POLL until the bytes are a real PNG/JPEG.

USAGE
  python3 screenshot_sites.py OUT_DIR https://site-a.com https://site-b.ca ...
  python3 screenshot_sites.py OUT_DIR --json sites.json     # {"key":"https://url", ...}

AFTER IT RUNS, for each good PNG:
  SaveFile(path) -> fileId  ->  PublishFilePublicly(fileId) -> pub.hyperagent.com URL
  Embed the pub URL in the dashboard HTML.  (Thread-scoped /api/files URLs break
  inside the published iframe; pub.hyperagent.com URLs render.)

IMPORTANT
- ALWAYS view each saved PNG (Read tool) before embedding. Discard captures that
  are a Cloudflare "verify you are human" page, a 404, or blank.
- Sites behind an INTERACTIVE Cloudflare gate cannot be captured by any automated
  renderer. Do NOT fake it — use an honest "view live ↗" tile on that card.
"""
import sys, os, json, time, subprocess, re

THUMB = "https://image.thum.io/get/width/1280/crop/860/"
THUMB_WAIT = "https://image.thum.io/get/width/1280/wait/{w}/crop/860/"

def fetch(url, out, wait=0):
    src = THUMB_WAIT.format(w=wait) if wait else THUMB
    subprocess.run(["curl", "-sL", "--max-time", "80", src + url, "-o", out],
                   capture_output=True)

def magic(p):
    try:
        with open(p, "rb") as f:
            return f.read(4)
    except Exception:
        return b""

def is_image(m):
    return m[:4] == b"\x89PNG" or m[:2] == b"\xff\xd8"   # GIF89a == still loading

def grab(key, url, out_dir, attempts=12):
    out = os.path.join(out_dir, f"{key}.png")
    fetch(url, out)                       # warm the async render
    for _ in range(attempts):
        if is_image(magic(out)) and os.path.getsize(out) > 8000:
            return out, True
        time.sleep(5)
        fetch(url, out)
    return out, is_image(magic(out))

def slug(u):
    host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", host).strip("-")

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: screenshot_sites.py OUT_DIR [--json sites.json | URL ...]")
        return
    out_dir = args[0]
    os.makedirs(out_dir, exist_ok=True)
    if len(args) >= 3 and args[1] == "--json":
        sites = json.load(open(args[2]))
    else:
        sites = {slug(u): u for u in args[1:]}
    for k, u in sites.items():
        p, ok = grab(k, u, out_dir)
        sz = os.path.getsize(p) if os.path.exists(p) else 0
        print(f"{k}\t{'OK' if ok else 'FAILED'}\t{sz}B\t{u}")
    print("DONE — VIEW each PNG before embedding; discard bot-check/404/blank captures.")

if __name__ == "__main__":
    main()
