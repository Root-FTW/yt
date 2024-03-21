import streamlit as st
import subprocess
import shlex

# Función para obtener el enlace de descarga usando yt-dlp
def obtener_enlace_descarga(url_video):
    # Comando para obtener el mejor formato que incluye video y audio en un solo archivo
    comando = f"yt-dlp -f best -g {url_video}"
    proceso = subprocess.run(shlex.split(comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if proceso.returncode == 0:
        enlace = proceso.stdout.strip()  # Retorna el enlace de descarga
        return enlace
    else:
        st.error("Error al obtener el enlace de descarga: " + proceso.stderr)
        return None

# Interfaz de usuario de Streamlit
def main():
    st.title("Obtener enlace de descarga de YouTube")
    
    url_video = st.text_input("Ingresa la URL del video de YouTube:")
    
    # Botón "Analizar"
    if st.button("Analizar"):
        if url_video:
            enlace_descarga = obtener_enlace_descarga(url_video)
            if enlace_descarga:
                st.success("Enlace de descarga obtenido con éxito:")
                # Mostrar el enlace de descarga como un botón
                st.markdown(f'<a href="{enlace_descarga}" download><button>Descargar Video</button></a>', unsafe_allow_html=True)
        else:
            st.error("Por favor, ingresa una URL válida.")

if __name__ == "__main__":
    main()
