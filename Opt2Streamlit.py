import streamlit as st
import time
import io

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Procesador OP72", layout="wide")

st.title("📂 Operacion 72 → CSV OP72")

archivo = st.file_uploader("Operacion 72", type=["txt"],accept_multiple_files=False)

# ==========================================
# FUNCIÓN GENERICA
# ==========================================
def procesar_archivo(file_bytes, mapa_campos, encabezados, filtro):
    total_bytes = len(file_bytes)
    procesado_bytes = 0
    contador = 0
    inicio_tiempo = time.time()

    output = io.StringIO()
    output.write(",".join(encabezados) + "\n")

    progress_bar = st.progress(0)
    status = st.empty()

    for linea in file_bytes.splitlines():
        procesado_bytes += len(linea)

        if linea[:2] == filtro:
            contador += 1
            fila = []

            for inicio, fin in mapa_campos:
                start = inicio - 1
                end = min(fin, len(linea))

                if start < len(linea):
                    valor = linea[start:end].decode("utf-8", errors="ignore").strip()
                else:
                    valor = ""

                fila.append(valor)

            output.write(",".join(fila) + "\n")

        # actualizar progreso
        porcentaje = procesado_bytes / total_bytes
        progress_bar.progress(min(porcentaje, 1.0))

        if procesado_bytes % (5 * 1024 * 1024) < len(linea):
            transcurrido = time.time() - inicio_tiempo
            velocidad = procesado_bytes / (1024*1024) / transcurrido if transcurrido > 0 else 0
            status.text(f"Procesando... {porcentaje*100:.2f}% | {velocidad:.2f} MB/s")

    status.text(f"✅ Finalizado | Registros: {contador}")

    return output.getvalue()


# ==========================================
# CONFIGURACIONES
# ==========================================

CONFIGS = {
    "01": {
        "mapa": [(1,2),(3,4),(5,6),(7,8),(9,11),(12,13),(14,16),(17,19),(20,27),(28,30),(31,400)],
        "encabezados": [
            "TIPO_REGISTRO","ID_SERVICIO","ID_OPERACION","TIPO_ENTIDAD_ORIGEN",
            "CLAVE_ENTIDAD_ORIGEN","TIPO_ENTIDAD_DESTINO","CLAVE_ENTIDAD_DESTINO",
            "CLAVE_ENTIDAD_GENERACION_LOTE","FECHA_TRANSFERENCIA_LOTE",
            "CONSECUTIVO_DIA","FILLER"
        ]
    },
    "02": {
        "mapa": [(1,2),(3,4),(5,6),(7,8),(9,11),(12,13),(14,16),(17,19),(20,27),(28,30),(31,400)],
        "encabezados": [
            "Tipo de Registro","Identificador de Servicio","Identificador de Operación",
            "Tipo de entidad origen","Clave de entidad origen","Tipo de entidad destino",
            "Clave de entidad destino","Clave de Entidad generación de envío de lote",
            "Fecha de transferencia de lote","Consecutivo del día","FILLER"
        ]
    },
    "03": {
        "mapa": [
            (1,2),(3,4),(5,15),(16,28),(29,46),(47,86),(87,126),(127,166),
            (167,174),(175,175),(176,177),(178,178),(179,189),(190,202),
            (203,220),(221,260),(261,300),(301,340),(341,348),(349,356),
            (357,357),(358,359),(360,400)
        ],
        "encabezados": [
            "Tipo de Registro","Clave de Operación","NSS","RFC","CURP",
            "Apellido paterno","Apellido materno","Nombres","Fecha nacimiento",
            "Sexo","Entidad","Estatus","NSS2","RFC2","CURP2","Apellido paterno2",
            "Apellido materno2","Nombres2","Fecha nacimiento2","Fecha recepción",
            "Sexo2","Entidad2","Filler"
        ]
    },
    "09": {
        "mapa": [
            (1,2),(3,4),(5,7),(8,9),(10,12),(13,14),(15,16),
            (17,24),(25,27),(28,36),(37,45),(46,400)
        ],
        "encabezados": [
            "Tipo de registro","Tipo entidad origen","Clave origen",
            "Tipo entidad destino","Clave destino","Servicio","Operación",
            "Fecha lote","Consecutivo","Registros entrada",
            "Registros salida","Filler"
        ]
    }
}

# ==========================================
# BOTONES
# ==========================================

if archivo:
    file_bytes = archivo.read()

    col1, col2, col3, col4 = st.columns(4)

    for i, key in enumerate(CONFIGS.keys()):
        with [col1, col2, col3, col4][i]:
            if st.button(f"Procesar {key}"):

                config = CONFIGS[key]

                resultado = procesar_archivo(
                    file_bytes,
                    config["mapa"],
                    config["encabezados"],
                    key.encode()
                )

                st.download_button(
                    label=f"⬇ Descargar CSV {key}",
                    data=resultado,
                    file_name=f"op72_{key}.csv",
                    mime="text/csv"
                )