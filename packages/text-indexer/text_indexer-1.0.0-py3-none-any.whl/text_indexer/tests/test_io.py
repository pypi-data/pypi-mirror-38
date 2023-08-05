from unittest import TestCase
from unittest.mock import patch
import shutil
from os.path import join, abspath, exists, dirname
import os

from ..io import save_indexer, load_indexer
from text_indexer.indexers.utils import save_json, load_json


class MockIndexer(object):

    def __init__(self, aa=1, bb=2):
        self.aa = aa
        self.bb = bb
        self.a = 1
        self.b = 2

    def save(self, output_dir):
        save_json({'a': self.a, 'b': self.b}, join(output_dir, 'fake_pipe.json'))
        save_json({'aa': self.aa, 'bb': self.bb}, join(output_dir, 'fake_indexer.json'))

    @classmethod
    def load(cls, output_dir):
        pipe = load_json(join(output_dir, 'fake_pipe.json'))
        params = load_json(join(output_dir, 'fake_indexer.json'))
        indexer = cls(**params)
        indexer.pipe = pipe
        return indexer


class IOTestCase(TestCase):

    def setUp(self):
        root_dir = dirname(abspath(__file__))
        self.output_dir = join(root_dir, 'example/')
        os.mkdir(self.output_dir)

    def tearDown(self):
        if exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_save_indexer(self):
        export_path = save_indexer(indexer=MockIndexer(), output_dir=self.output_dir)
        self.assertTrue(exists(export_path))
        os.remove(export_path)

    def test_load_indexer(self):
        export_path = save_indexer(indexer=MockIndexer(), output_dir=self.output_dir)
        with patch('text_indexer.io._get_indexer_module', return_value=MockIndexer):
            load_indexer(export_path)
        self.assertTrue(exists(self.output_dir))
        os.remove(export_path)
