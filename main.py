import streamlit as st
import yfinance as yf
import numpy as np

def AnaliseDeEntrada():
    st.title("Anlise de sequencia Numérica")
    stringNumeros = st.text_input('Entre com uma sequencia de Numeros: ',placeholder="1 2 34 2 5 1 2") 
    if stringNumeros:
        numeros = np.array(list(stringNumeros).split(" "))
        st.text(numeros)
def TCRS_Calculo():
    st.title("Taxa de Lixo")
    st.latex(r"Fp = A \times (1 + Ff + Fu + Fs) x GGm")
    st.markdown('''
        Onde:  
A = Área do imóvel edificado ou, não o sendo, do terreno  
Ff = Fator de Frequência aplicável sobre a área, de acordo com a frequência
da coleta  
Fu = Fator de Uso preponderante aplicável sobre a área, de acordo com os
registros municipais  
Fs = Fator Socioeconômico aplicável sobre a área, de acordo com o padrão
CGm = Custo Global Anual por m² em dourados é de R$ 1,15 que é o valor referente a ser usado.    
        ''')
    A = st.number_input("Entre com a  área do imóvel: ",min_value=0.00)
    Ff = st.number_input("Frequência da coleta: ",min_value=1,max_value=6)
    match Ff:
        case 1: Fs = 0.010989
        case 2: Fs = 0.043956
        case 3: Fs = 0.098901
        case 4: Fs = 0.175824
        case 5: Fs = 0.274725
        case 6: Fs = 0.395605

    Fu = st.selectbox('Select', ["Residencial","Misto","Serviço","Comercial I","Industrial I","Público","Outros"])
    match Fu:
        case "Residencial": Fu = 0.010989
        case "Misto": Fu = 0.098901
        case "Serviço": Fu = 0.175824
        case "Comercial I": Fu = 0.274725
        case "Industrial I": Fu = 0.395605
        case "Público": Fu = 0.010989
        case "Outros": Fu = 0.043956

    Fs = st.selectbox("Fator Socioeconômico aplicável ",["Precária","Popular","Médio","Fino","Luxo"])
    match Fs:
        case "Precária": Fs = 0.008264
        case "Popular": Fs = 0.033056
        case "Médio": Fs = 0.132224
        case "Fino": Fs = 0.297504
        case "Luxo": Fs = 0.528952
    
    CGm = 1.15

    TRSC = lambda A,Ff,Fu,Fs,CGm: (A * (1 + Ff + Fu + Fs))*CGm
    if A and Ff and Fu and Fs and CGm:
        st.text(f"O valor da taxa de lixo é de : {round(TRSC(A,Ff,Fu,Fs,CGm),2)}")
    else:
        st.text("Ainda não foi informada nenhuma das variaveis.")


def jurus():
    st.title("Jurus simples ")
    st.latex(r"J = P \cdot i \cdot t")
    st.text("J: Jurus\nP: Capital \n i: Taxa \n t: tempo meses")
    p = st.number_input("Entre com a Capital: ",min_value=0.00)
    i = st.number_input("Entre com a Taxa: ",min_value=0.00)
    t = st.number_input("Entre com a Tempo meses: ",min_value=0)
    J = lambda Capital,imposto,tempo: Capital*imposto*tempo
    M = lambda Capital,imposto,tempo: Capital*(1 + imposto*tempo)
    if p and i and t:
        st.text(f"O jurus vai ficar de {J(p,i,t)} em {t} meses.Com montante de {round(M(p,i,t),2)}")
    else:
        st.text("Falta de Imformação.")
    
    st.title("Jurus Composto ")
    st.latex(r" J = P \cdot \left( (1 + i)^t - 1 \right)")
    st.text("J: Jurus\nP: Capital \n i: Taxa \n t: tempo meses")
    cp = st.number_input("Entre com Capital: ",min_value=0.00)
    ci = st.number_input("Entre com Taxa: ",min_value=0.00)
    ct = st.number_input("Entre Tempo meses: ",min_value=0)
    cJ = lambda Capital,imposto,tempo: Capital*((1+imposto)**tempo - 1)
    if cp and ci and ct:
        st.text(f"O jurus vai ficar de {round(cJ(cp,ci,ct))} em {ct} meses. Montante {cp + round(cJ(cp,ci,ct)) }")
    else:
        st.text("Falta de Imformação.")


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

with st.expander("Calculo da taxa do lixo"):
    TCRS_Calculo()

with st.expander("Analise de entrada numérica"):
    AnaliseDeEntrada()