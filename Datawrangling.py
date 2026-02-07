"""
Data Wrangling - E-commerce
Objetivo: limpiar, transformar y enriquecer un dataset de e-commerce usando Pandas.
Pasos:
1) Cargar datos
2) Inspección inicial
3) Limpieza: nulos, duplicados, estandarización de texto
4) Conversión de tipos (precio, cantidad, fechas)
5) Enriquecimiento: columnas nuevas (total, iva, etc.)
6) Discretización (binning)
7) Guardar dataset final
"""

import pandas as pd


# -----------------------------
# 1) CARGA DE DATOS
# -----------------------------

df = pd.read_csv("data.csv", encoding="latin1")

print("\n✅ Dataset cargado")
print("Filas, columnas:", df.shape)


# -----------------------------
# 2) INSPECCIÓN INICIAL
# -----------------------------
print("\n--- Vista rápida (head) ---")
print(df.head())

print("\n--- Info (tipos y nulos) ---")
print(df.info())

print("\n--- Nulos por columna ---")
print(df.isna().sum().sort_values(ascending=False))

print("\n--- Duplicados (filas repetidas completas) ---")
print(df.duplicated().sum())


# -----------------------------
# 3) LIMPIEZA BÁSICA
# -----------------------------
# 3.1) Quitar duplicados (si existen)
antes = df.shape[0]
df = df.drop_duplicates()
despues = df.shape[0]
print(f"\n🧹 Duplicados eliminados: {antes - despues}")

# 3.2) Normalizar texto en columnas tipo string (si aplica)
# Tip: esto ayuda a unificar categorías como "Laptop" vs "laptop"
columnas_texto = df.select_dtypes(include="object").columns
for col in columnas_texto:
    df[col] = df[col].astype(str).str.strip()

# (Opcional) Pasar a minúsculas en columnas de categoría/producto si lo ves útil:
# for col in ["product", "category"]:
#     if col in df.columns:
#         df[col] = df[col].str.lower()


# -----------------------------
# 4) CONVERSIÓN DE TIPOS
# -----------------------------
# Ajusta estos nombres a los de TU dataset cuando los veas en df.columns
# Ejemplos típicos: "price", "quantity", "order_date"

# 4.1) Precio a numérico
if "price" in df.columns:
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 4.2) Cantidad a numérico
if "quantity" in df.columns:
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# 4.3) Fecha a datetime
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

print("\n✅ Conversión de tipos completada (con errores->NaN si había valores raros).")
print(df[["price", "quantity"]].head() if all(c in df.columns for c in ["price", "quantity"]) else "Columnas price/quantity no encontradas")


# -----------------------------
# 5) MANEJO DE NULOS (EJEMPLOS)
# -----------------------------
# Estrategias comunes:
# A) eliminar filas con nulos en campos clave
# B) imputar (rellenar) con 0 u otra estadística

campos_clave = [c for c in ["price", "quantity", "order_date"] if c in df.columns]
if campos_clave:
    antes = df.shape[0]
    df = df.dropna(subset=campos_clave)
    despues = df.shape[0]
    print(f"\n🧩 Filas eliminadas por nulos en {campos_clave}: {antes - despues}")

# Si hay columnas numéricas con nulos que quieras rellenar:
# df["discount"] = df["discount"].fillna(0)


# -----------------------------
# 6) ENRIQUECIMIENTO DE DATOS
# -----------------------------
# 6.1) total_compra = price * quantity
if all(c in df.columns for c in ["price", "quantity"]):
    df["total_compra"] = df["price"] * df["quantity"]

# 6.2) IVA (ejemplo 21%) -
IVA = 0.21
if "total_compra" in df.columns:
    df["total_con_iva"] = df["total_compra"] * (1 + IVA)

print("\n✨ Enriquecimiento listo (si existían columnas necesarias).")
print(df.head())


# -----------------------------
# 7) DISCRETIZACIÓN (BINNING)
# -----------------------------
# Ejemplo: categorizar total_compra en rangos
if "total_compra" in df.columns:
    bins = [-1, 50, 200, 500, float("inf")]
    etiquetas = ["baja", "media", "alta", "muy_alta"]
    df["segmento_compra"] = pd.cut(df["total_compra"], bins=bins, labels=etiquetas)

    print("\n📦 Segmento de compra creado (binning).")
    print(df["segmento_compra"].value_counts(dropna=False))


# -----------------------------
# 8) GUARDAR RESULTADO
# -----------------------------
SALIDA = "ecommerce_wrangled.csv"
df.to_csv(SALIDA, index=False)
print(f"\n💾 Archivo final guardado: {SALIDA}")
print("Filas, columnas finales:", df.shape)