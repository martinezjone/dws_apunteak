"""Convert PPTX files in docs/presentaciones to Markdown notes for MkDocs.

Usage:
    python scripts/convert_pptx_to_md.py

Dependencies:
    pip install python-pptx pillow
"""
from pathlib import Path
import re
import shutil
import sys
from pptx import Presentation

# ---------- Config ----------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRESENTATIONS_DIR = PROJECT_ROOT / "docs" / "presentaciones"
UNIT_DIR = PROJECT_ROOT / "docs" / "02-sintaxia"
UNIT_IMAGES_DIR = UNIT_DIR / "images"
MKDOCS_FILE = PROJECT_ROOT / "mkdocs.yml"

# Markdown-safe slugify for folder names
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "presentation"

# Detect if a paragraph is a title (bigger font size or placeholder title)
def _is_title(paragraph):
    if paragraph.font and paragraph.font.size:
        return paragraph.font.size.pt >= 24  # heuristic
    return False

# Convert PPTX file to Markdown

def convert_pptx(pptx_path: Path):
    pres = Presentation(pptx_path)
    base_name = pptx_path.stem
    folder_slug = slugify(base_name)
    destination_dir = UNIT_DIR / folder_slug
    images_dir = destination_dir / "images"
    destination_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    md_lines = [f"# {base_name}\n"]

    image_counter = 1
    for index, slide in enumerate(pres.slides, start=1):
        slide_title = None
        # first pass to find title
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = shape.text.strip()
            if not text:
                continue
            if shape.is_placeholder and shape.placeholder_format.type == 1:  # TITLE placeholder
                slide_title = text
                break
        if slide_title is None:
            # fallback: first non-empty text frame
            for shape in slide.shapes:
                if shape.has_text_frame and shape.text.strip():
                    slide_title = shape.text.strip().split("\n")[0]
                    break
        if slide_title:
            md_lines.append(f"\n## {slide_title}\n")

        # second pass for content
        for shape in slide.shapes:
            if shape.shape_type == 13:  # PICTURE
                image_ext = shape.image.ext
                img_name = f"slide{index}_{image_counter}.{image_ext}"
                img_path = images_dir / img_name
                with open(img_path, "wb") as f:
                    f.write(shape.image.blob)
                md_lines.append(f"![{slide_title or 'image'}](images/{img_name})\n")
                image_counter += 1
                continue

            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                # Task detection
                if text.lower().startswith("tarea") or text.lower().startswith("exercise"):
                    md_lines.append("\n!!! exercise \"Tarea\"\n    " + text + "\n")
                    continue
                # Code detection: monospaced font or text starts with '$' or '>' etc.
                if any(run.font and run.font.name and run.font.name.lower() in {"consolas", "courier new", "monaco"} for run in paragraph.runs):
                    md_lines.append("\n```\n" + text + "\n```\n")
                    continue
                # Bullet level
                level = paragraph.level
                bullet = "- " * (level + 1)
                md_lines.append(bullet + text + "\n")

    # Write markdown file
    md_path = destination_dir / "index.md"
    md_path.write_text("".join(md_lines), encoding="utf-8")
    print(f"Converted {pptx_path.name} -> {md_path.relative_to(PROJECT_ROOT)}")

    return folder_slug, md_path


def update_mkdocs_nav(entries):
    """Insert Unit 2 navigation if not present or extend it"""
    if not MKDOCS_FILE.exists():
        print("mkdocs.yml not found; skipping nav update")
        return

    import yaml  # PyYAML required
    with MKDOCS_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    nav = data.get("nav", [])
    # find Unit 2 position
    unit2_nav = None
    for item in nav:
        if isinstance(item, dict) and "Unitatea 2" in item:
            unit2_nav = item["Unitatea 2"]
            # if it is a string, replace with list
            if isinstance(unit2_nav, str):
                unit2_nav = []
                item["Unitatea 2"] = unit2_nav
            break
    if unit2_nav is None:
        unit2_nav = []
        nav.append({"Unitatea 2": unit2_nav})

    # clear current list and append entries
    unit2_nav.clear()
    for title, rel_path in entries:
        unit2_nav.append({title: rel_path})

    data["nav"] = nav
    with MKDOCS_FILE.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print("Updated mkdocs.yml navigation for Unitatea 2")


def main():
    if not PRESENTATIONS_DIR.exists():
        print(f"Presentations directory {PRESENTATIONS_DIR} not found", file=sys.stderr)
        sys.exit(1)

    pptx_files = list(PRESENTATIONS_DIR.glob("*.pptx"))
    if not pptx_files:
        print("No .pptx files found in presentaciones directory", file=sys.stderr)
        sys.exit(1)

    UNIT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    nav_entries = []
    for pptx_file in pptx_files:
        folder_slug, md_path = convert_pptx(pptx_file)
        # Title for nav = first letters capitalized sans slug modifications
        title = pptx_file.stem.replace("DWS - 2. unitatea - ", "").strip()
        rel_md = str(Path("02-sintaxia") / folder_slug / "index.md")
        nav_entries.append((title, rel_md))

    update_mkdocs_nav(nav_entries)


if __name__ == "__main__":
    main()
