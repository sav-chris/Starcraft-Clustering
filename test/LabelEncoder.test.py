import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from LabelEncoder import LabelEncoder
import unittest
import TestConstants

class TestLabelEncoder(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLabelEncoder, self).__init__(*args, **kwargs)
        self.fruit_salad = ['apple', 'apple', 'bannana', 'apple']
        self.dictionary = ['apple', 'bannana', 'pear']

    def test_transform(self):
        label_encoder: LabelEncoder = LabelEncoder()

        label_encoder.learn_words(self.dictionary)

        encoded_salad = label_encoder.transform(self.fruit_salad)

        self.assertListEqual(self.fruit_salad, label_encoder.inverse_transform(encoded_salad))

    def test_learn_words(self):
        label_encoder: LabelEncoder = LabelEncoder()

        label_encoder.learn_words(self.fruit_salad)

        self.assertTrue(label_encoder.is_word_known('apple'))
        self.assertTrue(label_encoder.is_word_known('bannana'))
        self.assertFalse(label_encoder.is_word_known('pear'))

        label_encoder.learn_words(['pear', 'pear'])

        self.assertTrue(label_encoder.is_word_known('apple'))
        self.assertTrue(label_encoder.is_word_known('bannana'))
        self.assertTrue(label_encoder.is_word_known('pear'))

    def test_save_load(self):
        filename:str = os.path.join(TestConstants.TEST_LABEL_ENCODER_DIR, 'TestLabelEncoder.npy')
        if os.path.exists(filename):
            os.remove(filename)
        label_encoder: LabelEncoder = LabelEncoder()
        label_encoder.learn_words(self.fruit_salad)
        label_encoder.learn_words(self.dictionary)
        
        label_encoder.save_to_file(filename)

        label_encoder2: LabelEncoder = LabelEncoder()
        label_encoder2.load_from_file(filename)

        self.assertListEqual(label_encoder.KnownWords, label_encoder2.KnownWords)


if __name__ == '__main__':
    unittest.main()        



