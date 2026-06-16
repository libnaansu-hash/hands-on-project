import logging
from datetime import datetime
from pathlib import Path

# ── Setup logging ──────────────────────────────────────────────────
log_filename = f'organiser_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),              # print to terminal
        logging.FileHandler(log_filename)     # write to log file
    ]
)
log = logging.getLogger('FileOrganiser')

log.info('FileOrganiser bot started')



# ── Extension → subfolder map ──────────────────────────────────────
EXT_MAP = {
    # Documents
    '.pdf': 'documents',
    '.docx': 'documents',
    '.doc': 'documents',
    '.pptx': 'documents',
    '.ppt': 'documents',
    '.odt': 'documents',

    # Data files
    '.csv': 'data',
    '.xlsx': 'data',
    '.xls': 'data',
    '.json': 'data',
    '.xml': 'data',
    '.sql': 'data',

    # Images
    '.jpg': 'images',
    '.jpeg': 'images',
    '.png': 'images',
    '.gif': 'images',
    '.bmp': 'images',
    '.tiff': 'images',
    '.svg': 'images',
    '.webp': 'images',
    '.ico': 'images',

    # Text files
    '.txt': 'text',
    '.md': 'text',
    '.rtf': 'text',
    '.log': 'text',

    # Scripts and code
    '.py': 'scripts',
    '.js': 'scripts',
    '.sh': 'scripts',
    '.html': 'scripts',
    '.css': 'scripts',
    '.java': 'scripts',
    '.cpp': 'scripts',
    '.c': 'scripts',
    '.php': 'scripts',
    '.ipynb': 'scripts',

    # Videos
    '.mp4': 'videos',
    '.mov': 'videos',
    '.avi': 'videos',
    '.mkv': 'videos',
    '.wmv': 'videos',
    '.flv': 'videos',
    '.webm': 'videos',

    # Audio
    '.mp3': 'audio',
    '.wav': 'audio',
    '.aac': 'audio',
    '.flac': 'audio',
    '.ogg': 'audio',
    '.m4a': 'audio',
    '.wma': 'audio',

    # Archives
    '.zip': 'archives',
    '.rar': 'archives',
    '.7z': 'archives',
    '.tar': 'archives',
    '.gz': 'archives',

    # Executables and installers
    '.exe': 'applications',
    '.msi': 'applications',
    '.apk': 'applications',

    # E-books
    '.epub': 'ebooks',
    '.mobi': 'ebooks',

    # Fonts
    '.ttf': 'fonts',
    '.otf': 'fonts',

    # Design files
    '.psd': 'designs',
    '.ai': 'designs',
    '.fig': 'designs',
}

import shutil

def organise(source_folder: str) -> dict:
    """
    Organise files in source_folder into subfolders by extension.
    Returns a summary dict: { category: count }
    """
    source = Path(source_folder)

    if not source.exists():
        log.error(f'Source folder not found: {source}')
        return {}

    log.info(f'Scanning folder: {source.resolve()}')

    summary = {}     # { category: count }
    skipped = []     # files with unknown extensions

    for file in source.iterdir():
        if not file.is_file():
            continue    # skip subdirectories

        ext = file.suffix.lower()

        if ext not in EXT_MAP:
            log.warning(f'Unknown extension — skipping: {file.name}')
            skipped.append(file.name)
            continue

        category = EXT_MAP[ext]
        dest_folder = source / category
        dest_folder.mkdir(exist_ok=True)

        dest_path = dest_folder / file.name
        shutil.move(str(file), str(dest_path))

        log.info(f'Moved [{category}] {file.name}')
        summary[category] = summary.get(category, 0) + 1

    if skipped:
        log.warning(f'Skipped {len(skipped)} file(s) with unknown extensions: {skipped}')

    return summary

def backup(source_folder: str) -> str:
    """
    Zip the organised folder and return the archive filename.
    """
    source = Path(source_folder)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f'{source.name}_backup_{timestamp}'

    log.info(f'Creating backup archive: {archive_name}.zip')
    shutil.make_archive(archive_name, 'zip', str(source))
    log.info(f'Backup complete: {archive_name}.zip')

    return f'{archive_name}.zip'

def print_summary(summary: dict) -> None:
    """Print a formatted summary table to the terminal."""
    if not summary:
        log.info('No files were organised.')
        return

    total = sum(summary.values())
    print('\n' + '─' * 40)
    print(f'  📊 Summary — {total} files organised')
    print('─' * 40)
    for category, count in sorted(summary.items()):
        bar = '█' * count
        print(f'  {category:<12} {bar}  ({count})')
    print('─' * 40 + '\n')

if __name__ == '__main__':
    SOURCE = Path.home() / 'Downloads'

    log.info('=== Starting File Organiser ===')

    if not SOURCE.exists():
        log.error(f'Source folder not found: {SOURCE}')
    else:
        summary = organise(SOURCE)
        archive = backup(SOURCE)
        print_summary(summary)

        log.info('=== Done ===')
        log.info(f'Backup saved to: {archive}')
