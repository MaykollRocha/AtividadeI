import streamlit as st
import yfinance as yf


def jurus():
    st.title("Jurus simples ")
    st.latex(r"J = P \cdot i \cdot t")
    st.text("J: Jurus\nP: Capital \n i: Taxa \n t: tempo")

def cotacao_atual():
    moedas = {
            "Dólar Americano":"USD",
            "Euro":"EUR", 
            "Libra Esterlina":"GBP",
            "Iene Japonês":"JPY",
            "Dólar Australiano":"AUD",
            "Dólar Canadense":"CAD", 
            "Franco Suíço":"CHF", 
            "Real Brasileiro":"BRL",
    }

    st.title("Cotações")
    moeda1 = st.selectbox('Valor da Moeda1', [k for k in moedas],0)
    moeda2 = st.selectbox('Valor da Moeda2', [k for k in moedas],1)
    valor = st.number_input("Valor de Comparação",min_value=0.00,step=1.00)
    cotacao = round(yf.Ticker(f'{moedas[moeda1]}{moedas[moeda2]}=X').info['bid'],2)
    st.text(f"De {moeda1} para {moeda2} será de {cotacao} {moedas[moeda2]}")
    st.text(f"Assim sendo {valor}{moedas[moeda1]} é igual a {round(valor*cotacao,2)} {moedas[moeda2]} ")

def calcIMC():
    IMC = lambda peso,altura : peso/(altura*altura)
    st.title("Caculadora de IMC")
    st.latex(r"\text{IMC} = \frac{\text{Peso}}{\text{Altura}^2}")
    st.image("Imagens/IMCTable.png")
    peso = st.number_input("Entrada de Peso: ",min_value=0.00)
    altura = st.number_input("Entrada de altura: ",min_value=0.00)
    if peso and altura:
        IMC_atual = IMC(peso,altura)
        st.text(f"Seu IMC é de {round(IMC_atual,2)}.")
        if IMC_atual < 20:
            IMC_atual = "Abaixo do Peso"
        elif IMC_atual < 25:
            IMC_atual = "Peso Normal"
        elif IMC_atual < 30:
            IMC_atual = "Excesso de Peso"
        elif IMC_atual < 35:
            IMC_atual = "Obesidade"
        else:
            IMC_atual = "Super Obesidade"
        st.text(f"Na tabela você se encaixa no quadro de {IMC_atual}")
          
    else:
        st.text("Não foi dado um dos valores.")


st.title("Atividade I - Streamlit")

with st.expander("IMC calculadora"):
    calcIMC()

with st.expander("Cotações"):
    cotacao_atual()

with st.expander("Jurus Simples e Composto"):
    jurus()