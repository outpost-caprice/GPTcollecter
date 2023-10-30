import os
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from ErrorLogger import ErrorLogger

class FileManager:

  def __init__(self, output_dir, log_file="file_manager_errors.log"):
    self.output_dir = Path(output_dir)
    self.logger = ErrorLogger(log_file)
    self._create_output_dir()

  def _create_output_dir(self):
    try:
      self.output_dir.mkdir(parents=True, exist_ok=True) 
    except Exception as e:
      self.logger.log(f"出力ディレクトリの作成中にエラーが発生しました: {e}")

  def save_summary(self, text, filename):
    try:
      filepath = self.output_dir / filename
      with open(filepath, 'w') as f:
        f.write(text)
      
      # バックアップ
      self._backup(filepath)
        
    except Exception as e:
      self.logger.log(f"サマリーの保存中にエラーが発生しました: {e}")

  def _backup(self, filepath):
    backup_dir = self.output_dir / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / filepath.name
    with open(filepath) as src, open(backup_path, 'w') as dst:
      dst.write(src.read())

  def make_zipfile(self, name):
    try:
      with ZipFile(name, 'w') as zip:
        for path in self.output_dir.glob('*'):
          zip.write(path, path.name)
    except Exception as e:
      self.logger.log(f"ZIPファイルの作成中にエラーが発生しました: {e}")