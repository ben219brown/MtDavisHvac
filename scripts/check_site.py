#!/usr/bin/env python3
"""Validate static Mt Davis HVAC output before deployment; no network calls."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://mtdavishvac.com"
ISSUES = []

def expect(condition, message):
    if not condition:
        ISSUES.append(message)

def site_path(url):
    parsed = urlsplit(url)
    route = unquote(parsed.path)
    if not route or route == "/" or route.endswith("/"):
        return ROOT / route.lstrip("/") / "index.html"
    p = ROOT / route.lstrip("/")
    # Cloudflare static-asset redirects may map slashless URLs to nested index.
    if not p.is_file() and (p / "index.html").is_file():
        return p / "index.html"
    return p

def check_page(path):
    html = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    sub = "" if rel == "index.html" else str(path.parent.relative_to(ROOT)).replace("\\", "/") + "/"
    expected = BASE + "/" + sub
    t = re.search(r"<title>([^<]+)</title>", html)
    expect(bool(t), rel + ": missing title")
    expect(bool(re.search(r'<meta name="description" content="[^"]+"', html)), rel + ": missing description")
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    expect(bool(canonical and canonical.group(1) == expected),
           rel + ": canonical does not match " + expected)
    robots = re.search(r'<meta name="robots" content="([^"]+)"', html)
    expect(bool(robots), rel + ": missing robots tag")
    if rel == "thank-you/index.html":
        expect(bool(robots and "noindex" in robots.group(1)), rel + ": thank-you must be noindex")
    else:
        expect(bool(robots and "noindex" not in robots.group(1)), rel + ": public page has noindex")
    expect(len(re.findall(r"<h1\b", html, flags=re.I)) == 1, rel + ": expected one H1")
    for icon in ("/favicon.ico", "/favicon-32.png", "/favicon-192.png", "/apple-touch-icon.png"):
        expect(icon in html, rel + ": missing favicon reference " + icon)
    for match in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', html):
        try:
            json.loads(match.group(1))
        except json.JSONDecodeError as ex:
            ISSUES.append(rel + ": invalid structured data: " + str(ex))
    for match in re.finditer(r'<(?:img|script|link|a)\b[^>]*(?:src|href)="([^"]*)"', html):
        src = match.group(1)
        if not src or src.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            continue
        parsed = urlsplit(src)
        if parsed.netloc:
            continue
        if src.startswith("/"):
            target = site_path(src)
        else:
            target = path.parent / src.split("?")[0].split("#")[0]
        expect(target.is_file(), rel + ": missing local target: " + src)
    for match in re.finditer(r'<img\b[^>]*>', html):
        expect('alt="' in match.group(0), rel + ": image missing alt attribute")
    return rel, t.group(1) if t else "", robots.group(1) if robots else ""

def main():
    paths = sorted(ROOT.glob("**/index.html"))
    expect(len(paths) >= 10, "Missing expected homepage, service, contact, privacy or thank-you pages")
    titles = []
    for path in paths:
        _, title, _ = check_page(path)
        titles.append(title)
    expect(len(titles) == len(set(titles)), "Duplicate page titles")
    for path in ("favicon-source.png","favicon.ico","favicon-32.png","favicon-192.png",
                 "apple-touch-icon.png","favicon.svg","social-preview.jpg",
                 "site.webmanifest","robots.txt","sitemap.xml","service-pages.css"):
        expect((ROOT / path).is_file(), "Missing production asset: " + path)
    for asset in ("chatbot.js", "chatbot.css", "chat-worker/src/index.js",
                  "chat-worker/wrangler.jsonc", "chat-worker/README.md"):
        expect((ROOT / asset).is_file(), "Missing chat integration file: " + asset)
    worker_config = json.loads((ROOT / "chat-worker/wrangler.jsonc").read_text(encoding="utf-8"))
    expect(worker_config.get("name") == "mtdavishvac-chat", "Incorrect chat worker name")
    expect(worker_config.get("ai", {}).get("binding") == "AI", "Missing free AI binding")
    worker = (ROOT / "chat-worker/src/index.js").read_text(encoding="utf-8")
    expect("@cf/zai-org/glm-4.7-flash" in worker and "OPENAI_API_KEY" not in worker,
           "Chat Worker must use free Cloudflare AI, not paid OpenAI API")
    for page in paths:
        if str(page.relative_to(ROOT)) == "thank-you/index.html":
            continue
        text = page.read_text(encoding="utf-8")
        expect('src="/chatbot.js"' in text and 'href="/chatbot.css"' in text,
               str(page.relative_to(ROOT)) + ": missing chat integration")
    privacy = (ROOT / "privacy/index.html").read_text(encoding="utf-8")
    expect("If you opt in" in privacy and "Cloudflare Workers AI" in privacy,
           "Privacy notice must disclose optional AI service")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    expect('action="https://formsubmit.co/mark@mtdavishvac.com"' in home,
           "Production form destination is not the approved business inbox")
    expect('name="_honey"' in home and 'name="_next"' in home,
           "Form spam trap or confirmation redirect missing")
    expect("mtdavishvac@protonmail.com" not in home and "Demo redesign" not in home,
           "Demo content remains in homepage")
    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    actual_urls = {node.find(ns + "loc").text for node in sitemap.findall(ns + "url")}
    expected_urls = {
        BASE + "/" + ("" if str(p.relative_to(ROOT)) == "index.html"
                      else str(p.parent.relative_to(ROOT)).replace("\\","/") + "/")
        for p in paths if str(p.relative_to(ROOT)) != "thank-you/index.html"
    }
    expect(actual_urls == expected_urls,
           "Sitemap mismatch: missing=" + repr(expected_urls - actual_urls)
           + " extra=" + repr(actual_urls - expected_urls))
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    expect("Sitemap: https://mtdavishvac.com/sitemap.xml" in robots,
           "Robots file missing sitemap reference")
    print(f"Checked {len(paths)} pages; {len(actual_urls)} indexable URLs.")
    if ISSUES:
        for issue in ISSUES:
            print("FAIL:", issue)
        sys.exit(1)
    print("Site QA passed: canonical URLs, indexation, sitemap, local assets, icons and form.")

if __name__ == "__main__":
    main()
