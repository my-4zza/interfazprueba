# ==========================================
# BARRA SUPERIOR ESTILO WINDOWS / STEAM FUNCIONAL
# ==========================================
st.markdown("""
<style>
.steam-top-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 40px;
    background-color: #171d25;
    color: #b8b6b4;
    display: flex;
    align-items: center;
    padding: 0 15px;
    z-index: 999999;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 13px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
}
.steam-logo {
    font-weight: 700;
    color: #c7d5e0;
    margin-right: 25px;
    font-size: 14px;
    letter-spacing: 0.5px;
}
.steam-menu {
    display: flex;
    gap: 5px;
}
.steam-menu-item {
    cursor: pointer;
    padding: 5px 12px;
    border-radius: 3px;
    position: relative;
    transition: background 0.2s, color 0.2s;
}
.steam-menu-item:hover {
    background-color: #2a475e;
    color: #ffffff;
}
.steam-dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #171d25;
    min-width: 180px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.6);
    z-index: 1;
    border-radius: 0 0 4px 4px;
    overflow: hidden;
}
.steam-menu-item:hover .steam-dropdown {
    display: block;
}
.steam-dropdown a {
    color: #b8b6b4;
    padding: 10px 15px;
    text-decoration: none;
    display: block;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: background 0.2s;
}
.steam-dropdown a:hover {
    background-color: #2a475e;
    color: #ffffff;
}
.steam-right {
    margin-left: auto;
    display: flex;
    align-items: center;
}
.steam-profile {
    color: #66c0f4;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    border-radius: 3px;
    transition: background 0.2s;
}
.steam-profile:hover {
    background-color: #2a475e;
    color: #ffffff;
}
.hamburguesa {
    font-size: 16px;
    font-weight: 800;
    margin-right: 15px;
}
</style>

<div class="steam-top-bar">
<div class="steam-menu">
<div class="steam-menu-item hamburguesa">&#9776;
<div class="steam-dropdown">
<a href="javascript:void(0)" onclick="let u = new URL(window.location.href); u.searchParams.set('lang', 'es'); window.location.href = u.toString();">Español</a>
<a href="javascript:void(0)" onclick="let u = new URL(window.location.href); u.searchParams.set('lang', 'en'); window.location.href = u.toString();">English</a>
</div>
</div>
</div>
<div class="steam-logo">Universidad Veracruzana</div>
<div class="steam-menu">
<div class="steam-menu-item">Archivo
<div class="steam-dropdown">
<a href="javascript:void(0)" onclick="window.location.reload();">Recargar plataforma</a>
<a href="javascript:void(0)" onclick="window.print();">Imprimir resultados</a>
</div>
</div>
<div class="steam-menu-item">Ver
<div class="steam-dropdown">
<a href="javascript:void(0)" onclick="if(!document.fullscreenElement){document.documentElement.requestFullscreen();}else{document.exitFullscreen();}">Pantalla Completa</a>
<a href="javascript:void(0)" onclick="document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString();">Zoom +</a>
<a href="javascript:void(0)" onclick="document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) - 0.1).toString();">Zoom -</a>
<a href="javascript:void(0)" onclick="let u = new URL(window.location.href); let t = u.searchParams.get('theme') === 'dark' ? 'light' : 'dark'; u.searchParams.set('theme', t); window.location.href = u.toString();">Modo Claro / Oscuro</a>
</div>
</div>
<div class="steam-menu-item">Ayuda
<div class="steam-dropdown">
<a href="https://github.com/Azavkm/Metodos-UV" target="_blank">Repositorio de GitHub</a>
<a href="javascript:void(0)" onclick="alert('Plataforma de Análisis Numérico v6.0\\\\nDesarrollada para la Universidad Veracruzana.\\\\nMotor Matemático: Streamlit + SymPy');">Acerca de...</a>
</div>
</div>
</div>
<div class="steam-right">
<div class="steam-menu-item steam-profile">Azael
<div class="steam-dropdown" style="left: auto; right: 0;">
<a href="javascript:void(0)" onclick="localStorage.clear(); sessionStorage.clear(); window.location.href = window.location.pathname;">Restablecer Sistema</a>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
