import os
import zipfile

def zipdir(path, zip, filter=None):
    with zipfile.ZipFile(zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(path):
            for file in files:
                fp = os.path.join(root, file)
                if not filter or filter(fp):
                    zf.write(fp, arcname=os.path.relpath(fp, path))