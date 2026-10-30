import os, time, shutil

temp_dir = os.environ.get('TEMP')
now = time.time()
freed_bytes = 0

# Clean old files in TEMP
if temp_dir and os.path.exists(temp_dir):
    for entry in os.scandir(temp_dir):
        try:
            if entry.is_file():
                # Older than 1 hour or starts with tmp
                if entry.name.startswith(('tmp', '~')) or (now - entry.stat().st_mtime) > 3600:
                    sz = entry.stat().st_size
                    os.remove(entry.path)
                    freed_bytes += sz
            elif entry.is_dir():
                if entry.name.startswith(('tmp', 'pip-', 'vscode-')) and (now - entry.stat().st_mtime) > 3600:
                    shutil.rmtree(entry.path, ignore_errors=True)
        except Exception:
            pass

# Also clean older tempmediaStorage files from past sessions (older than 1 hour)
media_dir = r'C:\Users\Abraham.sisay\.gemini\antigravity-ide\brain\e26cdabe-af62-4d68-8170-94db7d0ea027\.tempmediaStorage'
if os.path.exists(media_dir):
    for entry in os.scandir(media_dir):
        try:
            if entry.is_file() and (now - entry.stat().st_mtime) > 1800:
                sz = entry.stat().st_size
                os.remove(entry.path)
                freed_bytes += sz
        except Exception:
            pass

print(f"Freed: {freed_bytes / (1024*1024):.2f} MB")
