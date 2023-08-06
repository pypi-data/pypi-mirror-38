import os
import zipfile


def zipdir(path, dest, pattern=None):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(path):
            for file in files:
                fp = os.path.join(root, file)
                if not pattern or pattern(fp):
                    zf.write(fp, arcname=os.path.relpath(fp, path))
