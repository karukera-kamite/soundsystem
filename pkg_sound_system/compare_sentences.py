""" Calculate the Similarity of Two Sentences """

from difflib import SequenceMatcher


class sentence_similarity:

    def __init__(self, sentence_1, sentence_2):
        self.sent_1 = sentence_1
        self.sent_2 = sentence_2

    def similarity_percentage(self):
        ratio = SequenceMatcher(None, self.sent_1, self.sent_2).ratio()
        return ratio
