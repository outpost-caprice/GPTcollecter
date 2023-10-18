import os
from pathlib import Path
from zipfile import ZipFile

class FileManager:

  def __init__(self, output_dir):
    self.output_dir = Path(output_dir)

  def save_summary(self, text, url):
    filename = self._get_filename(url)
    file_path = self.output_dir / filename
    with open(file_path, 'w') as f:
      f.write(text)

  def _get_filename(self, url):
    return url.replace('/', '_') + '.txt'

  def make_zipfile(self, name):
    with ZipFile(name, 'w') as zip:
      for path in self.output_dir.glob('*'):
        zip.write(path, path.name)