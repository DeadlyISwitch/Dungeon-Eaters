def compare(a: dict, b: dict, analyzer):
    sa = analyzer(a)
    sb = analyzer(b)
    rec = 'A' if sa['score'] >= sb['score'] else 'B'
    return {'a':sa,'b':sb,'recommended':rec}
