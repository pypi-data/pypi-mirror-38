from unittest import TestCase

from pathlib import Path
import umsgpack

from .template import TestTemplate
from ..char_indexer import CharIndexer


def load_w2v(path: str):
    with open(path, 'rb') as filep:
        word2vec = umsgpack.unpack(filep)
    return word2vec


class CharIndexerWithoutW2vTestCase(TestTemplate, TestCase):

    def get_indexer_class(self):
        return CharIndexer

    def get_indexer(self):
        return CharIndexer.create_without_word2vec(
            sos_token=self.sos_token,
            eos_token=self.eos_token,
            pad_token=self.pad_token,
            unk_token=self.unk_token,
            maxlen=self.maxlen,
        )

    def get_correct_idxs_and_seqlen_of_input_data(self):
        correct_idxs = []
        for sent in self.input_data:
            sent_idxs = [self.indexer.word2index(self.indexer.sos_token)]
            for word in sent:
                try:
                    sent_idxs.append(
                        self.indexer.word2index(word),
                    )
                except KeyError:
                    sent_idxs.append(
                        self.indexer.word2index(self.indexer.unk_token),
                    )
            sent_idxs.append(self.indexer.word2index(self.indexer.eos_token))
            if len(sent_idxs) > self.maxlen:
                sent_idxs = sent_idxs[:self.maxlen]
            while len(sent_idxs) < self.maxlen:
                sent_idxs.append(self.indexer.word2index(self.indexer.pad_token))
            assert len(sent_idxs) == self.maxlen
            correct_idxs.append(sent_idxs)

        correct_seqs = [
            min(len(sent) + 2, self.maxlen)
            for sent in self.input_data
        ]
        return correct_idxs, correct_seqs

    def test_embedding_correct(self):
        self.assertIsNone(self.indexer.word2vec)


class CharIndexerWithW2vTestCase(CharIndexerWithoutW2vTestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_emb = load_w2v(
            Path(__file__).resolve().parent.joinpath('data/example.msg'),
        )
        super().setUpClass()

    def get_indexer(self):
        return CharIndexer.create_with_word2vec(
            word2vec=self.test_emb,
            sos_token=self.sos_token,
            eos_token=self.eos_token,
            pad_token=self.pad_token,
            unk_token=self.unk_token,
            maxlen=self.maxlen,
        )

    def test_embedding_correct(self):
        self.assertEqual(self.indexer.word2vec, self.test_emb)

    def test_transform_and_fit_dont_change(self):
        tx_data, meta = self.indexer.transform(self.input_data)
        correct_idxs, correct_seqs = self.get_correct_idxs_and_seqlen_of_input_data()
        self.assertEqual(correct_idxs, tx_data)
        self.assertEqual(correct_seqs, meta['seqlen'])
        self.indexer.fit(self.input_data)
        self.assertEqual(correct_idxs, tx_data)
        self.assertEqual(correct_seqs, meta['seqlen'])
