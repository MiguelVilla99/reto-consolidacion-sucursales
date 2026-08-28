# ============================================
# BOT DE VENTAS - Consolidacion, limpieza y analisis
# ============================================
import pandas as pd
import glob
import matplotlib.pyplot as plt

# --------------------------------------------
# PARTE 1: Buscar y leer los archivos
# --------------------------------------------
archivos_csv = glob.glob("datos/sucursal_*.csv")
archivos_xlsx = glob.glob("datos/sucursal_*.xlsx")
lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

# --------------------------------------------
# PARTE 2: Primer intento de consolidar
# (aqui se veria el problema de columnas distintas)
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)
# En este punto se ven mas de 7 columnas porque
# sucursal_bogota.xlsx tiene nombres distintos

# --------------------------------------------
# PARTE 3: Renombrar columnas de Bogota
# --------------------------------------------
# [IA] 'Cant' es la columna unica que solo existe en el
# archivo de Bogota; sirve para identificarlo dentro del ciclo
for i, df in enumerate(lista_informes):
    if 'Cant' in df.columns:
        lista_informes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })
        print("Columnas de Bogota renombradas correctamente")

df_consolidado = pd.concat(lista_informes, ignore_index=True)
print(df_consolidado.columns)  # ahora deberian ser exactamente 7

# --------------------------------------------
# PARTE 4: Limpieza de datos
# --------------------------------------------
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - después: {len(df_consolidado)}")

print(df_consolidado.isnull().sum())

# [IA] Quitamos espacios en blanco al inicio/final de las columnas de texto
columnas_texto = df_consolidado.select_dtypes(include='str').columns
for col in columnas_texto:
    df_consolidado[col] = df_consolidado[col].str.strip()

# Los unicos nulos que aparecen son en 'metodo_pago'; tiene sentido
# rellenarlos con un texto que indique que no quedo registrado,
# en vez de dejarlos vacios o inventar un metodo de pago
df_consolidado['metodo_pago'] = df_consolidado['metodo_pago'].fillna('No especificado')

# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# --------------------------------------------
# PARTE 6: Analisis y visualizacion
# --------------------------------------------

# 6a. EJEMPLO RESUELTO: ventas por categoria (grafico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("resultados/grafico_categoria.png")
plt.show()

# 6b. EJEMPLO RESUELTO: participacion por vendedor (grafico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')
plt.ylabel('')
plt.tight_layout()
plt.savefig("resultados/grafico_vendedor.png")
plt.show()

# 6c. Producto que mas veces aparece en las ventas
# value_counts() cuenta cuantas veces se repite cada valor unico
# en la columna y los ordena de mayor a menor automaticamente
producto_mas_vendido = df_consolidado['producto'].value_counts()
print("\nProductos por numero de veces vendido:")
print(producto_mas_vendido)
print(f"\nEl producto mas vendido (en cantidad de ventas) es: {producto_mas_vendido.index[0]} "
      f"con {producto_mas_vendido.iloc[0]} ventas")

# Conclusion: "Jean clasico" y "Cargador USB-C" son los productos que mas
# aparecen en las ventas (10 veces cada uno). Esto ayuda a identificar
# que productos mantener siempre bien abastecidos en las sucursales.