import math


def prepare():
    with open('../task4/tf-idf.txt', 'r', encoding="utf-8") as doc:
        tf_idf = doc.read().splitlines()

    for info in tf_idf:
        word, idf, tf_idf = info.split()
        tf_idf_dict[word] = tf_idf

    for i in range(1, 110):
        try:
            i_str = str(i)
            with open('../task4/tf/' + i_str + '.txt', 'r', encoding="utf-8") as doc:
                tf_temp = doc.read().splitlines()
            tf[i_str] = {}
            for line in tf_temp:
                word, tf_word = line.split()
                tf[i_str][word] = tf_word
        except Exception:
            print('Exception in page: ' + str(i))
            continue


def fill_tf():
    for i in range(1, 110):
        if i not in tf:
            return
        for word in tf_idf_dict:
            if word not in tf[i]:
                tf[i][word] = '0'


def resolve_expression(exp):
    suitable_docs = []
    words = exp.split()
    for i in range(1, 110):
        if str(i) not in tf:
            continue
        doc = tf[str(i)]
        scalar = 0
        sqr = 0
        for word in doc:
            if word in words:
                scalar = scalar + float(doc[word])
            var = float(doc[word])
            sqr = sqr + var * var
        normalized_expression = math.sqrt(len(words))
        normalized_doc = math.sqrt(sqr)
        total = scalar / (normalized_doc * normalized_expression)
        if total > 0:
            suitable_docs.append(i)

    return suitable_docs


if __name__ == '__main__':
    tf_idf_dict = {}
    tf = {}

    prepare()
    fill_tf()

    expression = 'огонь лежать'
    suitable_docs = resolve_expression(expression)
    print(suitable_docs)
