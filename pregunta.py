# """
# Limpieza de datos usando Pandas
# -----------------------------------------------------------------------------------------

# Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
# correctamente. Tenga en cuenta datos faltantes y duplicados.

# """

import pandas as pd
from datetime import datetime as dt
import re

#formato para fecha
def format_date(str_date):
    try:
        return dt.strptime(str_date, "%d/%m/%Y")
    except ValueError:
        try:
            return dt.strptime(str_date, "%Y/%m/%d")
        except ValueError:
            return None

def clean_data():
    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)
    # se realiza una copia de la data
    df = df.copy()
    #transforma a minusculas todas las columnas tipo object o string
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.lower()
    #reemplaza los simbolos

    df.idea_negocio = df.idea_negocio.str.replace("[+-_,/$.\|?¿)(*#)]", " ", regex=True)
    df.barrio = df.barrio.str.replace("[-]", " ", regex=True)
    df.barrio = df.barrio.str.replace("[ ]+", "_", regex=True)
    df.sexo = df.sexo.str.replace("[+-_,/$.\|?¿)(*#)]", " ", regex=True)
    df.comuna_ciudadano = df.comuna_ciudadano.astype(int)
    df.fecha_de_beneficio = df.fecha_de_beneficio.apply(format_date)
    df.monto_del_credito = df.monto_del_credito.replace("[\,$]|(\.00$)", "", regex=True).astype(float)
    df.línea_credito = df.línea_credito.str.replace("[+-_,/$.\|?¿)(*#)]", " ", regex=True)

    df = df.drop_duplicates()
    df = df.dropna()

    return df

# Llama a la función clean_data() y guarda el resultado en una variable
cleaned_df = clean_data()

# Imprime el DataFrame limpio
print(cleaned_df.head())

#Aplica value_counts() a la columna 'barrio' y convierte el resultado a una lista
conteo_barrio = cleaned_df['barrio'].value_counts()
print(conteo_barrio)
