#!/usr/bin/env python3
"""One-time import of 19 real Mt Davis project photos from a prepared upload ZIP."""
from __future__ import annotations

from html import escape
from pathlib import Path
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "photo-import" / "mt-davis-gallery-upload.zip"
DEST = ROOT / "hvac-assets" / "gallery"
if not ARCHIVE.is_file():
    raise SystemExit(f"Missing {ARCHIVE} — upload the prepared gallery ZIP first.")

with zipfile.ZipFile(ARCHIVE) as z:
    photos = json.loads(z.read("gallery-manifest.json"))["photos"]
    if len(photos) != 19:
        raise SystemExit(f"Expected 19 gallery photos, got {len(photos)}")
    DEST.mkdir(exist_ok=True, parents=True)
    for p in photos:
        if not re.fullmatch(r"[a-z0-9-]+", p["slug"]):
            raise SystemExit("Unsafe photo slug: " + repr(p["slug"]))
        for key in ("thumb", "full"):
            name = p[key]
            if name != p["slug"] + "-" + key + ".webp":
                raise SystemExit("Unexpected photo path: " + repr(name))
            data = z.read(name)
            if len(data) < 1000 or data[8:12] != b"WEBP":
                raise SystemExit("Invalid WebP image " + name)
            (DEST / name).write_bytes(data)

imgroot = "/hvac-assets/gallery/"
homefile = ROOT / "index.html"
home = homefile.read_text(encoding="utf-8")

# Choose strongest, well-lit photographs for the two large marketing positions.
home = home.replace(
    'src="./hvac-assets/fujitsu-mini-split.jpg" fetchpriority="high" decoding="async" width="600" height="300" alt="Fujitsu mini-split outdoor unit installed by Mt Davis HVAC"',
    'src="' + imgroot + 'bosch-outdoor-unit-full.webp" fetchpriority="high" decoding="async" width="1600" height="1200" alt="Bosch outdoor HVAC unit installed next to a brick home"'
)
home = home.replace(
    '<img loading="lazy" decoding="async" src="./hvac-assets/bosch-installation.jpg" alt="Bosch HVAC equipment installation">',
    '<img loading="lazy" decoding="async" src="' + imgroot + 'heating-piping-installation-full.webp" width="1600" height="1200" alt="Clean heating installation with wall-mounted equipment and organized piping">'
)
home = home.replace(
    '"image":"https://mtdavishvac.com/hvac-assets/fujitsu-mini-split.jpg"',
    '"image":"https://mtdavishvac.com/hvac-assets/gallery/bosch-outdoor-unit-full.webp"'
)
# Only update the intended gallery section, leaving the review slider and quote form intact.
start = home.index('<section class="section gallery"')
end = home.index('<section class="section brands"', start)
gallery = home[start:end]
filter_names = [
    ("all", "All Work"), ("heating", "Heating"),
    ("cooling", "Air Conditioning"), ("minisplit", "Mini-Splits"),
    ("outdoor", "Outdoor Systems"), ("indoor", "Indoor Equipment")
]
buttons = '\n          '.join(
    '<button class="filter-btn' + (' active' if i == 0 else '') +
    '" type="button" aria-pressed="' + ('true' if i == 0 else 'false') +
    '" data-filter="' + key + '">' + label + '</button>'
    for i, (key, label) in enumerate(filter_names)
)
gallery, filter_count = re.subn(
    r'<div class="filter-row" aria-label="Gallery filters">[\s\S]*?</div>',
    '<div class="filter-row" aria-label="Gallery filters">\n          ' + buttons + '\n        </div>',
    gallery, count=1
)
if filter_count != 1:
    raise SystemExit("Could not update gallery filters safely.")
gallery = re.sub(
    r'<p class="gallery-note">[^<]*</p>',
    '<p class="gallery-note">19 genuine project photos supplied by Mt Davis HVAC. Select a category to view real heating, cooling, ductless and installation work.</p>',
    gallery, count=1
)
cards = []
for i,p in enumerate(photos):
    slug = escape(p["slug"], quote=True)
    title = escape(p["title"])
    alt = escape(p["alt"], quote=True)
    tag = escape(p["tag"])
    categories = escape(" ".join(p["categories"]), quote=True)
    class_name = "gallery-item" + (" featured" if i == 0 else " tall" if i == 1 else "")
    cards.append(
        '          <article class="' + class_name + '" data-category="' + categories + '">\n'
        '            <button type="button" class="gallery-photo-btn" data-full="' +
        imgroot + slug + '-full.webp" aria-label="Open project photo: ' + alt + '">\n'
        '              <img loading="lazy" decoding="async" src="' + imgroot + slug +
        '-thumb.webp" width="920" height="' +
        str(round(920 / p["ratio"])) + '" alt="' + alt + '">\n'
        '            </button>\n'
        '            <div class="gallery-caption"><span class="tag">' + tag +
        '</span><strong>' + title + '</strong></div>\n'
        '          </article>'
    )
grid_start = gallery.index('<div class="gallery-grid">') + len('<div class="gallery-grid">')
grid_end = gallery.index('\n        </div>\n      </div>\n    </section>', grid_start)
gallery = gallery[:grid_start] + '\n' + '\n\n'.join(cards) + '\n' + gallery[grid_end:]
gallery = gallery.replace(
    '\n        </div>\n      </div>\n    </section>',
    '\n        </div>\n'
    '        <div class="gallery-expander"><button id="galleryShowMore" type="button" '
    'class="btn btn-primary" aria-expanded="false">Show all 19 project photos ↓</button></div>\n'
    '      </div>\n    </section>', 1
)
home = home[:start] + gallery + home[end:]
if '.gallery-photo-btn{' not in home:
    home = home.replace(
        '    .gallery-item img{width:100%;height:100%;object-fit:cover;transition:.4s transform}',
        '    .gallery-photo-btn{width:100%;height:100%;border:0;padding:0;display:block;cursor:zoom-in;background:transparent}\n'
        '    .gallery-photo-btn:focus-visible{outline:4px solid var(--orange);outline-offset:-5px}\n'
        '    .gallery-item img{width:100%;height:100%;object-fit:cover;transition:.4s transform}\n'
        '    .gallery-item:after,.gallery-caption{pointer-events:none}\n'
        '    .gallery-expander{text-align:center;margin-top:30px}'
    )
gallery_js_start = home.index("    const filterBtns = document.querySelectorAll('.filter-btn');")
gallery_js_end = home.index("    function closeLightbox()", gallery_js_start)
home = home[:gallery_js_start] + """
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = Array.from(document.querySelectorAll('.gallery-item'));
    const showMoreBtn = document.getElementById('galleryShowMore');
    let galleryExpanded = false;
    function updateGallery() {
      const filter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
      let shown = 0;
      galleryItems.forEach(item => {
        const matching = filter === 'all' || item.dataset.category.split(' ').includes(filter);
        const display = matching && (filter !== 'all' || galleryExpanded || shown < 6);
        item.classList.toggle('hidden', !display);
        if (matching) shown++;
      });
      if (showMoreBtn) {
        showMoreBtn.style.display = filter === 'all' && galleryItems.length > 6 ? 'inline-flex' : 'none';
        showMoreBtn.textContent = galleryExpanded ? 'Show fewer photos ↑' : 'Show all ' + galleryItems.length + ' project photos ↓';
        showMoreBtn.setAttribute('aria-expanded', String(galleryExpanded));
      }
    }
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        updateGallery();
      });
    });
    if (showMoreBtn) showMoreBtn.addEventListener('click', () => {
      galleryExpanded = !galleryExpanded;
      updateGallery();
      if (!galleryExpanded) document.getElementById('gallery').scrollIntoView({behavior:'smooth'});
    });
    updateGallery();

    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    document.querySelectorAll('.gallery-photo-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        lightboxImg.src = btn.dataset.full;
        lightboxImg.alt = btn.querySelector('img')?.alt || 'Mt Davis HVAC project photo';
        lightbox.classList.add('open');
        document.getElementById('lightboxClose').focus();
      });
    });
""" + home[gallery_js_end:]
if len(re.findall(r'class="gallery-photo-btn"',home)) != 19:
    raise SystemExit("Gallery generation failed; not writing home.")
homefile.write_text(home,encoding="utf-8")

# Featured service-page images use suitable, authentic originals from the same upload.
updates = {
    "services/air-conditioning/index.html": (
        '/hvac-assets/fujitsu-mini-split.jpg', imgroot + 'bosch-outdoor-unit-full.webp',
        'Fujitsu ductless outdoor unit installed by Mt Davis HVAC',
        'Bosch outdoor HVAC unit installed beside a brick home'
    ),
    "services/heating-furnaces/index.html": (
        '/hvac-assets/bosch-installation.jpg', imgroot + 'heating-piping-installation-full.webp',
        'Bosch heating and cooling equipment installed by Mt Davis HVAC',
        'Wall-mounted heating equipment and hydronic piping'
    ),
    "services/mini-splits/index.html": (
        '/hvac-assets/fujitsu-mini-split.jpg', imgroot + 'fujitsu-ductless-installation-full.webp',
        'Actual Fujitsu mini-split installation project completed by Mt Davis HVAC',
        'Fujitsu outdoor ductless system installed against house siding'
    ),
}
for path, (old_img,new_img,old_alt,new_alt) in updates.items():
    f = ROOT/path
    txt = f.read_text(encoding="utf-8")
    if old_img not in txt:
        raise SystemExit("Expected service image not found: "+path)
    txt = txt.replace(old_img,new_img).replace(old_alt,new_alt)
    f.write_text(txt,encoding="utf-8")

# Link the new originals to image search from the canonical homepage in the sitemap.
sitemap_path = ROOT/"sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
sitemap = re.sub(
    r'(<loc>https://mtdavishvac.com/</loc>\s*<lastmod>[^<]+</lastmod>)[\s\S]*?(\s*</url>)',
    lambda m: m.group(1) + ''.join(
        '\n    <image:image><image:loc>https://mtdavishvac.com/hvac-assets/gallery/'
        + p["full"] + '</image:loc></image:image>' for p in photos
    ) + m.group(2), sitemap, count=1
)
sitemap = sitemap.replace("https://mtdavishvac.com/hvac-assets/fujitsu-mini-split.jpg",
                          "https://mtdavishvac.com/hvac-assets/gallery/fujitsu-ductless-installation-full.webp")
sitemap = sitemap.replace("https://mtdavishvac.com/hvac-assets/bosch-installation.jpg",
                          "https://mtdavishvac.com/hvac-assets/gallery/heating-piping-installation-full.webp")
sitemap = re.sub(
    r'(<loc>https://mtdavishvac.com/services/air-conditioning/</loc>[\\s\\S]*?<image:loc>)https://mtdavishvac.com/hvac-assets/gallery/fujitsu-ductless-installation-full.webp',
    lambda m: m.group(1) + 'https://mtdavishvac.com/hvac-assets/gallery/bosch-outdoor-unit-full.webp',
    sitemap, count=1
)
sitemap_path.write_text(sitemap,encoding="utf-8")
print(f"Imported {len(photos)} originals and {len(photos)} thumbnails, updated homepage, service images and sitemap.")
