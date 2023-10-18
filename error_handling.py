
class ErrorHandling:
    def __init__(self, error_file_path='error_urls.txt'):
        self.error_file_path = error_file_path

    def log_error(self, url, error_message):
        with open(self.error_file_path, 'a') as f:
            f.write(f"URL: {url}, Error: {error_message}\n")
