import math
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2


def prepare_text(text):
    text = text.replace('>', '> ')
    text = text.replace('<', ' <')
    text = text.replace('&nbsp;', ' &nbsp; ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), r'', text)
    text = re.sub(r'[^\w\s]+|[\d]+', r'', text).strip()
    text = re.sub(r'[A-Za-z]', r'', text)
    text = re.sub(r'[+_]', r'', text)
    text = ' '.join(text.split())

    return text


def get_tf(word_entry, word_count):
    return float(word_entry / word_count)


def get_idf(document_entry, document_count):
    return math.log(document_count / len(document_entry))


def get_lemma(word):
    p = morph.parse(word)[0]
    return p.normal_form


def get_lemmas(text):
    lemmas = []
    for item in text.split():
        lemmas.append(get_lemma(item))
    return lemmas


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    tf_doc = {}
    tf_mean = {}
    doc_count = 110

    for i in range(1, 110):
        try:
            with open('../task1/data/' + str(i) + '.html', 'r', encoding="utf-8") as fp:
                text = fp.read()

            text = prepare_text(text)

            make_tf_idf = TfidfVectorizer(
                stop_words=['и', 'а', 'но', 'да', 'без', 'безо', 'близ', 'в', 'во', 'вместо', 'вне', 'для', 'до', 'за',
                            'из', 'изо', 'из-за', 'из-под', 'к', 'ко', 'кроме', 'между', 'меж', 'на', 'над', 'о', 'об',
                            'обо', 'от', 'ото', 'перед', 'передо', 'пред', 'пo', 'под', 'подо', 'при', 'про', 'ради',
                            'с',
                            'со', 'сквозь', 'среди', 'у', 'через', 'чрез'])
            texts_as_tfidf_vectors = make_tf_idf.fit_transform([text])

            lemmas = get_lemmas(text)

            tf_arr = {}

            for item in lemmas:
                if item in make_tf_idf.get_feature_names():
                    if item in tf_arr:
                        tf_arr[item] = tf_arr[item] + 1
                    else:
                        tf_arr[item] = 1
                    if item in tf_doc:
                        tf_doc[item].append(i)
                        tf_doc[item] = list(set(tf_doc[item]))
                    else:
                        tf_doc[item] = [i]

            word_count = len(lemmas)

            file_tf = open('tf/' + str(i) + ".txt", 'a', encoding="utf-8")
            for item in tf_arr:
                tf = get_tf(tf_arr[item], word_count)
                file_tf.write(item + ' ' + str(tf) + '\n')
                file_tf.flush()
                if item in tf_mean:
                    tf_mean[item] = (tf_mean[item] + tf) / 2
                else:
                    tf_mean[item] = tf

        except Exception:
            print('Exception in index: ' + str(i))
            continue

    file_idf = open('idf.txt', 'a', encoding="utf-8")
    for item in set(tf_doc):
        file_idf.write(item + ' ' + str(get_idf(tf_doc[item], doc_count)) + '\n')
        file_idf.flush()

    file_tf_idf = open('tf-idf.txt', 'a', encoding="utf-8")
    for item in set(tf_doc):
        file_tf_idf.write(item + ' ' + str(get_idf(tf_doc[item], doc_count)) + ' ' + str(
            float(tf_mean[item]) * float(get_idf(tf_doc[item], doc_count))) + '\n')
        file_tf_idf.flush()
