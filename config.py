EJERCICIOS = {
    "dolar": {
        "titulo": "Precio del dólar",
        "archivo": "dolar_data.csv",
        "objetivo": "Precio_Dolar",
        "unidad": "COP",
        "variables": {
            "Dia": {"etiqueta": "Día", "tipo": "entero", "minimo": 1, "ayuda": "Número de día desde el inicio de los datos"},
            "Inflacion": {"etiqueta": "Inflación", "tipo": "decimal", "ayuda": "Fracción decimal: 0.02 equivale a 2 %"},
            "Tasa_interes": {"etiqueta": "Tasa de interés", "tipo": "decimal", "ayuda": "Porcentaje: escribe 5 para 5 %"},
        },
    },
    "glucosa": {
        "titulo": "Nivel de glucosa",
        "archivo": "glucosa_data.csv",
        "objetivo": "Nivel_Glucosa",
        "unidad": "mg/dL",
        "variables": {
            "Edad": {"etiqueta": "Edad", "tipo": "entero", "minimo": 0, "maximo": 120, "ayuda": "Años cumplidos"},
            "IMC": {"etiqueta": "IMC", "tipo": "decimal", "minimo": 0.1, "ayuda": "Índice de masa corporal"},
            "Actividad_Fisica": {"etiqueta": "Actividad física", "tipo": "entero", "minimo": 0, "maximo": 168, "ayuda": "Horas de ejercicio por semana"},
        },
    },
    "energia": {
        "titulo": "Consumo de energía",
        "archivo": "energia_data.csv",
        "objetivo": "Consumo_Energia",
        "unidad": "kWh",
        "variables": {
            "Temperatura": {"etiqueta": "Temperatura", "tipo": "decimal", "ayuda": "Grados Celsius"},
            "Hora": {"etiqueta": "Hora", "tipo": "entero", "minimo": 1, "maximo": 24, "ayuda": "Hora del día, de 1 a 24"},
            "Dia_Semana": {"etiqueta": "Día de la semana", "tipo": "entero", "minimo": 1, "maximo": 7, "ayuda": "1 = lunes; 7 = domingo"},
        },
    },
}
