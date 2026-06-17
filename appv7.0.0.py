import base64
import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# ==========================================
# CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
# ==========================================
st.set_page_config(page_title="Itera Studio", layout="wide")

# ==========================================
# INYECCIÓN DE IMAGEN DE FONDO
# ==========================================
def agregar_fondo_local(ruta_imagen):
    with open(ruta_imagen, "rb") as archivo_imagen:
        imagen_codificada = base64.b64encode(archivo_imagen.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{imagen_codificada}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Llama a la función con el nombre exacto de tu archivo de imagen
agregar_fondo_local("mikurescaled.jpeg")

# ==========================================
# GESTIÓN DE ACCIONES Y PARÁMETROS DE URL
# ==========================================
params = st.query_params

if "action" in params:
    action = params["action"]
    if action == "reload":
        del st.query_params["action"]
        st.rerun()
    elif action == "reset":
        st.session_state.clear()
        del st.query_params["action"]
        st.rerun()
    elif action == "tutorial":
        st.session_state["show_tutorial"] = True
        del st.query_params["action"]
        st.rerun()
    elif action == "expert":
        st.session_state["expert_mode"] = not st.session_state.get("expert_mode", False)
        del st.query_params["action"]
        st.rerun()
    elif action == "close_tut":
        st.session_state["show_tutorial"] = False
        del st.query_params["action"]
        st.rerun()

# Idioma
if "lang" in params and params["lang"].lower() == "en":
    idioma_seleccionado = "ENGLISH"
else:
    idioma_seleccionado = "ESPAÑOL"

# ==========================================
# DICCIONARIO DE IDIOMAS 
# ==========================================
LANG = {
    "ESPAÑOL": {
        "TITLE": "ITERA STUDIO",
        "TAB1": "SOLUCIÓN DE ECUACIONES",
        "TAB2": "REGRESIÓN E INTERPOLACIÓN",
        "TAB_INFO": "INFORMACIÓN",
        "TAB_HELP": "AYUDA",
        "TAB_EXAMPLES": "EJEMPLOS",
        "PARAMS": "PARÁMETROS",
        "F_MAIN": "Función principal f(x):",
        "F_DESP": "Función despejada g(x) *(Para Punto Fijo)*:",
        "WAIT_FUNC": "Esperando una función válida...",
        "SHOW_F": "MOSTRAR GRÁFICA f(x)",
        "SHOW_G": "MOSTRAR GRÁFICA g(x)",
        "LIM_INF": "Límite inferior xₗ *(o x_ant)*",
        "LIM_SUP": "Límite superior xᵤ *(o x_act)*",
        "PTO_INI": "Punto inicial x₀",
        "TOL": "Tolerancia ε",
        "CALC_BTN": "CALCULAR RAÍCES",
        "RES_TITLE": "RESULTADOS E ITERACIONES",
        "COMP_GRAPH": "VER GRÁFICA COMPARATIVA DE RAÍCES",
        "NO_ROOTS": "No se encontraron raíces válidas para graficar.",
        "ERR_SYNTAX": "ERROR en la sintaxis de las funciones o división por cero detectada. Revisa los datos ingresados.",
        "INFO_START_ROOTS": "INGRESA LOS PARÁMETROS A LA IZQUIERDA Y PRESIONA 'CALCULAR RAÍCES'.",
        "INFO_START_REG": "INGRESA LOS DATOS A LA IZQUIERDA Y PRESIONA EL BOTÓN DE CÁLCULO.",
        "INFO_START_DERIV": "INGRESA LOS PARÁMETROS A LA IZQUIERDA Y PRESIONA 'CALCULAR DERIVADAS'.",
        "INFO_START_INTG": "INGRESA LOS PARÁMETROS A LA IZQUIERDA Y PRESIONA 'CALCULAR ÁREA'.",
        "INFO_START_ODE": "INGRESA LOS PARÁMETROS A LA IZQUIERDA Y PRESIONA 'RESOLVER EDO'.",
        "CONSTRUCTION": "MÓDULO EN CONSTRUCCIÓN.",
        "ERR_OPPOSITE": "ERROR: f(xₗ) y f(xᵤ) no tienen signos opuestos.",
        "ERR_EVAL": "ERROR: Fallo al evaluar los límites en la función.",
        "ERR_DIV0": "ERROR: División por cero durante el cálculo.",
        "ERR_DIV0_FAIL": "ERROR: División por cero. El método falla.",
        "ERR_CONVERGE": "ERROR: El método no converge después de 100 iteraciones.",
        "ERR_DIVERGE": "ERROR: El método diverge con este despeje o punto inicial x₀.",
        "ROOT_APPROX": "Raíz Aproximada",
        "ITERS": "Iteraciones",
        "METH_BIS": "BISECCIÓN",
        "METH_FP": "FALSA POSICIÓN",
        "METH_NR": "NEWTON-RAPHSON",
        "METH_SEC": "SECANTE",
        "METH_PF": "PUNTO FIJO",
        "COL_ITER": "Iteración",
        "COL_XL": "xₗ",
        "COL_XU": "xᵤ",
        "COL_XR": "xᵣ",
        "COL_XI": "xᵢ",
        "COL_XSIG": "xᵢ₊₁",
        "COL_ERR": "Error Absoluto",
        "CURVE_F": "Curva f(x) y Puntos Encontrados",
        "AXIS_X": "EJE X",
        "AXIS_Y": "EJE Y",
        "INFO_TEXT": "Somos estudiantes de la Universidad Veracruzana y desarrolladmos esta herramienta interactiva que te permite explorar los métodos numéricos clásicos aplicados a la ingeniería y ciencias exactas. No solo calcula raíces de ecuaciones, sino que también abarca regresión, interpolación, derivación, integración y ecuaciones diferenciales ordinarias (E.D.O.). El objetivo es que puedas comparar la precisión, velocidad y comportamiento de cada algoritmo mediante visualizaciones claras y tablas iterativas.",
        "HELP_SYNTAX": "### SINTAXIS DE FUNCIONES\nLa calculadora interpreta texto natural matemático. Puedes usar:\n* **Potencias:** `x^2` o `x**2`\n* **Multiplicación implícita:** `2x` se interpreta automáticamente como `2*x`\n* **Fracciones:** `(x+1)/2`\n* **Funciones trigonométricas:** `sin(x)`, `cos(x)`, `tan(x)`\n* **Exponenciales y logaritmos:** `exp(x)` para e^x, `log(x)` para el logaritmo natural.\n* **Múltiples variables:** Para las E.D.O., puedes usar `x` e y juntas (ej. `x + 2y` o `x*y`).",
        "HELP_PARAMS": "### PARÁMETROS PRINCIPALES\n**Módulo de Raíces:**\n* **xₗ y xᵤ:** Límites que encierran la raíz (Bisección y Falsa Posición).\n* **x₀:** Valor inicial de búsqueda (Newton-Raphson y Punto Fijo).\n* **ε:** Tolerancia. El cálculo se detiene cuando el error es menor a este valor.\n\n**Otros Módulos:**\n* **P₀ y P₁ / Puntos (x,y):** Coordenadas base para trazar los ajustes de regresión o interpolación.\n* **h:** Tamaño de paso utilizado para el cálculo de Derivadas y E.D.O.\n* **a y b:** Límites inferior y superior para delimitar el área de Integración.\n* **n:** Número de intervalos o particiones para los métodos de Integración.",
        "EX_1_TITLE": "Ejemplo 1: Polinomio Algebraico",
        "EX_2_TITLE": "Ejemplo 2: Ecuación Trascendente",
        "EX_3_TITLE": "Ejemplo 3: Convergencia de Punto Fijo",
        "REG_TITLE": "REGRESIÓN LINEAL (MÍNIMOS CUADRADOS)",
        "REG_DATA": "Ingreso de Datos",
        "REG_ADD_DEL": "Haz doble clic para editar. Puedes agregar o eliminar filas en la última celda.",
        "CALC_REG_BTN": "CALCULAR AJUSTE LINEAL",
        "REG_RES": "Resultados de la Regresión",
        "MODEL_EQ": "Ecuación del Modelo:",
        "COEF_CORR": "Coeficiente de Correlación (r)",
        "COEF_DET": "Coeficiente de Determinación (R²)",
        "GRAPH_REG": "Gráfica de Ajuste",
        "ERR_DATA": "ERROR: Por favor ingresa al menos 2 puntos de datos válidos.",
        "METHOD_LS": "Mínimos Cuadrados",
        "METHOD_NEWTON_LIN": "Interpolación Lineal (Newton)",
        "INT_TITLE": "INTERPOLACIÓN LINEAL DE NEWTON",
        "P0_LABEL": "Punto Inicial P₀",
        "P1_LABEL": "Punto Final P₁",
        "INT_X_VAL": "Valor a interpolar x:",
        "CALC_INT_BTN": "CALCULAR INTERPOLACIÓN",
        "INT_RES": "Resultado de la Interpolación",
        "INT_EQ": "Sustitución en la fórmula:",
        "ERR_X_EQUAL": "ERROR: x₀ y x₁ no pueden ser iguales (división por cero).",
        "METHOD_LAGRANGE": "Interpolación (Lagrange)",
        "LAG_TITLE": "INTERPOLACIÓN POLINOMIAL DE LAGRANGE",
        "LAG_DATA": "Puntos Conocidos (x, y)",
        "LAG_ADD_DEL": "Agrega tantos puntos como necesites. No repitas valores de X.",
        "LAG_X_VAL": "Valor a interpolar x:",
        "CALC_LAG_BTN": "CALCULAR POLINOMIO",
        "LAG_RES": "Resultado de Lagrange",
        "LAG_POLY": "Polinomio Evaluado:",
        "ERR_DUP_X": "ERROR: Hay valores de X repetidos. Esto causa división por cero en Lagrange.",
        "TAB3": "DERIVACIÓN NUMÉRICA",
        "DF_TITLE": "DIFERENCIAS FINITAS (1ra Derivada)",
        "DF_X": "Punto a evaluar xᵢ:",
        "DF_H": "Tamaño de paso h:",
        "CALC_DF_BTN": "CALCULAR DERIVADAS",
        "DF_RES": "Resultados de Aproximación",
        "ERR_H_ZERO": "ERROR: El tamaño de paso h no puede ser cero.",
        "TAB4": "INTEGRACIÓN NUMÉRICA",
        "INTG_TITLE": "MÉTODO DEL TRAPECIO",
        "INTG_METHOD": "Selecciona la variante:",
        "TRAP_SIMPLE": "Trapecio Simple",
        "TRAP_MULTIPLE": "Trapecio Múltiple",
        "INTG_A": "Límite inferior a:",
        "INTG_B": "Límite superior b:",
        "INTG_N": "Número de intervalos n:",
        "CALC_INTG_BTN": "CALCULAR ÁREA",
        "INTG_RES": "Resultados de Integración",
        "EXACT_AREA": "Área Alta Resolución (Ref.)",
        "APPROX_AREA": "Área Aproximada",
        "ERR_LIMITS": "ERROR: El límite superior b debe ser mayor al límite inferior a.",
        "SIMPSON_METHOD": "Simpson (1/3 y 3/8)",
        "SIMP_TITLE": "MÉTODO DE SIMPSON",
        "ERR_N_SIMPSON": "ERROR: El método de Simpson requiere al menos n=2 intervalos.",
        "INFO_SIMPSON_EVEN": "Se aplicó **Simpson 1/3** en todo el rango porque n es par.",
        "INFO_SIMPSON_ODD": "Se aplicó **Simpson 1/3** al principio y **Simpson 3/8** en los últimos 3 intervalos porque n es impar.",
        "TAB5": "ECUACIONES DIFERENCIALES",
        "ODE_TITLE": "RESOLUCIÓN DE E.D.O.",
        "ODE_METHOD": "Selecciona el método:",
        "METH_EULER": "Método de Euler",
        "METH_HEUN": "Método de Heun",
        "METH_RALSTON": "Método de Ralston",
        "ODE_F": "Ecuación y' = f(x, y):",
        "ODE_X0": "Valor inicial x₀:",
        "ODE_Y0": "Condición inicial y₀:",
        "ODE_XF": "Valor final x_f:",
        "ODE_H": "Tamaño de paso h:",
        "CALC_ODE_BTN": "RESOLVER EDO",
        "ODE_RES": "Tabla de Iteraciones",
        "ODE_GRAPH": "Trayectoria de la Solución",
        "ERR_ODE_H": "ERROR: El tamaño de paso h debe ser mayor a 0 y caber en el intervalo.",
    },
    "ENGLISH": {
        "TITLE": "ITERA STUDIO",
        "TAB1": "EQUATION SOLVING",
        "TAB2": "REGRESSION & INTERPOLATION",
        "TAB_INFO": "INFO",
        "TAB_HELP": "HELP",
        "TAB_EXAMPLES": "EXAMPLES",
        "PARAMS": "PARAMETERS",
        "F_MAIN": "Main function f(x):",
        "F_DESP": "Isolated function g(x) *(For Fixed Point)*:",
        "WAIT_FUNC": "Waiting for a valid function...",
        "SHOW_F": "SHOW f(x) GRAPH",
        "SHOW_G": "SHOW g(x) GRAPH",
        "LIM_INF": "Lower limit xₗ *(or x_prev)*",
        "LIM_SUP": "Upper limit xᵤ *(or x_curr)*",
        "PTO_INI": "Initial point x₀",
        "TOL": "Tolerance ε",
        "CALC_BTN": "CALCULATE ROOTS",
        "RES_TITLE": "RESULTS & ITERATIONS",
        "COMP_GRAPH": "VIEW COMPARATIVE ROOTS GRAPH",
        "NO_ROOTS": "No valid roots found to plot.",
        "ERR_SYNTAX": "ERROR in function syntax or division by zero detected. Check the input data.",
        "INFO_START_ROOTS": "ENTER PARAMETERS ON THE LEFT AND PRESS 'CALCULATE ROOTS'.",
        "INFO_START_REG": "ENTER DATA ON THE LEFT AND PRESS THE CALCULATE BUTTON.",
        "INFO_START_DERIV": "ENTER PARAMETERS ON THE LEFT AND PRESS 'CALCULATE DERIVATIVES'.",
        "INFO_START_INTG": "ENTER PARAMETERS ON THE LEFT AND PRESS 'CALCULATE AREA'.",
        "INFO_START_ODE": "ENTER PARAMETERS ON THE LEFT AND PRESS 'SOLVE ODE'.",
        "CONSTRUCTION": "MODULE UNDER CONSTRUCTION.",
        "ERR_OPPOSITE": "ERROR: f(xₗ) and f(xᵤ) do not have opposite signs.",
        "ERR_EVAL": "ERROR: Failed to evaluate limits in the function.",
        "ERR_DIV0": "ERROR: Division by zero during calculation.",
        "ERR_DIV0_FAIL": "ERROR: Division by zero. Method fails.",
        "ERR_CONVERGE": "ERROR: Method does not converge after 100 iterations.",
        "ERR_DIVERGE": "ERROR: Method diverges with this function or initial point x₀.",
        "ROOT_APPROX": "Approximate Root",
        "ITERS": "Iterations",
        "METH_BIS": "BISECTION",
        "METH_FP": "FALSE POSITION",
        "METH_NR": "NEWTON-RAPHSON",
        "METH_SEC": "SECANT",
        "METH_PF": "FIXED POINT",
        "COL_ITER": "Iteration",
        "COL_XL": "xₗ",
        "COL_XU": "xᵤ",
        "COL_XR": "xᵣ",
        "COL_XI": "xᵢ",
        "COL_XSIG": "xᵢ₊₁",
        "COL_ERR": "Absolute Error",
        "CURVE_F": "Curve f(x) and Found Points",
        "AXIS_X": "X AXIS",
        "AXIS_Y": "Y AXIS",
        "INFO_TEXT": "We are students at the University of Veracruz and we developed this interactive tool that allows you to explore classical numerical methods applied to engineering and the exact sciences. It not only calculates roots of equations, but also covers regression, interpolation, differentiation, integration, and ordinary differential equations (ODEs). The goal is for you to be able to compare the accuracy, speed, and behavior of each algorithm through clear visualizations and iterative tables.",
        "HELP_SYNTAX": "### FUNCTION SYNTAX\nThe calculator interprets natural mathematical text. You can use:\n* **Powers:** `x^2` or `x**2`\n* **Implicit multiplication:** `2x` is automatically parsed as `2*x`\n* **Fractions:** `(x+1)/2`\n* **Trigonometric functions:** `sin(x)`, `cos(x)`, `tan(x)`\n* **Exponentials and logarithms:** `exp(x)` for e^x, `log(x)` for natural logarithm.\n* **Multiple variables:** For ODEs, you can use `x` and `y` together (e.g. `x + 2y` or `x*y`).",
        "HELP_PARAMS": "### MAIN PARAMETERS\n**Roots Module:**\n* **xₗ and xᵤ:** Limits that enclose the root (Bisection and False Position).\n* **x₀:** Initial search value (Newton-Raphson and Fixed Point).\n* **ε:** Tolerance. Calculation stops when the error is less than this value.\n\n**Other Modules:**\n* **P₀ and P₁ / Points (x,y):** Base coordinates to draw regression or interpolation fits.\n* **h:** Step size used for Derivatives and ODE calculations.\n* **a and b:** Lower and upper limits to bound the Integration area.\n* **n:** Number of intervals or partitions for Integration methods.",
        "EX_1_TITLE": "Example 1: Algebraic Polynomial",
        "EX_2_TITLE": "Example 2: Transcendental Equation",
        "EX_3_TITLE": "Example 3: Fixed Point Convergence",
        "REG_TITLE": "LINEAR REGRESSION (LEAST SQUARES)",
        "REG_DATA": "Data Input",
        "REG_ADD_DEL": "Double click to edit. You can add or delete rows at the bottom.",
        "CALC_REG_BTN": "CALCULATE LINEAR FIT",
        "REG_RES": "Regression Results",
        "MODEL_EQ": "Model Equation:",
        "COEF_CORR": "Correlation Coefficient (r)",
        "COEF_DET": "Coefficient of Determination (R²)",
        "GRAPH_REG": "Fit Graph",
        "ERR_DATA": "ERROR: Please enter at least 2 valid data points.",
        "METHOD_LS": "Least Squares",
        "METHOD_NEWTON_LIN": "Linear Interpolation (Newton)",
        "INT_TITLE": "NEWTON'S LINEAR INTERPOLATION",
        "P0_LABEL": "Initial Point P₀",
        "P1_LABEL": "Final Point P₁",
        "INT_X_VAL": "Value to interpolate x:",
        "CALC_INT_BTN": "CALCULATE INTERPOLATION",
        "INT_RES": "Interpolation Result",
        "INT_EQ": "Formula substitution:",
        "ERR_X_EQUAL": "ERROR: x₀ and x₁ cannot be equal (division by zero).",
        "METHOD_LAGRANGE": "Interpolation (Lagrange)",
        "LAG_TITLE": "LAGRANGE POLYNOMIAL INTERPOLATION",
        "LAG_DATA": "Known Points (x, y)",
        "LAG_ADD_DEL": "Add as many points as needed. Do not repeat X values.",
        "LAG_X_VAL": "Value to interpolate x:",
        "CALC_LAG_BTN": "CALCULATE POLYNOMIAL",
        "LAG_RES": "Lagrange Result",
        "LAG_POLY": "Evaluated Polynomial:",
        "ERR_DUP_X": "ERROR: Duplicate X values found. This causes division by zero in Lagrange.",
        "TAB3": "NUMERICAL DIFFERENTIATION",
        "DF_TITLE": "FINITE DIFFERENCES (1st Derivative)",
        "DF_X": "Evaluation point xᵢ:",
        "DF_H": "Step size h:",
        "CALC_DF_BTN": "CALCULATE DERIVATIVES",
        "DF_RES": "Approximation Results",
        "ERR_H_ZERO": "ERROR: Step size h cannot be zero.",
        "TAB4": "NUMERICAL INTEGRATION",
        "INTG_TITLE": "TRAPEZOIDAL RULE",
        "INTG_METHOD": "Select variant:",
        "TRAP_SIMPLE": "Single Trapezoid",
        "TRAP_MULTIPLE": "Multiple Trapezoids",
        "INTG_A": "Lower limit a:",
        "INTG_B": "Upper limit b:",
        "INTG_N": "Number of intervals n:",
        "CALC_INTG_BTN": "CALCULATE AREA",
        "INTG_RES": "Integration Results",
        "EXACT_AREA": "High-Res Area (Reference)",
        "APPROX_AREA": "Approximate Area",
        "ERR_LIMITS": "ERROR: Upper limit b must be greater than lower limit a.",
        "SIMPSON_METHOD": "Simpson (1/3 & 3/8)",
        "SIMP_TITLE": "SIMPSON'S RULE",
        "ERR_N_SIMPSON": "ERROR: Simpson's rule requires at least n=2 intervals.",
        "INFO_SIMPSON_EVEN": "Applied **Simpson 1/3** over the entire range because n is even.",
        "INFO_SIMPSON_ODD": "Applied **Simpson 1/3** initially and **Simpson 3/8** on the last 3 intervals because n is odd.",
        "TAB5": "DIFFERENTIAL EQUATIONS",
        "ODE_TITLE": "O.D.E. SOLVER",
        "ODE_METHOD": "Select method:",
        "METH_EULER": "Euler's Method",
        "METH_HEUN": "Heun's Method",
        "METH_RALSTON": "Ralston's Method",
        "ODE_F": "Equation y' = f(x, y):",
        "ODE_X0": "Initial value x₀:",
        "ODE_Y0": "Initial condition y₀:",
        "ODE_XF": "Final value x_f:",
        "ODE_H": "Step size h:",
        "CALC_ODE_BTN": "SOLVE ODE",
        "ODE_RES": "Iteration Table",
        "ODE_GRAPH": "Solution Trajectory",
        "ERR_ODE_H": "ERROR: Step size h must be greater than 0 and fit within the interval."
    }
}

t = LANG[idioma_seleccionado]

# ==========================================
# CONFIGURACIÓN DE ESTILOS CSS BASE
# ==========================================
st.markdown("""
<style>
    .block-container {
        padding-top: 4.5rem !important; 
        padding-bottom: 1rem !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
    @import url('https://fonts.cdnfonts.com/css/samsung-sharp-sans');
    html, body, p, h1, h2, h3, h4, h5, h6, li, label, input, button {
        font-family: 'Samsung Sharp Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    span.material-symbols-rounded, span[class*="material"], [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    }
    .katex, .katex *, .katex-display * {
        font-family: KaTeX_Math, 'KaTeX_Main', serif !important;
    }
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {
        display: none !important;
    }
    h1 {
        text-align: center !important;
        font-weight: 700 !important;
        margin-bottom: 0.2rem !important;
        padding-top: 1rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: flex; justify-content: center; gap: 35px;
        background-color: transparent; border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        padding-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto !important; padding: 12px 0px !important;
        background-color: transparent !important; border: none !important;
        transition: all 0.2s ease-in-out; font-weight: 600; font-size: 0.85rem !important;
        color: #424245 !important; letter-spacing: 0.5px;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #000000 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #000000 !important; border-bottom: 2px solid #000000 !important; font-weight: 700 !important;
    }
    @media (prefers-color-scheme: dark) {
        .stTabs [data-baseweb="tab"] { color: #a1a1a6 !important; }
        .stTabs [data-baseweb="tab"]:hover { color: #ffffff !important; }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important; border-bottom: 2px solid #ffffff !important;
        }
    }
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important; transition: all 0.3s ease;
        border: 1px solid rgba(128, 128, 128, 0.3); background-color: rgba(128, 128, 128, 0.05);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #7c6dd9; box-shadow: 0 4px 10px rgba(124, 109, 217, 0.2);
    }
    div[data-testid="stNumberInputContainer"] { border-radius: 10px !important; overflow: hidden; }
    div[data-testid="stNumberInput"] button:first-of-type { color: #ff4d4d !important; transition: all 0.2s ease; }
    div[data-testid="stNumberInput"] button:first-of-type svg { fill: #ff4d4d !important; }
    div[data-testid="stNumberInput"] button:first-of-type:hover { background-color: rgba(255, 77, 77, 0.15) !important; color: #ff1a1a !important; }
    div[data-testid="stNumberInput"] button:first-of-type:hover svg { fill: #ff1a1a !important; }
    div[data-testid="stNumberInput"] button:last-of-type { color: #00cc66 !important; transition: all 0.2s ease; }
    div[data-testid="stNumberInput"] button:last-of-type svg { fill: #00cc66 !important; }
    div[data-testid="stNumberInput"] button:last-of-type:hover { background-color: rgba(0, 204, 102, 0.15) !important; color: #00994d !important; }
    div[data-testid="stNumberInput"] button:last-of-type:hover svg { fill: #00994d !important; }
    div[data-testid="stButton"] button {
        border-radius: 15px; background-color: #7c6dd9; color: white;
        font-weight: bold; transition: all 0.3s ease; border: none; padding: 10px 20px;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #5a4eb3; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(124, 109, 217, 0.4);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.05); padding: 15px; border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
    .math-preview { padding: 10px 0px; margin-bottom: 5px; display: flex; justify-content: center; }
    div[data-testid="stExpander"] details summary {
        background-color: #7c6dd9 !important; color: #000000 !important; border-radius: 8px; font-weight: 600;
    }
    div[data-testid="stExpander"] details summary:hover { background-color: #5a4eb3 !important; }
    div[data-testid="stExpander"] details summary p { font-family: 'Samsung Sharp Sans', -apple-system, sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA SUPERIOR 100% NATIVA EN PYTHON (Sin JavaScript)
# ==========================================
st.markdown("""
<style>
.steam-top-bar {
    position: fixed; top: 0; left: 0; width: 100%; height: 40px;
    background-color: #171d25; color: #b8b6b4; display: flex; align-items: center;
    padding: 0 15px; z-index: 999999; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 13px; box-shadow: 0 1px 4px rgba(0,0,0,0.4);
}
.steam-logo { font-weight: 700; color: #c7d5e0; margin-right: 25px; font-size: 14px; letter-spacing: 0.5px; }
.steam-menu { display: flex; gap: 5px; }
.steam-menu-item { cursor: pointer; padding: 5px 12px; border-radius: 3px; position: relative; transition: background 0.2s, color 0.2s; }
.steam-menu-item:hover { background-color: #2a475e; color: #ffffff; }
.steam-dropdown {
    display: none; position: absolute; top: 100%; left: 0; background-color: #171d25;
    min-width: 180px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.6); z-index: 1;
    border-radius: 0 0 4px 4px; overflow: hidden;
}
.steam-menu-item:hover .steam-dropdown { display: block; }
.steam-dropdown a {
    color: #b8b6b4; padding: 10px 15px; text-decoration: none; display: block;
    border-bottom: 1px solid rgba(255,255,255,0.03); transition: background 0.2s;
}
.steam-dropdown a:hover { background-color: #2a475e; color: #ffffff; }
.steam-right { margin-left: auto; display: flex; align-items: center; }
.hamburguesa { font-size: 16px; font-weight: 800; margin-right: 15px; }
</style>

<div class="steam-top-bar">
    <div class="steam-menu">
        <div class="steam-menu-item hamburguesa">&#9776;
            <div class="steam-dropdown">
                <a href="?lang=es" target="_self">Español</a>
                <a href="?lang=en" target="_self">English</a>
            </div>
        </div>
    </div>
    <div class="steam-logo">Itera Studio</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# NOTIFICACIÓN Y GUÍA DE INICIO (Nativo)
# ==========================================
if "tutorial_seen" not in st.session_state:
    st.toast('¡Hola! Si eres nuevo, ve al menú **Ayuda** para aprender a usar la plataforma.', icon='🎓')
    st.session_state["tutorial_seen"] = True

if st.session_state.get("show_tutorial", False):
    st.success("""
    ### 🎓 Guía de Inicio Rápido
    1. **Ingresa tu Función:** A la izquierda, escribe tu función usando lenguaje natural (Ej: `x^2 - 4` o `sin(x)`).
    2. **Define Parámetros:** Ajusta los límites (xₗ, xᵤ) y el punto inicial (x₀). Fija tu tolerancia.
    3. **Calcula:** Haz clic en 'CALCULAR RAÍCES'. El motor procesará los 5 algoritmos a la vez.
    4. **Analiza:** Observa la gráfica comparativa y abre cada pestaña para ver la tabla iterativa.
    
    *(Para cerrar esta guía, usa la X en la esquina superior derecha de este cuadro)*
    """)

# ==========================================
# ESTRUCTURA PRINCIPAL
# ==========================================
# Título centrado
st.markdown(f"<h1>{t['TITLE']}</h1>", unsafe_allow_html=True)

if st.session_state.get("expert_mode", False):
    st.caption("⚙️ **MODO EXPERTO ACTIVADO:** Monitor de rendimiento en segundo plano listo.")

# Creación de Pestañas 
tab_raices, tab_regresion, tab_derivacion, tab_integracion, tab_edo, tab_ayuda = tab_raices, tab_regresion, tab_derivacion, tab_integracion, tab_edo, tab_ayuda = st.tabs([
    t["TAB1"], 
    t["TAB2"], 
    t.get("TAB3", "DERIVACIÓN"), 
    t.get("TAB4", "INTEGRACIÓN"), 
    t.get("TAB5", "E.D.O."), 
    t["TAB_HELP"]
])

x = sp.Symbol('x')
transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))

# ==========================================
# FUNCIÓN PARA GENERAR GRÁFICAS
# ==========================================
def crear_grafica(func_lambdificada, titulo, raices_encontradas=None):
    x_vals = np.linspace(-10, 10, 1000)
    y_vals = np.zeros_like(x_vals)
    
    for i, val in enumerate(x_vals):
        try:
            res = func_lambdificada(val)
            y_vals[i] = float(res) if not isinstance(res, complex) else np.nan
        except:
            y_vals[i] = np.nan

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=titulo, line=dict(color='#7c6dd9', width=2)))
    
    fig.update_layout(
        title=titulo,
        xaxis_title=t["AXIS_X"],
        yaxis_title=t["AXIS_Y"],
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
        minor=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.08)'),
        zeroline=True, zerolinewidth=2, zerolinecolor='rgba(128,128,128,0.5)',
        tickformat="g"
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
        minor=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.08)'),
        zeroline=True, zerolinewidth=2, zerolinecolor='rgba(128,128,128,0.5)',
        tickformat="g"
    )

    if raices_encontradas:
        colores = ['#ff4d4d', '#00cc66', '#ff9900', '#9900ff', '#e600e6']
        for i, (nombre, raiz) in enumerate(raices_encontradas):
            if raiz is not None:
                try:
                    y_raiz = float(func_lambdificada(raiz))
                except:
                    y_raiz = 0.0
                fig.add_trace(go.Scatter(
                    x=[raiz], y=[y_raiz],
                    mode='markers',
                    name=f"{nombre}: {raiz:.5f}",
                    marker=dict(size=12, color=colores[i % len(colores)], symbol='circle-open', line=dict(width=3))
                ))
    return fig

# ==========================================
# MÉTODOS NUMÉRICOS REFACTORIZADOS
# ==========================================
def biseccion(f, xl, xu, tol):
    historial = []
    try:
        if f(xl) * f(xu) >= 0:
            return None, [{"Mensaje": t["ERR_OPPOSITE"]}]
    except:
        return None, [{"Mensaje": t["ERR_EVAL"]}]

    xr_old = 0
    iteracion = 1

    while True:
        xr = (xl + xu) / 2.0
        error = abs(xr - xr_old) if iteracion > 1 else "-"

        historial.append({
            t["COL_ITER"]: iteracion, 
            t["COL_XL"]: f"{xl:.5f}", 
            t["COL_XU"]: f"{xu:.5f}",
            t["COL_XR"]: f"{xr:.5f}", 
            t["COL_ERR"]: f"{error:.5f}" if iteracion > 1 else "-"
        })

        if iteracion > 1 and error < tol:
            break

        if f(xl) * f(xr) < 0:
            xu = xr
        elif f(xl) * f(xr) > 0:
            xl = xr
        else:
            break 

        xr_old = xr
        iteracion += 1

    return xr, historial

def falsa_posicion(f, xl, xu, tol):
    historial = []
    try:
        if f(xl) * f(xu) >= 0:
            return None, [{"Mensaje": t["ERR_OPPOSITE"]}]
    except:
        return None, [{"Mensaje": t["ERR_EVAL"]}]

    xr_old = 0
    iteracion = 1

    while True:
        try:
            xr = xu - (f(xu) * (xl - xu)) / (f(xl) - f(xu))
        except ZeroDivisionError:
            return None, [{"Mensaje": t["ERR_DIV0"]}]
            
        error = abs(xr - xr_old) if iteracion > 1 else "-"

        historial.append({
            t["COL_ITER"]: iteracion, 
            t["COL_XL"]: f"{xl:.5f}", 
            t["COL_XU"]: f"{xu:.5f}",
            t["COL_XR"]: f"{xr:.5f}", 
            t["COL_ERR"]: f"{error:.5f}" if iteracion > 1 else "-"
        })

        if iteracion > 1 and error < tol:
            break

        if f(xl) * f(xr) < 0:
            xu = xr
        elif f(xl) * f(xr) > 0:
            xl = xr
        else:
            break

        xr_old = xr
        iteracion += 1

    return xr, historial

def newton_raphson(f, df, x0, tol):
    historial = []
    iteracion = 1

    while True:
        df_val = df(x0)
        if df_val == 0:
            x0 += 0.001  
            df_val = df(x0) 

        x1 = x0 - (f(x0) / df_val)
        error = abs(x1 - x0)

        historial.append({
            t["COL_ITER"]: iteracion, 
            t["COL_XI"]: f"{x1:.5f}",
            t["COL_ERR"]: f"{error:.5f}" if iteracion > 1 else "-"
        })

        if error < tol:
            break
        if iteracion > 100:
             return None, [{"Mensaje": t["ERR_CONVERGE"]}]

        x0 = x1
        iteracion += 1

    return x1, historial

def secante(f, x_ant, x_act, tol):
    historial = []
    iteracion = 1
    error = float('inf')

    while error > tol:
        denominador = f(x_ant) - f(x_act)
        if denominador == 0:
            return None, [{"Mensaje": t["ERR_DIV0_FAIL"]}]
            
        numerador = f(x_act) * (x_ant - x_act)
        x_sig = x_act - (numerador / denominador)
        error = abs(x_sig - x_act)
        
        historial.append({
            t["COL_ITER"]: iteracion, 
            t["COL_XSIG"]: f"{x_sig:.5f}", 
            t["COL_ERR"]: f"{error:.5f}"
        })
        
        x_ant = x_act
        x_act = x_sig
        iteracion += 1
        
        if iteracion > 100:
             return None, [{"Mensaje": t["ERR_CONVERGE"]}]

    return x_act, historial

def punto_fijo(g, xi, tol):
    historial = []
    iteracion = 1
    error = float('inf')

    while error > tol:
        try:
            xi_next = g(xi)
        except Exception as e:
            return None, [{"Mensaje": f"ERROR: {e}"}]
            
        error = abs(xi_next - xi)
        historial.append({
            t["COL_ITER"]: iteracion, 
            t["COL_XSIG"]: f"{xi_next:.5f}", 
            t["COL_ERR"]: f"{error:.5f}"
        })
        
        xi = xi_next
        iteracion += 1
        
        if iteracion > 100:
            return None, [{"Mensaje": t["ERR_DIVERGE"]}]

    return xi, historial

# ==========================================
# PESTAÑA 1: RAÍCES DE ECUACIONES
# ==========================================
with tab_raices:
    col_input, col_results = st.columns([1, 2], gap="large")
    
    with col_input:
        st.markdown(f"### {t['PARAMS']}")
        with st.container():
            
            st.markdown(f"**{t['F_MAIN']}**")
            f_str = st.text_input("f(x)", value="2x^2 - x - 1", label_visibility="collapsed", key="f_str_tab1")
            f_valida = False
            try:
                f_expr_preview = parse_expr(f_str, transformations=transformations)
                f_lamb_preview = sp.lambdify(x, f_expr_preview, 'math')
                st.markdown("<div class='math-preview'>", unsafe_allow_html=True)
                st.latex(rf"f(x) = {sp.latex(f_expr_preview)}")
                st.markdown("</div>", unsafe_allow_html=True)
                f_valida = True
            except Exception:
                st.caption(t["WAIT_FUNC"])
            
            if f_valida:
                with st.expander(t["SHOW_F"]):
                    fig_f = crear_grafica(f_lamb_preview, "f(x)")
                    st.plotly_chart(fig_f, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"**{t['F_DESP']}**")
            g_str = st.text_input("g(x)", value="(x + 1)/2x", label_visibility="collapsed", key="g_str_tab1")
            g_valida = False
            try:
                g_expr_preview = parse_expr(g_str, transformations=transformations)
                g_lamb_preview = sp.lambdify(x, g_expr_preview, 'math')
                st.markdown("<div class='math-preview'>", unsafe_allow_html=True)
                st.latex(rf"g(x) = {sp.latex(g_expr_preview)}")
                st.markdown("</div>", unsafe_allow_html=True)
                g_valida = True
            except Exception:
                st.caption(t["WAIT_FUNC"])

            if g_valida:
                with st.expander(t["SHOW_G"]):
                    fig_g = crear_grafica(g_lamb_preview, "g(x)")
                    st.plotly_chart(fig_g, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**{t['LIM_INF']}**")
                xl = st.number_input("xₗ", value=1.0, format="%.5f", label_visibility="collapsed", key="xl_tab1")
            with c2:
                st.markdown(f"**{t['LIM_SUP']}**")
                xu = st.number_input("xᵤ", value=2.0, format="%.5f", label_visibility="collapsed", key="xu_tab1")
            
            st.markdown(f"**{t['PTO_INI']}**")
            x0 = st.number_input("x₀", value=1.0, format="%.5f", label_visibility="collapsed", key="x0_tab1")
            
            st.markdown(f"**{t['TOL']}**")
            tol = st.number_input("ε", value=0.001, format="%.5f", label_visibility="collapsed", key="tol_tab1")
            
            st.markdown("<br>", unsafe_allow_html=True)
            ejecutar = st.button(t["CALC_BTN"], use_container_width=True)

    with col_results:
        st.markdown(f"### {t['RES_TITLE']}")
        if ejecutar:
            start_time = time.time()
            try:
                f_expr = parse_expr(f_str, transformations=transformations)
                f = sp.lambdify(x, f_expr, 'math')
                
                g_expr = parse_expr(g_str, transformations=transformations)
                g = sp.lambdify(x, g_expr, 'math')
                
                df_expr = sp.diff(f_expr, x)
                df = sp.lambdify(x, df_expr, 'math')

                res_bis, hist_bis = biseccion(f, xl, xu, tol)
                res_fp, hist_fp = falsa_posicion(f, xl, xu, tol)
                res_nr, hist_nr = newton_raphson(f, df, x0, tol)
                res_sec, hist_sec = secante(f, xl, xu, tol) 
                res_pf, hist_pf = punto_fijo(g, x0, tol)

                metodos = [
                    (t["METH_BIS"], res_bis, hist_bis),
                    (t["METH_FP"], res_fp, hist_fp),
                    (t["METH_NR"], res_nr, hist_nr),
                    (t["METH_SEC"], res_sec, hist_sec),
                    (t["METH_PF"], res_pf, hist_pf)
                ]

                raices_validas = [(nombre, raiz) for nombre, raiz, hist in metodos if raiz is not None]
                
                with st.expander(t["COMP_GRAPH"], expanded=False):
                    if raices_validas:
                        fig_comparativa = crear_grafica(f, t["CURVE_F"], raices_validas)
                        st.plotly_chart(fig_comparativa, use_container_width=True)
                    else:
                        st.warning(t["NO_ROOTS"])

                for nombre, raiz, historial in metodos:
                    with st.expander(f"{nombre}", expanded=(raiz is not None)):
                        if raiz is not None:
                            st.metric(label=t["ROOT_APPROX"], value=f"{raiz:.7f}", delta=f"{len(historial)} {t['ITERS']}", delta_color="off")
                            st.dataframe(pd.DataFrame(historial), use_container_width=True, hide_index=True)
                        else:
                            st.error(historial[0]["Mensaje"])
                
                if st.session_state.get("expert_mode", False):
                    st.success(f"⏱️ Tiempo total de procesamiento SymPy: {(time.time() - start_time):.4f} segundos.")

            except Exception as e:
                st.error(t["ERR_SYNTAX"])
        else:
            st.info(t["INFO_START_ROOTS"])

# ==========================================
# PESTAÑA 2: REGRESIÓN E INTERPOLACIÓN
# ==========================================
with tab_regresion:
    # Submenú interno de 3 opciones
    metodo_tab2 = st.radio(
        "", 
        [t.get("METHOD_LS", "Mínimos Cuadrados"), 
         t.get("METHOD_NEWTON_LIN", "Interpolación Lineal"),
         t.get("METHOD_LAGRANGE", "Interpolación Lagrange")], 
        horizontal=True, 
        label_visibility="collapsed"
    )
    
    st.markdown("---")

    # ------------------------------------------
    # OPCIÓN A: MÍNIMOS CUADRADOS
    # ------------------------------------------
    if metodo_tab2 == t.get("METHOD_LS", "Mínimos Cuadrados"):
        st.markdown(f"### {t.get('REG_TITLE', 'REGRESIÓN LINEAL (MÍNIMOS CUADRADOS)')}")
        col_data, col_res_reg = st.columns([1, 2], gap="large")
        
        with col_data:
            st.markdown(f"**{t.get('REG_DATA', 'Ingreso de Datos')}**")
            st.caption(t.get('REG_ADD_DEL', 'Haz doble clic para editar.'))
            
            if 'df_reg' not in st.session_state:
                st.session_state.df_reg = pd.DataFrame({"X": [1.0, 2.0, 3.0, 4.0], "Y": [0.5, 2.5, 2.0, 4.0]})
                
            edited_df = st.data_editor(st.session_state.df_reg, num_rows="dynamic", use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)
            ejecutar_reg = st.button(t.get('CALC_REG_BTN', 'CALCULAR AJUSTE LINEAL'), use_container_width=True)

        with col_res_reg:
            st.markdown(f"### {t.get('REG_RES', 'Resultados de la Regresión')}")
            if ejecutar_reg:
                df_clean = edited_df.dropna()
                n = len(df_clean)
                if n < 2:
                    st.error(t.get('ERR_DATA', 'ERROR: Ingresa al menos 2 puntos válidos.'))
                else:
                    x_data, y_data = df_clean["X"].values, df_clean["Y"].values
                    sum_x, sum_y = np.sum(x_data), np.sum(y_data)
                    sum_xy, sum_x2 = np.sum(x_data * y_data), np.sum(x_data**2)
                    
                    denominador = (n * sum_x2 - sum_x**2)
                    if denominador == 0:
                        st.error("División por cero. Revisa que las X no sean iguales.")
                    else:
                        a1 = (n * sum_xy - sum_x * sum_y) / denominador
                        a0 = np.mean(y_data) - a1 * np.mean(x_data)
                        
                        st_dev_tot = np.sum((y_data - np.mean(y_data))**2)
                        st_dev_res = np.sum((y_data - (a0 + a1 * x_data))**2)
                        r2 = 1 - (st_dev_res / st_dev_tot) if st_dev_tot != 0 else 1
                        r = np.sqrt(abs(r2)) * (1 if a1 > 0 else -1)
                        
                        st.info(f"**{t.get('MODEL_EQ', 'Ecuación:')}** y = {a1:.5f}x {'+' if a0 >= 0 else ''} {a0:.5f}")
                        c1, c2 = st.columns(2)
                        c1.metric(t.get('COEF_CORR', 'r'), f"{r:.5f}")
                        c2.metric(t.get('COEF_DET', 'R²'), f"{r2:.5f}")
                        
                        fig_reg = go.Figure()
                        fig_reg.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name='Datos', marker=dict(size=10, color='#ff4d4d')))
                        
                        x_line = np.linspace(min(x_data) - 1, max(x_data) + 1, 100)
                        fig_reg.add_trace(go.Scatter(x=x_line, y=a0 + a1 * x_line, mode='lines', name='Ajuste', line=dict(color='#7c6dd9', width=3)))
                        
                        fig_reg.update_layout(title=t.get('GRAPH_REG', 'Gráfica'), xaxis_title=t["AXIS_X"], yaxis_title=t["AXIS_Y"], hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig_reg, use_container_width=True)
            else:
                st.info(t["INFO_START_REG"])

    # ------------------------------------------
    # OPCIÓN B: INTERPOLACIÓN LINEAL DE NEWTON
    # ------------------------------------------
    elif metodo_tab2 == t.get("METHOD_NEWTON_LIN", "Interpolación Lineal"):
        st.markdown(f"### {t.get('INT_TITLE', 'INTERPOLACIÓN LINEAL DE NEWTON')}")
        col_data, col_res_int = st.columns([1, 2], gap="large")
        
        with col_data:
            st.markdown(f"**{t.get('P0_LABEL', 'Punto Inicial P₀')}**")
            cx1, cy1 = st.columns(2)
            x0_int = cx1.number_input("x₀", value=1.0, format="%.5f", key="x0_int")
            y0_int = cy1.number_input("f(x₀)", value=2.0, format="%.5f", key="y0_int")
            
            st.markdown(f"**{t.get('P1_LABEL', 'Punto Final P₁')}**")
            cx2, cy2 = st.columns(2)
            x1_int = cx2.number_input("x₁", value=4.0, format="%.5f", key="x1_int")
            y1_int = cy2.number_input("f(x₁)", value=5.0, format="%.5f", key="y1_int")
            
            st.markdown("---")
            st.markdown(f"**{t.get('INT_X_VAL', 'Valor a interpolar x:')}**")
            x_target = st.number_input("x", value=2.5, format="%.5f", label_visibility="collapsed", key="xtarget_int")
            
            st.markdown("<br>", unsafe_allow_html=True)
            ejecutar_int = st.button(t.get('CALC_INT_BTN', 'CALCULAR INTERPOLACIÓN'), use_container_width=True)

        with col_res_int:
            st.markdown(f"### {t.get('INT_RES', 'Resultado')}")
            if ejecutar_int:
                if x0_int == x1_int:
                    st.error(t.get('ERR_X_EQUAL', 'ERROR: x₀ y x₁ no pueden ser iguales.'))
                else:
                    diferencia_dividida = (y1_int - y0_int) / (x1_int - x0_int)
                    fx_target = y0_int + diferencia_dividida * (x_target - x0_int)
                    st.metric(label=f"f({x_target})", value=f"{fx_target:.5f}")
                    
                    st.info(f"**{t.get('INT_EQ', 'Sustitución:')}** f₁({x_target}) = {y0_int} + (({y1_int} - {y0_int}) / ({x1_int} - {x0_int})) * ({x_target} - {x0_int})")
                    
                    fig_int = go.Figure()
                    fig_int.add_trace(go.Scatter(x=[x0_int, x1_int], y=[y0_int, y1_int], mode='markers+lines', name='Intervalo', marker=dict(size=10, color='#7c6dd9')))
                    fig_int.add_trace(go.Scatter(x=[x_target], y=[fx_target], mode='markers', name='Punto Interpolado', marker=dict(size=12, color='#ff4d4d', symbol='star')))
                    fig_int.update_layout(title=t.get('GRAPH_REG', 'Gráfica'), xaxis_title=t["AXIS_X"], yaxis_title=t["AXIS_Y"], hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig_int, use_container_width=True)
            else:
                st.info(t["INFO_START_REG"])

    # ------------------------------------------
    # OPCIÓN C: INTERPOLACIÓN DE LAGRANGE
    # ------------------------------------------
    elif metodo_tab2 == t.get("METHOD_LAGRANGE", "Interpolación Lagrange"):
        st.markdown(f"### {t.get('LAG_TITLE', 'INTERPOLACIÓN POLINOMIAL DE LAGRANGE')}")
        col_data, col_res_lag = st.columns([1, 2], gap="large")
        
        with col_data:
            st.markdown(f"**{t.get('LAG_DATA', 'Puntos Conocidos')}**")
            st.caption(t.get('LAG_ADD_DEL', 'Agrega puntos. No repitas X.'))
            
            if 'df_lag' not in st.session_state:
                st.session_state.df_lag = pd.DataFrame({"X": [1.0, 4.0, 6.0], "Y": [1.5, 3.0, 5.0]})
                
            edited_df_lag = st.data_editor(st.session_state.df_lag, num_rows="dynamic", use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown(f"**{t.get('LAG_X_VAL', 'Valor a interpolar x:')}**")
            x_target_lag = st.number_input("x_lag", value=3.0, format="%.5f", label_visibility="collapsed", key="xtarget_lag")
            
            st.markdown("<br>", unsafe_allow_html=True)
            ejecutar_lag = st.button(t.get('CALC_LAG_BTN', 'CALCULAR POLINOMIO'), use_container_width=True)

        with col_res_lag:
            st.markdown(f"### {t.get('LAG_RES', 'Resultado de Lagrange')}")
            if ejecutar_lag:
                df_clean_lag = edited_df_lag.dropna()
                x_vals = df_clean_lag["X"].values
                y_vals = df_clean_lag["Y"].values
                n_lag = len(x_vals)
                
                # Validaciones
                if n_lag < 2:
                    st.error(t.get('ERR_DATA', 'ERROR: Ingresa al menos 2 puntos válidos.'))
                elif len(set(x_vals)) != len(x_vals):
                    st.error(t.get('ERR_DUP_X', 'ERROR: Valores de X repetidos.'))
                else:
                    # Función interna para evaluar Lagrange en un punto
                    def lagrange_eval(x_target):
                        resultado = 0.0
                        for i in range(n_lag):
                            termino = y_vals[i]
                            for j in range(n_lag):
                                if i != j:
                                    termino = termino * (x_target - x_vals[j]) / (x_vals[i] - x_vals[j])
                            resultado += termino
                        return resultado

                    # Cálculo del punto objetivo
                    fx_target_lag = lagrange_eval(x_target_lag)
                    st.metric(label=f"P({x_target_lag})", value=f"{fx_target_lag:.5f}")
                    
                    # Graficación
                    fig_lag = go.Figure()
                    
                    # Puntos base
                    fig_lag.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, 
                        mode='markers', 
                        name='Puntos Conocidos',
                        marker=dict(size=10, color='#7c6dd9', symbol='circle')
                    ))
                    
                    # Punto interpolado
                    fig_lag.add_trace(go.Scatter(
                        x=[x_target_lag], y=[fx_target_lag], 
                        mode='markers', 
                        name=f'Punto Interpolado ({x_target_lag}, {fx_target_lag:.3f})',
                        marker=dict(size=14, color='#ff4d4d', symbol='star')
                    ))
                    
                    # Curva polinomial (generando 100 puntos en el rango)
                    x_rango = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 100)
                    y_rango = [lagrange_eval(xi) for xi in x_rango]
                    
                    fig_lag.add_trace(go.Scatter(
                        x=x_rango, y=y_rango, 
                        mode='lines', 
                        name=f'Polinomio P(x)',
                        line=dict(color='rgba(124, 109, 217, 0.5)', width=2, dash='dot')
                    ))
                    
                    fig_lag.update_layout(
                        title=t.get('GRAPH_REG', 'Gráfica'),
                        xaxis_title=t["AXIS_X"], yaxis_title=t["AXIS_Y"],
                        hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig_lag, use_container_width=True)
            else:
                st.info(t["INFO_START_REG"])

# ==========================================
# PESTAÑA 3: DERIVACIÓN NUMÉRICA (DIFERENCIAS FINITAS)
# ==========================================
with tab_derivacion:
    st.markdown(f"### {t.get('DF_TITLE', 'DIFERENCIAS FINITAS')}")
    
    col_in_df, col_out_df = st.columns([1, 2], gap="large")
    
    with col_in_df:
        st.markdown(f"**{t.get('F_MAIN', 'Función f(x):')}**")
        f_str_df = st.text_input("f(x)_df", value="sin(x) + x**2", label_visibility="collapsed", key="f_tab3")
        
        st.markdown(f"**{t.get('DF_X', 'Punto a evaluar xᵢ:')}**")
        xi = st.number_input("xᵢ", value=1.0, format="%.5f", label_visibility="collapsed", key="xi_tab3")
        
        st.markdown(f"**{t.get('DF_H', 'Tamaño de paso h:')}**")
        h = st.number_input("h_paso", value=0.1, format="%.5f", label_visibility="collapsed", key="h_tab3")
        
        st.markdown("<br>", unsafe_allow_html=True)
        ejecutar_df = st.button(t.get('CALC_DF_BTN', 'CALCULAR DERIVADAS'), use_container_width=True)
        
    with col_out_df:
        st.markdown(f"### {t.get('DF_RES', 'Resultados de Aproximación')}")
        if ejecutar_df:
            if h == 0:
                st.error(t.get('ERR_H_ZERO', 'ERROR: h no puede ser cero.'))
            else:
                try:
                    # Preparar función y derivada exacta con Sympy
                    f_expr_df = parse_expr(f_str_df, transformations=transformations)
                    f_lamb_df = sp.lambdify(x, f_expr_df, 'math')
                    
                    df_expr_exact = sp.diff(f_expr_df, x)
                    df_lamb_exact = sp.lambdify(x, df_expr_exact, 'math')
                    
                    # Cálculos exactos
                    f_xi = f_lamb_df(xi)
                    exact_val = df_lamb_exact(xi)
                    
                    # Puntos desplazados
                    f_xi_mas_h = f_lamb_df(xi + h)
                    f_xi_menos_h = f_lamb_df(xi - h)
                    
                    # Fórmulas de Diferencias Finitas
                    df_adelante = (f_xi_mas_h - f_xi) / h
                    df_atras = (f_xi - f_xi_menos_h) / h
                    df_centrada = (f_xi_mas_h - f_xi_menos_h) / (2 * h)
                    
                    # Errores absolutos
                    err_adelante = abs(exact_val - df_adelante)
                    err_atras = abs(exact_val - df_atras)
                    err_centrada = abs(exact_val - df_centrada)
                    
                    # Mostrar valor exacto analítico
                    st.info(f"**Valor Exacto (Analítico):** f'({xi}) = {exact_val:.6f}")
                    
                    # Mostrar métricas de las aproximaciones
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Hacia Adelante", f"{df_adelante:.5f}", f"Error: {err_adelante:.5f}", delta_color="off")
                    c2.metric("Hacia Atrás", f"{df_atras:.5f}", f"Error: {err_atras:.5f}", delta_color="off")
                    c3.metric("Centrada", f"{df_centrada:.5f}", f"Error: {err_centrada:.5f}", delta_color="off")
                    
                    st.markdown("#### Puntos Evaluados")
                    tabla_df = pd.DataFrame({
                        "Punto": ["x_i - h (Atrás)", "x_i (Centro)", "x_i + h (Adelante)"],
                        "Valor x": [f"{xi - h:.5f}", f"{xi:.5f}", f"{xi + h:.5f}"],
                        "f(x)": [f"{f_xi_menos_h:.5f}", f"{f_xi:.5f}", f"{f_xi_mas_h:.5f}"]
                    })
                    st.dataframe(tabla_df, use_container_width=True, hide_index=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    # =================================
                    
                    # Graficar la función y las tangentes
                    fig_df = go.Figure()
                    
                    # Rango visible de la gráfica (depende del paso h)
                    rango_x = np.linspace(xi - 4*h, xi + 4*h, 150)
                    rango_y = [f_lamb_df(val) for val in rango_x]
                    
                    # Curva principal
                    fig_df.add_trace(go.Scatter(x=rango_x, y=rango_y, mode='lines', name='Curva f(x)', line=dict(color='#7c6dd9', width=3)))
                    
                    # Línea Tangente Exacta
                    y_tangente = exact_val * (rango_x - xi) + f_xi
                    fig_df.add_trace(go.Scatter(x=rango_x, y=y_tangente, mode='lines', name='Tangente Exacta', line=dict(color='#00cc66', width=2, dash='dash')))
                    
                    # Puntos evaluados
                    fig_df.add_trace(go.Scatter(
                        x=[xi-h, xi, xi+h], y=[f_xi_menos_h, f_xi, f_xi_mas_h], 
                        mode='markers', name='Puntos Evaluados', 
                        marker=dict(size=10, color='#ff4d4d', symbol='circle-open', line=dict(width=2))
                    ))
                    
                    fig_df.update_layout(
                        title="Comparativa Visual de Pendientes",
                        xaxis_title=t["AXIS_X"], yaxis_title=t["AXIS_Y"],
                        hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_df.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    fig_df.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    
                    st.plotly_chart(fig_df, use_container_width=True)
                    
                except Exception as e:
                    st.error(t.get('ERR_SYNTAX', 'ERROR: Sintaxis inválida o función no soportada.'))
        else:
            st.info(t["INFO_START_DERIV"])

# ==========================================
# PESTAÑA 4: INTEGRACIÓN NUMÉRICA (TRAPECIOS)
# ==========================================
with tab_integracion:
    # Submenú interno de 3 opciones
    metodo_intg = st.radio(
        t.get("INTG_METHOD", "Selecciona la variante:"), 
        [t.get("TRAP_SIMPLE", "Trapecio Simple"), 
         t.get("TRAP_MULTIPLE", "Trapecio Múltiple"),
         t.get("SIMPSON_METHOD", "Simpson (1/3 y 3/8)")], 
        horizontal=True
    )
    
    st.markdown("---")
    
    # Cambio dinámico de título según la selección
    if metodo_intg == t.get("SIMPSON_METHOD", "Simpson (1/3 y 3/8)"):
        st.markdown(f"### {t.get('SIMP_TITLE', 'MÉTODO DE SIMPSON')}")
    else:
        st.markdown(f"### {t.get('INTG_TITLE', 'MÉTODO DEL TRAPECIO')}")
    
    col_in_intg, col_out_intg = st.columns([1, 2], gap="large")
    
    with col_in_intg:
        st.markdown(f"**{t.get('F_MAIN', 'Función f(x):')}**")
        f_str_intg = st.text_input("f(x)_intg", value="x**2 * exp(-x)", label_visibility="collapsed", key="f_tab4")
        
        c_lim1, c_lim2 = st.columns(2)
        with c_lim1:
            st.markdown(f"**{t.get('INTG_A', 'Límite a:')}**")
            a_intg = st.number_input("a_intg", value=0.0, format="%.5f", label_visibility="collapsed", key="a_tab4")
        with c_lim2:
            st.markdown(f"**{t.get('INTG_B', 'Límite b:')}**")
            b_intg = st.number_input("b_intg", value=3.0, format="%.5f", label_visibility="collapsed", key="b_tab4")
            
        n_intg = 1
        # Pedir n solo si no es Trapecio Simple
        if metodo_intg != t.get("TRAP_SIMPLE", "Trapecio Simple"):
            st.markdown(f"**{t.get('INTG_N', 'Número de intervalos n:')}**")
            # Si es Simpson, n debe ser al menos 2
            min_n = 2 if metodo_intg == t.get("SIMPSON_METHOD", "Simpson (1/3 y 3/8)") else 1
            n_intg = st.number_input("n_intg", min_value=min_n, max_value=1000, value=max(5, min_n), step=1, label_visibility="collapsed", key="n_tab4")
            
        st.markdown("<br>", unsafe_allow_html=True)
        ejecutar_intg = st.button(t.get('CALC_INTG_BTN', 'CALCULAR ÁREA'), use_container_width=True)

    with col_out_intg:
        st.markdown(f"### {t.get('INTG_RES', 'Resultados de Integración')}")
        if ejecutar_intg:
            if a_intg >= b_intg:
                st.error(t.get('ERR_LIMITS', 'ERROR: El límite superior debe ser mayor.'))
            elif metodo_intg == t.get("SIMPSON_METHOD", "Simpson (1/3 y 3/8)") and n_intg < 2:
                st.error(t.get('ERR_N_SIMPSON', 'ERROR: Se requieren al menos 2 intervalos.'))
            else:
                try:
                    f_expr_intg = parse_expr(f_str_intg, transformations=transformations)
                    f_lamb_intg = sp.lambdify(x, f_expr_intg, 'math')
                    
                    # 1. Cálculo del Área Exacta (Alta resolución)
                    x_exact = np.linspace(a_intg, b_intg, 5000)
                    y_exact = [f_lamb_intg(val) for val in x_exact]
                    area_exacta = np.trapezoid(y_exact, x_exact)
                    
                    # 2. Vectores de evaluación
                    h_intg = (b_intg - a_intg) / n_intg
                    x_eval = np.linspace(a_intg, b_intg, n_intg + 1)
                    y_eval = np.array([f_lamb_intg(val) for val in x_eval])
                    
                    area_aprox = 0.0
                    
                    # ------------------------------------------
                    # ALGORITMOS DE INTEGRACIÓN
                    # ------------------------------------------
                    if metodo_intg == t.get("TRAP_SIMPLE", "Trapecio Simple"):
                        area_aprox = (b_intg - a_intg) * (y_eval[0] + y_eval[1]) / 2.0
                        
                    elif metodo_intg == t.get("TRAP_MULTIPLE", "Trapecio Múltiple"):
                        area_aprox = (h_intg / 2.0) * (y_eval[0] + 2 * np.sum(y_eval[1:-1]) + y_eval[-1])
                        
                    elif metodo_intg == t.get("SIMPSON_METHOD", "Simpson (1/3 y 3/8)"):
                        if n_intg % 2 == 0:
                            # Simpson 1/3 puro (n es par)
                            area_aprox = (h_intg / 3.0) * (y_eval[0] + 4 * np.sum(y_eval[1:-1:2]) + 2 * np.sum(y_eval[2:-2:2]) + y_eval[-1])
                            st.success(t.get("INFO_SIMPSON_EVEN", "Simpson 1/3 en todo el rango."))
                        else:
                            # Simpson combinado (n es impar, n >= 3)
                            m = n_intg - 3
                            area_13 = 0.0
                            if m > 0:
                                area_13 = (h_intg / 3.0) * (y_eval[0] + 4 * np.sum(y_eval[1:m:2]) + 2 * np.sum(y_eval[2:m-1:2]) + y_eval[m])
                            
                            area_38 = (3 * h_intg / 8.0) * (y_eval[m] + 3 * y_eval[m+1] + 3 * y_eval[m+2] + y_eval[m+3])
                            area_aprox = area_13 + area_38
                            st.success(t.get("INFO_SIMPSON_ODD", "Simpson 1/3 al inicio y 3/8 al final."))
                    
                    error_intg = abs(area_exacta - area_aprox)
                    
                    # Mostrar métricas
                    c1, c2, c3 = st.columns(3)
                    c1.metric(t.get('APPROX_AREA', 'Área Aproximada'), f"{area_aprox:.6f}")
                    c2.metric(t.get('EXACT_AREA', 'Ref. Alta Resolución'), f"{area_exacta:.6f}")
                    c3.metric(t.get('COL_ERR', 'Error Absoluto'), f"{error_intg:.6f}", delta_color="off")
                    
                    st.markdown("#### Coordenadas de los Intervalos")
                    tabla_intg = pd.DataFrame({
                        "Intervalo (i)": range(len(x_eval)),
                        "Valor x_i": [f"{val:.5f}" for val in x_eval],
                        "f(x_i)": [f"{val:.5f}" for val in y_eval]
                    })
                    # st.dataframe mostrará una tabla con scroll si hay muchos intervalos
                    st.dataframe(tabla_intg, use_container_width=True, hide_index=True, height=200)
                    st.markdown("<br>", unsafe_allow_html=True)
                    # ==================================

                    # 3. Gráfica de la Integración
                    fig_intg = go.Figure()
                    
                    # Curva principal
                    rango_x_curva = np.linspace(a_intg - 0.5, b_intg + 0.5, 300)
                    rango_y_curva = [f_lamb_intg(val) for val in rango_x_curva]
                    fig_intg.add_trace(go.Scatter(
                        x=rango_x_curva, y=rango_y_curva, 
                        mode='lines', name='Curva f(x)', 
                        line=dict(color='#7c6dd9', width=3)
                    ))
                    
                    # Relleno del área aproximada
                    fig_intg.add_trace(go.Scatter(
                        x=x_eval, y=y_eval,
                        mode='lines+markers',
                        name='Puntos de Evaluación',
                        fill='tozeroy', 
                        fillcolor='rgba(255, 77, 77, 0.3)' if "Simpson" not in metodo_intg else 'rgba(0, 204, 102, 0.3)',
                        line=dict(color='#ff4d4d' if "Simpson" not in metodo_intg else '#00cc66', width=2),
                        marker=dict(size=8)
                    ))
                    
                    fig_intg.update_layout(
                        title="Área evaluada",
                        xaxis_title=t["AXIS_X"], yaxis_title=t["AXIS_Y"],
                        hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_intg.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    fig_intg.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    
                    st.plotly_chart(fig_intg, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"ERROR TÉCNICO DETECTADO: {e}")
        else:
            st.info(t["INFO_START_INTG"])

# ==========================================
# PESTAÑA 5: ECUACIONES DIFERENCIALES ORDINARIAS (EDO)
# ==========================================
with tab_edo:
    st.markdown(f"### {t.get('ODE_TITLE', 'RESOLUCIÓN DE E.D.O.')}")
    
    # Submenú interno de métodos
    metodo_edo = st.radio(
        t.get("ODE_METHOD", "Selecciona el método:"), 
        [t.get("METH_EULER", "Método de Euler"), 
         t.get("METH_HEUN", "Método de Heun"),
         t.get("METH_RALSTON", "Método de Ralston")], 
        horizontal=True
    )
    
    st.markdown("---")
    
    col_in_edo, col_out_edo = st.columns([1, 2], gap="large")
    
    with col_in_edo:
        st.markdown("**" + t.get("ODE_F", "Ecuación y' = f(x, y):") + "**")
        f_str_edo = st.text_input("f(x,y)_edo", value="x + y", label_visibility="collapsed", key="f_tab5")
        
        c_val1, c_val2 = st.columns(2)
        with c_val1:
            st.markdown(f"**{t.get('ODE_X0', 'Valor inicial x₀:')}**")
            x0_edo = st.number_input("x0_edo", value=0.0, format="%.5f", label_visibility="collapsed", key="x0_tab5")
        with c_val2:
            st.markdown(f"**{t.get('ODE_Y0', 'Condición inicial y₀:')}**")
            y0_edo = st.number_input("y0_edo", value=1.0, format="%.5f", label_visibility="collapsed", key="y0_tab5")
            
        c_val3, c_val4 = st.columns(2)
        with c_val3:
            st.markdown(f"**{t.get('ODE_XF', 'Valor final x_f:')}**")
            xf_edo = st.number_input("xf_edo", value=2.0, format="%.5f", label_visibility="collapsed", key="xf_tab5")
        with c_val4:
            st.markdown(f"**{t.get('ODE_H', 'Tamaño de paso h:')}**")
            h_edo = st.number_input("h_edo", value=0.5, format="%.5f", label_visibility="collapsed", key="h_tab5")
            
        st.markdown("<br>", unsafe_allow_html=True)
        ejecutar_edo = st.button(t.get('CALC_ODE_BTN', 'RESOLVER EDO'), use_container_width=True)

    with col_out_edo:
        st.markdown(f"### {t.get('ODE_RES', 'Tabla de Iteraciones')}")
        if ejecutar_edo:
            if h_edo <= 0 or x0_edo >= xf_edo:
                st.error(t.get('ERR_ODE_H', 'ERROR: Parámetros de rango o paso inválidos.'))
            else:
                try:
                    # Se requiere declarar 'y' para funciones de dos variables
                    y_sym = sp.Symbol('y')
                    f_expr_edo = parse_expr(f_str_edo, transformations=transformations)
                    f_lamb_edo = sp.lambdify((x, y_sym), f_expr_edo, 'math')
                    
                    # Inicialización de listas para resultados
                    x_vals = [x0_edo]
                    y_vals = [y0_edo]
                    historial_edo = []
                    
                    # Valores actuales
                    xi = x0_edo
                    yi = y0_edo
                    iteracion = 0
                    
                    historial_edo.append({
                        t.get("COL_ITER", "Iteración"): iteracion,
                        "x": f"{xi:.5f}",
                        "y": f"{yi:.5f}"
                    })
                    
                    # Bucle de cálculo
                    while xi < xf_edo - 1e-9: # Margen de tolerancia para punto flotante
                        # Ajustar el último paso si nos pasamos de xf
                        h_actual = min(h_edo, xf_edo - xi)
                        
                        # Evaluar la derivada en el punto actual
                        k1 = f_lamb_edo(xi, yi)
                        
                        if metodo_edo == t.get("METH_EULER", "Método de Euler"):
                            # Euler Clásico
                            yi_next = yi + k1 * h_actual
                            
                        elif metodo_edo == t.get("METH_HEUN", "Método de Heun"):
                            # Heun (Euler Modificado / RK2)
                            k2 = f_lamb_edo(xi + h_actual, yi + k1 * h_actual)
                            yi_next = yi + (0.5 * k1 + 0.5 * k2) * h_actual
                            
                        elif metodo_edo == t.get("METH_RALSTON", "Método de Ralston"):
                            # Ralston (RK2 con 3/4)
                            k2 = f_lamb_edo(xi + 0.75 * h_actual, yi + 0.75 * k1 * h_actual)
                            yi_next = yi + ((1/3) * k1 + (2/3) * k2) * h_actual
                            
                        # Actualizar variables
                        xi += h_actual
                        yi = yi_next
                        iteracion += 1
                        
                        x_vals.append(xi)
                        y_vals.append(yi)
                        
                        historial_edo.append({
                            t.get("COL_ITER", "Iteración"): iteracion,
                            "x": f"{xi:.5f}",
                            "y": f"{yi:.5f}"
                        })
                    
                    # Mostrar tabla de resultados
                    st.dataframe(pd.DataFrame(historial_edo), use_container_width=True, hide_index=True)
                    
                    st.markdown(f"### {t.get('ODE_GRAPH', 'Trayectoria de la Solución')}")
                    # Gráfica de la solución
                    fig_edo = go.Figure()
                    
                    fig_edo.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, 
                        mode='lines+markers', 
                        name=f'Solución ({metodo_edo})',
                        line=dict(color='#7c6dd9', width=3),
                        marker=dict(size=8, color='#ff4d4d', symbol='circle')
                    ))
                    
                    fig_edo.update_layout(
                        title=f"Aproximación Numérica: y' = {f_str_edo}",
                        xaxis_title="Eje X", yaxis_title="Eje Y",
                        hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_edo.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    fig_edo.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', zeroline=True)
                    
                    st.plotly_chart(fig_edo, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"ERROR TÉCNICO DETECTADO: {e}")
        else:
            st.info(t["INFO_START_ODE"])

# ==========================================
# PESTAÑA 6: AYUDA FUSIONADA (Info, Ayuda, Ejemplos)
# ==========================================
with tab_ayuda:
    st.markdown(f"### {t['TAB_INFO']}")
    st.markdown(t["INFO_TEXT"])
    
    st.markdown("---")
    
    st.markdown(f"### {t['TAB_HELP']}")
    st.markdown(t["HELP_SYNTAX"])
    st.markdown(t["HELP_PARAMS"])
    
    st.markdown("---")
    
    st.markdown(f"### {t['TAB_EXAMPLES']}")
    st.markdown(f"#### {t['EX_1_TITLE']}")
    st.markdown("* **f(x):** `x^3 - 2x^2 - 5`")
    st.markdown("* **xₗ / xᵤ:** `2.0` / `3.0`")
    st.markdown("* **x₀:** `2.5`")
    
    st.markdown(f"#### {t['EX_2_TITLE']}")
    st.markdown("* **f(x):** `exp(-x) - x`")
    st.markdown("* **xₗ / xᵤ:** `0.0` / `1.0`")
    st.markdown("* **x₀:** `0.0`")

    st.markdown(f"#### {t['EX_3_TITLE']}")
    st.markdown("* **f(x):** `x^2 - x - 1`")
    st.markdown("* **g(x):** `(x + 1)^(1/2)` o `sqrt(x + 1)`")
    st.markdown("* **xₗ / xᵤ:** `1.0` / `2.0`")
    st.markdown("* **x₀:** `1.0`")
