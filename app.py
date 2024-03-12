import streamlit as st
import time
import requests
import json

# Streamed response emulator
def response_generator(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.05)

# Función para mapear géneros
def map_gender(gender):
    gender_mapping = {"Hombre": "M", "Mujer": "F", "Otro": "O"}
    return gender_mapping.get(gender, gender)

# Función para mapear Preferencia
def map_pref(preferencia):
    pref_mapping = {"Ciudad": "city", "Montaña": "mnt", "Mar": "sea"}
    return pref_mapping.get(preferencia, preferencia)

st.title("iTravel Assistant - Planificación de Viajes")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial en la recarga de la aplicación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Preguntas secuenciales
questions = [
    "Hola, bienvenido a iTravel Assistant. Estoy aquí para ayudarte en la planificación de tu viaje. Te haré algunas preguntas que me permitirán recomendarte un destino turístico. ¿Estás de acuerdo?",
    "Muy bien!, favor dame tu nombre",
    "Con qué genero te identificas? (Hombre, Mujer, Otro)",
    "Cuántos años tienes?",
    "Cuál es tu preferencia de viaje? (Ciudad, Montaña, Mar)",
    "Desde qué país saldrás?",
    "y por último, en qué fecha planeas viajar? (AAAA-MM-DD)",
    # Agrega más preguntas según sea necesario
]

# Índice para rastrear la pregunta actual
if "indice" not in st.session_state:
    st.session_state.indice = 0
    # Mostrar el primer mensaje al iniciar la aplicación
    current_question = questions[st.session_state.indice]
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(current_question))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.indice += 1

if prompt := st.chat_input("Mensaje iTravel"):
    # Agrega el mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Muestra el mensaje del usuario en el contenedor de mensajes del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    # Muestra la pregunta del asistente en el contenedor de mensajes del asistente
    if st.session_state.indice < len(questions):
        current_question = questions[st.session_state.indice]
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(current_question))
        # Agrega la respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Incrementa el índice para la siguiente pregunta
        st.session_state.indice += 1

# Enviar datos a través de una URL (API)
if len(st.session_state.messages) == 14:
    pais_origen = st.session_state.messages[11]["content"]
    edad = st.session_state.messages[7]["content"]
    genero = map_gender(st.session_state.messages[5]["content"])
    preferencia_viaje = map_pref(st.session_state.messages[9]["content"])
    fecha_viaje = st.session_state.messages[13]["content"]

    # Cambia la URL de la API a la que deseas enviar los datos
    api_url = "http://200.79.113.129/api/"
    
    # Parámetros a enviar
    params = {
        "pais_origen": pais_origen,
        "age": edad,
        "sex": genero,
        "typo": preferencia_viaje,
        "fecha_inicio": fecha_viaje
    }

    # Envía la solicitud a la API
    responseAPI = requests.get(api_url, params=params)

    # Imprimir la URL final
    url_final = f"{api_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    print(f"URL Final: {url_final}")

    # Procesar la respuesta de la API
    api_response = json.loads(responseAPI.text)
    if api_response.get("status") == "success":
        pais_destino = api_response.get("pais_destino")
        mensaje_asistente = f"De acuerdo con tus preferencias, te recomiendo visitar {pais_destino}."
        with st.chat_message("assistant"):
            st.write_stream(response_generator(mensaje_asistente))
        st.session_state.messages.append({"role": "assistant", "content": mensaje_asistente})
    else:
        error_mensaje = "Hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde."
        with st.chat_message("assistant"):
            st.write_stream(response_generator(error_mensaje))
        st.session_state.messages.append({"role": "assistant", "content": error_mensaje})

# Mostrar la tabla con la biblioteca de mensajes
#st.table(st.session_state.messages)