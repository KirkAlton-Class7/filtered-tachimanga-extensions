import json
import os
from pathlib import Path

# Paths
ROOT = Path(__file__).parent
INDEX_FILES = ["index.json", "index.min.json"]
APK_DIR = ROOT / "apk"
ICON_DIR = ROOT / "icon"

def safe_delete(filepath: Path):
    """Delete a file if it exists, with logging."""
    if filepath.exists():
        print(f"🗑️  Deleting: {filepath}")
        filepath.unlink()
    else:
        print(f"⚠️  Not found: {filepath}")

def filter_index_file(filename: str):
    filepath = ROOT / filename
    if not filepath.exists():
        print(f"❌ Skipping missing file: {filepath}")
        return

    print(f"\n📂 Processing: {filename}")
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON in {filename}: {e}")
            return

    filtered = []
    removed_count = 0

    for entry in data:
        if entry.get("nsfw") == 1:
            removed_count += 1

            # Delete associated APK
            apk_name = entry.get("apk")
            if apk_name:
                safe_delete(APK_DIR / apk_name)

            # Delete icons for each source
            for source in entry.get("sources", []):
                icon_id = source.get("id")
                if icon_id:
                    icon_path = ICON_DIR / f"{icon_id}.png"
                    safe_delete(icon_path)

            continue  # skip adding this entry

        filtered.append(entry)

    # Write filtered results back to file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"✅ Done. Kept {len(filtered)} entries, removed {removed_count} NSFW entries.")

def main():
    print("🚀 Starting NSFW filter script...\n")
    for index_file in INDEX_FILES:
        filter_index_file(index_file)
    print("\n🏁 All done.")

if __name__ == "__main__":
    main()
