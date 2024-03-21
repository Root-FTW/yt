import streamlit as st
import subprocess
import shlex

# Función para obtener el enlace de descarga usando yt-dlp
def obtener_enlace_descarga(url_video):
    comando = f"yt-dlp -f b -g {url_video}"
    proceso = subprocess.run(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if proceso.returncode == 0:
        enlace = proceso.stdout.strip()
        return enlace
    else:
        st.error("Error al obtener el enlace de descarga: " + proceso.stderr)
        return None

def add_bookmark():
    st.sidebar.markdown("Para añadir esta página a tus marcadores, presiona `Ctrl+D` en Windows/Linux o `Cmd+D` en macOS.")

def main():
    st.title("BuscaLink")
    st.header("Descarga tu video favorito")
    st.subheader("Soporte para YouTube, Twitter, Facebook:")
    
    # Botón en la barra lateral para instrucciones de marcadores
    add_bookmark()
    
    url_video = st.text_input("Ingresa la URL del video:")
    
    if st.button("Analizar"):
        if url_video:
            enlace_descarga = obtener_enlace_descarga(url_video)
            if enlace_descarga:
                st.success("Enlace de descarga obtenido con éxito:")
                st.markdown(f'<a href="{enlace_descarga}" download><button>Descargar Video</button></a>', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresa una URL válida.")
    
    # Agrega la leyenda personalizada en el pie de página
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 12px; /* Tamaño de la fuente más pequeño */
        color: grey; /* Color de la fuente en gris */
    }
    </style>
    <div class="footer">
    <p>Made with ❤️ by <a href='https://www.linkedin.com/in/jonathanftw/' style='color: grey;'>Jonathan Paz</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
