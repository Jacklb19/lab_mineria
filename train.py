import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from config import EJERCICIOS


BASE = Path(__file__).resolve().parent
MODELOS = BASE / "modelos"
GRAFICAS = BASE / "graficas"


def cargar_datos(nombre, ejercicio):
    datos = pd.read_csv(BASE / ejercicio["archivo"])
    columnas = [*ejercicio["variables"], ejercicio["objetivo"]]
    faltantes = set(columnas) - set(datos.columns)
    if faltantes:
        raise ValueError(f"{nombre}: faltan columnas: {', '.join(sorted(faltantes))}")
    datos = datos[columnas]
    if datos.isna().any().any():
        raise ValueError(f"{nombre}: hay valores vacíos en el CSV")
    for columna in columnas:
        datos[columna] = pd.to_numeric(datos[columna], errors="raise")
    if not np.isfinite(datos.to_numpy()).all():
        raise ValueError(f"{nombre}: hay valores no finitos en el CSV")
    if len(datos) < 10:
        raise ValueError(f"{nombre}: se necesitan al menos 10 filas")
    return datos


def guardar_graficas(nombre, datos, ejercicio):
    objetivo = ejercicio["objetivo"]
    fig, ejes = plt.subplots(1, 3, figsize=(12, 3.5), constrained_layout=True)
    for eje, variable in zip(ejes, ejercicio["variables"]):
        eje.scatter(datos[variable], datos[objetivo], s=9, alpha=0.35, color="#2563eb")
        eje.set_xlabel(variable)
        eje.set_ylabel(objetivo)
        eje.grid(alpha=0.2)
    fig.suptitle(ejercicio["titulo"])
    fig.savefig(GRAFICAS / f"{nombre}.png", dpi=160)
    plt.close(fig)


def entrenar(nombre, ejercicio):
    datos = cargar_datos(nombre, ejercicio)
    variables = list(ejercicio["variables"])
    objetivo = ejercicio["objetivo"]
    x = datos[variables]
    y = datos[objetivo]

    if nombre == "dolar":
        datos_ordenados = datos.sort_values("Dia")
        corte = int(len(datos_ordenados) * 0.8)
        entrenamiento = datos_ordenados.iloc[:corte]
        prueba = datos_ordenados.iloc[corte:]
        x_train, x_test = entrenamiento[variables], prueba[variables]
        y_train, y_test = entrenamiento[objetivo], prueba[objetivo]
        particion = "80 % primeros días / 20 % últimos días"
    else:
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        particion = "80 % entrenamiento / 20 % prueba, aleatoria (semilla 42)"

    modelo_prueba = LinearRegression().fit(x_train, y_train)
    predicciones = modelo_prueba.predict(x_test)
    modelo_final = LinearRegression().fit(x, y)
    coeficientes = dict(zip(variables, modelo_final.coef_.tolist()))
    desviacion_y = float(y.std(ddof=0))
    coeficientes_estandarizados = {
        variable: float(coeficientes[variable] * x[variable].std(ddof=0) / desviacion_y)
        for variable in variables
    }

    resultado = {
        "archivo": ejercicio["archivo"],
        "filas": len(datos),
        "filas_entrenamiento": len(x_train),
        "filas_prueba": len(x_test),
        "particion": particion,
        "objetivo": objetivo,
        "variables": variables,
        "intercepto": float(modelo_final.intercept_),
        "coeficientes": coeficientes,
        "coeficientes_estandarizados": coeficientes_estandarizados,
        "mse": float(mean_squared_error(y_test, predicciones)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predicciones))),
        "r2": float(r2_score(y_test, predicciones)),
        "rangos": {
            variable: [float(datos[variable].min()), float(datos[variable].max())]
            for variable in variables
        },
    }

    joblib.dump({"modelo": modelo_final, "variables": variables}, MODELOS / f"{nombre}.joblib")
    guardar_graficas(nombre, datos, ejercicio)
    return resultado


def main():
    MODELOS.mkdir(exist_ok=True)
    GRAFICAS.mkdir(exist_ok=True)
    resultados = {nombre: entrenar(nombre, ejercicio) for nombre, ejercicio in EJERCICIOS.items()}
    (BASE / "resultados.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for nombre, resultado in resultados.items():
        print(
            f"{nombre}: MSE={resultado['mse']:.3f}, "
            f"RMSE={resultado['rmse']:.3f}, R²={resultado['r2']:.4f}"
        )


if __name__ == "__main__":
    main()
