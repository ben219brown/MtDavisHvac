# Upload approved project photographs

The owner-supplied photos have already been reviewed, rotated where needed, optimized to WebP at gallery and enlarged viewing resolutions, labeled and sorted.

**To import all 19 into the live site:**

1. Download the prepared file named `mt-davis-gallery-upload.zip` from the ChatGPT conversation.
2. Here in the GitHub `photo-import/` folder, click **Add file → Upload files**.
3. Upload **only** `mt-davis-gallery-upload.zip` — leave it as a ZIP; do not extract it.
4. Commit to the `main` branch.
5. Open the repository **Actions** tab and look for **Import approved project photo gallery**. It will copy the photos into `hvac-assets/gallery/`, regenerate the gallery and featured pictures, run the existing quality checks, and commit the website changes automatically.
6. Verify Cloudflare picks up the new commit. If it does not deploy automatically, select **New deployment** in Cloudflare for the new `main` commit.

This is a one-time import. The workflow deletes the temporary ZIP in its publishing commit, keeping only optimized web photos in the site. The existing site remains unchanged if the import or quality tests fail.

## Image selection
- **New hero:** clear outdoor Bosch system photographed beside a brick house (`IMG_2299.jpeg`).
- **New About photo:** neatly mounted heating equipment and piping (`IMG_9444.jpeg`).
- **Primary gallery highlights:** those two photos plus the existing Fujitsu ductless outdoor installation in full-resolution form.
- Remaining photos categorized as heating, air conditioning, ductless mini-splits, indoor or outdoor equipment. Avoid claiming jobs were completed or specific hardware specifications beyond what the photos establish.
