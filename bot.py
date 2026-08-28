import pandas as pd
import glob


# =========================================================
# 1. Buscar datos y leer archivos
# =========================================================

archivos_csv = glob.glob('*.csv')
print(f"Archivos CSV encontrados: {archivos_csv}")

archivos_xlsx = glob.glob('*.xlsx')
print(f"Archivos XLSX encontrados: {archivos_xlsx}")

# 2. Guardar cada archivo leido en una lista de DataFrames

lista_dataframes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"leido {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"leido {archivo} - {len(df)} filas")


# =========================================================
# 3. Corregir el archivo con columnas distintas (Bogota)
# =========================================================
# [IA] El archivo sucursal_bogota.xlsx trae los nombres de columna
# distintos a los otros 3 (usa mayusculas y abreviaturas).
# Usamos 'Cant' como columna unica para identificarlo, ya que
# ningun otro archivo tiene una columna con ese nombre.

for i, df in enumerate(lista_dataframes):
    # enumerate nos da el indice (i) y el propio DataFrame (df)
    # de cada vuelta del ciclo; necesitamos el indice porque
    # vamos a reemplazar el DataFrame dentro de la lista.
    if 'Cant' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })
        print("Columnas de Bogota renombradas correctamente")


# =========================================================
# 4. Consolidar todo en un solo DataFrame (7 columnas)
# =========================================================

df_consolidado = pd.concat(lista_dataframes, ignore_index=True)
print(f"\nTotal filas consolidadas: {len(df_consolidado)}")
print(f"Columnas finales: {list(df_consolidado.columns)}")


# =========================================================
# 5. Limpieza de datos
# =========================================================

# [IA] Quitamos espacios en blanco al inicio/final de las columnas
# de texto (evita que "Efectivo " y "Efectivo" cuenten como distintos)
columnas_texto = df_consolidado.select_dtypes(include='object').columns
for col in columnas_texto:
    df_consolidado[col] = df_consolidado[col].str.strip()

# Reemplazamos valores vacios/nulos en metodo_pago por un texto claro
# en vez de dejarlos en NaN
df_consolidado['metodo_pago'] = df_consolidado['metodo_pago'].fillna('No especificado')

# Eliminamos filas duplicadas (por ejemplo, se detectaron 3 en Cali)
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
filas_despues = len(df_consolidado)
print(f"Duplicados eliminados: {filas_antes - filas_despues}")

print("\nDatos limpios y consolidados:")
print(df_consolidado.head())

# 6. Guardar el resultado final
df_consolidado.to_csv('ventas_consolidadas.csv', index=False)
print("\nArchivo 'ventas_consolidadas.csv' generado con exito")
