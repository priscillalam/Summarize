import io
import numpy
import re
import spacy
import string
import sys
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from spacy.lang.en.stop_words import STOP_WORDS

class Summarizer:
    def __init__(self, clusters=5):
        self.clusters = clusters
        self.nlp = spacy.load('en_core_web_sm')

    def summarize(self, text):
        print("Compiling summary.")
        sentences_to_vectors = dict()
        sentences = []
        for sentence in self.nlp(text).sents:
            vector = sentence.vector
            sentences_to_vectors[sentence] = vector
            sentences.append(sentence)
       
        vectors = list(sentences_to_vectors.values())
        clusters = KMeans(n_clusters=self.clusters, random_state=None).fit(vectors)
        closest, _ = pairwise_distances_argmin_min(clusters.cluster_centers_, vectors)

        closest.sort()
        return " ".join([str(sentences[index]) for index in closest])
       
class WordUtils:
    excluded_characters = set(string.punctuation).union(set(string.digits))

    @staticmethod 
    def remove_non_ascii(text):
        return re.sub(r'[^\x00-\x7f]', r'', str(text)).replace("\n", "")

    @staticmethod
    def clean_word(word):
        ascii_word = WordUtils.remove_non_ascii(word)
        return ''.join(character for character in ascii_word \
            if character not in WordUtils.excluded_characters).lower()

    @staticmethod
    def is_word_useful(word, length_minimum):
        cleaned_word = WordUtils.clean_word(word)

        if len(cleaned_word) <= length_minimum:
            return False

        if cleaned_word.lower() in STOP_WORDS:
            return False

        return True

class SentenceUtils:
    @staticmethod
    def word_pairs_in_sentence(sentence, vocabulary, window_size):
        pairs = set()
        enumerated_sentence = enumerate(sentence)
        for first_word_index, first_word in enumerated_sentence:
            cleaned_first_word = WordUtils.clean_word(first_word)
            if cleaned_first_word not in vocabulary:
                continue
            for second_word in sentence[first_word_index + 1: first_word_index + window_size]:
                cleaned_second_word = WordUtils.clean_word(second_word)
                if cleaned_second_word not in vocabulary:
                    continue
                pairs.add((cleaned_first_word, cleaned_second_word))
        return pairs

    @staticmethod
    def word_pairs(sentences, vocabulary, window_size):
        pairs = set()
        for sentence in sentences:
            pairs.update(SentenceUtils.word_pairs_in_sentence(sentence, vocabulary, window_size))
        return pairs

class KeywordFinder:
    def __init__(
        self,
        damping_coefficient=0.85,
        acceptable_error=0.00001,
        max_iterations = 10,
        word_length_minimum=4,
        window_size=4,
        number_of_keywords=5):
        self.damping_coefficient = damping_coefficient
        self.acceptable_error = acceptable_error
        self.max_iterations = max_iterations
        self.word_length_minimum = word_length_minimum
        self.window_size = window_size
        self.number_of_keywords = number_of_keywords
        self.nlp = spacy.load('en_core_web_sm')

    def vocabulary(self, sentence):
        return [WordUtils.clean_word(word) for word in sentence \
            if WordUtils.is_word_useful(word, self.word_length_minimum)]

    def cooccurence_matrix(self, word_pairs, vocabulary):
        matrix_size = len(vocabulary)
        cooccurence_matrix = numpy.zeros((matrix_size, matrix_size), dtype='float')
        word_to_matrix_index = {word:index for (index, word) in enumerate(vocabulary)}

        for first_word, second_word in word_pairs:
            row, column = word_to_matrix_index[first_word], word_to_matrix_index[second_word]
            cooccurence_matrix[row][column] = 1
            cooccurence_matrix[column][row] = 1
        
        column_sums = numpy.sum(cooccurence_matrix, axis=0)
        return numpy.divide(cooccurence_matrix, column_sums, where=column_sums != 0)

    def iterate(self, matrix):
        vector = numpy.array([1] * matrix.shape[0])
        previous_sum = numpy.int64(0)
        while range(0, self.max_iterations):
            vector = (1 - self.damping_coefficient) + \
                self.damping_coefficient * numpy.dot(matrix, vector)
            vector_sum = vector.sum(dtype=numpy.int64)
            if (numpy.abs(numpy.subtract(previous_sum, vector_sum)) < self.acceptable_error):
                break
            previous_sum = vector_sum
        return vector

    def flatten_vocabulary(self, vocabularies_per_sentence):
        vocabulary = set()
        for sentence_vocabulary in vocabularies_per_sentence:
            vocabulary.update([word for word in sentence_vocabulary])
        return list(vocabulary)

    def build_keyword_dictionary(self, vector, vocabulary, vocabularies_per_sentence):
        keywords_to_sentence_index = {}
        for index in vector.argsort()[::-1][:self.number_of_keywords]:
            keyword = vocabulary[index]
            counter = 0
            for sentence_vocabulary in vocabularies_per_sentence:
                if keyword in sentence_vocabulary:
                    keywords_to_sentence_index[keyword] = counter
                counter += 1
        return keywords_to_sentence_index

    def keywords(self, sentences):
        print("Finding keywords.")
        nlp_sentences = [self.nlp(sentence) for sentence in sentences]
        vocabularies_per_sentence = [self.vocabulary(sentence) for sentence in nlp_sentences]
        vocabulary = self.flatten_vocabulary(vocabularies_per_sentence)
        word_pairs = SentenceUtils.word_pairs(nlp_sentences, vocabulary, self.window_size)
        matrix = self.cooccurence_matrix(word_pairs, vocabulary)
        vector = self.iterate(matrix)
        return self.build_keyword_dictionary(vector, vocabulary, vocabularies_per_sentence)
