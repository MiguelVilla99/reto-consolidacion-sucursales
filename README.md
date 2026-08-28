# Bot de Ventas — Consolidación y Análisis

Proyecto que consolida los reportes de ventas de 4 sucursales
(Medellín, Bogotá, Cali y Barranquilla), limpia los datos y genera
un análisis con gráficos.

## Estructura del proyecto
bot-ventas/
├── datos/ # Archivos originales de cada sucursal
├── resultados/ # Consolidado limpio y gráficos generados
├── main.py # Script principal
└── README.md


## ¿Qué hace el script?

1. Lee los 4 archivos de la carpeta `datos/` (2 CSV, 2 XLSX).
2. Detecta que el archivo de Bogotá trae columnas con nombres distintos
   (`Fecha_Venta`, `Cant`, `Valor_Unitario`, etc.) y las renombra para
   que coincidan con las de las demás sucursales.
3. Consolida los 4 archivos en un solo DataFrame de 7 columnas.
4. Limpia los datos: elimina duplicados y espacios en blanco, y
   completa los valores vacíos de método de pago.
5. Genera un análisis con gráficos y guarda todo en `resultados/`.

## Resultados

- Filas totales antes de limpiar: **66**
- Duplicados eliminados: **3**
- Filas finales consolidadas: **63**

### Ventas por categoría

| Categoría   | Total ventas |
|-------------|--------------|
| Electrónica | $3,265,600   |
| Ropa        | $2,495,000   |

### Ventas por vendedor

| Vendedor       | Total ventas |
|----------------|--------------|
| Camila Ruiz    | $1,696,600   |
| Andres Gomez   | $1,323,600   |
| Sofia Mena     | $1,322,300   |
| Felipe Torres  | $651,200     |
| Laura Diaz     | $580,200     |

### Producto más vendido

El producto que más veces aparece en las ventas es **Jean clasico**,
con **10 ventas**, empatado con **Cargador USB-C** (también 10 ventas).

## Cómo correr el proyecto

```bash
pip install pandas openpyxl matplotlib
python main.py
```

Los resultados (Excel consolidado y gráficos) se guardan automáticamente
en la carpeta `resultados/`.

