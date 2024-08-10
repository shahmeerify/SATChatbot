import pandas as pd

data = pd.read_csv("../Sentiment_Analysis_Dataset.csv")

data2 = list(data["sentence"])

with open(f"./sentiment/sentences_all.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(data2))