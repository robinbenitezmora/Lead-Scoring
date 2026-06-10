import json

with open(r'c:\Users\robin\dev\01_LEADSCORING\03_notebooks\01_Importacion_Datos.ipynb', 'r') as f:
    notebook = json.load(f)

# Eliminar celdas desde la 22 (índice 21) hasta el final
notebook['cells'] = notebook['cells'][:21]

# Crear celdas nuevas y funcionales
nuevas_celdas = [
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# VALIDACIÓN FINAL DEL DATASET\n",
            "print('='*80)\n",
            "print('VALIDACIÓN FINAL')\n",
            "print('='*80)\n",
            "\n",
            "print(f'\\nDIMENSIONES DEL DATASET:')\n",
            "print(f'   Registros: {len(df_leads):,}')\n",
            "print(f'   Columnas: {df_leads.shape[1]}')\n",
            "\n",
            "print(f'\\nVALORES NULOS:')\n",
            "nulos = df_leads.isnull().sum()\n",
            "if (nulos == 0).all():\n",
            "    print('   NO hay valores nulos')\n",
            "else:\n",
            "    print('   Columnas con nulos:')\n",
            "    print(nulos[nulos > 0])\n",
            "\n",
            "print(f'\\nTIPOS DE DATOS:')\n",
            "print(df_leads.dtypes)\n",
            "\n",
            "print(f'\\nESTADÍSTICAS BÁSICAS:')\n",
            "print(df_leads.describe())"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ANÁLISIS UNIVARIANTE: VARIABLES NUMÉRICAS\n",
            "import numpy as np\n",
            "\n",
            "print('\\n' + '='*80)\n",
            "print('ANÁLISIS UNIVARIANTE: VARIABLES NUMÉRICAS')\n",
            "print('='*80)\n",
            "\n",
            "numeric_cols = df_leads.select_dtypes(include=[np.number]).columns.tolist()\n",
            "print(f'\\nVariables numéricas: {len(numeric_cols)}')\n",
            "print(numeric_cols)\n",
            "\n",
            "for col in numeric_cols:\n",
            "    data = df_leads[col]\n",
            "    print(f'\\n{col}:')\n",
            "    print(f'  Media: {data.mean():.4f}')\n",
            "    print(f'  Mediana: {data.median():.4f}')\n",
            "    print(f'  Desv. Est: {data.std():.4f}')\n",
            "    print(f'  Min: {data.min():.4f}')\n",
            "    print(f'  Max: {data.max():.4f}')"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ANÁLISIS UNIVARIANTE: VARIABLES CATEGÓRICAS\n",
            "print('\\n' + '='*80)\n",
            "print('ANÁLISIS UNIVARIANTE: VARIABLES CATEGÓRICAS')\n",
            "print('='*80)\n",
            "\n",
            "cat_cols = df_leads.select_dtypes(include=['object']).columns.tolist()\n",
            "print(f'\\nVariables categóricas: {len(cat_cols)}')\n",
            "print(cat_cols)\n",
            "\n",
            "for col in cat_cols:\n",
            "    data = df_leads[col]\n",
            "    print(f'\\n{col}:')\n",
            "    print(f'  Valores únicos: {data.nunique()}')\n",
            "    print(f'  Top 5:')\n",
            "    for val, count in data.value_counts().head(5).items():\n",
            "        pct = (count / len(df_leads) * 100)\n",
            "        print(f'    {val}: {count} ({pct:.2f}%)')"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ANÁLISIS BIVARIANTE: CORRELACIÓN CON OBJETIVO\n",
            "print('\\n' + '='*80)\n",
            "print('ANÁLISIS BIVARIANTE: CORRELACIÓN CON COMPRA')\n",
            "print('='*80)\n",
            "\n",
            "target = 'compra'\n",
            "print(f'\\nDistribución de {target}:')\n",
            "print(df_leads[target].value_counts())\n",
            "\n",
            "numeric_cols_sin_id = [col for col in numeric_cols if col != 'id']\n",
            "print(f'\\nCORRELACIÓN CON COMPRA:')\n",
            "for col in numeric_cols_sin_id:\n",
            "    corr = df_leads[[target, col]].corr().iloc[0, 1]\n",
            "    print(f'  {col:25s}: {corr:+.4f}')"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# RESUMEN FINAL\n",
            "print('\\n' + '='*80)\n",
            "print('RESUMEN FINAL: EDA COMPLETADO')\n",
            "print('='*80)\n",
            "\n",
            "print(f'\\nDATASET CARACTERIZADO:')\n",
            "print(f'  Registros: {len(df_leads):,}')\n",
            "print(f'  Variables: {df_leads.shape[1]}')\n",
            "print(f'  Valores nulos: {df_leads.isnull().sum().sum()}')\n",
            "\n",
            "print(f'\\nVARIABLE OBJETIVO (COMPRA):')\n",
            "compra = df_leads['compra'].value_counts()\n",
            "print(f'  No compra: {compra[0]:,} ({(compra[0]/len(df_leads)*100):.2f}%)')\n",
            "print(f'  Compra: {compra[1]:,} ({(compra[1]/len(df_leads)*100):.2f}%)')\n",
            "\n",
            "print(f'\\nPRÓXIMOS PASOS:')\n",
            "print(f'  1. Feature engineering')\n",
            "print(f'  2. Modelización')\n",
            "print(f'  3. Evaluación')\n",
            "\n",
            "print('\\n' + '='*80)"
        ]
    }
]

# Agregar las nuevas celdas
for celda in nuevas_celdas:
    notebook['cells'].append(celda)

# Guardar
with open(r'c:\Users\robin\dev\01_LEADSCORING\03_notebooks\01_Importacion_Datos.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("✓ Notebook replanteado")
print(f"✓ Total de celdas: {len(notebook['cells'])}")
