
def save_to_file(summary, url, file_path='summary.txt'):
    with open(file_path, 'a') as f:
        f.write(f"Summary: {summary}\n")
        f.write(f"URL: {url}\n\n")

def create_zip_file(files, zip_file_name):
    import zipfile
    import os
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
