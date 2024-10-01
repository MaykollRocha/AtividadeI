import streamlit as st

def calcIMC():
    st.title("Caculadora de IMC")
    st.latex(r"\text{IMC} = \frac{\text{Peso}}{\text{Altura}^2}")
    st.image("Imagens/IMCTable.png")


st.title("Atividade I - Streamlit")

calcIMC()