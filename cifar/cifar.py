"""
Class that encapsulates CIFAR-10 dataset.

The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes,
 with 6000 images per class. There are 50000 training images and 10000 test images.
"""
import pickle
import numpy as np
from pathlib import Path

from cifar.utils import Downloader
from cifar.utils import Extractor


class CIFARSample:
    def __init__(self, image, label, filename):
        self.image = image
        self.label = label
        self.filename = filename


class CIFAR10:
    # URL to download the dataset from Toronto university
    cifar_url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'

    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)
        self.tgz_filename = Path('cifar-10-python.tar.gz')

        # There are 50000 training images and 10000 test images.
        self.samples = {
            'train': np.ndarray(shape=(50000,), dtype=CIFARSample),
            'test': np.ndarray(shape=(10000,), dtype=CIFARSample),
        }

        # Possibly download and extract the dataset
        if not self.dataset_root.is_dir():
            self._download_and_extract_cifar10()

        # Unpickle the five train batches
        for batch_f in self.dataset_root.glob('data_batch*'):
            self._unpickle_data_batch(batch_f, split='train')

        # Unpickle the only test batch
        self._unpickle_data_batch(self.dataset_root / 'test_batch', split='test')

    def _unpickle_data_batch(self, batch_file, split):
        # Read pickle file
        with open(batch_file, 'rb') as f:
            data = pickle.load(f, encoding='bytes')

        # Handle the fact that train set is split into five batch files
        samples_start_idx = 0
        if split == 'train':
            batch_num = int(batch_file.name[-1])
            samples_start_idx = int(10000 * (batch_num - 1))

        # Each pickle batch file contains 10000 examples
        for i in range(10000):
            idx = samples_start_idx + i
            sample = CIFARSample(image=data[b'data'][i].reshape(32, 32, 3),
                                 label=data[b'labels'][i],
                                 filename=data[b'filenames'][i].decode())
            self.samples[split][idx] = sample

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
