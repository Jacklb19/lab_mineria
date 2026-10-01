import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from config import EJERCICIOS


BASE = Path(__file__).resolve().parent


@st.cache_resource
def cargar_modelo(nombre):
    ruta = BASE / "modelos" / f"{nombre}.joblib"
    if not ruta.exists():
        raise FileNotFoundError("Falta el modelo. Ejecuta primero python train.py.")
    return joblib.load(ruta)


@st.cache_data
def cargar_resultados():
    ruta = BASE / "resultados.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def pedir_valor(nombre, variable, definicion):
    entero = definicion["tipo"] == "entero"
    convertir = int if entero else float
    valor = st.number_input(
        definicion["etiqueta"],
        min_value=convertir(definicion["minimo"]) if "minimo" in definicion else None,
        max_value=convertir(definicion["maximo"]) if "maximo" in definicion else None,
        value=None,
        step=1 if entero else 0.01,
        key=f"{nombre}_{variable}",
    )
    st.caption(definicion["ayuda"])
    return valor


def main():
    st.set_page_config(page_title="Predicciones", layout="centered")
    st.title("Predicciones")
    st.write("Modelos de regresión lineal del laboratorio de minería de datos.")

    nombre = st.selectbox(
        "Ejercicio",
        list(EJERCICIOS),
        format_func=lambda clave: EJERCICIOS[clave]["titulo"],
    )
    ejercicio = EJERCICIOS[nombre]

    with st.form(f"formulario_{nombre}"):
        valores = {
            variable: pedir_valor(nombre, variable, definicion)
            for variable, definicion in ejercicio["variables"].items()
        }
        enviar = st.form_submit_button("Predecir")

    if enviar:
        if any(valor is None for valor in valores.values()):
            st.error("Completa los tres campos antes de predecir.")
            return
        try:
            guardado = cargar_modelo(nombre)
            fila = pd.DataFrame([valores], columns=guardado["variables"])
            prediccion = float(guardado["modelo"].predict(fila)[0])
        except (FileNotFoundError, ValueError) as error:
            st.error(str(error))
            return

        st.metric("Predicción estimada", f"{prediccion:.2f} {ejercicio['unidad']}")
        rangos = cargar_resultados().get(nombre, {}).get("rangos", {})
        fuera_de_rango = [
            variable for variable, valor in valores.items()
            if variable in rangos and not rangos[variable][0] <= valor <= rangos[variable][1]
        ]
        if fuera_de_rango:
            st.warning(
                "Fuera del rango observado: "
                + ", ".join(fuera_de_rango)
                + ". La predicción puede ser menos fiable."
            )

    st.caption("Estimación académica. Consulta las métricas y limitaciones en el README.")


if __name__ == "__main__":
    main()
