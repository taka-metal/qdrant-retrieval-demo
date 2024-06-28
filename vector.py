import numpy as np
import pandas as pd
import spacy
from multiprocessing import Pool, cpu_count

nlp = spacy.load('ja_ginza', exclude=["tagger", "parser", "ner", "lemmatizer", "textcat", "custom"])

QDRANT_NPY = 'vectors-livedoor-ginza.npy'  # 出力ファイル名

def f(x):
    doc = nlp(x)  # GiNZAでベクトル化
    return doc.vector

def main():
    try:
        df = pd.read_json('livedoor.json', lines=True)  # 入力ファイル。ファイルのパスが違うと意味不明なエラーメッセージが出ます。パスをよく確認してください。
        print(df.head())
    except FileNotFoundError:
        print("livedoor.json file not found. Please check the file path.")
        return

    # linux環境では動作しました。macなどでは動かないかも。
    with Pool(cpu_count() - 1) as p:  # マルチプロセスで処理
        vectors = p.map(f, df.body.values.tolist())  # 本文のリスト化
        np.save(QDRANT_NPY, vectors, allow_pickle=False)  # ベクトル保存

if __name__ == '__main__':
    main()
