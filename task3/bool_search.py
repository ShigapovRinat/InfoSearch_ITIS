import re


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


def create_inverted_index(tokens, text, document_id):
    for token in tokens:
        key = token.split()[0]
        for word in token.split():
            if word in text:
                positions = [m.start() for m in re.finditer(word, text)]
                index = {
                    'documentId': document_id,
                    'positions': positions
                }
                if key in inverted_index:
                    if index not in inverted_index[key]:
                        inverted_index[key].append(index)
                else:
                    inverted_index[key] = [index]

    return inverted_index


def is_operation(symbol):
    symbol = symbol.lower()
    if symbol == 'and':
        return True
    if symbol == 'or':
        return True
    return False


def operation_prior(symbol):
    if symbol == 'and':
        return 2
    if symbol == 'or':
        return 1


def get_document_by_param(param):
    if param not in inverted_index:
        return []
    ids = []
    for item in inverted_index[param]:
        ids.append(item['documentId'])
    return ids


def operation(sbOut):
    stack = []
    used_symbols = 0
    while used_symbols < len(sbOut):
        symbol = sbOut[used_symbols]
        if is_operation(symbol):
            dB = stack.pop()
            dA = stack.pop()
            if symbol == 'and':
                dA = list(set(dA) & set(dB))
            if symbol == 'or':
                dA = list(set(dA + dB))
        else:
            dA = get_document_by_param(symbol)

        stack.append(dA)
        used_symbols = used_symbols + 1

    return stack


def boolean_search(expression):
    sbStack = []
    sbOut = []
    for symbol in expression.split():
        if is_operation(symbol):
            while len(sbStack) > 0:
                cTmp = sbStack[len(sbStack) - 1][0]
                if is_operation(cTmp) and (operation_prior(symbol) <= operation_prior(cTmp)):
                    sbOut.append(cTmp)
                else:
                    break

            sbStack.append(symbol)
        elif symbol == '(':
            sbStack.append(symbol)
        elif symbol == ')':
            cTmp = sbStack.pop()
            while '(' != cTmp:
                if len(sbStack) < 1:
                    print("Неправильно поставлены скобки")
                sbOut.append(cTmp)
                cTmp = sbStack.pop()
        else:
            sbOut.append(symbol)

    while len(sbStack) > 0:
        sbOut.append(sbStack.pop())

    return operation(sbOut)[0]


if __name__ == '__main__':
    inverted_index = {}
    near = 5
    url = 'https://www.litmir.me/br/?b=217310&p='

    with open('../task2/tokens.txt', 'r', encoding="utf-8") as token_text:
        tokens = token_text.read().splitlines()

    for i in range(1, 110):
        try:
            with open('../task1/data/' + str(i) + '.html', 'r', encoding="utf-8") as fp:
                text = fp.read()

            text = prepare_text(text)

            create_inverted_index(tokens, text, i)

        except Exception:
            print('Exception in index: ' + str(i))
            continue

    bool_expression = 'отношение or ( война and мир )'
    results = boolean_search(bool_expression)
    for document_id in results:
        print(url + str(document_id))
