import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# ==========================================
# CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
# ==========================================
st.set_page_config(page_title="MÉTODOS NUMÉRICOS", layout="wide")

# ==========================================
# GESTIÓN DE IDIOMA POR PARÁMETROS DE URL
# ==========================================
params = st.query_params
if "lang" in params and params.get("lang", "").lower() == "en":
    idioma_seleccionado = "ENGLISH"
else:
    idioma_seleccionado = "ESPAÑOL"

# ==========================================
# DICCIONARIO DE IDIOMAS
# ==========================================
LANG = {
    "ESPAÑOL": {
        "TITLE": "PLATAFORMA DE ANÁLISIS NUMÉRICO",
        "TAB1": "SOLUCIÓN DE ECUACIONES",
        "TAB2": "REGRESIÓN E INTERPOLACIÓN",
        "TAB_INFO": "INFORMACIÓN",
        "TAB_HELP": "AYUDA",
        "TAB_EXAMPLES": "EJEMPLOS",
        "PARAMS": "PARÁMETROS",
        "F_MAIN": "Función principal f(x):",
        "F_DESP": "Función despejada g(x) (Para Punto Fijo):",
        "WAIT_FUNC": "Esperando una función válida...",
        "SHOW_F": "MOSTRAR GRÁFICA f(x)",
        "SHOW_G": "MOSTRAR GRÁFICA g(x)",
        "LIM_INF": "Límite inferior xl (o x_ant)",
        "LIM_SUP": "Límite superior xu (o x_act)",
        "PTO_INI": "Punto inicial x0",
        "TOL": "Tolerancia",
        "CALC_BTN": "CALCULAR RAÍCES",
        "RES_TITLE": "RESULTADOS E ITERACIONES",
        "COMP_GRAPH": "VER GRÁFICA COMPARATIVA DE RAÍCES",
        "NO_ROOTS": "No se encontraron raíces válidas para graficar.",
        "ERR_SYNTAX": "ERROR en la sintaxis de las funciones o división por cero detectada. Revisa los datos ingresados.",
        "INFO_START": "INGRESA LOS PARÁMETROS A LA IZQUIERDA Y PRESIONA 'CALCULAR RAÍCES'.",
        "CONSTRUCTION": "MÓDULO EN CONSTRUCCIÓN.",
        "ERR_OPPOSITE": "ERROR: f(xl) y f(xu) no tienen signos opuestos.",
        "ERR_EVAL": "ERROR: Fallo al evaluar los límites en la función.",
        "ERR_DIV0": "ERROR: División por cero durante el cálculo.",
        "ERR_DIV0_FAIL": "ERROR: División por cero. El método falla.",
        "ERR_CONVERGE": "ERROR: El método no converge después de 100 iteraciones.",
        "ERR_DIVERGE": "ERROR: El método diverge con este despeje o punto inicial x0.",
        "ROOT_APPROX": "Raíz Aproximada",
        "ITERS": "Iteraciones",
        "METH_BIS": "BISECCIÓN",
        "METH_FP": "FALSA POSICIÓN",
        "METH_NR": "NEWTON-RAPHSON",
        "METH_SEC": "SECANTE",
        "METH_PF": "PUNTO FIJO",
        "COL_ITER": "Iteración",
        "COL_XL": "x_l",
        "COL_XU": "x_u",
        "COL_XR": "x_r",
        "COL_XI": "x_i",
        "COL_XSIG": "x_i+1",
        "COL_ERR": "Error Absoluto",
        "CURVE_F": "Curva f(x) y Puntos Encontrados",
        "AXIS_X": "EJE X",
        "AXIS_Y": "EJE Y",
        "INFO_TEXT": "Esta plataforma permite encontrar las raíces de ecuaciones algebraicas y trascendentes mediante cinco métodos numéricos clásicos ejecutados de forma simultánea. El objetivo es comparar la velocidad de convergencia y la precisión de cada algoritmo para una misma función matemática.",
        "HELP_SYNTAX": "### SINTAXIS DE FUNCIONES\nLa calculadora interpreta texto natural matemático. Puedes usar:\n* **Potencias:** `x^2` o `x**2`\n* **Multiplicación implícita:** `2x` se interpreta automáticamente como `2*x`\n* **Fracciones:** `(x+1)/2`\n* **Funciones trigonométricas:** `sin(x)`, `cos(x)`, `tan(x)`\n* **Exponenciales y logaritmos:** `exp(x)` para e^x, `log(x)` para el logaritmo natural.",
        "HELP_PARAMS": "### PARÁMETROS\n* **xl y xu:** Requeridos para Bisección y Falsa Posición (deben encerrar la raíz).\n* **x0:** Requerido para Newton-Raphson y Punto Fijo como valor inicial de búsqueda.\n* **Tolerancia:** El criterio de detención. El cálculo se detendrá cuando el error absoluto sea menor a este valor.",
        "EX_1_TITLE": "Ejemplo 1: Polinomio Algebraico",
        "EX_2_TITLE": "Ejemplo 2: Ecuación Trascendente",
        "EX_3_TITLE": "Ejemplo 3: Convergencia de Punto Fijo"
    },
    "ENGLISH": {
        "TITLE": "NUMERICAL ANALYSIS PLATFORM",
        "TAB1": "EQUATION SOLVING",
        "TAB2": "REGRESSION & INTERPOLATION",
        "TAB_INFO": "INFO",
        "TAB_HELP": "HELP",
        "TAB_EXAMPLES": "EXAMPLES",
        "PARAMS": "PARAMETERS",
        "F_MAIN": "Main function f(x):",
        "F_DESP": "Isolated function g(x) (For Fixed Point):",
        "WAIT_FUNC": "Waiting for a valid function...",
        "SHOW_F": "SHOW f(x) GRAPH",
        "SHOW_G": "SHOW g(x) GRAPH",
        "LIM_INF": "Lower limit xl (or x_prev)",
        "LIM_SUP": "Upper limit xu (or x_curr)",
        "PTO_INI": "Initial point x0",
        "TOL": "Tolerance",
        "CALC_BTN": "CALCULATE ROOTS",
        "RES_TITLE": "RESULTS & ITERATIONS",
        "COMP_GRAPH": "VIEW COMPARATIVE ROOTS GRAPH",
        "NO_ROOTS": "No valid roots found to plot.",
        "ERR_SYNTAX": "ERROR in function syntax or division by zero detected. Check the input data.",
        "INFO_START": "ENTER PARAMETERS ON THE LEFT AND PRESS 'CALCULATE ROOTS'.",
        "CONSTRUCTION": "MODULE UNDER CONSTRUCTION.",
        "ERR_OPPOSITE": "ERROR: f(xl) and f(xu) do not have opposite signs.",
        "ERR_EVAL": "ERROR: Failed to evaluate limits in the function.",
        "ERR_DIV0": "ERROR: Division by zero during calculation.",
        "ERR_DIV0_FAIL": "ERROR: Division by zero. Method fails.",
        "ERR_CONVERGE": "ERROR: Method does not converge after 100 iterations.",
        "ERR_DIVERGE": "ERROR: Method diverges with this function or initial point x0.",
        "ROOT_APPROX": "Approximate Root",
        "ITERS": "Iterations",
        "METH_BIS": "BISECTION",
        "METH_FP": "FALSE POSITION",
        "METH_NR": "NEWTON-RAPHSON",
        "METH_SEC": "SECANT",
        "METH_PF": "FIXED POINT",
        "COL_ITER": "Iteration",
        "COL_XL": "x_l",
        "COL_XU": "x_u",
        "COL_XR": "x_r",
        "COL_XI": "x_i",
        "COL_XSIG": "x_i+1",
        "COL_ERR": "Absolute Error",
        "CURVE_F": "Curve f(x) and Found Points",
        "AXIS_X": "X AXIS",
        "AXIS_Y": "Y AXIS",
        "INFO_TEXT": "This platform allows finding the roots of algebraic and transcendental equations using five classic numerical methods executed simultaneously. The objective is to compare the convergence speed and precision of each algorithm for the same mathematical function.",
        "HELP_SYNTAX": "### FUNCTION SYNTAX\nThe calculator interprets natural mathematical text. You can use:\n* **Powers:** `x^2` or `x**2`\n* **Implicit multiplication:** `2x` is automatically parsed as `2*x`\n* **Fractions:** `(x+1)/2`\n* **Trigonometric functions:** `sin(x)`, `cos(x)`, `tan(x)`\n* **Exponentials and logarithms:** `exp(x)` for e^x, `log(x)` for natural logarithm.",
        "HELP_PARAMS": "### PARAMETERS\n* **xl and xu:** Required for Bisection and False Position (must enclose the root).\n* **x0:** Required for Newton-Raphson and Fixed Point as the initial search value.\n* **Tolerance:** The stopping criterion. Calculation stops when the absolute error is less than this value.",
        "EX_1_TITLE": "Example 1: Algebraic Polynomial",
        "EX_2_TITLE": "Example 2: Transcendental Equation",
        "EX_3_TITLE": "Example 3: Fixed Point Convergence"
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
        border-color: #1a73e8; box-shadow: 0 4px 10px rgba(26, 115, 232, 0.1);
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
        border-radius: 15px; background-color: #1a73e8; color: white;
        font-weight: bold; transition: all 0.3s ease; border: none; padding: 10px 20px;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #1557b0; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(26, 115, 232, 0.3);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.05); padding: 15px; border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
    .math-preview { padding: 10px 0px; margin-bottom: 5px; display: flex; justify-content: center; }
    div[data-testid="stExpander"] details summary {
        background-color: #88C7F2 !important; color: #000000 !important; border-radius: 8px; font-weight: 600;
    }
    div[data-testid="stExpander"] details summary:hover { background-color: #7ab3da !important; }
    div[data-testid="stExpander"] details summary p { font-family: 'Samsung Sharp Sans', -apple-system, sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA SUPERIOR, STEAM MENU Y TUTORIAL INYECTADO (Puro HTML estático sin onclicks)
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
.steam-dropdown a, .steam-dropdown .menu-action {
    color: #b8b6b4; padding: 10px 15px; text-decoration: none; display: block;
    border-bottom: 1px solid rgba(255,255,255,0.03); transition: background 0.2s; cursor: pointer;
}
.steam-dropdown a:hover, .steam-dropdown .menu-action:hover { background-color: #2a475e; color: #ffffff; }
.steam-right { margin-left: auto; display: flex; align-items: center; }
.steam-profile {
    color: #66c0f4; font-weight: 500; cursor: pointer; display: flex;
    align-items: center; gap: 5px; padding: 5px 10px; border-radius: 3px; transition: background 0.2s;
}
.steam-profile:hover { background-color: #2a475e; color: #ffffff; }
.hamburguesa { font-size: 16px; font-weight: 800; margin-right: 15px; }

/* CSS del Tutorial Toast y Modal */
.tut-toast {
    position: fixed; bottom: 20px; right: 20px; background: #171d25; color: white;
    padding: 15px 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    display: none; flex-direction: column; gap: 12px; z-index: 999999;
    border: 1px solid #2a475e; font-family: 'Samsung Sharp Sans', sans-serif;
}
.tut-buttons { display: flex; gap: 10px; justify-content: flex-end; }
.tut-btn-yes { background: #1a73e8; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold;}
.tut-btn-no { background: transparent; color: #b8b6b4; border: 1px solid #b8b6b4; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.tut-btn-yes:hover { background: #1557b0; }
.tut-btn-no:hover { background: #fff; color: #171d25; }

.tut-modal-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.6); display: none; justify-content: center;
    align-items: center; z-index: 1000000; backdrop-filter: blur(3px);
}
.tut-modal-box {
    background: white; padding: 30px; border-radius: 12px; max-width: 450px;
    text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2); font-family: 'Samsung Sharp Sans', sans-serif;
}
.tut-modal-box h3 { color: #1a73e8; margin-top: 0; }
.tut-modal-box p { color: #333; font-size: 15px; line-height: 1.5; margin-bottom: 25px;}
.tut-nav-btns { display: flex; justify-content: space-between; }
@media (prefers-color-scheme: dark) {
    .tut-modal-box { background: #1e1e1e; }
    .tut-modal-box p { color: #eee; }
}
</style>

<div class="steam-top-bar">
    <div class="steam-menu">
        <div class="steam-menu-item hamburguesa">&#9776;
            <div class="steam-dropdown">
                <a class="menu-action" href="?lang=es" target="_self">Español</a>
                <a class="menu-action" href="?lang=en" target="_self">English</a>
            </div>
        </div>
    </div>
    <div class="steam-logo">Universidad Veracruzana</div>
    <div class="steam-menu">
        <div class="steam-menu-item">Archivo
            <div class="steam-dropdown">
                <div class="menu-action" id="btn-reload">Recargar plataforma</div>
                <div class="menu-action" id="btn-print">Imprimir resultados</div>
            </div>
        </div>
        <div class="steam-menu-item">Ver
            <div class="steam-dropdown">
                <div class="menu-action" id="btn-fs">Pantalla Completa</div>
                <div class="menu-action" id="btn-zoom-in">Zoom +</div>
                <div class="menu-action" id="btn-zoom-out">Zoom -</div>
                <div class="menu-action" id="btn-theme">Modo Claro / Oscuro</div>
            </div>
        </div>
        <div class="steam-menu-item">Ayuda
            <div class="steam-dropdown">
                <a href="https://github.com/Azavkm/Metodos-UV" target="_blank">Repositorio de GitHub</a>
                <div class="menu-action" id="btn-tutorial">Ver Tutorial Interactivo</div>
                <div class="menu-action" id="btn-about">Acerca de...</div>
            </div>
        </div>
    </div>
    <div class="steam-right">
        <div class="steam-menu-item steam-profile">Azael
            <div class="steam-dropdown" style="left: auto; right: 0;">
                <div class="menu-action" id="btn-reset">Restablecer Sistema</div>
            </div>
        </div>
    </div>
</div>

<div id="tut-toast" class="tut-toast">
    <div style="font-weight: bold; font-size: 14px;">👋 ¿Eres nuevo por aquí?</div>
    <div style="font-size: 13px; color: #c7d5e0;">Aprende a calcular raíces paso a paso con nuestra guía rápida.</div>
    <div class="tut-buttons">
        <button class="tut-btn-no" id="tut-btn-skip">Omitir</button>
        <button class="tut-btn-yes" id="tut-btn-start">Comenzar Guía</button>
    </div>
</div>

<div id="tut-modal" class="tut-modal-overlay">
    <div class="tut-modal-box">
        <h3 id="tut-title">Título</h3>
        <p id="tut-text">Texto del paso actual.</p>
        <div class="tut-nav-btns">
            <button class="tut-btn-no" id="tut-btn-prev">Anterior</button>
            <button class="tut-btn-yes" id="tut-btn-next">Siguiente</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# EL "MOTOR INVISIBLE": JAVASCRIPT SEGURO
# ==========================================
js_code = """
<script>
    // Este script corre en un iframe seguro pero controla la página principal
    const doc = window.parent.document;
    const win = window.parent;

    // Función auxiliar para asignar clics con seguridad
    function addClick(id, action) {
        const el = doc.getElementById(id);
        if(el) { el.onclick = action; }
    }

    // LÓGICA DE LA BARRA SUPERIOR
    addClick('btn-reload', () => win.location.reload());
    addClick('btn-print', () => win.print());
    addClick('btn-fs', () => {
        if(!doc.fullscreenElement) { doc.documentElement.requestFullscreen(); }
        else { doc.exitFullscreen(); }
    });
    addClick('btn-zoom-in', () => {
        let currentZoom = parseFloat(doc.body.style.zoom || 1);
        doc.body.style.zoom = (currentZoom + 0.1).toString();
    });
    addClick('btn-zoom-out', () => {
        let currentZoom = parseFloat(doc.body.style.zoom || 1);
        doc.body.style.zoom = (currentZoom - 0.1).toString();
    });
    addClick('btn-theme', () => {
        let u = new URL(win.location.href);
        let t = u.searchParams.get('theme') === 'dark' ? 'light' : 'dark';
        u.searchParams.set('theme', t);
        win.location.href = u.toString();
    });
    addClick('btn-about', () => {
        win.alert('Plataforma de Análisis Numérico v6.0\\nDesarrollada para la Universidad Veracruzana.\\nMotor Matemático: Streamlit + SymPy');
    });
    addClick('btn-reset', () => {
        win.localStorage.clear(); win.sessionStorage.clear();
        win.location.href = win.location.pathname;
    });

    // LÓGICA DEL TUTORIAL
    const pasosTutorial = [
        {title: "¡Bienvenido a la Plataforma!", text: "Esta herramienta resuelve ecuaciones utilizando 5 métodos numéricos simultáneos. Ideal para comparar su eficiencia en tiempo real."},
        {title: "1. Ingresa tu Función", text: "En el panel izquierdo, escribe tu función f(x) usando lenguaje matemático natural. Ej: 'x^2 - 4' o 'sin(x)'. Puedes previsualizar su gráfica al instante."},
        {title: "2. Define los Parámetros", text: "Ajusta los límites inferior (xl) y superior (xu) para los métodos cerrados, y el punto inicial (x0) para los abiertos. No olvides fijar tu tolerancia."},
        {title: "3. Calcula las Raíces", text: "Haz clic en el botón azul 'CALCULAR RAÍCES'. El motor procesará todos los algoritmos a la vez."},
        {title: "4. Analiza los Resultados", text: "A la derecha verás una gráfica comparativa con las raíces encontradas por cada método. Expande cada caja para ver la tabla iterativa completa."},
        {title: "¡Todo Listo!", text: "Recuerda que puedes usar el menú superior para pantalla completa o imprimir reportes. ¡Éxito en tus cálculos!"}
    ];
    let pasoActual = 0;

    function actualizarModal() {
        doc.getElementById('tut-title').innerText = pasosTutorial[pasoActual].title;
        doc.getElementById('tut-text').innerText = pasosTutorial[pasoActual].text;
        doc.getElementById('tut-btn-prev').style.visibility = pasoActual === 0 ? 'hidden' : 'visible';
        doc.getElementById('tut-btn-next').innerText = pasoActual === pasosTutorial.length - 1 ? 'Finalizar' : 'Siguiente';
    }

    addClick('tut-btn-skip', () => {
        doc.getElementById('tut-toast').style.display = 'none';
        win.sessionStorage.setItem('tutorialVisto', 'true');
    });

    addClick('tut-btn-start', () => {
        doc.getElementById('tut-toast').style.display = 'none';
        win.sessionStorage.setItem('tutorialVisto', 'true');
        pasoActual = 0;
        doc.getElementById('tut-modal').style.display = 'flex';
        actualizarModal();
    });

    addClick('btn-tutorial', () => {
        pasoActual = 0;
        doc.getElementById('tut-modal').style.display = 'flex';
        actualizarModal();
    });

    addClick('tut-btn-prev', () => {
        if(pasoActual > 0) { pasoActual--; actualizarModal(); }
    });

    addClick('tut-btn-next', () => {
        if(pasoActual < pasosTutorial.length - 1) {
            pasoActual++; actualizarModal();
        } else {
            doc.getElementById('tut-modal').style.display = 'none';
        }
    });

    // Mostrar el toast si no se ha visto en la sesión actual
    setTimeout(() => {
        if(!win.sessionStorage.getItem('tutorialVisto')) {
            const toast = doc.getElementById('tut-toast');
            if(toast) toast.style.display = 'flex';
        }
    }, 1000);
</script>
"""
components.html(js_code, height=0, width=0)

# ==========================================
# ESTRUCTURA PRINCIPAL DE STREAMLIT
# ==========================================
# Título centrado
st.markdown(f"<h1>{t['TITLE']}</h1>", unsafe_allow_html=True)

# Creación de Pestañas Reducidas (Ayuda, Info y Ejemplos fusionadas)
tab_raices, tab_regresion, tab_ayuda = st.tabs([
    t["TAB1"], t["TAB2"], t["TAB_HELP"]
])

x = sp.Symbol('x')
transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))

# ==========================================
# FUNCIÓN PARA GENERAR GRÁFICAS
# ==========================================
def crear_grafica(func_lambdificada, titulo, raices_encontradas=None):
    x_vals = np.linspace(-100, 100, 4000)
    y_vals = np.zeros_like(x_vals)
    
    for i, val in enumerate(x_vals):
        try:
            res = func_lambdificada(val)
            y_vals[i] = float(res) if not isinstance(res, complex) else np.nan
        except:
            y_vals[i] = np.nan

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=titulo, line=dict(color='#1a73e8', width=2)))
    
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
        range=[-10, 10], tickformat="g"
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
        minor=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.08)'),
        zeroline=True, zerolinewidth=2, zerolinecolor='rgba(128,128,128,0.5)',
        range=[-10, 10], tickformat="g"
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
            f_str = st.text_input("f(x)", value="2x^2 - x - 1", label_visibility="collapsed")
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
            g_str = st.text_input("g(x)", value="(x + 1)/2x", label_visibility="collapsed")
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
                xl = st.number_input("xl", value=1.0, format="%.5f", label_visibility="collapsed")
            with c2:
                st.markdown(f"**{t['LIM_SUP']}**")
                xu = st.number_input("xu", value=2.0, format="%.5f", label_visibility="collapsed")
            
            st.markdown(f"**{t['PTO_INI']}**")
            x0 = st.number_input("x0", value=1.0, format="%.5f", label_visibility="collapsed")
            
            st.markdown(f"**{t['TOL']}**")
            tol = st.number_input("tol", value=0.001, format="%.5f", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            ejecutar = st.button(t["CALC_BTN"], use_container_width=True)

    with col_results:
        st.markdown(f"### {t['RES_TITLE']}")
        if ejecutar:
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

            except Exception as e:
                st.error(t["ERR_SYNTAX"])
        else:
            st.info(t["INFO_START"])

# ==========================================
# PESTAÑA 2: REGRESIÓN E INTERPOLACIÓN
# ==========================================
with tab_regresion:
    st.markdown(f"### {t['TAB2']}")
    st.info(t["CONSTRUCTION"])

# ==========================================
# PESTAÑA 3: AYUDA FUSIONADA (Info, Ayuda, Ejemplos)
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
    st.markdown("* **xl / xu:** `2.0` / `3.0`")
    st.markdown("* **x0:** `2.5`")
    
    st.markdown(f"#### {t['EX_2_TITLE']}")
    st.markdown("* **f(x):** `exp(-x) - x`")
    st.markdown("* **xl / xu:** `0.0` / `1.0`")
    st.markdown("* **x0:** `0.0`")

    st.markdown(f"#### {t['EX_3_TITLE']}")
    st.markdown("* **f(x):** `x^2 - x - 1`")
    st.markdown("* **g(x):** `(x + 1)^(1/2)` o `sqrt(x + 1)`")
    st.markdown("* **xl / xu:** `1.0` / `2.0`")
    st.markdown("* **x0:** `1.0`")
