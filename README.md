# Laboratorio 1: regresión lineal múltiple

Este proyecto resuelve los tres ejercicios del laboratorio de minería de datos: predicción del precio del dólar, del nivel de glucosa y del consumo de energía. Incluye el entrenamiento, la evaluación, las gráficas, los modelos exportados y aplicaciones web sencillas en Flask y Streamlit. El análisis sigue las fases de CRISP-DM y utiliza los tres CSV suministrados con el enunciado.

## 1. Objetivo y datos

En los tres casos se usa **regresión lineal múltiple**. El modelo estima una variable numérica a partir de tres entradas. Cada fila del CSV es una observación.

| Ejercicio | Archivo | Entradas | Variable que se predice | Filas |
| --- | --- | --- | --- | ---: |
| Dólar | `dolar_data.csv` | `Dia`, `Inflacion`, `Tasa_interes` | `Precio_Dolar` (COP) | 500 |
| Glucosa | `glucosa_data.csv` | `Edad`, `IMC`, `Actividad_Fisica` | `Nivel_Glucosa` (mg/dL) | 2.000 |
| Energía | `energia_data.csv` | `Temperatura`, `Hora`, `Dia_Semana` | `Consumo_Energia` (kWh) | 10.000 |

Significado y unidades de las entradas:

- `Dia`: número de día desde el inicio del conjunto. No es una fecha de calendario.
- `Inflacion`: tasa escrita como fracción decimal; `0.02` representa 2 %.
- `Tasa_interes`: tasa escrita en puntos porcentuales; `5` representa 5 %.
- `Edad`: años cumplidos.
- `IMC`: índice de masa corporal.
- `Actividad_Fisica`: horas de ejercicio por semana.
- `Temperatura`: grados Celsius.
- `Hora`: número entero de 1 a 24.
- `Dia_Semana`: número entero de 1 (lunes) a 7 (domingo).

El PDF no especifica la moneda del precio del dólar. En el proyecto se muestra **COP** porque los valores del CSV están alrededor de 4.000 a 6.500; es una suposición de presentación que debe confirmarse con el origen de los datos.

## 2. Pasos realizados según CRISP-DM

1. **Comprensión del problema:** se identificó qué valor debe predecirse en cada ejercicio y cuáles son las tres entradas disponibles. Se escogió regresión lineal múltiple porque la pide el laboratorio y permite interpretar cada coeficiente.
2. **Comprensión de los datos:** se inspeccionaron las columnas, los tipos y los rangos. Los tres archivos contienen únicamente valores numéricos, sin celdas vacías ni filas duplicadas.
3. **Preparación:** `train.py` comprueba que estén todas las columnas, que sus valores sean numéricos y finitos, y que haya suficientes observaciones. No se imputaron datos ni se eliminaron filas porque no fue necesario. Las variables se usan en sus unidades originales para facilitar la interpretación.
4. **Modelado:** se entrena un `LinearRegression` independiente para cada ejercicio. Para dólar se usan los primeros 400 días para entrenar y los últimos 100 para probar; así la evaluación representa predicción de días posteriores. Para glucosa y energía se separa aleatoriamente el 80 % para entrenamiento y el 20 % para prueba, con semilla fija `42`.
5. **Evaluación:** el modelo se ajusta solo con el grupo de entrenamiento y se calculan MSE, RMSE y R² sobre el grupo de prueba. Los datos de prueba no participan en ese ajuste. Después de medir el desempeño, se entrena un **modelo final con todas las filas** y se guarda para la web. Por eso los coeficientes de este informe corresponden al modelo final, mientras las métricas corresponden al modelo evaluado con datos separados.
6. **Uso:** los modelos finales se guardan con `joblib` en `modelos/`. `app.py` los carga y permite introducir las tres variables de cualquier ejercicio en el navegador.

El modelo tiene la forma `predicción = intercepto + coeficiente_1 × variable_1 + coeficiente_2 × variable_2 + coeficiente_3 × variable_3`. Cada coeficiente expresa el cambio estimado en la salida al aumentar una unidad de esa entrada **manteniendo constantes las otras dos**.

## 3. Resultados e interpretación

| Ejercicio | MSE en prueba | RMSE en prueba | R² en prueba |
| --- | ---: | ---: | ---: |
| Dólar | 2.905,71 COP² | 53,90 COP | 0,879 |
| Glucosa | 233,69 (mg/dL)² | 15,29 mg/dL | 0,681 |
| Energía | 429,52 kWh² | 20,72 kWh | 0,897 |

**MSE** es el promedio de los errores al cuadrado; cuanto menor, mejor. **RMSE** es su raíz cuadrada y vuelve a las unidades de la variable predicha. **R²** indica qué proporción de la variación del grupo de prueba explica el modelo; cuanto más cerca de 1, mejor. Las métricas de ejercicios distintos no se comparan directamente por sus diferentes unidades y dispersiones.

### Dólar

Ecuación aproximada del modelo final:

`Precio_Dolar = 3978,98 + 4,9991 × Dia − 338,06 × Inflacion − 2,5328 × Tasa_interes`

- Un día adicional se asocia con **+5,00 COP** aproximadamente, manteniendo las otras entradas constantes.
- Un aumento de **0,01 en `Inflacion`** (un punto porcentual) se asocia con **−3,38 COP**. El coeficiente `−338,06` corresponde a aumentar la fracción completa en 1, un cambio fuera de la escala usual de estos datos.
- Un punto porcentual adicional en `Tasa_interes` se asocia con **−2,53 COP**.
- El coeficiente estandarizado absoluto de `Dia` es **0,998**; los de inflación e interés son aproximadamente **0,002**. Por tanto, `Dia` domina en este conjunto. El R² de 0,879 se midió sobre días posteriores; no garantiza que la tendencia continúe indefinidamente.

Gráficas: [relaciones del dólar](graficas/dolar.png). La relación con `Dia` es muy clara; las gráficas individuales de inflación e interés no muestran un patrón fuerte.

### Glucosa

Ecuación aproximada del modelo final:

`Nivel_Glucosa = 66,32 + 1,2337 × Edad + 0,8832 × IMC − 2,0104 × Actividad_Fisica`

- Un año adicional de edad se asocia con **+1,23 mg/dL**.
- Una unidad adicional de IMC se asocia con **+0,88 mg/dL**.
- Una hora semanal adicional de actividad física se asocia con **−2,01 mg/dL**.
- Para comparar variables de distintas unidades se calcularon coeficientes estandarizados: `Edad` **0,792**, `Actividad_Fisica` **−0,214** e `IMC` **0,129**. La edad tiene el mayor impacto relativo dentro de los valores observados. El R² de 0,681 muestra que todavía queda variación sin explicar.

Gráficas: [relaciones de glucosa](graficas/glucosa.png). La relación de edad con glucosa es la más visible.

### Energía

Ecuación aproximada del modelo final:

`Consumo_Energia = 101,38 + 9,9660 × Temperatura + 5,0118 × Hora − 3,0892 × Dia_Semana`

- Un grado Celsius adicional se asocia con **+9,97 kWh**.
- Una unidad adicional en `Hora` se asocia con **+5,01 kWh**.
- Avanzar una unidad en la codificación `Dia_Semana` se asocia con **−3,09 kWh** en este modelo.
- Los coeficientes estandarizados son `Temperatura` **0,781**, `Hora` **0,544** y `Dia_Semana` **−0,097**. La temperatura tiene el mayor impacto relativo. El RMSE de prueba es 20,72 kWh.

Gráficas: [relaciones de energía](graficas/energia.png). Se ven relaciones positivas claras con temperatura y hora; el día de la semana muestra una relación más débil.

Los coeficientes estandarizados se calculan como `coeficiente × desviación estándar de la entrada / desviación estándar de la salida`. Su valor absoluto ayuda a comparar la importancia relativa **dentro de cada modelo**. Ninguno de estos resultados demuestra causalidad.

## 4. Archivos del proyecto

| Ruta | Función |
| --- | --- |
| `config.py` | Define archivos, variables, unidades y campos de la web. |
| `train.py` | Valida datos, separa entrenamiento y prueba, entrena, evalúa, exporta y dibuja. |
| `app.py` | Carga los modelos y atiende el formulario de predicción. |
| `streamlit_app.py` | Interfaz equivalente en Streamlit para ejecución local o en Community Cloud. |
| `templates/index.html` y `static/style.css` | Página web minimalista. |
| `modelos/*.joblib` | Un modelo final exportado por ejercicio. |
| `graficas/*.png` | Tres gráficas por ejercicio, agrupadas en una imagen. |
| `resultados.json` | Métricas, coeficientes y rangos exactos calculados por `train.py`. |
| `requirements.txt` | Versiones de las bibliotecas necesarias. |

## 5. Cómo ejecutarlo

Se recomienda Python 3.12. En PowerShell, desde la carpeta raíz del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train.py
.\.venv\Scripts\python.exe app.py
```

Si `py -3.12` no existe, se puede usar `python -m venv .venv` con una instalación compatible de Python. El comando anterior abre la versión Flask en `http://127.0.0.1:5000`. Para usar la versión Streamlit, se ejecuta en su lugar:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

En cualquiera de las dos interfaces se elige el ejercicio, se introducen las tres entradas y se pulsa **Predecir**. Por ejemplo, para dólar se puede ingresar `Dia=400`, `Inflacion=0.02` y `Tasa_interes=5`. La página avisa si una entrada queda fuera del rango observado en el CSV.

### Publicar en Streamlit Community Cloud

1. Subir a GitHub `streamlit_app.py` y los cambios en `requirements.txt` y `README.md`. `config.py`, `resultados.json` y `modelos/` ya forman parte del proyecto; los modelos no necesitan entrenarse en la nube.
2. Entrar a `https://share.streamlit.io/` con GitHub y elegir **Create app**.
3. Seleccionar el repositorio `Jacklb19/lab_mineria`, la rama `main` y `streamlit_app.py` como archivo de entrada.
4. En **Advanced settings**, elegir Python 3.12 y pulsar **Deploy**. Streamlit instalará lo indicado en `requirements.txt` y cargará los archivos del repositorio.

Desde la raíz del proyecto, los cambios se pueden subir con:

```powershell
git add streamlit_app.py requirements.txt README.md
git commit -m "Agregar aplicación Streamlit"
git push origin main
```

La guía oficial del servicio está en [Deploy your app on Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

Estas son instrucciones para una publicación posterior; el proyecto no se publica automáticamente al ejecutar el código local.

Si se cambian los CSV, hay que ejecutar de nuevo `train.py` y reiniciar la aplicación para cargar los modelos actualizados. Los archivos `.joblib` solo deben cargarse si provienen de este proyecto o de una fuente de confianza.

## 6. Conclusiones y límites

Los tres modelos cumplen el objetivo del laboratorio y predicen en los datos separados con el desempeño indicado arriba. Dólar y energía alcanzan R² cercanos a 0,9; glucosa, cerca de 0,68. La variable más influyente según los coeficientes estandarizados es `Dia` para dólar, `Edad` para glucosa y `Temperatura` para energía.

La regresión lineal supone efectos lineales y constantes. En energía, `Hora` y `Dia_Semana` se usan como números aunque son ciclos; por ello el modelo no representa explícitamente el salto de 24 a 1 ni de domingo a lunes. Las predicciones de dólar fuera de los 500 días observados son extrapolaciones y pueden perder precisión. Los resultados de glucosa son estimaciones académicas y no sustituyen una medición clínica. En general, conviene usar la web con valores parecidos a los rangos de los CSV.
