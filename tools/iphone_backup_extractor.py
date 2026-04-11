#!/usr/bin/env python3
"""
iPhone Backup Extractor
-----------------------
Scans an iTunes/Finder iPhone backup, presents extractable content categories,
and copies selected files to a destination with original filenames.

Usage:
    python3 iphone_backup_extractor.py --backup /path/to/backup --dest /path/to/output
    python3 iphone_backup_extractor.py  # interactive mode
"""

import argparse
import os
import shutil
import sqlite3
import sys
import plistlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
#  ANSI Colors
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

def c(color, text): return f"{color}{text}{C.RESET}"
def bold(text):     return c(C.BOLD, text)
def dim(text):      return c(C.DIM, text)
def ok(text):       return c(C.GREEN, text)
def warn(text):     return c(C.YELLOW, text)
def err(text):      return c(C.RED, text)
def info(text):     return c(C.CYAN, text)
def hi(text):       return c(C.MAGENTA, text)


# ─────────────────────────────────────────────
#  File type definitions
#  Maps category → (label, domains, path patterns, extensions)
# ─────────────────────────────────────────────
CATEGORIES = {
    "photos": {
        "label": "📷  Photos & Videos",
        "domains": ["CameraRollDomain"],
        "path_patterns": [],
        "extensions": [".jpg", ".jpeg", ".heic", ".heif", ".png", ".gif",
                       ".bmp", ".tiff", ".tif", ".webp", ".dng", ".raw",
                       ".mov", ".mp4", ".m4v", ".avi", ".3gp", ".mkv"],
        "description": "Camera roll photos and videos (HEIC, JPG, MOV, MP4, etc.)"
    },
    "sms": {
        "label": "💬  Messages (SMS/iMessage)",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/SMS/sms.db"],
        "extensions": [],
        "description": "Full SMS and iMessage database"
    },
    "contacts": {
        "label": "👤  Contacts",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/AddressBook/AddressBook.sqlitedb",
                          "Library/AddressBook/AddressBookImages.sqlitedb"],
        "extensions": [],
        "description": "Contacts database and photos"
    },
    "call_history": {
        "label": "📞  Call History",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/CallHistoryDB/CallHistory.storedata"],
        "extensions": [],
        "description": "Incoming, outgoing, and missed calls"
    },
    "voicemail": {
        "label": "📼  Voicemail",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Voicemail/voicemail.db"],
        "extensions": [".amr"],
        "description": "Voicemail database and audio files"
    },
    "notes": {
        "label": "📝  Notes",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Notes/notes.sqlite"],
        "extensions": [],
        "description": "Apple Notes database"
    },
    "calendars": {
        "label": "📅  Calendars",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Calendar/Calendar.sqlitedb"],
        "extensions": [],
        "description": "Calendar events and reminders"
    },
    "reminders": {
        "label": "✅  Reminders",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Reminders/"],
        "extensions": [],
        "description": "Reminders database"
    },
    "safari": {
        "label": "🌐  Safari (History, Bookmarks, Tabs)",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Safari/"],
        "extensions": [],
        "description": "Safari browsing history, bookmarks, and open tabs"
    },
    "health": {
        "label": "❤️   Health & Fitness Data",
        "domains": ["HealthDomain", "HomeDomain"],
        "path_patterns": ["Library/Health/"],
        "extensions": [],
        "description": "Apple Health database (steps, heart rate, workouts, etc.)"
    },
    "location": {
        "label": "📍  Location History",
        "domains": ["HomeDomain", "RootDomain"],
        "path_patterns": ["Library/Caches/locationd/", "Library/Maps/"],
        "extensions": [],
        "description": "Location services cache and Maps data"
    },
    "wallet": {
        "label": "💳  Wallet & Passes",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Passes/"],
        "extensions": [".pkpass"],
        "description": "Apple Wallet passes (boarding passes, tickets, cards)"
    },
    "keychain": {
        "label": "🔑  Keychain",
        "domains": ["KeychainDomain"],
        "path_patterns": ["keychain-backup.plist"],
        "extensions": [],
        "description": "Saved passwords and credentials (encrypted if backup is encrypted)"
    },
    "mail": {
        "label": "✉️   Mail",
        "domains": ["HomeDomain"],
        "path_patterns": ["Library/Mail/"],
        "extensions": [],
        "description": "Apple Mail app data"
    },
    "whatsapp": {
        "label": "💚  WhatsApp",
        "domains": [],
        "path_patterns": [],
        "app_bundle": "net.whatsapp.WhatsApp",
        "extensions": [],
        "description": "WhatsApp messages, media, and attachments"
    },
    "signal": {
        "label": "🔒  Signal",
        "domains": [],
        "path_patterns": [],
        "app_bundle": "org.whispersystems.signal",
        "extensions": [],
        "description": "Signal encrypted messages database"
    },
    "telegram": {
        "label": "✈️   Telegram",
        "domains": [],
        "path_patterns": [],
        "app_bundle": "ph.telegra.Telegraph",
        "extensions": [],
        "description": "Telegram messages and media"
    },
    "instagram": {
        "label": "📸  Instagram",
        "domains": [],
        "path_patterns": [],
        "app_bundle": "com.burbn.instagram",
        "extensions": [],
        "description": "Instagram app data and cached media"
    },
    "facebook": {
        "label": "👥  Facebook / Messenger",
        "domains": [],
        "path_patterns": [],
        "app_bundle": "com.facebook",
        "extensions": [],
        "description": "Facebook and Messenger app data"
    },
    "voice_memos": {
        "label": "🎙️  Voice Memos",
        "domains": ["MediaDomain"],
        "path_patterns": ["Media/Recordings/"],
        "extensions": [".m4a", ".mp3", ".wav", ".aiff", ".caf"],
        "description": "Voice Memo recordings"
    },
    "podcasts": {
        "label": "🎧  Podcasts",
        "domains": ["MediaDomain"],
        "path_patterns": ["Media/Podcasts/"],
        "extensions": [".mp3", ".m4a"],
        "description": "Downloaded podcast episodes"
    },
    "music": {
        "label": "🎵  Music",
        "domains": ["MediaDomain"],
        "path_patterns": ["Media/iTunes_Control/Music/"],
        "extensions": [".mp3", ".m4a", ".aac", ".flac", ".wav"],
        "description": "Locally synced music files"
    },
    "books": {
        "label": "📚  Books & Documents",
        "domains": ["MediaDomain", "HomeDomain"],
        "path_patterns": ["Media/Books/", "Library/Books/"],
        "extensions": [".epub", ".pdf", ".ibooks"],
        "description": "Apple Books and iBooks content"
    },
    "crash_logs": {
        "label": "💥  Crash Logs",
        "domains": ["HomeDomain", "RootDomain"],
        "path_patterns": ["Library/Logs/CrashReporter/"],
        "extensions": [".ips", ".crash"],
        "description": "App and system crash reports"
    },
    "app_data_all": {
        "label": "📦  All App Data (everything in AppDomain)",
        "domains": [],
        "path_patterns": [],
        "domain_prefix": "AppDomain-",
        "extensions": [],
        "description": "All third-party app data (databases, caches, documents)"
    },
    "everything": {
        "label": "🗂️  Everything (full backup extraction)",
        "domains": ["ALL"],
        "path_patterns": [],
        "extensions": [],
        "description": "Extract every file in the backup with original paths preserved"
    }
}

KNOWN_EXTENSIONS = {
    # Images
    ".jpg", ".jpeg", ".heic", ".heif", ".png", ".gif", ".bmp", ".tiff",
    ".tif", ".webp", ".dng", ".raw", ".cr2", ".nef",
    # Video
    ".mov", ".mp4", ".m4v", ".avi", ".3gp", ".mkv", ".wmv", ".flv",
    # Audio
    ".mp3", ".m4a", ".aac", ".wav", ".aiff", ".flac", ".ogg", ".caf", ".amr",
    # Documents
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",
    ".rtf", ".pages", ".numbers", ".key",
    # Data
    ".sqlite", ".sqlitedb", ".db", ".storedata", ".plist", ".json", ".xml",
    # Archives
    ".zip", ".gz", ".tar", ".ipa", ".pkpass",
    # Ebooks
    ".epub", ".ibooks",
    # Logs
    ".ips", ".crash", ".log",
}


# ─────────────────────────────────────────────
#  Backup Scanner
# ─────────────────────────────────────────────
class BackupScanner:
    def __init__(self, backup_path: Path):
        self.backup_path = backup_path
        self.manifest_db = backup_path / "Manifest.db"
        self.info_plist  = backup_path / "Info.plist"
        self.manifest_plist = backup_path / "Manifest.plist"
        self.conn = None
        self.device_info = {}
        self.all_files = []
        self.unknown_types = set()

    def validate(self) -> bool:
        if not self.backup_path.exists():
            print(err(f"✗ Backup path does not exist: {self.backup_path}"))
            return False
        if not self.manifest_db.exists():
            print(err(f"✗ Manifest.db not found in: {self.backup_path}"))
            return False
        if not self.info_plist.exists():
            print(err(f"✗ Info.plist not found in: {self.backup_path}"))
            return False
        return True

    def load_device_info(self):
        try:
            with open(self.info_plist, "rb") as f:
                p = plistlib.load(f)
            self.device_info = {
                "Device Name":    p.get("Device Name", "Unknown"),
                "Product Name":   p.get("Product Name", "Unknown"),
                "Product Type":   p.get("Product Type", "Unknown"),
                "iOS Version":    p.get("Product Version", "Unknown"),
                "Serial Number":  p.get("Serial Number", "Unknown"),
                "Phone Number":   p.get("Phone Number", "Unknown"),
                "IMEI":           p.get("IMEI", "Unknown"),
                "Last Backup":    str(p.get("Last Backup Date", "Unknown")),
                "GUID":           p.get("GUID", "Unknown"),
            }
        except Exception as e:
            print(warn(f"⚠ Could not parse Info.plist: {e}"))

        try:
            with open(self.manifest_plist, "rb") as f:
                mp = plistlib.load(f)
            self.device_info["Encrypted"] = str(mp.get("IsEncrypted", False))
            self.device_info["Passcode Protected"] = str(mp.get("WasPasscodeSet", False))
        except Exception:
            pass

    def connect_db(self):
        import tempfile
        try:
            # SQLite cannot open databases over NFS/SMB — copy to temp first
            tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
            self._tmp_db_path = tmp.name
            tmp.close()
            print(info("⟳  Copying Manifest.db to temp location for SQLite access..."))
            shutil.copy2(str(self.manifest_db), self._tmp_db_path)
            for ext in ["-wal", "-shm"]:
                src = Path(str(self.manifest_db) + ext)
                if src.exists():
                    shutil.copy2(str(src), self._tmp_db_path + ext)
            self.conn = sqlite3.connect(self._tmp_db_path)
            self.conn.row_factory = sqlite3.Row
            print(ok("✓  Manifest.db ready\n"))
        except sqlite3.Error as e:
            print(err(f"✗ Could not open Manifest.db: {e}"))
            sys.exit(1)
        except Exception as e:
            print(err(f"✗ Could not copy Manifest.db: {e}"))
            sys.exit(1)

    def load_all_files(self):
        cur = self.conn.cursor()
        cur.execute("SELECT fileID, domain, relativePath FROM Files")
        self.all_files = cur.fetchall()

    def scan_category(self, cat_key: str) -> list:
        cat = CATEGORIES[cat_key]
        results = []

        for row in self.all_files:
            fid, domain, path = row["fileID"], row["domain"], row["relativePath"] or ""

            # ALL / everything
            if "ALL" in cat.get("domains", []):
                results.append(row)
                continue

            # Domain prefix match (e.g. AppDomain-)
            if "domain_prefix" in cat:
                if domain.startswith(cat["domain_prefix"]):
                    results.append(row)
                continue

            # App bundle match
            if "app_bundle" in cat:
                if cat["app_bundle"].lower() in domain.lower():
                    results.append(row)
                continue

            # Domain + path pattern match
            domain_match = domain in cat["domains"] if cat["domains"] else True
            if not domain_match:
                continue

            if cat["path_patterns"]:
                for pattern in cat["path_patterns"]:
                    if path.startswith(pattern) or path == pattern.rstrip("/"):
                        results.append(row)
                        break
            elif cat["extensions"]:
                ext = Path(path).suffix.lower()
                if ext in cat["extensions"]:
                    results.append(row)
            else:
                results.append(row)

        return results

    def find_unknown_types(self):
        seen_extensions = set()
        for row in self.all_files:
            path = row["relativePath"] or ""
            if path:
                ext = Path(path).suffix.lower()
                if ext and ext not in KNOWN_EXTENSIONS:
                    self.unknown_types.add(ext)
        return self.unknown_types

    def get_physical_path(self, file_id: str) -> Path:
        return self.backup_path / file_id[:2] / file_id

    def file_exists(self, file_id: str) -> bool:
        return self.get_physical_path(file_id).exists()


# ─────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────
def print_banner():
    print()
    print(bold(c(C.CYAN, "╔══════════════════════════════════════════════════╗")))
    print(bold(c(C.CYAN, "║") + c(C.WHITE, "      iPhone Backup Extractor  v1.0             ") + c(C.CYAN, "║")))
    print(bold(c(C.CYAN, "╚══════════════════════════════════════════════════╝")))
    print()

def print_device_info(info: dict):
    print(bold(c(C.BLUE, "┌─ Device Information " + "─" * 30)))
    for k, v in info.items():
        color = C.RED if k == "Encrypted" and v == "True" else C.WHITE
        print(f"{c(C.BLUE, '│')}  {dim(k+':'): <25} {c(color, v)}")
    print(c(C.BLUE, "└" + "─" * 51))
    print()

def print_scan_results(results: dict):
    print(bold(c(C.BLUE, "┌─ Available Content " + "─" * 31)))
    print(f"{c(C.BLUE, '│')}  {'#': <4} {'Category': <45} {'Files': >8}  {'Status'}")
    print(f"{c(C.BLUE, '│')}  {'─'*4} {'─'*45} {'─'*8}  {'─'*10}")

    available = []
    for i, (key, (count, present)) in enumerate(results.items(), 1):
        cat = CATEGORIES[key]
        if count == 0:
            status = dim("not found")
            count_str = dim("0")
        elif not present:
            status = warn("in DB only")
            count_str = warn(str(count))
        else:
            status = ok("✓ available")
            count_str = ok(str(count))
            available.append((i, key))

        print(f"{c(C.BLUE, '│')}  {str(i): <4} {cat['label']: <45} {count_str: >8}  {status}")

    print(c(C.BLUE, "└" + "─" * 51))
    print()
    return available

def progress_bar(current, total, width=40):
    pct = current / total if total else 0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"{c(C.CYAN, bar)} {c(C.WHITE, f'{current}/{total}')} {c(C.DIM, f'({pct:.0%})')}"


# ─────────────────────────────────────────────
#  Extractor
# ─────────────────────────────────────────────
def extract_files(scanner: BackupScanner, cat_key: str, files: list, dest: Path):
    cat = CATEGORIES[cat_key]
    cat_dest = dest / cat_key
    cat_dest.mkdir(parents=True, exist_ok=True)

    total = len(files)
    copied = 0
    skipped = 0
    missing = 0
    errors = 0

    print(f"\n{bold(hi('Extracting:'))} {cat['label']}")
    print(f"{dim('Destination:')} {cat_dest}")
    print(f"{dim('Total records:')} {total}")
    print()

    for i, row in enumerate(files, 1):
        fid   = row["fileID"]
        path  = row["relativePath"] or fid
        domain = row["domain"]

        src = scanner.get_physical_path(fid)

        # Build destination path preserving structure
        if cat_key == "everything":
            rel = Path(domain.replace("AppDomain-", "apps/")) / path
        else:
            rel = Path(path)

        dst = cat_dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Print progress every 50 files or on last
        if i % 50 == 0 or i == total:
            bar = progress_bar(i, total)
            print(f"\r  {bar}  {dim(f'copied:{copied} skip:{skipped} miss:{missing} err:{errors}')}", end="", flush=True)

        if not src.exists():
            missing += 1
            continue

        if dst.exists():
            skipped += 1
            continue

        try:
            shutil.copy2(src, dst)
            copied += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"\n  {err(f'Error copying {path}: {e}')}")

    print(f"\n\n  {bold('Done!')}")
    print(f"  {ok(f'✓ Copied:  {copied}')}")
    print(f"  {warn(f'↷ Skipped: {skipped}')} (already exist)")
    print(f"  {c(C.DIM, f'? Missing: {missing}')} (iCloud-only or not backed up)")
    if errors:
        print(f"  {err(f'✗ Errors:  {errors}')}")
    print()

    return copied, skipped, missing, errors


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="iPhone Backup Extractor — extract content from iTunes/Finder backups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--backup", "-b", type=str, help="Path to iPhone backup folder")
    parser.add_argument("--dest",   "-d", type=str, help="Destination folder for extracted files")
    parser.add_argument("--all",    "-a", action="store_true", help="Extract everything without prompting")
    args = parser.parse_args()

    print_banner()

    # ── Get backup path ──
    if args.backup:
        backup_path = Path(args.backup).expanduser()
    else:
        raw = input(f"{bold('Backup path')} {dim('(drag folder here or type path)')}: ").strip().strip("'\"")
        backup_path = Path(raw).expanduser()

    # ── Get destination ──
    if args.dest:
        dest_path = Path(args.dest).expanduser()
    else:
        default_dest = Path.home() / "Desktop" / "iphone_extracted"
        raw = input(f"{bold('Destination')} {dim(f'(default: {default_dest})')}: ").strip().strip("'\"")
        dest_path = Path(raw).expanduser() if raw else default_dest

    print()

    # ── Validate & load ──
    scanner = BackupScanner(backup_path)
    if not scanner.validate():
        sys.exit(1)

    print(info("⟳  Loading device info..."))
    scanner.load_device_info()
    print_device_info(scanner.device_info)

    if scanner.device_info.get("Encrypted") == "True":
        print(err("⚠  This backup is ENCRYPTED. Files may be unreadable without the backup password."))
        print(warn("   Extraction will proceed but databases will be encrypted.\n"))

    print(info("⟳  Scanning Manifest.db..."))
    scanner.connect_db()
    scanner.load_all_files()
    print(ok(f"✓  Loaded {len(scanner.all_files):,} file records\n"))

    # ── Scan all categories ──
    print(info("⟳  Analyzing available content..."))
    scan_results = {}
    for key in CATEGORIES:
        files = scanner.scan_category(key)
        present_count = sum(1 for f in files if scanner.file_exists(f["fileID"]))
        scan_results[key] = (len(files), present_count)
    print(ok("✓  Scan complete\n"))

    # ── Unknown file types ──
    unknown = scanner.find_unknown_types()
    if unknown:
        print(warn(f"⚠  Unknown file extensions found in backup ({len(unknown)} types):"))
        print(f"   {dim(', '.join(sorted(unknown)))}")
        print(f"   {dim('These will be included in the Everything extraction.')}\n")

    # ── Show menu ──
    available = print_scan_results(scan_results)

    if not available:
        print(err("No extractable content found in this backup."))
        sys.exit(0)

    # ── Selection ──
    if args.all:
        selected_keys = [k for k, (count, present) in scan_results.items() if present > 0]
        print(info(f"--all flag set: extracting all {len(selected_keys)} available categories"))
    else:
        print(f"{bold('Select categories to extract:')}")
        print(dim("  Enter numbers separated by commas (e.g. 1,3,5)"))
        print(dim("  Enter 'a' for all available  |  'q' to quit"))
        print()

        while True:
            raw = input(f"{bold('Your choice')} › ").strip().lower()
            if raw == "q":
                print(dim("Exiting."))
                sys.exit(0)
            if raw == "a":
                selected_keys = [k for k, (count, present) in scan_results.items() if present > 0]
                break
            try:
                nums = [int(x.strip()) for x in raw.split(",")]
                idx_map = {i: k for i, k in [(i, k) for i, (k, _) in enumerate(scan_results.items(), 1)]}
                selected_keys = [idx_map[n] for n in nums if n in idx_map]
                if selected_keys:
                    break
                print(warn("  No valid selections. Try again."))
            except ValueError:
                print(warn("  Invalid input. Enter numbers separated by commas."))

    # ── Confirm ──
    print()
    print(bold("Extraction plan:"))
    total_files = 0
    for key in selected_keys:
        count, present = scan_results[key]
        print(f"  {ok('✓')} {CATEGORIES[key]['label']} — {ok(str(present))} files")
        total_files += present

    print(f"\n{bold('Destination:')} {dest_path}")
    print(f"{bold('Total files:')} ~{total_files:,}")
    print()

    confirm = input(f"{bold('Proceed?')} {dim('[Y/n]')} › ").strip().lower()
    if confirm in ("n", "no"):
        print(dim("Aborted."))
        sys.exit(0)

    dest_path.mkdir(parents=True, exist_ok=True)
    print()

    # ── Extract ──
    start_time = datetime.now()
    grand_total = {"copied": 0, "skipped": 0, "missing": 0, "errors": 0}

    for key in selected_keys:
        files = scanner.scan_category(key)
        c_count, s_count, m_count, e_count = extract_files(scanner, key, files, dest_path)
        grand_total["copied"]  += c_count
        grand_total["skipped"] += s_count
        grand_total["missing"] += m_count
        grand_total["errors"]  += e_count

    # ── Summary ──
    elapsed = datetime.now() - start_time
    print(bold(c(C.CYAN, "═" * 52)))
    print(bold(c(C.WHITE, "  Extraction Complete")))
    print(c(C.CYAN, "─" * 52))
    copied_n  = grand_total["copied"]
    skipped_n = grand_total["skipped"]
    missing_n = grand_total["missing"]
    errors_n  = grand_total["errors"]
    print(f"  {ok(f'✓ Files copied:   {copied_n:,}')}")
    print(f"  {warn(f'↷ Files skipped:  {skipped_n:,}')} (already existed)")
    print(f"  {dim(f'? Files missing:  {missing_n:,}')} (iCloud-only)")
    if errors_n:
        print(f"  {err(f'✗ Errors:         {errors_n:,}')}")
    print(f"  {dim(f'⏱ Time elapsed:   {elapsed.seconds}s')}")
    print(f"  {dim(f'📁 Output:         {dest_path}')}")
    print(bold(c(C.CYAN, "═" * 52)))
    print()


if __name__ == "__main__":
    main()