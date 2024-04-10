import streamlit as st
import time
import datetime
import requests
import json
from openai import OpenAI

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

def set_state(i):
    st.session_state.stage = i


def guardarMensaje(mensaje, state):
    print(f"Guardando.... {mensaje}")
    st.session_state.messages.append({"role": "user", "content": mensaje})
    # Muestra el mensaje del usuario en el contenedor de mensajes del usuario
    
    set_state(state)

def guardarEdad(edad, state):
    print(f"Guardando.... {edad}")
    st.session_state.messages.append({"role": "user", "content": edad})
    # Muestra el mensaje del usuario en el contenedor de mensajes del usuario
    
    set_state(state)

def guardarOrigen(origen, state):
    print(f"Guardando.... {origen}")
    st.session_state.messages.append({"role": "user", "content": origen})
    # Muestra el mensaje del usuario en el contenedor de mensajes del usuario
    
    set_state(state)

def guardarFecha(fecha, state):
    print(f"Guardando.... {fecha}")
    st.session_state.messages.append({"role": "user", "content": fecha})
    # Muestra el mensaje del usuario en el contenedor de mensajes del usuario
    
    set_state(state)

st.title("iTravel Assistant - Planificación de Viajes")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"], organization=st.secrets["organization"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'stage' not in st.session_state:
    st.session_state.stage = 0

if 'estadoEdad' not in st.session_state:
    st.session_state.estadoEdad = 0

if 'estadoOrigen' not in st.session_state:
    st.session_state.estadoOrigen = 0

if 'estadoFecha' not in st.session_state:
    st.session_state.estadoFecha = 0

# Mostrar mensajes del historial en la recarga de la aplicación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Preguntas secuenciales
questions = [
    "Hola, bienvenido a iTravel Assistant. Estoy aquí para ayudarte en la planificación de tu viaje. Te haré algunas preguntas que me permitirán recomendarte un destino turístico. ¿Estás de acuerdo?",
    "Con qué genero te identificas? (Hombre, Mujer, Otro)",
    "Cuántos años tienes?",
    "Cuál es tu preferencia de viaje? (Ciudad, Montaña, Mar)",
    "Desde qué país saldrás?",
    "y por último, en qué fecha planeas viajar?",
    # Agrega más preguntas según sea necesario
]

print(f"Stage_inicial: {st.session_state.stage}")

# Índice para rastrear la pregunta actual
if "indice" not in st.session_state:
    st.session_state.indice = 0
    # Mostrar el primer mensaje al iniciar la aplicación
    current_question = questions[st.session_state.indice]
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(current_question))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.indice = 1

if st.session_state.stage == 0:
    print("dentro de stage == 0")
    if st.button('Si', on_click=guardarMensaje, args=["Si", 1]):
        with st.chat_message("user"):
            st.markdown("Si")

    if st.button('No', on_click=guardarMensaje, args=["No", 1]):
        with st.chat_message("user"):
            st.markdown("No")
    
    

if st.session_state.stage == 1:
    print("dentro de stage == 1")
    current_question = questions[st.session_state.indice]
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(current_question))
    # Agrega la respuesta del asistente al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.button('Hombre', on_click=guardarMensaje, args=["Hombre", 2])

    st.button('Mujer', on_click=guardarMensaje, args=["Mujer", 2])

    st.button('Otro', on_click=guardarMensaje, args=["Otro", 2])

    st.session_state.indice = 2
    

print(f"Stage_final: {st.session_state.stage}")

if st.session_state.stage == 2:
    if st.session_state.estadoEdad == 0:
        print("dentro de stage == 2")
        current_question = questions[st.session_state.indice]
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(current_question))
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    edad = st.selectbox(

        'Selecciona tu edad',
        ['None','18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60'],
        placeholder="Selecciona una opcion"
        )
   

    if edad  == 'None':
        st.session_state.estadoEdad = 1
    elif edad != 'None':
        with st.chat_message("user"):
            st.markdown(edad)
        st.session_state.indice = 3
        guardarEdad(edad, 3)



if st.session_state.stage == 3:
    print("dentro de stage == 3")
    current_question = questions[st.session_state.indice]
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(current_question))
    # Agrega la respuesta del asistente al historial de chat
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.button('Ciudad', on_click=guardarMensaje, args=["Ciudad", 4])

    st.button('Montaña', on_click=guardarMensaje, args=["Montaña", 4])

    st.button('Mar', on_click=guardarMensaje, args=["Mar", 4])

    st.session_state.indice = 4


if st.session_state.stage == 4:
    
    if st.session_state.estadoOrigen == 0:
        print("dentro de stage == 4")
        current_question = questions[st.session_state.indice]
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(current_question))
        # Agrega la respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    paisOrigen = st.selectbox(
        'Seleccione país de origen',
        ['None','Austria', 'Bulgaria','Suiza','Chipre','Alemania','Dinamarca','Estonia','Grecia','España','Finlandia','Francia','Croacia','Irlanda','Italia','Lituania','Luxemburgo','Letonia','Macedonia del Norte','Malta','Noruega','Polonia','Portugal','Suecia','Eslovenia','Reino Unido']
        )
    

    if paisOrigen  == 'None':
            st.session_state.estadoOrigen = 1
    elif paisOrigen != 'None':
        with st.chat_message("user"):
            st.markdown(paisOrigen)
        st.session_state.indice = 5
        guardarOrigen(paisOrigen, 5)

 

if st.session_state.stage == 5:
    
    if st.session_state.estadoFecha == 0:
        print("dentro de stage == 5")
        current_question = questions[st.session_state.indice]
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(current_question))
        # Agrega la respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": response})

    fechaViaje = st.date_input("Fecha viaje", value=None)

    print(fechaViaje)
    if fechaViaje  is None:
        st.session_state.estadoFecha = 1
    else:
        with st.chat_message("user"):
            st.markdown(fechaViaje)
        st.session_state.indice = 6
        guardarFecha(fechaViaje, 6)


# Enviar datos a través de una URL (API)
if st.session_state.stage == 6:
    
    pais_origen = st.session_state.messages[9]["content"]
    edad = st.session_state.messages[5]["content"]
    genero = map_gender(st.session_state.messages[3]["content"])
    preferencia_viaje = map_pref(st.session_state.messages[7]["content"])
    fecha_viaje = st.session_state.messages[11]["content"]

    # Cambia la URL de la API a la que deseas enviar los datos
    api_url = "http://200.79.113.129/api/"
    

    fecha_viaje_str = fecha_viaje.strftime("%Y-%m-%d")

    # Parámetros a enviar
    params = {
        "pais_origen": pais_origen,
        "age": edad,
        "sex": genero,
        "typo": preferencia_viaje,
        "fecha_inicio": fecha_viaje_str
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
        prompt = f"Dame una breve descripción de {pais_destino} y dame 3 lugares para visitar en dicho país."
        mensaje_asistente = f"De acuerdo con tus preferencias, te recomiendo visitar {pais_destino}."

        with st.chat_message("assistant"):
                    st.write_stream(response_generator(mensaje_asistente))
        st.session_state.messages.append({"role": "assistant", "content": mensaje_asistente})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                    messages=[
                        {"role":"user", "content": prompt}
                    ],
                    stream=True,
            )
            
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            

        
    else:
        error_mensaje = "Hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde."
        with st.chat_message("assistant"):
            st.write_stream(response_generator(error_mensaje))
        st.session_state.messages.append({"role": "assistant", "content": error_mensaje})
