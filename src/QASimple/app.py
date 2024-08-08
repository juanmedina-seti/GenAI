import streamlit as st
from QASimple.chain import get_response

# Configuración de la aplicación
st.title("Chatbot con LangChain y Streamlit")

# Área de entrada de texto
user_input = st.text_input("Escribe tu pregunta:")
if st.button("Preguntar"):

    # Obtener respuesta del modelo
    response = get_response(user_input)
    
    # Mostrar la respuesta
    #st.write("Respuesta:", response)
    st.markdown(response)


