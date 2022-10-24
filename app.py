from flask import Flask, render_template, request 
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("search.html")

@app.route("/result", methods=["GET"])
def result():
    # Collegamento al database
    import pandas as pd 
    import pymssql
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')
    # Invio query al database e ricezione informazioni
    NomeProdotto = request.args["NomeProdotto"]
    query = f"SELECT * FROM production.products INNER JOIN production.brands on production.brands.brand_id = production.products.brand_id INNER JOIN production.categories on production.categories.category_id = production.products.category_id WHERE product_name LIKE '{NomeProdotto}%'" 
    # Visualizzare le informazioni 
    dfProdotti = pd.read_sql(query,conn)
    return render_template("result.html", tabella = dfProdotti.to_html(), nomiColonne = dfProdotti.columns.values, dati = dfProdotti.values)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)