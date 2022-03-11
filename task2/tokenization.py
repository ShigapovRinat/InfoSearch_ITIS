from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pymorphy2


def prepare(text):
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), r'', text)
    text = re.sub(r'[^\w\s]+|[\d]+', r'', text).strip()
    text = re.sub(r'[A-Za-z]', r'', text)
    text = re.sub(r'[+_]', r'', text)
    return text


def get_token_dict(arr):
    for word in arr:
        p = morph.parse(word)[0]
        normal_form = p.normal_form
        if normal_form in tokens:
            tokens[normal_form].append(word)
            tokens[normal_form] = list(set(tokens[normal_form]))
        else:
            tokens[normal_form] = [word]

    return tokens


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    tokens = {}

    for i in range(1, 109):
        try:
            with open('data/' + str(i) + '.html', 'r', encoding="utf-8") as fp:
                text = fp.read()

            text = prepare(text)

            make_tf_idf = TfidfVectorizer(
                stop_words=['и', 'а', 'но', 'да', 'без', 'безо', 'близ', 'в', 'во', 'вместо', 'вне', 'для', 'до', 'за',
                            'из', 'изо', 'из-за', 'из-под', 'к', 'ко', 'кроме', 'между', 'меж', 'на', 'над', 'о', 'об',
                            'обо', 'от', 'ото', 'перед', 'передо', 'пред', 'пo', 'под', 'подо', 'при', 'про', 'ради',
                            'с', 'со', 'сквозь', 'среди', 'у', 'через', 'чрез'])
            texts_as_tfidf_vectors = make_tf_idf.fit_transform([text])

            get_token_dict(make_tf_idf.get_feature_names())
        except Exception:
            print('Exception in index: ' + str(i))
            continue

    token_file = open('tokens.txt', 'a', encoding="utf-8")
    for token in tokens:
        token_file.write(token + '\n')
        token_file.flush()

    lemmas_file = open('lemmas.txt', 'a', encoding="utf-8")
    for token in tokens:
        lemmas_file.write(token + ': ' + " ".join(tokens[token]) + '\n')
        lemmas_file.flush()

