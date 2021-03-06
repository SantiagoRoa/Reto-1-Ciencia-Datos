from flask import Flask, request
from flask import url_for
from flask import render_template
import pandas as pd
from sodapy import Socrata


client = Socrata("www.datos.gov.co", None)
results = client.get("sdvb-4x4j", limit=2000)
df = pd.DataFrame.from_records(results)

tablaOriginal = df.rename(columns={'num_resolucion': 'Número de resolución', 'fecha_resolucion': 'Fecha de resolución', 'a_o': 'Año', 'cod_territorio': 'Código de territorio',
                          'nom_territorio': 'Departamento', 'laboratorio_vacuna': 'Laboratorio', 'cantidad': 'Dosis aplicadas', 'uso_vacuna': 'Población vacunada', 'fecha_corte': 'Fecha de registro'})

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', tables=[tablaOriginal.to_html(classes='data')], titles=tablaOriginal.columns.values)


@app.route("/", methods=["GET", "POST"])
def pressButton():
    if request.method == "POST":
        if request.form.get("buttonB") == "clean":
            return render_template('index.html', tables=[tablaOriginal.to_html(classes='data')], titles=tablaOriginal.columns.values)
        elif request.form.get("buttonA") == "filter":
            param = request.form["param"]
            value = request.form.get("valor")
            tablaFiltrada = tablaOriginal[tablaOriginal[param] == value]
            return render_template('index.html', tables=[tablaFiltrada.to_html(classes='data')], titles=tablaFiltrada.columns.values)
        else:
            pass