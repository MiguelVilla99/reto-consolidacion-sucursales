# ============================================
# AUTOMATIZACION - Bot de Ventas
# Este script vigila la carpeta "datos/" y cuando detecta
# un archivo nuevo, procesa todo automaticamente:
# lee, corrige columnas, consolida, limpia, analiza
# y guarda un registro (log) del proceso.
# ============================================
import time
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

ruta_datos = "datos/"
# [IA] Guardamos una "foto" de los archivos que ya existen al iniciar,
# para poder comparar despues y detectar solo los que se agreguen nuevos
archivos_vistos = set(os.listdir(ruta_datos))


def procesar_todo(archivo_nuevo):
    """
    Lee todos los archivos de sucursales en datos/, corrige las
    columnas del archivo de Bogota, consolida todo, limpia
    duplicados y espacios, genera los graficos y guarda un log
    del proceso.
    """
    archivos_csv = glob.glob("datos/sucursal_*.csv")
    archivos_xlsx = glob.glob("datos/sucursal_*.xlsx")
    lista_informes = []

    for archivo in archivos_csv:
        lista_informes.append(pd.read_csv(archivo))
    for archivo in archivos_xlsx:
        lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))

    # Correccion de columnas del archivo de Bogota (igual que en main.py)
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

    df_consolidado = pd.concat(lista_informes, ignore_index=True)

    # Limpieza: duplicados, espacios en blanco y nulos
    df_consolidado = df_consolidado.drop_duplicates()
    columnas_texto = df_consolidado.select_dtypes(include='str').columns
    for col in columnas_texto:
        df_consolidado[col] = df_consolidado[col].str.strip()
    df_consolidado['metodo_pago'] = df_consolidado['metodo_pago'].fillna('No especificado')

    df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)

    # Grafico de ventas por categoria
    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoria')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales (COP)')
    plt.tight_layout()
    plt.savefig("resultados/grafico_categoria.png")
    plt.close()

    # Grafico de participacion por vendedor
    ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
    ventas_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("resultados/grafico_vendedor.png")
    plt.close()

    # Registro (log) del proceso: queda historial de cada vez que se ejecuta
    with open("resultados/log_automatizacion.txt", "a") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo detectado: {archivo_nuevo}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write("---\n")

    print("Proceso completado - archivos actualizados en resultados/")


print("Monitoreando carpeta 'datos/'... (Ctrl+C para detener)")
while True:
    archivos_actuales = set(os.listdir(ruta_datos))
    archivos_nuevos = archivos_actuales - archivos_vistos

    if archivos_nuevos:
        print(f"Nuevo archivo detectado: {archivos_nuevos}")
        procesar_todo(archivos_nuevos)
        archivos_vistos = archivos_actuales

    time.sleep(5)