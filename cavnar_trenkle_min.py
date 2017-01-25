from __future__ import division # Safety measure in case we extend to py2.7

from collections import defaultdict
import sys

from nltk.tokenize import wordpunct_tokenize
from nltk.util import ngrams

# TODO: Store instance variables (e.g. model)
class CavnarTrenkleImpl(object):
    def __init__(self):
        pass

    def _compute_profile_from_frequencies(self, frequencies_dict, limit):
        # Sort by value first, and then also by key (alphabetic order) if values are equal
        return [ngram[0] for ngram in sorted(frequencies_dict.items(), key= lambda x: (x[1], x[0]), reverse=True)[:limit]]

    def _compute_text_profile(self, text, limit=None):
        """
        >>> implementation = CavnarTrenkleImpl()
        >>> text = 'Hello'
        >>> implementation._compute_text_profile(text)
        ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', 'ello', 'ell', 'el', 'e']
        >>> implementation._compute_text_profile(text, limit=2)
        ['l', 'o']

        """
        text_ngram_freqs = self._extract_text_ngram_freqs(text)
        return self._compute_profile_from_frequencies(text_ngram_freqs, limit)

    def _extract_text_ngram_freqs(self, text):
        """
        Tokenize the text. For each token in the text, extract ngrams of different
        length (from 1 to 5). Compute how many times each of these ngrams occur
        in the text. Then return a dictionary of { ngram: frequencies }.

        >>> implementation = CavnarTrenkleImpl()
        >>> ngrams = implementation._extract_text_ngram_freqs("HeLLo")
        >>> ngrams == {'h':1, 'e': 1, 'l': 2, 'o': 1, 'he': 1, 'el': 1, 'll': 1, \
            'lo': 1, 'hel': 1, 'ell': 1, 'llo': 1, 'hell': 1, 'ello': 1, 'hello': 1}
        True
        >>> ngrams = implementation._extract_text_ngram_freqs("CIAO")
        >>> ngrams == {'c':1, 'i': 1, 'a': 1, 'o': 1, 'ci': 1, 'ia': 1, 'ao': 1, \
            'cia': 1, 'iao': 1, 'ciao': 1}
        True
        """
        tokens = wordpunct_tokenize(text.lower()) # Force lower case
        #TODO: Delete numbers and punctuation

        ngram_freqs = defaultdict(int)
        for token in tokens:
            for n in range(1,6): # Use 1-grams to 5-grams
                for ngram in ngrams(token, n):
                    ngram_string = ''.join(ngram)
                    ngram_freqs[ngram_string] += 1
                # ngram_freqs[ngrams(token, n)] += 1

        return ngram_freqs

    def predict_language(self, text, training_profiles, error_value=8000):
        """
        >>> implementation = CavnarTrenkleImpl()
        >>> text = 'hello'
        >>> training_profiles = {\
            'en': ['l', 'o', 'lo', 'llo', 'll', 'hello', 'hell', 'hel', 'he', 'h', \
                'ello', 'ell', 'el', 'e'],\
            'it': ['o', 'iao', 'ia', 'i', 'ciao', 'cia', 'ci', 'c', 'ao', 'a']}
        >>> implementation.predict_language(text, training_profiles)
        'en'

        NOTE: This method could be improved by simply iterating over distances and
        discarding them when they are smaller than the previous one. This would
        not allow us to reuse `predict_language_scores` here.

        NOTE: This is the same as:
            lang_distances = self.predict_language_scores(text, training_profiles, error_value)
            min(lang_distances, key=lang_distances.get)

        """
        min_distance = sys.maxsize # Set it to a high number before iterating
        predicted_language = ''

        text_profile = self._compute_text_profile(text)

        for language in training_profiles:
            distance = self._distance(text_profile, training_profiles[language], error_value=error_value)
            if distance < min_distance:
                min_distance = distance
                predicted_language = language

        return predicted_language

    def predict_language_scores(self, text, training_profiles, error_value):
        """
        Predict scores for all languages. Each score represent the distance between
        the text and each language.

        """
        text_profile = self._compute_text_profile(text)
        lang_distances = dict()
        for language in training_profiles:
            lang_distances[language] = self._distance(text_profile, training_profiles[language], error_value=error_value)

        return lang_distances

    def _distance(self, text_profile, training_profile, error_value=1000):
        """
        This method compares two profiles and returns a number which represents the
        distance between them. A high distance means that the language of the texts
        that have been used to generate the profiles is not the same. This distance
        is called "out-of-place" metric in the paper.
        We usually compare a language profile (generated from a training set) to the
        profile generated from a single text (e.g. a tweet or a facebook post).
        Note: If a ngram is not present in the training profile, we penalize the
        text profile using an arbitrary `error_value`. This value should be decided
        based on tuning on the test set.

        >>> text_profile = ['h', 'e', 'l', 'o', 'he']
        >>> training_profile = ['h', 'e', 'l', 'o', 'he']
        >>> implementation = CavnarTrenkleImpl()
        >>> implementation._distance(text_profile, training_profile)
        0
        >>> training_profile = ['l', 'o', 'h', 'e', 'he']
        >>> implementation._distance(text_profile, training_profile)
        8

        """
        total_distance = 0
        for index, text_ngram in enumerate(text_profile):
            if text_ngram in training_profile:
                distance = abs(index - training_profile.index(text_ngram))
            else:
                distance = error_value
            total_distance += distance

        return total_distance
