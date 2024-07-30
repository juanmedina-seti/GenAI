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
            st.text_area("Usuario", value=entry[len("Usuario:"):], height=50, key=entry)
        elif entry.startswith("Asistente:"):
            st.text_area("Asistente", value=entry[len("Asistente:"):], height=50, key=entry, disabled=True)

# Área de entrada de texto
user_input = st.text_input("Escribe tu mensaje:", "")

if st.button("Enviar"):
    if user_input:
        # Obtener respuesta del modelo
        response = get_response(user_input)
        
        # Mostrar la respuesta
        st.session_state.chat_memory.add_entry(user_input, response)
        
        # Limpiar el campo de entrada
        st.text_input("Escribe tu mensaje:", "", key="new_input")

# Mostrar el historial de conversación
display_chat(st.session_state.chat_memory.history)
