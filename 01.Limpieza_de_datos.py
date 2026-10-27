import datetime as dt
import pandas as pd


# 1. CARGAMOS EL DATASET
# Ejecutamos el archivo desde la carpeta que contiene el CSV.
df = pd.read_csv('Unicorn_companies.csv')


# 2. EXPLORAMOS LOS DATOS ORIGINALES
print('\nPrimeras tres filas:')
print(df.head(3).to_string(index=False))

print(f'\nNúmero total de celdas, incluidas las vacías: {df.size}')
print(f'Número total de filas: {df.shape[0]}')
print(f'Número total de columnas: {df.shape[1]}')

print('\nNombres de las columnas:')
print(df.columns.tolist())

# info() muestra los tipos de datos y los valores no nulos de cada columna.
# No necesita print() y evita repetir esta información con dtypes.
print('\nInformación general del dataset:')
df.info()

# Mostrar los tipos de datos de cada columna
print('Los tipos de datos de cada columna son:')
print(df.dtypes)

print('\nEstadísticas de las columnas numéricas originales:')
print(df.describe())

# 3. REVISAMOS DUPLICADOS Y VALORES NULOS
# Solo los contamos: no eliminamos filas automáticamente.
print(f'\nFilas completamente duplicadas: {df.duplicated().sum()}')

print('\nValores nulos por columna antes de las conversiones:')
print(df.isna().sum())

print('\nIndustrias del dataset:')
print(df['Industry'].unique())

# 4. CONVERTIMOS LAS FECHAS Y CREAMOS EL AÑO DE INCORPORACIÓN


# Conservamos las fechas originales para identificar conversiones fallidas.
fechas_originales = df['Date Joined'].copy()

# Convertimos a fecha. Los valores que no puedan convertirse serán NaT.
df['Date Joined'] = pd.to_datetime(df['Date Joined'], errors='coerce')

# Detectamos fechas que tenían contenido, pero no pudieron convertirse.
fechas_invalidas = fechas_originales.notna() & df['Date Joined'].isna()

print(f'\nFechas que no se han podido convertir: {fechas_invalidas.sum()}')

if fechas_invalidas.any():
    print(pd.DataFrame({
        'Company': df.loc[fechas_invalidas, 'Company'],
        'Fecha original': fechas_originales[fechas_invalidas],
    }).to_string(index=False))

# Creamos la columna con el año de incorporación como unicornio.
df['Year Joined'] = df['Date Joined'].dt.year

print('\nEjemplo de fechas convertidas y años extraídos:')
print(df[['Date Joined', 'Year Joined']].head())


# 5. COMPROBAMOS LOS DATOS NECESARIOS Y LOS AÑOS INCOHERENTES
columnas_necesarias = ['Industry', 'Year Founded', 'Year Joined']

print('\nValores nulos necesarios para el análisis, tras las conversiones:')
print(df[columnas_necesarias].isna().sum())

# Una empresa no puede convertirse en unicornio antes de su fundación.
incoherentes = df['Year Joined'] < df['Year Founded']

print(f'\nEmpresas con años incoherentes: {incoherentes.sum()}')
if incoherentes.any():
    print(df.loc[
        incoherentes,
        ['Company', 'Industry', 'Year Founded', 'Year Joined']
    ].to_string(index=False))

# Yidian Zixun aparecerá arriba si conserva los años 2021 y 2017.
# No corregimos sus años sin verificar primero la fuente.


# 6. PREPARAMOS UNA COPIA PARA EL ANÁLISIS
# Conservamos df completo. La copia excluye registros con datos necesarios
# nulos o con años incoherentes para evitar resultados negativos o incompletos.
datos_completos = df[columnas_necesarias].notna().all(axis=1)
df_analisis = df.loc[datos_completos & ~incoherentes].copy()

print(f'\nFilas disponibles para el análisis: {len(df_analisis)}')
print(f'Filas excluidas del análisis: {len(df) - len(df_analisis)}')

# Calculamos la diferencia entre años, no la duración exacta entre fechas.
df_analisis['years_till_unicorn'] = (
    df_analisis['Year Joined'] - df_analisis['Year Founded']
)


# 7. TOMAMOS UNA MUESTRA ALEATORIA
# Seleccionamos 50 filas, o todas si quedan menos de 50 disponibles.
# random_state=42 permite repetir la selección con los mismos datos.
df_muestra = df_analisis.sample(
    n=min(50, len(df_analisis)), random_state=42
).copy()

print(f'\nMuestra de {len(df_muestra)} empresas:')
print(df_muestra[
    ['Company', 'Industry', 'Year Founded', 'Year Joined', 'years_till_unicorn']
].to_string(index=False))


# 8. ANALIZAMOS EL MENOR TIEMPO POR INDUSTRIA EN LA MUESTRA
# min() obtiene el menor tiempo de cada industria; max() obtendría el mayor.
# Ordenamos de menor a mayor y mostramos hasta diez industrias.
grupo_industria = (
    df_muestra.groupby('Industry')[['years_till_unicorn']]
    .min()
    .sort_values(by='years_till_unicorn')
)

print('\nMenor número de años por industria dentro de la muestra:')
print(grupo_industria.head(10))

# Este resultado no es la media ni representa necesariamente todo el dataset.
# Para analizar todas las filas válidas, usa df_analisis en el groupby.







