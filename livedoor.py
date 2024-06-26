import json
import datetime
from typing import List, Dict
from pathlib import Path
import random

CORPUS_DIR = './livedoor-homme'  # ライブドアコーパスをここにおく
QDRANT_JSON = 'livedoor.json'
SAMPLE_TEXT_LEN: int = 500  # ドキュメントを500文字でトランケート


def read_document(path: Path) -> Dict[str, str]:
    """1ドキュメントの処理"""
    with open(path, 'r', encoding='utf-8') as f:
        lines: List[any] = f.readlines(SAMPLE_TEXT_LEN)
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

    with open(QDRANT_JSON, 'w') as fp:
        for x in corpus:
            doc: Dict[str, str] = read_document(x)
            json.dump(doc, fp)  # 1行分
            fp.write('\n')


if __name__ == '__main__':
    load_dataset_from_livedoor_files()
