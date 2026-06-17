import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

def load_data(path: str = os.path.join(os.path.dirname(__file__), "..", "data", "Space_Corrected.csv")) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #drop unused columns
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])

    #clean datum and rename
    df["Datum"] = pd.to_datetime(df["Datum"], format="mixed", utc=True)
    df = df.rename(columns={"Datum": "Date"})

    #clean rocket column, assign variable
    df = df.rename(columns={" Rocket": "Rocket"})
    df["Rocket"] = pd.to_numeric(df["Rocket"], errors="coerce")

    return df

def add_country(df: pd.DataFrame) -> pd.DataFrame:
    df['Country'] = df['Location'].str.split(',').str[-1].str.strip()
    return df

def get_data() -> pd.DataFrame:
    df: pd.DataFrame = load_data()
    return clean_data(df)

if __name__ == "__main__":
    dataframe = clean_data(load_data())
    dataframe.info()


