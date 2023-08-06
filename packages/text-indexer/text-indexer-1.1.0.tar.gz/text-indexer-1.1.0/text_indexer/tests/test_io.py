from typing import List
from unittest import TestCase
from unittest.mock import patch
import shutil
from os.path import join, abspath, exists, dirname
import os

from ..io import save_indexer, load_indexer
from text_indexer.indexers.utils import save_json, load_json


def list_all_files(root: str) -> List[str]:
    output = []
    for prefix, _, files in os.walk(root):
        for f in files:
            path = os.path.join(prefix, f)
            output.append(path)
    return output


class MockIndexer(object):

    pipe_filename = 'fake_pipe.json'
    indexer_filename = 'fake_indexer.json'

    def __init__(self, aa=1, bb=2):
        self.aa = aa
        self.bb = bb
        self.a = 1
        self.b = 2

    def save(self, output_dir):
        save_json({'a': self.a, 'b': self.b}, join(output_dir, self.pipe_filename))
        save_json({'aa': self.aa, 'bb': self.bb}, join(output_dir, self.indexer_filename))

    @classmethod
    def load(cls, output_dir):
        pipe = load_json(join(output_dir, cls.pipe_filename))
        params = load_json(join(output_dir, cls.indexer_filename))
        indexer = cls(**params)
        indexer.pipe = pipe
        return indexer

    def transform(self, utterances):
        return [f"{self.aa}_{self.bb}_{utt}" for utt in utterances]


class IOTestCase(TestCase):

    def setUp(self):
        root_dir = dirname(abspath(__file__))
        self.output_dir = join(root_dir, 'example/')
        os.mkdir(self.output_dir)

    def tearDown(self):
        if exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_save_indexer(self):
        save_indexer(indexer=MockIndexer(), output_dir=self.output_dir)
        self.assertTrue(exists(self.output_dir))
        self.assertEqual(
            set(
                [
                    os.path.join(self.output_dir, MockIndexer.pipe_filename),
                    os.path.join(self.output_dir, MockIndexer.indexer_filename),
                    os.path.join(self.output_dir, 'name'),
                ],
            ),
            set(list_all_files(self.output_dir)),
        )

    def test_load_indexer(self):
        save_indexer(indexer=MockIndexer(), output_dir=self.output_dir)
        with patch('text_indexer.io._get_indexer_module', return_value=MockIndexer):
            indexer = load_indexer(self.output_dir)
        output = indexer.transform(['dummy_utt'])
        self.assertEqual([f'{indexer.aa}_{indexer.bb}_dummy_utt'], output)
