import streamlit as st
import subprocess
import shlex

# Función para obtener el enlace de descarga usando yt-dlp
def obtener_enlace_descarga(url_video):
    comando = f"yt-dlp -f bestvideo -g {url_video}"
    proceso = subprocess.run(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if proceso.returncode == 0:
        return proceso.stdout.strip()  # Retorna el enlace de descarga
    else:
        st.error("Error al obtener el enlace de descarga: " + proceso.stderr)
        return None

# Interfaz de usuario de Streamlit
def main():
    st.title("Obtener enlace de descarga de YouTube")
    
    url_video = st.text_input("Ingresa la URL del video de YouTube:")
    
    if url_video:
        enlace_descarga = obtener_enlace_descarga(url_video)
        if enlace_descarga:
            st.success("Enlace de descarga obtenido con éxito:")
            st.write(enlace_descarga)
            st.markdown(f"[Descargar Video]({enlace_descarga})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
