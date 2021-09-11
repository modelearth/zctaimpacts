import os
import pandas as pd
import sqlite3


def NAICS2017_NAICS2012(db):
    df = pd.read_excel(
        os.path.join("raw", "2017_to_2012_NAICS.xlsx"),
        dtype=str,
        skiprows=2,
        usecols="A:D",
        index_col=None,
    )

    df.columns = ["NAICS2017", "NAICS2017_TITLE", "NAICS2012", "NAICS2012_TITLE"]

    df.to_csv(
        os.path.join("out", "NAICS2017_NAICS2012.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
    )

    df.to_sql("NAICS2017_NAICS2012", db, if_exists="replace", index=False)


def NAICS2007_NAICS2012(db):
    df = pd.read_excel(
        os.path.join("raw", "2007_to_2012_NAICS.xls"),
        dtype=str,
        skiprows=2,
        usecols="A:D",
        index_col=None,
    )

    df.columns = ["NAICS2007", "NAICS2007_TITLE", "NAICS2012", "NAICS2012_TITLE"]

    df.to_csv(
        os.path.join("out", "NAICS2007_NAICS2012.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
        header=["NAICS2007", "NAICS2007_TITLE", "NAICS2012", "NAICS2012_TITLE"],
    )

    df.to_sql("NAICS2007_NAICS2012", db, if_exists="replace", index=False)


def BEA_NAICS2007(db):
    df = pd.read_excel(
        os.path.join("raw", "GDPbyInd_GO_NAICS_1997-2016.xlsx"),
        sheet_name="NAICS codes",
        dtype=str,
        skiprows=[0, 1, 2, 3, 4, 5, 6],
        usecols="C,D,F",
    )
    colnames = [colname for colname in df.columns]
    df = df[df[colnames[0]].notna()]
    df = df[df[colnames[2]].notna()]

    df.columns = ["BEA_CODE", "TITLE", "NAICS2007"]

    df.to_csv(
        os.path.join("out", "GDPbyInd_GO_NAICS_1997-2016.csv"),
        sep="|",
        encoding="utf-8",
        index=False,
    )

    df.to_sql("BEA_NAICS2007", db, if_exists="replace", index=False)


if __name__ == "__main__":
    db = sqlite3.connect(os.path.join("out", "db.sqlite3"))

    NAICS2017_NAICS2012(db)
    NAICS2007_NAICS2012(db)
    BEA_NAICS2007(db)

    db.close()