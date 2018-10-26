"""
Simple classes to download and extract CIFAR-10 data avoiding wget dependencies.
"""
import sys
import tarfile
import urllib.request
from pathlib import Path


class Downloader:
    """
    Simple class to download a file avoiding wget dependency.
    """
    def __init__(self):
        pass

    def download_file(self, url: str, filename: Path):
        """
        Download a file from remote URL.

        :param url: URL of file to be downloaded
        :param filename: Filename of downloaded file on disk
        :return: None
        """
        urllib.request.URLopener().retrieve(url, filename, reporthook=self._progress_hook)

    @staticmethod
    def _progress_hook(count, block_size, total_size):
        """ Function hook for printing download progress"""
        percent = int(count * block_size / total_size * 100)
        msg = f'\r{percent}% ' + '[' + '.' * percent + ' ' * (100 - percent) + ']'
        sys.stdout.write(msg)
        sys.stdout.flush()


class Extractor:
    """
    Simple class to extract CIFAR-10 archive
    """
    def __init__(self):
        self.mode = 'r:gz'  # tar.gz

    def extract(self, archive_path, extract_path):
        tarfile.open(name=archive_path, mode=self.mode).extractall(extract_path)
