import trafilatura
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from config import *
from operator import itemgetter

nltk.download("stopwords")
from collections import Counter
import requests


def get_status_code(url):
    try:
        r = requests.get(url, headers=useragent, allow_redirects=False, verify=False)
        if r.status_code == 200:
            return r.status_code
        else:
            "Requests error URL:" + str(r.status_code)

    except Exception as e:
        print("Error: " + str(e))
        return "Error"


def get_text_from_page_html(url):
    try:
        status_code = get_status_code(url)
        if status_code == 200:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(firefox_options=options,
                                       executable_path=path_for_browser)
            driver.get(url)
            time.sleep(5)
            html = driver.page_source
            text_from_page = trafilatura.extract(html)
            driver.close()
            return text_from_page
    except Exception as e:
        print("Error page HTML: " + str(e))
        return "Error"


def main():
    pass


def preprocess_text(text_from_page):
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")
    tokens = mystem.lemmatize(text_from_page.lower())
    tokens = [token for token in tokens if
              token not in russian_stopwords and token != " " and token.strip() not in punctuation]

    text_without_trash = " ".join(tokens)
    return text_without_trash


def dictionary_count_lemmas(lemma_text_from_page):
    try:
        word_list = []
        # print(word_str)
        for word in lemma_text_from_page.split():
            clear_word = ''
            for letter in word:
                if letter.isalpha():
                    clear_word += letter.lower()
            word_list.append(clear_word)

        counts = Counter(word_list)
        """
        print(word_list)
        print(type(counts))
        print(counts)
        for i in counts:
            word = i
            count_word = counts[i]
        лечение
        95
        алкоголизм
        42
        санктпетербург
        """
        return counts
    except Exception as e:
        print("Error counts lemma: " + str(e))
        return "Error"


def get_lemmas_from_url(url):
    page_url = url
    text = get_text_from_page_html(page_url)
    text_length = len(text)

    lemm_word_str = preprocess_text(text)
    # print(f"WORD_STR: {lemm_word_str}")
    counts_words = dictionary_count_lemmas(lemm_word_str)
    """
    Генерируем словарь
    """
    dict_words = {}
    for i in counts_words:
        word = i
        count_word = counts_words[i]
        if dict_words.get(word) is None:
            dict_words[word] = count_word
        else:
            dict_words[word] = int(dict_words[word]) + 1

    sorted_dict = sorted(dict_words.items(), key=itemgetter(1), reverse=True)
    return sorted_dict


def get_lemmas_from_list(list_words):
    print(f"LIST_WORDS: {list_words}")
    for str_in_list in list_words:
        lemm_word_str = preprocess_text(str_in_list)
        print(f"Начальное слово: {str_in_list}\n"
              f"Лемма: {lemm_word_str}")
        # print(f"WORD_STR: {lemm_word_str}")
        counts_words = dictionary_count_lemmas(lemm_word_str)
        list_words_lem = []
        for i in counts_words:
            word = i
            count_word = counts_words[i]
            if word not in list_words_lem:
                list_words_lem.append(word)
    return list_words_lem
        # print(sorted_dict)
    # for i in sorted_dict:
    #     print(i)
    #     print(type(i))
    #     print(i[0])
    #     print(i[1])
    # print(sorted_dict[i])
    # print(i[0])
    # print(type(i[0]))

# print(dict_lemmas)
#
#
# my_list_stop_words = ['в', 'интернетмагазин', 'москве', 'воллитолль', 'волль', 'толль', 'c', 'из', 'для', 'москва', 'и']
#
#

#
#
