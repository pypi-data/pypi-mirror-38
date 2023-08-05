from typing import List
import os
import warnings

import strpipe as sp

from .base import Indexer
from .pipe_indexer import PipeIndexer
from .utils import load_json, save_json, mkdir_p


class CharIndexer(PipeIndexer):

    def __init__(
            self,
            word2vec=None,
            sos_token: str = '<sos>',
            eos_token: str = '</s>',
            pad_token: str = '<pad>',
            unk_token: str = '<unk>',
            maxlen: int = 50,
        ):
        self.word2vec = word2vec
        self._token2index_pipe_layer = None
        super().__init__(
            sos_token=sos_token,
            eos_token=eos_token,
            pad_token=pad_token,
            unk_token=unk_token,
            maxlen=maxlen,
        )

    @classmethod
    def create_without_word2vec(
            cls,
            sos_token: str = '<sos>',
            eos_token: str = '</s>',
            pad_token: str = '<pad>',
            unk_token: str = '<unk>',
            maxlen: int = 50,
        ):
        indexer = cls(
            sos_token=sos_token,
            eos_token=eos_token,
            pad_token=pad_token,
            unk_token=unk_token,
            maxlen=maxlen,
        )
        return indexer

    @classmethod
    def create_with_word2vec(
            cls,
            word2vec,
            sos_token: str = '<sos>',
            eos_token: str = '</s>',
            pad_token: str = '<pad>',
            unk_token: str = '<unk>',
            maxlen: int = 50,
        ):
        indexer = cls(
            word2vec=word2vec,
            sos_token=sos_token,
            eos_token=eos_token,
            pad_token=pad_token,
            unk_token=unk_token,
            maxlen=maxlen,
        )
        return indexer

    def _build_pipe(self):
        p = sp.Pipe()
        p.add_step_by_op_name('CharTokenizer')
        p.add_step_by_op_name(
            'AddSosEos',
            op_kwargs={
                'sos_token': self.sos_token,
                'eos_token': self.eos_token,
            },
        )
        p.add_checkpoint()
        p.add_step_by_op_name(
            'Pad',
            op_kwargs={
                'pad_token': self.pad_token,
                'maxlen': self.maxlen,
            },
        )
        if self.word2vec is None:
            p.add_step_by_op_name(
                'TokenToIndex',
                op_kwargs={
                    'unk_token': self.unk_token,
                },
            )
        else:
            p.add_step_by_op_name(
                'TokenToIndex',
                op_kwargs={
                    'unk_token': self.unk_token,
                    'token2index': self.word2vec['token2index'],
                },
            )
        self._token2index_pipe_layer = 3
        return p

    @property
    def token2index_pipe_layer(self):
        return self._token2index_pipe_layer

    def fit(self, utterances: List[str]):
        if self.word2vec is None:
            self.pipe.fit(utterances)
        else:
            warnings.warn(
                "CharwtWord2Vec fit function doesn't actually fit on utterances.",
                UserWarning,
            )
            self.pipe.fit(['dummy fit'])

    def save(self, output_dir: str):
        mkdir_p(output_dir)
        params = {
            "maxlen": self.maxlen,
            "sos_token": self.sos_token,
            "eos_token": self.eos_token,
            "pad_token": self.pad_token,
            "unk_token": self.unk_token,
        }
        save_json(params, os.path.join(output_dir, 'indexer.json'))
        self.pipe.save_json(os.path.join(output_dir, 'pipe.json'))

    @classmethod
    def load(cls, output_dir: str) -> Indexer:
        params = load_json(os.path.join(output_dir, 'indexer.json'))
        indexer = cls.create_without_word2vec(**params)
        indexer.pipe = sp.Pipe.restore_from_json(os.path.join(output_dir, 'pipe.json'))
        return indexer
