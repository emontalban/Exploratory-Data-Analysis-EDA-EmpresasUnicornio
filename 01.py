import datetime as dt
import pandas as pd

# Cargar el conjunto de datos de las compañias unicornio

df = pd.read_csv('Unicorn_companies.csv')

# Mostras las primeras filas del conjunto de datos y ponermos index=False para que no se muestre el índice
print(df.head(3).to_string(index=False))

# Número total de celdas, incluidos los valores vacíos.
print(f'El número total de valores es: {df.size}')

# Número de filas y columnas.
print(f'El número total de filas es: {df.shape[0]}')
print(f'El número total de columnas es: {df.shape[1]}')

# Mostrar los tipos de datos de cada columna
print('Los tipos de datos de cada columna son:')
print(df.dtypes)


print('\nInformación general del dataset:')
df.info()

# Mostramos las estadísticas de las columnas numéricas.
print('\nEstadísticas de las columnas numéricas:')
print(df.describe())


# convertimos la columna Date Joined  datatime(fecha)
df['Date Joined'] = pd.to_datetime(df['Date Joined'])
print(df['Date Joined'].head())

# creamos una columna nueva llamada Year Joined que contenga el año de la fecha
df['Year Joined'] = df['Date Joined'].dt.year
print(df['Year Joined'].head())

# tomaños una muestra de datos quiero 50 filas aleatorias
df_muestra = df.sample(n=50, random_state=42)
print(df_muestra.to_string)

#calculamos el tiempo que tardaro las empresas en alcanzar el objetivo unicornio
df_muestra["years_till_unicorn"] = df_muestra["Year Joined"] - df_muestra["Year Founded"]
print(df_muestra.head(10))

# segunn la industrias cual fue la que llego mas rapido a convertirse en unicornio
grupo_industria = df_muestra[['Industry', 'years_till_unicorn']].groupby('Industry').max().sort_values(by='years_till_unicorn')
print(grupo_industria.head(10))

