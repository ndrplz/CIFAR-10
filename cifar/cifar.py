"""
Class that encapsulates CIFAR-10 dataset.
"""
from pathlib import Path

from cifar.utils import Downloader
from cifar.utils import Extractor


class CIFAR10:
    # URL to download the dataset from Toronto university
    cifar_url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'

    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)
        self.tgz_filename = Path('cifar-10-python.tar.gz')

        # Possibly download and extract the dataset
        if not self.dataset_root.is_dir():
            self._download_and_extract_cifar10()

    def _download_and_extract_cifar10(self):
        """
        Download the CIFAR10 `tar.gz` file from Toronto university
        """
        # Possibly download the dataset
        if not self.tgz_filename.is_file():
            print(f'Downloading CIFAR-10 dataset from {self.cifar_url}...', flush=True)
            Downloader().download_file(url=self.cifar_url, filename=self.tgz_filename)
            print('\nDone.')

        # Extract downloaded archive
        print(f'Extracting {self.tgz_filename} to {self.dataset_root}...', flush=True)
        Extractor().extract(self.tgz_filename, extract_path=self.dataset_root)
        print('Done.')

        # Move all files into the chosen dataset root (up one directory)
        [f.rename(f.absolute().parents[1] / f.name) for f in self.dataset_root.glob('*/*')]
        Path(self.dataset_root / 'cifar-10-batches-py').rmdir()  # remove inner directory

        # Finally remove the archive
        self.tgz_filename.unlink()
