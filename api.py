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
    "programmato": [
        "in programmazione",
        "in progettazione esecutiva",
        "in progettazione definitiva",
    ],
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
    res = {"fibra": [], "fwa": []}
    res["fibra"] = calcoloMedia("Stato Fibra")
    res["fwa"] = calcoloMedia("Stato FWA")
    return json.dumps(res)

@app.route("/media-regione", methods=["POST"])
def mediaRegione():
    regione=request.json["regione"]
    res = {"fibra": [], "fwa": []}
    res["fibra"] = calcoloMedia("Stato Fibra",regione)
    res["fwa"] = calcoloMedia("Stato FWA",regione)
    return json.dumps(res)


def calcoloMedia(stato,regione=""):
    res = {}
    data=df
    if(regione!=""):
        data=df[df["Regione"] == regione]
    for term in terms.keys():
        res[term] = round(
            len([x for x in data[stato] if x in terms[term]]) / len(data[stato]) * 100, 2
        )

    res["altro"] = round(
        100 - (res["programmato"] + res["esecuzione"] + res["terminato"]), 2
    )
    return res


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
