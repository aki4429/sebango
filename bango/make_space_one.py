#文字列の複数連続スペースを一つに変換する。

def s_one(text):
    result = " ".join(text.split())
    return result
