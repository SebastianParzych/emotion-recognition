from constraints import *
import emoji
import re
from bs4 import BeautifulSoup
import string


def clean_text(text):
    text = emoji.demojize(text)
    text = re.sub(r"\:(.*?)\:", "", text)
    text = str(text).lower()  # Making Text Lowercase
    text = re.sub("\[.*?\]", "", text)
    # The next 2 lines remove html text
    text = BeautifulSoup(text, "html").get_text()
    text = re.sub("https?://\S+|www\.\S+", "", text)
    text = re.sub("<.*?>+", "", text)
    text = re.sub("\n", "", text)
    text = re.sub("\w*\d\w*", "", text)
    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",", "'")
    text = re.sub(r"[^a-zA-Z?.!,¿']+", " ", text)
    return text


def clean_contractions(text, mapping):
    specials = ["’", "‘", "´", "`"]
    for s in specials:
        text = text.replace(s, "'")
    for word in mapping.keys():
        if "" + word + "" in text:
            text = text.replace("" + word + "", "" + mapping[word] + "")
    # Remove Punctuations
    text = re.sub("[%s]" % re.escape(string.punctuation), "", text)
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    text = re.sub(r"([?.!,¿])", r" \1 ", text)
    text = re.sub(r'[" "]+', " ", text)
    return text


def clean_special_chars(text, punct, mapping):
    for p in mapping:
        text = text.replace(p, mapping[p])

    for p in punct:
        text = text.replace(p, f" {p} ")

    specials = {"\u200b": " ", "…": " ... ",
                "\ufeff": "", "करना": "", "है": ""}
    for s in specials:
        text = text.replace(s, specials[s])

    return text


def correct_spelling(x, dic):
    for word in dic.keys():
        x = x.replace(word, dic[word])
    return x


def remove_space(text):
    # Removes awkward spaces
    text = text.strip()
    text = text.split()
    return " ".join(text)


def remove_sw(text):
    """Removes stop words"""
    text = [word for word in text.split() if word.lower() not in sw_nltk]
    return " ".join(text)


def text_preprocessing_pipeline(text):
    text = clean_text(text)
    text = clean_contractions(text, contraction_mapping)
    text = clean_special_chars(text, punct, punct_mapping)
    text = correct_spelling(text, mispell_dict)
    text = remove_space(text)
    return text
