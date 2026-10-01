import json
import math
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, render_template, request

from config import EJERCICIOS


BASE = Path(__file__).resolve().parent
app = Flask(__name__)


def cargar_modelos():
    modelos = {}
    for nombre in EJERCICIOS:
        ruta = BASE / "modelos" / f"{nombre}.joblib"
        if ruta.exists():
            modelos[nombre] = joblib.load(ruta)
    return modelos


MODELOS = cargar_modelos()
RUTA_RESULTADOS = BASE / "resultados.json"
RESULTADOS = json.loads(RUTA_RESULTADOS.read_text(encoding="utf-8")) if RUTA_RESULTADOS.exists() else {}


def leer_valores(formulario, ejercicio):
    valores = {}
    for variable, definicion in ejercicio["variables"].items():
        texto = formulario.get(variable, "").strip()
        if not texto:
            raise ValueError(f"Completa el campo {definicion['etiqueta']}.")
        try:
            valor = float(texto)
        except ValueError as error:
            raise ValueError(f"{definicion['etiqueta']} debe ser un número.") from error
        if not math.isfinite(valor):
            raise ValueError(f"{definicion['etiqueta']} debe ser un número finito.")
        if definicion["tipo"] == "entero" and not valor.is_integer():
            raise ValueError(f"{definicion['etiqueta']} debe ser un número entero.")
        if "minimo" in definicion and valor < definicion["minimo"]:
            raise ValueError(f"{definicion['etiqueta']} debe ser al menos {definicion['minimo']}.")
        if "maximo" in definicion and valor > definicion["maximo"]:
            raise ValueError(f"{definicion['etiqueta']} debe ser como máximo {definicion['maximo']}.")
        valores[variable] = int(valor) if definicion["tipo"] == "entero" else valor
    return valores


@app.route("/", methods=["GET", "POST"])
def inicio():
    nombre = request.values.get("ejercicio", "dolar")
    if nombre not in EJERCICIOS:
        nombre = "dolar"
    ejercicio = EJERCICIOS[nombre]
    prediccion = None
    error = None
    advertencia = None
    valores = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            if nombre not in MODELOS:
                raise ValueError("Falta el modelo. Ejecuta primero python train.py.")
            entrada = leer_valores(request.form, ejercicio)
            variables = MODELOS[nombre]["variables"]
            fila = pd.DataFrame([entrada], columns=variables)
            prediccion = float(MODELOS[nombre]["modelo"].predict(fila)[0])
            rangos = RESULTADOS.get(nombre, {}).get("rangos", {})
            fuera_de_rango = [
                variable for variable, valor in entrada.items()
                if variable in rangos and not rangos[variable][0] <= valor <= rangos[variable][1]
            ]
            if fuera_de_rango:
                advertencia = "Fuera del rango observado: " + ", ".join(fuera_de_rango) + ". La predicción puede ser menos fiable."
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        ejercicios=EJERCICIOS,
        nombre=nombre,
        ejercicio=ejercicio,
        prediccion=prediccion,
        error=error,
        advertencia=advertencia,
        valores=valores,
    )


if __name__ == "__main__":
    app.run(debug=False)
