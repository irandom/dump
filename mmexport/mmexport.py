import collections
import operator
import os
import shutil

import pyodbc


db_file = "C:\\users\\andrey\\catalog.mdb"
catalog_table = "Catalog"
dst_dir = "C:\\andrey\\zz_catalog"

TEMPO_SLOW = "slow"
TEMPO_MODERATE = "moderate"
TEMPO_FAST = "fast"

TEMPOS = [
    TEMPO_SLOW,
    TEMPO_MODERATE,
    TEMPO_FAST,
]


def get_tempo_name(bpm):
    if bpm < 80:
        return TEMPO_SLOW
    elif bpm < 100:
        return TEMPO_MODERATE
    else:
        return TEMPO_FAST


Composition = collections.namedtuple("Composition", [
    "file_name",
    "title",
    "artist",
    "comments",
    "bitrate",
    "bpm",
])


def read_db(db_file, catalog_table):
    query_template = """
        SELECT
            `File Name`,
            `Song Title`,
            `Artist Name`,
            `Comments`,
            `Bitrate`,
            `BPM`
        FROM {catalog_table}
    """


    conn = pyodbc.connect(r'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={};'.format(db_file))
    cursor = conn.cursor()
    cursor.execute(query_template.format(catalog_table=catalog_table))
       
    return [Composition(*row) for row in cursor.fetchall()]


def copy_catalog(compositions, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for tempo in TEMPOS:
        os.makedirs(os.path.join(dst_dir, tempo), exist_ok=True)

    for composition in compositions:
        tempo_dir = os.path.join(dst_dir, get_tempo_name(composition.bpm))
        basename = os.path.basename(composition.file_name)
        shutil.copyfile(composition.file_name, os.path.join(tempo_dir, basename))




def main():
    compositions = [c for c in read_db(db_file, catalog_table) if c.comments is not None and "[FRR]" in c.comments]
    # print(len([1 for c in compositions if c.comments is not None and "[FRR]" in c.comments]))
    print(len(compositions))
    copy_catalog(compositions, dst_dir)


if __name__ == "__main__":
    main()
