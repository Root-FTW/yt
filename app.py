import streamlit as st
import subprocess
import shlex
import json

# Función para obtener el enlace de descarga usando yt-dlp
def obtener_enlace_descarga(url_video, formato, solo_audio=False):
    if solo_audio:
        comando = f"yt-dlp -x --audio-format mp3 -g {url_video}"
    else:
        comando = f"yt-dlp -f {formato} -g {url_video}"
    try:
        proceso = subprocess.run(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proceso.check_returncode()
        enlace = proceso.stdout.strip()
        return enlace
    except subprocess.CalledProcessError as e:
        st.error(f"Error al obtener el enlace de descarga (yt-dlp): {e}")
        if "ERROR: Unsupported URL" in e.stderr:
            st.error("Parece que la URL proporcionada no es compatible.")
        elif "ERROR: Video unavailable" in e.stderr:
            st.error("El video no está disponible o es privado.")
        else:
            st.error(f"Detalles del error: {e.stderr}")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None

def obtener_info_video(url_video):
    comando = f"yt-dlp -j {url_video}"
    try:
        proceso = subprocess.run(shlex.split(comando), capture_output=True, text=True, check=True)
        info = json.loads(proceso.stdout)
        return info
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        st.error(f"Error al obtener información del video: {e}")
        return None

def add_bookmark():
    st.sidebar.markdown("Para añadir esta página a tus marcadores, presiona `Ctrl+D` en Windows/Linux o `Cmd+D` en macOS.")

def main():
    st.title("BuscaLink")
    add_bookmark()

    url_video = st.text_input("Soporte para YouTube, Twitter, Facebook y muchos más:", value="")

    formatos_disponibles = {
        "Mejor calidad": "b",
        "MP4 (720p)": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "WebM (1080p)": "bv*[ext=webm]+ba[ext=webm]/b[ext=webm]",
        "Solo Audio (MP3)": "ba/b",
    }

    formato_seleccionado = st.selectbox("Selecciona el formato de descarga:", options=list(formatos_disponibles.keys()))
    solo_audio = st.checkbox("Descargar solo audio (MP3)")

    if st.button("Analizar"):
        if url_video:
            info_video = obtener_info_video(url_video)
            if info_video:
                st.write(f"**Título:** {info_video.get('title', 'No disponible')}")
                st.write(f"**Duración:** {info_video.get('duration_string', 'No disponible')}")
                st.write(f"**Canal:** {info_video.get('channel', 'No disponible')}")

            with st.spinner("Obteniendo enlace de descarga..."):
                enlace_descarga = obtener_enlace_descarga(url_video, formatos_disponibles[formato_seleccionado], solo_audio)
            if enlace_descarga:
                st.success("Enlace de descarga obtenido con éxito:")
                if solo_audio:
                    st.markdown(f'<a href="{enlace_descarga}" download><button>Descargar Audio</button></a>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<a href="{enlace_descarga}" download><button>Descargar Video</button></a>', unsafe_allow_html=True)
                url_video = ""
        else:
            st.error("Por favor, ingresa una URL válida.")
        st.markdown("[Lista de sitios soportados por yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)")

    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: grey;
    }
    </style>
    <div class="footer">
    <p>Made with ❤️ by <a href='https://www.linkedin.com/in/jonathanftw/' style='color: grey;'>Jonathan Paz</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
