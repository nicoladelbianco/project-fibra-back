from flask import Flask, request
import pandas as pd
import json

app = Flask(__name__)

df = pd.read_csv("stato_lavori.csv", sep=";", encoding="UTF-8")

df["Piano fibra (anno)"] = df["Piano fibra (anno)"].fillna(0)
df["Piano FWA (anno)"] = df["Piano FWA (anno)"].fillna(0)

df["Piano fibra (anno)"] = df["Piano fibra (anno)"].astype("int64")
df["Piano FWA (anno)"] = df["Piano FWA (anno)"].astype("int64")

terms = {
    "programmato": ["in programmazione", "in progettazione"],
    "esecuzione": ["in esecuzione"],
    "terminato": ["terminato", "lavori chiusi", "in collaudo"],
}


@app.route("/")
def index():
    res = {
        "regioni": df["Regione"].to_json(),
        "provincie": df["Provincia"].to_json(),
        "citta": df["Citta"].to_json(),
    }
    return json.dumps(res)


@app.route("/media")
def media():
    res = {}
    for term in terms.keys():
        res.update(
            {
                term: round(
                    len([x for x in df["Stato Fibra"] if x in terms[term]])
                    / len(df["Stato Fibra"])
                    * 100,
                    2,
                )
            }
        )
    res.update(
        {
            "altro": round(
                100 - (res["programmato"] + res["esecuzione"] + res["terminato"]), 2
            )
        }
    )
    return json.dumps(res)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
