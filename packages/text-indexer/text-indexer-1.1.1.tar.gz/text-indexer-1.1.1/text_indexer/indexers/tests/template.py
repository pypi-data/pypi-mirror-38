import abc
import os
from pathlib import Path
import shutil


def list_all_files(root: str):
    output = []
    for prefix, _, files in os.walk(root):
        for f in files:
            path = os.path.join(prefix, f)
            output.append(path)
    return output


class TestTemplate(abc.ABC):

    @classmethod
    def setUpClass(cls):
        cls.sos_token = '<sos>'
        cls.eos_token = '</s>'
        cls.pad_token = '<pad>'
        cls.unk_token = '<unk>'
        cls.maxlen = 7
        cls.input_data = [
            '克安是牛肉大粉絲',  # longer than 7 after adding sos eos
            '繼良喜歡喝星巴巴',  # longer than 7 after adding sos eos
            '安靜的祥睿',  # equal to 7 after adding sos eos
            '喔',  # shorter than 7 after adding sos eos
        ]
        cls.output_dir = Path(__file__).parent / 'example_indexer/'

    def setUp(self):
        self.indexer = self.get_indexer()
        self.indexer.fit(self.input_data)

    def tearDown(self):
        if self.output_dir.exists():
            shutil.rmtree(str(self.output_dir))

    @abc.abstractmethod
    def get_indexer_class(self):
        pass

    @abc.abstractmethod
    def get_indexer(self):
        pass

    @abc.abstractmethod
    def get_correct_idxs_and_seqlen_of_input_data(self):
        pass

    def test_word2index_out_of_range(self):
        with self.assertRaises(KeyError):
            self.indexer.word2index('凢')

    def test_index2word_out_of_range(self):
        with self.assertRaises(KeyError):
            self.indexer.index2word(100000000000)

    def test_transform(self):
        tx_data, meta = self.indexer.transform(self.input_data)
        correct_idxs, correct_seqs = self.get_correct_idxs_and_seqlen_of_input_data()
        self.assertEqual(correct_idxs, tx_data)
        self.assertEqual(correct_seqs, meta['seqlen'])

    def test_inverse_transform(self):
        tx_data, meta = self.indexer.transform(self.input_data)
        output = self.indexer.inverse_transform(tx_data, meta['inv_info'])
        self.assertEqual(output, self.input_data)

    def test_save(self):
        output_dir = str(self.output_dir)
        self.indexer.save(output_dir)
        self.assertEqual(
            set([os.path.join(output_dir, filepath) for filepath in ['pipe.json', 'indexer.json']]),
            set(list_all_files(output_dir)),
        )

    def test_load(self):
        self.indexer.save(str(self.output_dir))
        indexer = self.get_indexer_class().load(str(self.output_dir))
        tx_data, meta = indexer.transform(self.input_data)
        correct_idxs, correct_seqs = self.get_correct_idxs_and_seqlen_of_input_data()
        self.assertEqual(correct_idxs, tx_data)
        self.assertEqual(correct_seqs, meta['seqlen'])
