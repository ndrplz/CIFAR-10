"""
Class that encapsulates CIFAR-10 dataset.
"""
from pathlib import Path

from cifar.downloader import Downloader


class CIFAR10:
    # URL to download the dataset from Toronto university
    cifar_url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'

    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)
        self.tgz_filename = 'cifar-10-python.tar.gz'

        if not self.dataset_root.exists():
            self._download_cifar10()

    def _download_cifar10(self):
        """
        Download the CIFAR10 `tar.gz` file from Toronto university
        """
        print(f'Downloading CIFAR-10 from {self.cifar_url}...', flush=True)
        Downloader().download_file(url=self.cifar_url, filename=self.tgz_filename)
        print('\nDone.')
