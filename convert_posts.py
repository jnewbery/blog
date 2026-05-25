#!/usr/bin/env python3
"""Convert Jekyll posts to Pelican format."""

import os
import re
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pyyaml"], check=True)
    import yaml

POSTS_DIR = Path("/home/user/blog/_posts")
ARTICLES_DIR = Path("/home/user/blog/content/articles")
ATTACHMENTS_DIR = Path("/home/user/blog/content/attachments")
PAGES_DIR = Path("/home/user/blog/content/pages")

ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
PAGES_DIR.mkdir(parents=True, exist_ok=True)


def parse_front_matter(text):
    """Parse Jekyll YAML front matter, return (metadata_dict, body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    yaml_str = parts[1]
    body = parts[2].lstrip("\n")
    try:
        metadata = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        metadata = {}
    return metadata, body


def extract_slug_from_filename(filename):
    """Extract slug (title part) from Jekyll filename like 2017-07-21-my-post."""
    name = Path(filename).name  # Final path component (no stem truncation)
    # Strip markdown extension without truncating on embedded dots
    for ext in (".markdown", ".md"):
        if name.endswith(ext):
            name = name[: -len(ext)]
            break
    # Remove date prefix YYYY-MM-DD-
    match = re.match(r"\d{4}-\d{2}-\d{2}-(.*)", name)
    if match:
        return match.group(1)
    return name


def extract_date_from_filename(filename):
    """Extract date from Jekyll filename."""
    name = Path(filename).name
    match = re.match(r"(\d{4}-\d{2}-\d{2})", name)
    if match:
        return match.group(1)
    return None


def convert_tags(tags_value):
    """Convert Jekyll tags (list or string) to comma-separated string."""
    if not tags_value:
        return ""
    if isinstance(tags_value, list):
        return ", ".join(str(t) for t in tags_value)
    # Handle inline YAML list string like "[tag1, tag2]"
    s = str(tags_value).strip()
    if s.startswith("[") and s.endswith("]"):
        items = [x.strip().strip("'\"") for x in s[1:-1].split(",")]
        return ", ".join(items)
    return s


def update_asset_paths(body, slug):
    """Update relative ./filename paths to /attachments/slug/filename."""
    # Replace ./filename with /attachments/slug/filename
    body = re.sub(
        r'src=["\']\./([\w\-\.]+)["\']',
        lambda m: f'src="/attachments/{slug}/{m.group(1)}"',
        body,
    )
    body = re.sub(
        r'\]\(\./([^\)]+)\)',
        lambda m: f"](/attachments/{slug}/{m.group(1)})",
        body,
    )
    # Markdown reference-style links: [label]: ./file
    body = re.sub(
        r'(\[[\w\s]+\]):\s*\./(\S+)',
        lambda m: f"{m.group(1)}: /attachments/{slug}/{m.group(2)}",
        body,
    )
    return body


def build_pelican_metadata(metadata, slug, date_from_filename):
    """Build Pelican metadata block from Jekyll metadata."""
    lines = []

    title = metadata.get("title", "")
    if title:
        # Remove surrounding quotes if present
        title = str(title).strip('"\'')
        lines.append(f"Title: {title}")

    # Date: prefer front matter, fallback to filename
    date = metadata.get("date", date_from_filename)
    if date:
        date_str = str(date)
        # Handle datetime objects from YAML
        if hasattr(date, "strftime"):
            date_str = date.strftime("%Y-%m-%d")
        lines.append(f"Date: {date_str}")

    category = metadata.get("category", "")
    if category:
        lines.append(f"Category: {category}")

    lines.append(f"Slug: {slug}")

    # excerpt → Summary
    summary = metadata.get("excerpt", metadata.get("summary", ""))
    if summary:
        summary = " ".join(str(summary).split())
        lines.append(f"Summary: {summary}")

    tags = metadata.get("tags", [])
    tags_str = convert_tags(tags)
    if tags_str:
        lines.append(f"Tags: {tags_str}")

    subtitle = metadata.get("subtitle", "")
    if subtitle:
        subtitle = str(subtitle).strip('"\'')
        lines.append(f"Subtitle: {subtitle}")

    feature_img = metadata.get("feature-img", "")
    if feature_img:
        lines.append(f"Feature_img: {feature_img}")

    feature_title = metadata.get("feature-title", "")
    if feature_title:
        lines.append(f"Feature_title: {feature_title}")

    return "\n".join(lines)


def copy_attachments(post_dir, slug):
    """Copy non-markdown files from post directory to attachments."""
    if not post_dir.is_dir():
        return
    dest_dir = ATTACHMENTS_DIR / slug
    has_attachments = False
    for f in post_dir.iterdir():
        if f.suffix.lower() not in (".md", ".markdown"):
            if not has_attachments:
                dest_dir.mkdir(parents=True, exist_ok=True)
                has_attachments = True
            shutil.copy2(f, dest_dir / f.name)


def convert_post(md_file, slug, date_from_filename):
    """Convert a single Jekyll markdown file to Pelican format."""
    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    metadata, body = parse_front_matter(content)
    pelican_meta = build_pelican_metadata(metadata, slug, date_from_filename)
    body = update_asset_paths(body, slug)

    return pelican_meta + "\n\n" + body


def process_posts():
    """Process all Jekyll posts."""
    for entry in sorted(POSTS_DIR.iterdir()):
        if entry.is_dir():
            # Find the markdown file inside
            md_files = list(entry.glob("*.md")) + list(entry.glob("*.markdown"))
            if not md_files:
                continue
            md_file = md_files[0]
            slug = extract_slug_from_filename(entry.name)
            date = extract_date_from_filename(entry.name)
            copy_attachments(entry, slug)
        elif entry.suffix.lower() in (".md", ".markdown"):
            md_file = entry
            slug = extract_slug_from_filename(entry.name)
            date = extract_date_from_filename(entry.name)
        else:
            continue

        converted = convert_post(md_file, slug, date)
        out_file = ARTICLES_DIR / f"{slug}.md"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(converted)
        print(f"Converted: {slug}")


def convert_about_page():
    """Convert about.md to Pelican page format."""
    about_src = Path("/home/user/blog/about.md")
    with open(about_src, encoding="utf-8") as f:
        content = f.read()

    metadata, body = parse_front_matter(content)
    title = metadata.get("title", "About")
    date = metadata.get("date", "2018-08-22")
    if hasattr(date, "strftime"):
        date = date.strftime("%Y-%m-%d")

    pelican_meta = f"Title: {title}\nDate: {date}\nSlug: about"
    out_content = pelican_meta + "\n\n" + body

    out_file = PAGES_DIR / "about.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_content)
    print("Converted: about page")


if __name__ == "__main__":
    process_posts()
    convert_about_page()
    print("Done!")
