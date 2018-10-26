"""
Simple class to download a file avoiding wget dependency.
"""
import sys
import urllib.request


class Downloader:
    """
    Simple class to download a file avoiding wget dependency.
    """
    def __init__(self):
        pass

    def download_file(self, url: str, filename: str):
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
