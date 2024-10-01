import streamlit as st

def calcIMC():
    IMC = lambda peso,altura : peso/(altura*altura)
    st.title("Caculadora de IMC")
    st.latex(r"\text{IMC} = \frac{\text{Peso}}{\text{Altura}^2}")
    st.image("Imagens/IMCTable.png")
    peso = st.number_input("Entrada de Peso: ",min_value=0.00)
    altura = st.number_input("Entrada de altura: ",min_value=0.00)
    if peso and altura:
        st.text(f"Seu IMC é de {round(IMC(peso,altura),2)}.")
    else:
        st.text("Não foi dado um dos valores.")


st.title("Atividade I - Streamlit")

calcIMC()