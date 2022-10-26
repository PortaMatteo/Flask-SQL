from flask import Flask, render_template, request 
app = Flask(__name__)

import pandas as pd 
import matplotlib.pyplot as plt
import pymssql



@app.route("/", methods=["GET"])
def home():
    return render_template("homepage.html")

@app.route("/scelta", methods=["GET"])
def scelta():
    global tabella, sceltaUtente
    sceltaUtente = request.args["scelta"]
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')
    if sceltaUtente == "es1":
        query = 'SELECT category_name,count(*) as numero_prodotti FROM production.categories INNER JOIN production.products ON categories.category_id = products.category_id GROUP BY category_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_prodotti',ascending=False,inplace=True)
        return render_template("result.html", nomiColonne = tabella.columns.values, dati = tabella.values)

    elif scelta == "es2":
        query = 'SELECT store_name,count(order_id) as numero_ordini FROM sales.orders INNER JOIN sales.stores ON orders.store_id = stores.store_id GROUP BY store_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_ordini',ascending=False,inplace=True)
        return render_template("result.html", nomiColonne = tabella.columns.values, dati = tabella.values)
        
    elif scelta == "es3":
        query = 'SELECT brand_name,count(*) as numero_prodotti FROM production.products INNER JOIN production.brands ON products.brand_id = brands.brand_id GROUP BY brand_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_prodotti',ascending=False,inplace=True)
        return render_template("result.html", nomiColonne = tabella.columns.values, dati = tabella.values)

    else:
        return render_template("search.html")


@app.route("/grafico.png", methods=["GET"])
def visualizza():
    if sceltaUtente == "es1":
        grafico = plt.figure()
        ax = plt.axes()
        ax.bar(tabella.category_name,tabella.numero_prodotti)
        plt.xticks(rotation=90)

    elif sceltaUtente == "es2":
        grafico = plt.figure()
        ax = plt.axes()
        ax.barh(tabella.store_name,tabella.numero_ordini)
    else:
        grafico ==  plt.figure(figsize=(8,8))
        ax = plt.axes()
        ax.pie(tabella.numero_prodotti,labels = tabella.brand_name)
        grafico.show()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/result", methods=["GET"])
def result():
    # Collegamento al database
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')
    # Invio query al database e ricezione informazioni
    NomeProdotto = request.args["NomeProdotto"]
    query = f"SELECT * FROM production.products INNER JOIN production.brands on production.brands.brand_id = production.products.brand_id INNER JOIN production.categories on production.categories.category_id = production.products.category_id WHERE product_name LIKE '{NomeProdotto}%'" 
    # Visualizzare le informazioni 
    dfProdotti = pd.read_sql(query,conn)
    return render_template("result_search.html", tabella = dfProdotti.to_html(), nomiColonne = dfProdotti.columns.values, dati = dfProdotti.values)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)