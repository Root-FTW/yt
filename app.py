import streamlit as st
import subprocess
import shlex
import requests
import tempfile
from pathlib import Path

# Función para descargar el video y subirlo a tmpfiles.org
def descargar_y_subir(url_video):
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = Path(tmpdirname) / "video.mp4"
        comando = f"yt-dlp -f b -o {file_path} {url_video}"
        proceso = subprocess.run(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if proceso.returncode == 0:
            # Subir el archivo a tmpfiles.org
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post("https://tmpfiles.org/api/v1/upload", files=files)
                if response.ok:
                    return response.text.strip()
                else:
                    st.error("Error al subir el archivo a tmpfiles.org")
                    return None
        else:
            st.error("Error al descargar el video: " + proceso.stderr)
            return None

def main():
    st.title("Descarga de Videos")
    url_video = st.text_input("Ingresa la URL del video:")
    
    if st.button("Analizar"):
        if url_video:
            if "tiktok.com" in url_video or "reddit.com" in url_video:
                # Procesar para TikTok o Reddit
                enlace_tmpfiles = descargar_y_subir(url_video)
                if enlace_tmpfiles:
                    st.success("Video procesado con éxito:")
                    st.markdown(f'<a href="{enlace_tmpfiles}" target="_blank"><button>Descargar Video</button></a>', unsafe_allow_html=True)
            else:
                # Procesamiento normal
                enlace_descarga = obtener_enlace_descarga(url_video)  # Asume que esta función ya existe en tu script
                if enlace_descarga:
                    st.success("Enlace de descarga obtenido con éxito:")
                    st.markdown(f'<a href="{enlace_descarga}" target="_blank"><button>Descargar Video</button></a>', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresa una URL válida.")

if __name__ == "__main__":
    main()
