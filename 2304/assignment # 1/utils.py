import re
import string
import pandas as pd
from typing import Iterable
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

import spacy
from nltk.stem import WordNetLemmatizer


class Tokenizer:
    def __init__(self) -> None:
        self.tokenizer = RegexpTokenizer("[\w']+")

    def word_tokenizer(self, text) -> Iterable:
        return self.tokenizer.tokenize(text)


class TextCleaner(Tokenizer):

    def __init__(self) -> None:
        super().__init__()

        # the acronyms url
        self._acronyms_url = "https://raw.githubusercontent.com/sugatagh/E-commerce-Text-Classification/main/JSON/english_acronyms.json"

        # link to data where contractios list is present
        self._contractions_url = "https://raw.githubusercontent.com/sugatagh/E-commerce-Text-Classification/main/JSON/english_contractions.json"

        # load the acronym dict
        self._acronyms_dict = self.load_acronym()
        # load acronym list
        self._acronym_list = list(self._acronyms_dict.keys())

        # load the contractions dict
        self._contractions_dict = self.load_contractions()
        # load contractions list
        self._contractions_list = list(self._contractions_dict.keys())

    def load_acronym(self):
        return pd.read_json(self._acronyms_url, typ="series")

    def load_contractions(self):
        return pd.read_json(self._contractions_url, typ="series")

    # Converting to lowercase
    def convert_to_lowercase(self, text):
        return text.lower()

    # remove whitespace from the text
    def remove_whitespace(self, text):
        return text.strip()

    # Removing punctuations from the given string
    def remove_punctuation(self, text):
        # get all the punctuations
        punct_str = string.punctuation

        # the apostrophe will be remove using contraction.
        punct_str = punct_str.replace("'", "")
        return text.translate(str.maketrans("", "", punct_str))

    # Remove any HTML if present in the text.
    def remove_html(self, text):
        html = re.compile(r"<.*?>")
        return html.sub(r"", text)

    # Remove URLs
    def remove_http(self, text):
        http = "https?://\S+|www\.\S+"  # matching strings beginning with http (but not just "http")
        pattern = r"({})".format(http)  # creating pattern
        return re.sub(pattern, "", text)

    # Remove any Emojis present in the text.
    def remove_emoji(self, text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", text)

    def convert_acronyms(self, text):
        words = []
        for word in self.word_tokenizer(text):
            if word in self._acronym_list:
                words = words + self._acronyms_dict[word].split()
            else:
                words = words + word.split()

        text_converted = " ".join(words)
        return text_converted

    def convert_contractions(self, text):
        words = []
        for word in self.word_tokenizer(text):
            if word in self._contractions_list:
                words = words + self._contractions_dict[word].split()
            else:
                words = words + word.split()

        text_converted = " ".join(words)
        return text_converted

    def __call__(self, text):
        text = self.convert_to_lowercase(text=text)
        text = self.remove_whitespace(text=text)
        text = self.remove_punctuation(text=text)
        text = self.remove_html(text=text)
        text = self.remove_http(text=text)
        text = self.remove_emoji(text=text)
        text = self.convert_acronyms(text=text)
        text = self.convert_contractions(text=text)

        return text


prepositions = [
    "about",
    "above",
    "across",
    "after",
    "against",
    "among",
    "around",
    "at",
    "before",
    "behind",
    "below",
    "beside",
    "between",
    "by",
    "down",
    "during",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "near",
    "of",
    "off",
    "on",
    "out",
    "over",
    "through",
    "to",
    "toward",
    "under",
    "up",
    "with",
]
prepositions_less_common = [
    "aboard",
    "along",
    "amid",
    "as",
    "beneath",
    "beyond",
    "but",
    "concerning",
    "considering",
    "despite",
    "except",
    "following",
    "like",
    "minus",
    "onto",
    "outside",
    "per",
    "plus",
    "regarding",
    "round",
    "since",
    "than",
    "till",
    "underneath",
    "unlike",
    "until",
    "upon",
    "versus",
    "via",
    "within",
    "without",
]
coordinating_conjunctions = ["and", "but", "for", "nor", "or", "so", "and", "yet"]
correlative_conjunctions = [
    "both",
    "and",
    "either",
    "or",
    "neither",
    "nor",
    "not",
    "only",
    "but",
    "whether",
    "or",
]
subordinating_conjunctions = [
    "after",
    "although",
    "as",
    "as if",
    "as long as",
    "as much as",
    "as soon as",
    "as though",
    "because",
    "before",
    "by the time",
    "even if",
    "even though",
    "if",
    "in order that",
    "in case",
    "in the event that",
    "lest",
    "now that",
    "once",
    "only",
    "only if",
    "provided that",
    "since",
    "so",
    "supposing",
    "that",
    "than",
    "though",
    "till",
    "unless",
    "until",
    "when",
    "whenever",
    "where",
    "whereas",
    "wherever",
    "whether or not",
    "while",
]


class TextPreprocess(Tokenizer):

    def __init__(self) -> None:
        super().__init__()
        # initialize the stop words
        self.stopwords = stopwords.words("english")

        # update stop words
        self.stopwords = self.stopwords + [
            "among",
            "onto",
            "shall",
            "thrice",
            "thus",
            "twice",
            "unto",
            "us",
            "would",
        ]

        # spell checker
        self.spell = SpellChecker()

        # stemmer object
        self.stemmer = PorterStemmer()

        # spacy lemittizer object
        self.spacy_lemmatizer = spacy.load("en_core_web_sm", disable=["parser", "ner"])

        # remove additional stop words
        self.additioanal_stop_words = (
            prepositions
            + prepositions_less_common
            + coordinating_conjunctions
            + correlative_conjunctions
        )

    def remove_stopwords(self, text):
        return " ".join(
            [word for word in self.word_tokenizer(text) if word not in self.stopwords]
        )

    def pyspellchecker(self, text):
        word_list = self.word_tokenizer(text)
        word_list_corrected = []
        for word in word_list:
            if word in self.spell.unknown(word_list):
                word_corrected = self.spell.correction(word)
                if word_corrected == None:
                    word_list_corrected.append(word)
                else:
                    word_list_corrected.append(word_corrected)
            else:
                word_list_corrected.append(word)
        text_corrected = " ".join(word_list_corrected)
        return text_corrected

    def porter_stemmer(self, text):
        text_stem = " ".join(
            [self.stemmer.stem(word) for word in self.word_tokenizer(text)]
        )
        return text_stem

    def lemmatizer(self, text):
        text_spacy = " ".join([token.lemma_ for token in self.spacy_lemmatizer(text)])
        return text_spacy

    def remove_additional_stopwords(self, text):
        return " ".join(
            [
                word
                for word in self.word_tokenizer(text)
                if word not in self.additioanal_stop_words
            ]
        )

    def __call__(self, text):

        text = self.remove_stopwords(text=text)
        # text = self.pyspellchecker(text=text)
        text = self.porter_stemmer(text=text)
        text = self.lemmatizer(text=text)
        text = self.remove_additional_stopwords(text=text)

        return text


# class TextPreprocess(Tokenizer):
#     def __init__(self) -> None:
#         super().__init__()
#         # initialize the stop words
#         self.stopwords = stopwords.words("english")

#         # update stop words
#         self.stopwords.extend(
#             [
#                 "among",
#                 "onto",
#                 "shall",
#                 "thrice",
#                 "thus",
#                 "twice",
#                 "unto",
#                 "us",
#                 "would",
#             ]
#         )

#         # spell checker
#         self.spell = SpellChecker()

#         # stemmer object
#         self.stemmer = PorterStemmer()

#         # spacy lemmatizer object
#         self.spacy_lemmatizer = spacy.load("en_core_web_sm", disable=["parser", "ner"])

#         # remove additional stop words
#         self.additional_stop_words = (
#             prepositions
#             + prepositions_less_common
#             + coordinating_conjunctions
#             + correlative_conjunctions
#         )

#     def remove_stopwords(self, words):
#         return [word for word in words if word not in self.stopwords]

#     def pyspellchecker(self, words):
#         unknown_words = self.spell.unknown(words)
#         return [
#             self.spell.correction(word) if word in unknown_words else word
#             for word in words
#         ]

#     def porter_stemmer(self, words):
#         return [self.stemmer.stem(word) for word in words]

#     def lemmatizer(self, words):
#         text = " ".join(words)
#         doc = self.spacy_lemmatizer(text)
#         return [token.lemma_ for token in doc]

#     def remove_additional_stopwords(self, words):
#         return [word for word in words if word not in self.additional_stop_words]

#     def __call__(self, text):
#         if text is None:
#             return ""
#         words = self.word_tokenizer(text)
#         words = self.remove_stopwords(words)
#         # words = self.pyspellchecker(words)
#         words = self.porter_stemmer(words)
#         words = self.lemmatizer(words)
#         words = self.remove_additional_stopwords(words)
#         return " ".join(words)


from typing import Iterable
from nltk.util import ngrams
from collections import Counter


class GetNgramsFrequency:

    def __init__(self, text_list: Iterable) -> None:
        self.text_list = text_list
        self.unigram = None
        self.bigram = None
        self.trigram = None

    def find_n_gram(self, size, top_n):
        ngrams_all = []
        for document in self.text_list:
            tokens = document.split()
            if len(tokens) <= size:
                continue
            else:
                output = list(ngrams(tokens, size))
            for ngram in output:
                ngrams_all.append(" ".join(ngram))
        cnt_ngram = Counter()
        for word in ngrams_all:
            cnt_ngram[word] += 1
        df = pd.DataFrame.from_dict(cnt_ngram, orient="index").reset_index()
        df = df.rename(columns={"index": "words", 0: "count"})
        df = df.sort_values(by="count", ascending=False)
        df = df.head(top_n)
        df = df.sort_values(by="count")
        return df

    def generate_n_grams(self, top_n):

        self.unigram = self.find_n_gram(size=1, top_n=top_n)
        self.bigram = self.find_n_gram(size=2, top_n=top_n)
        self.trigram = self.find_n_gram(size=3, top_n=top_n)

    def plot_distribution(self):
        fig = make_subplots(
            rows=1, cols=3, subplot_titles=("Unigrams", "Bigrams", "Trigrams")
        )
        fig.add_trace(
            go.Bar(
                x=self.unigram["count"],
                y=self.unigram["words"],
                orientation="h",
                marker=dict(opacity=0.5),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=self.bigram["count"],
                y=self.bigram["words"],
                orientation="h",
                marker=dict(opacity=0.5),
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Bar(
                x=self.trigram["count"],
                y=self.trigram["words"],
                orientation="h",
                marker=dict(opacity=0.5),
            ),
            row=1,
            col=3,
        )
        fig.update_layout(height=700, width=1500, showlegend=False)
        fig.update_xaxes(title_text="Count", row=1, col=1)
        fig.update_xaxes(title_text="Count", row=1, col=2)
        fig.update_xaxes(title_text="Count", row=1, col=3)
        fig.show()
