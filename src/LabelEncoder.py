from typing import List
import numpy as np
import numpy.typing as npt
import pickle

class LabelEncoder:
    def __init__(self):
        self.KnownWords : List[str] = []

    def transform(self, words: List[str])->List[int]:
        self.learn_words(words)
        return [self.KnownWords.index(word) for word in words]

    def inverse_transform(self, symbols:int)->List[str]:
        return [self.KnownWords[symbol] for symbol in symbols]

    def is_word_known(self,word:str)->bool:
        return word in self.KnownWords

    def learn_words(self,words:List[str])->None:
        for word in words:
            if not self.is_word_known(word):
                self.KnownWords.append(word)

    def save_to_file(self,filepath: str)->None:
        with open(filepath, 'wb') as fp:
            pickle.dump(self.KnownWords, fp)        

    def load_from_file(self,filepath: str)->None:
        with open (filepath, 'rb') as fp:
            self.KnownWords = pickle.load(fp)



