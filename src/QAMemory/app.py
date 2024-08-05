import streamlit as st
from model import get_response, ChatMemory

# Inicializar la memoria de chat
if 'chat_memory' not in st.session_state:
    st.session_state.chat_memory = ChatMemory()

# Configuración de la aplicación
st.title("Chatbot con LangChain y Streamlit")

# Mostrar el historial de la conversación
def display_chat(history):
    for entry in history:
        if entry.startswith("Usuario:"):
            with st.chat_message("user",):
                st.markdown(entry[len("Usuario:"):],)
        elif entry.startswith("Asistente:"):
            with st.chat_message("assistant"):
                st.markdown(entry[len("Asistente:"):])


# Área de entrada de texto

display_chat(st.session_state.chat_memory.history)

if prompt := st.chat_input("What is up?"):
    if prompt:
        # Obtener respuesta del modelo
        response = get_response(prompt)
        
        # Mostrar la respuesta
        st.session_state.chat_memory.add_entry(prompt, response)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)       
        # Limpiar el campo de entrada


