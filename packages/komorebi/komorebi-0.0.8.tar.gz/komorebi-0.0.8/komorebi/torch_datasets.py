# -*- coding: utf-8 -*-

import numpy as np

from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader

from komorebi.parallel import ParallelData
from komorebi.util import absolute_path, timing

class ParallelDataset(Dataset):
    def __init__(self, src_file, trg_file, src_max_len=None, trg_max_len=None,
                 **kwargs):
        """
        This is the object to be used by PyTorch.
        """
        # ParallelData object is an iterator packe with goodies =)
        self._data = ParallelData(src_file, trg_file, **kwargs)
        # Iterate through the dataset to get the source and data.
        _source_texts, _target_texts = zip(*self._data)
        self._data.reset() # Resets the iterator to the start.
        # Pre-computes the no. of data points.
        self._len = len(_source_texts)
        # Precompute the real leangth of the source and target text.
        self.source_lens = list(map(len, _source_texts))
        self.target_lens = list(map(len, _target_texts))
        # Set the max lengths if not specified by user.
        self.src_max_len = src_max_len if src_max_len else max(self.source_lens)
        self.trg_max_len = trg_max_len if trg_max_len else max(self.target_lens)
        # Converts the indices to torch tensors.
        pad_idx = self._data.src_data.PAD_IDX
        self.source_texts = np.array([self.pad_sequence(_s, self.src_max_len, pad_idx)
                                      for _s in _source_texts])
        self.target_texts = np.array([self.pad_sequence(_t, self.trg_max_len, pad_idx)
                                      for _t in _target_texts])

    def pad_sequence(self, sequence, max_len, pad_idx):
        padded_sequence = np.zeros(max_len, dtype=np.int64)
        padded_sequence[:len(sequence)] = sequence[:max_len]
        if pad_idx != 0:
            padded_sequence[len(x):] = pad_idx
        return padded_sequence

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        return {'x': self.source_texts[index],
                'x_len': np.clip(self.source_lens[index], 1, self.src_max_len),
                'y': self.target_texts[index]}

    def batches(self, batch_size, shuffle=True):
        dataloader = DataLoader(dataset=self, batch_size=batch_size, shuffle=shuffle)
        for data_dict in dataloader:
            # Sort indices of data in batch by lengths.
            sorted_indices = np.array(data_dict['x_len']).argsort()[::-1].tolist()
            data_batch = {name:_tensor[sorted_indices]
                          for name, _tensor in data_dict.items()}
            yield data_batch

    @timing
    def save(self, saveto, save_tensors=True):
        pass

    @timing
    def load():
        pass
