import re
import string
import pandas as pd
from nltk.tokenize import RegexpTokenizer


class Tokenizer:
    def __init__(self) -> None:
        self.tokenizer = RegexpTokenizer("[\w']+")

    def word_tokenizer(self, text) -> re.Any:
        return self.tokenizer.tokenize(text)


class TextCleaner(Tokenizer):

    def __init__(self, text: str) -> None:
        super().__init__()
        # The input text
        self.text = text

        # the acronyms url
        self.acronyms_url = "https://raw.githubusercontent.com/sugatagh/E-commerce-Text-Classification/main/JSON/english_acronyms.json"

        # load the acronym dict
        self.acronym_dict = self.load_acronym()

        # load acronym list
        self.acronym_list = list(self.acronym_dict.keys())

    def load_acronym(self):
        return pd.read_json(self.acronyms_url, typ="series")

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
            if word in self.acronym_list:
                words = words + self.acronyms_dict[word].split()
            else:
                words = words + word.split()

        text_converted = " ".join(words)
        return text_converted
