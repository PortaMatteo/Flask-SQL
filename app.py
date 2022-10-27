from flask import Flask, render_template, request, Response
app = Flask(__name__)

import io
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import pymssql



@app.route("/", methods=["GET"])
def home():
    return render_template("homepage.html")

@app.route("/scelta", methods=["GET"])
def scelta():
    global tabella, sceltaUtente
    sceltaUtente = request.args["scelta"]
    print(sceltaUtente)
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')
    if sceltaUtente == "es1":
        query = 'SELECT category_name,count(*) as numero_prodotti FROM production.categories INNER JOIN production.products ON categories.category_id = products.category_id GROUP BY category_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_prodotti',ascending=False,inplace=True)
        testo = "Numero di prodotti per ogni categoria"

    elif sceltaUtente == "es2":
        query = 'SELECT store_name,count(order_id) as numero_ordini FROM sales.orders INNER JOIN sales.stores ON orders.store_id = stores.store_id GROUP BY store_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_ordini',ascending=False,inplace=True)
        testo = "Numero di orrdini per ogni store"
        
    elif sceltaUtente == "es3":
        query = 'SELECT brand_name,count(*) as numero_prodotti FROM production.products INNER JOIN production.brands ON products.brand_id = brands.brand_id GROUP BY brand_name'
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_prodotti',ascending=False,inplace=True)
        testo = "Il numero di prodotti per ogni store"

    else:
        return render_template("search.html")

    return render_template("result.html", nomiColonne = tabella.columns.values, dati = tabella.values, testo = testo)

@app.route("/grafico.png", methods=["GET"])
def visualizza():
    if sceltaUtente == "es1":
        fig = plt.figure()
        ax = plt.axes()
        ax.bar(tabella.category_name,tabella.numero_prodotti)
        plt.xticks(rotation=90)

    elif sceltaUtente == "es2":
        fig = plt.figure()
        ax = plt.axes()
        ax.barh(tabella.store_name,tabella.numero_ordini)
    else:
        fig =  plt.figure(figsize=(8,8))
        ax = plt.axes()
        ax.pie(tabella.numero_prodotti,labels = tabella.brand_name)
        fig.show()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/result", methods=["GET"])
def result():
    # Collegamento al database
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')
    # Invio query al database e ricezione informazioni
    NomeProdotto = request.args["NomeProdotto"]
    query = f"SELECT * FROM production.products WHERE product_name LIKE '{NomeProdotto}%'" 
    # Visualizzare le informazioni 
    dfProdotti = pd.read_sql(query,conn)
    return render_template("result_search.html", tabella = dfProdotti.to_html(), nomiColonne = dfProdotti.columns.values, dati = dfProdotti.values, ricerca = NomeProdotto)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)