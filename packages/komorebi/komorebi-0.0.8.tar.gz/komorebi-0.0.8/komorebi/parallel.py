# -*- coding: utf-8 -*-

import heapq
import itertools
import json
import os
import pickle
import random
import sys

from collections import Iterator
from itertools import chain
from pathlib import Path
from operator import itemgetter

from komorebi.text import TextData
from komorebi.util import per_chunk, timing
from komorebi.util import DataError

class ParallelData(Iterator):
    def __init__(self,
                 src_filename=None,
                 trg_filename=None,
                 src_vocab_size=10**5,
                 trg_vocab_size=None,
                 chunk_size=10**5,
                 delimiter=None,
                 size_mb=4024,
                 pad_symbol='<pad>',
                 start_symbol='<s>',
                 end_symbol='</s>',
                 unknown_symbol='<unk>',
                 default_pad_start=False,
                 default_pad_end=True,
                 filter_on='tf',
                 prune_at=10**10,
                 encoding='utf8',
                 **kwargs):
        """
        This is the object to store parallel text and read them into vocabulary
        indices. The object is an iterable that yields tuples of the vocabulary
        indices, one from the source sentence, another from the target.

        :param src_filename: Textfile that contains source sentences.
        :type src_filename: str
        :param trg_filename: Textfile that contains target sentences.
        :type trg_filename: str
        :param src_vocab_size: Max no. of words to keep in the source vocab.
        :type src_vocab_size: int
        :param trg_vocab_size: Max no. of words to keep in the target vocab.
        :type trg_vocab_size: int
        :param chunk_size: Use to limit no. of sentences to load at a time when populating the vocabulary.
        :type chunk_size: int
        :param delimiter: Delimiter to split on when "tokenizing"
        :type delimiter: str
        :param size_mb: Memory footprint of the bounter object use to count the vocab.
        :type size_mb: int
        :param start_symbol: Start symbol use for padding.
        :type start_symbol: str
        :param end_symbol: End symbol use for padding.
        :type end_symbol: str
        :param unknown_symbol: Unknown symbol for OOV words.
        :type unknown_symbol: str
        :param filter_on: Option to filter on term-freq ('tf') or doc-freq ('df')
        :type filter_on: str
        :param prune_at: *prune_at* parameter used by gensim.Dictionary
        :type prune_at: int
        """

        if 'loadfrom' not in kwargs: # Creating.
            self.default_pad_start = default_pad_start
            self.default_pad_end = default_pad_end
            print('Creating source TextData...', end='\n', file=sys.stderr)
            self.src_data = TextData(src_filename, src_vocab_size, **kwargs)
            print('Creating target TextData...', end='\n', file=sys.stderr)
            self.trg_data = TextData(trg_filename, trg_vocab_size, **kwargs)
            self.iterable = self._iterate()

        else: # Loading.
            self.load(kwargs['loadfrom'],
                      src_filename, trg_filename,
                      kwargs.get('load_counter', False))
            self.iterable = self._iterate()

    @timing
    def load(self, loadfrom, src_filename=None, trg_filename=None,
             load_counter=False):
        """
        The load function.
        :param loadfrom: The path to load the directory for the ParallelData.
        :type loadfrom: str
        :param load_counter: Whether to load the src and trg bounter objects.
        :type load_counter: bool
        """
        config_file = loadfrom + '/ParallelData.json'
        if not Path(config_file).exists():
            raise DataError('{} config file not found!!'.format(config_file))
        else:
            print('Loading ParallelData from {}'.format(config_file),
                  end=' ', file=sys.stderr)
            with open(config_file) as fin:
                self.__dict__ = json.load(fin)

            if ('src_data' not in self.__dict__ or
                'trg_data' not in self.__dict__):
                raise DataError('source/target TextData not found!!')

            json.load(open(config_file))['src_data']
            json.load(open(config_file))['trg_data']

            # Actual loading of TextData objects.
            textdatas = {'src_data': src_filename, 'trg_data': trg_filename}
            for textdata, filename in textdatas.items():
                try:
                    self.__dict__[textdata] = TextData(loadfrom=self.__dict__[textdata],
                                                       filename=filename,
                                                       load_counter=load_counter)
                except DataError as e:
                    raise DataError("You need to set the src_filename and trg_filename when loading TextData, e.g.\n"
                                    "\tParallelData(loadfrom='path/to/textdata', \n"
                                    "\t\t\tsrc_filename='srcfile.txt', \n"
                                    "\t\t\ttrg_filename='trgfile.txt')")

    @timing
    def save(self, saveto, save_counter=False, copy_data=True):
        """
        The save function.
        :param saveto: The path to save the directory for the ParallelData.
        :type saveto: str
        :param save_counter: Whether to save the src and trg bounter objects.
        :type save_counter: bool
        :para copy_data: Make a local copy of the data.
        :type copy_data: bool
        """
        print("Saving ParallelData to {saveto}".format(saveto=saveto), end='\n', file=sys.stderr)
        # Create the directory if it doesn't exist.
        if not Path(saveto).exists():
            os.makedirs(saveto)
            os.makedirs(saveto+'/src/')
            os.makedirs(saveto+'/trg/')

        self.src_data.save(saveto+'/src/', save_counter, copy_data)
        self.trg_data.save(saveto+'/trg/', save_counter, copy_data)

        # Initialize the config file.
        config_json = {'src_data': saveto+'/src/',
                       'trg_data': saveto+'/trg/'}

        # Dump the config file.
        with open(saveto+'/ParallelData.json', 'w') as fout:
            json.dump(config_json, fout, indent=2)
        print("Saving ParallelData to {saveto}".format(saveto=saveto), end=' ', file=sys.stderr)

    def reset(self):
        """
        Resets the iterator to the 0th item.
        """
        self.iterable = self._iterate()

    def _iterate(self):
        """
        The helper function to iterate through the source and target file
        and convert the lines into vocabulary indices.
        """
        for src_line, trg_line in zip(self.src_data.lines(), self.trg_data.lines()):
            src_sent = self.src_data.vectorize(src_line,
                                               self.default_pad_start,
                                               self.default_pad_end)
            trg_sent = self.trg_data.vectorize(trg_line,
                                               self.default_pad_start,
                                               self.default_pad_end)
            yield src_sent, trg_sent

    def __next__(self):
        return next(self.iterable)

    def shuffle(self):
        return iter(sorted(self, key=lambda k: random.random()))
