import json
import datetime
from typing import List, Dict
from pathlib import Path
import random
import chardet

CORPUS_DIR = './livedoor-homme'  # ライブドアコーパスをここにおく
QDRANT_JSON = 'livedoor.json'
SAMPLE_TEXT_LEN: int = 500  # ドキュメントを500文字でトランケート


def detect_encoding(file_path: Path) -> str:
    """ファイルのエンコーディングを自動検出する"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def read_document(path: Path) -> Dict[str, str]:
    """1ドキュメントの処理"""
    encoding = detect_encoding(path)
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        lines: List[str] = f.readlines()
        lines = list(map(lambda x: x.rstrip(), lines))

        d = datetime.datetime.strptime(lines[1], "%Y-%m-%dT%H:%M:%S%z")
        created_at = int(round(d.timestamp()))  # 数値(UNIXエポックタイプ)に変換

        return {
            "url": lines[0],
            # ['livedoor-corpus', 'it-life-hack', 'it-life-hack-12345.txt']
            "publisher": path.parts[1],
            "created_at": created_at,
            "body": ' '.join(lines[2:])  # 初めの２行をスキップし、各行をスペースで連結し、１行にする。
        }


def load_dataset_from_livedoor_files() -> (List[List[float]], List[str]):
    # NB. exclude LICENSE.txt, README.txt, CHANGES.txt
    corpus: List[Path] = list(Path(CORPUS_DIR).rglob('*-*.txt'))
    random.shuffle(corpus)  # 記事をシャッフルします

    with open(QDRANT_JSON, 'w', encoding="utf-8") as fp:
        for x in corpus:
            doc: Dict[str, str] = read_document(x)
            # ensure_ascii=Falseで日本語をそのまま保存
            json.dump(doc, fp, ensure_ascii=False)
            fp.write('\n')


if __name__ == '__main__':
    load_dataset_from_livedoor_files()
