import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def JogoDaVelha():
    # Função para inicializar o tabuleiro
    def inicializar_tabuleiro():
        return np.full((3, 3), '')

    # Função para verificar se há um vencedor
    def verificar_vencedor(tabuleiro):
        # Verificar linhas
        for linha in tabuleiro:
            if linha[0] == linha[1] == linha[2] != '':
                return linha[0]

        # Verificar colunas
        for col in range(3):
            if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] != '':
                return tabuleiro[0][col]

        # Verificar diagonais
        if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '':
            return tabuleiro[0][0]
        if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != '':
            return tabuleiro[0][2]

        return None

    # Função para verificar se há empate
    def verificar_empate(tabuleiro):
        return '' not in tabuleiro

    # Função para renderizar o tabuleiro e capturar a jogada
    def exibir_tabuleiro(tabuleiro, jogador_atual):
        col1, col2, col3 = st.columns(3)
        for i in range(3):
            with [col1, col2, col3][i]:
                for j in range(3):
                    if st.button(f'{tabuleiro[i][j] or " "}', key=f'{i}-{j}'):
                        if tabuleiro[i][j] == '':
                            tabuleiro[i][j] = jogador_atual
                            return True
        return False

    # Função para trocar o jogador
    def trocar_jogador(jogador_atual):
        return 'O' if jogador_atual == 'X' else 'X'

    # Inicializando o estado da sessão
    if 'tabuleiro' not in st.session_state:
        st.session_state['tabuleiro'] = inicializar_tabuleiro()
        st.session_state['jogador_atual'] = 'X'
        st.session_state['vencedor'] = None

    # Cabeçalho do jogo
    st.title("Jogo da Velha")
    st.text("Não funciona muito bem mas da pro gasto(Culpa dos constante recarregamento), e é JxJ")
    # Exibir o tabuleiro e capturar a jogada
    if st.session_state['vencedor'] is None:
        jogada_feita = exibir_tabuleiro(st.session_state['tabuleiro'], st.session_state['jogador_atual'])

        # Verificar se houve uma jogada
        if jogada_feita:
            # Verificar se há um vencedor
            st.session_state['vencedor'] = verificar_vencedor(st.session_state['tabuleiro'])

            # Verificar se houve empate
            if st.session_state['vencedor'] is None and verificar_empate(st.session_state['tabuleiro']):
                st.session_state['vencedor'] = 'Empate'

            # Trocar de jogador
            if st.session_state['vencedor'] is None:
                st.session_state['jogador_atual'] = trocar_jogador(st.session_state['jogador_atual'])

    # Exibir o resultado final
    if st.session_state['vencedor'] is not None:
        if st.session_state['vencedor'] == 'Empate':
            st.subheader("O jogo terminou em empate!")
        else:
            st.subheader(f"O jogador {st.session_state['vencedor']} venceu!")

        # Botão para reiniciar o jogo
        if st.button("Reiniciar Jogo"):
            st.session_state['tabuleiro'] = inicializar_tabuleiro()
            st.session_state['jogador_atual'] = 'X'
            st.session_state['vencedor'] = None

def DespesasMensais():
 # Título do app
    st.title("Calculadora de Despesas Mensais")

    # Inserir orçamento total
    orçamento = st.number_input("Insira o seu orçamento mensal:", min_value=0.0, format="%.2f")

    # Inicializando o dicionário de despesas na sessão do usuário (preservado durante a interação)
    if 'despesas' not in st.session_state:
        st.session_state['despesas'] = {}

    # Formulário para adicionar despesas
    st.header("Adicionar nova despesa")
    with st.form(key='form_despesa'):
        nome = st.text_input("Nome da despesa:")
        descricao = st.text_input("Descrição da despesa:")
        valor = st.number_input("Valor da despesa:", min_value=0.0, format="%.2f")
        
        # Botão para adicionar a despesa
        submit_button = st.form_submit_button(label='Adicionar Despesa')
        
        if submit_button and nome:
            st.session_state['despesas'][nome] = {'descrição': descricao, 'valor': valor}
            st.success(f"Despesa '{nome}' adicionada com sucesso!")

    # Exibir despesas adicionadas
    despesas = st.session_state['despesas']
    if despesas:
        st.subheader("Despesas Adicionadas")
        total_despesas = 0.0
        labels = []
        valores = []
        
        # Exibir as despesas e calcular o total
        for nome, info in despesas.items():
            st.write(f"**{nome}**: {info['descrição']} - R${info['valor']:.2f}")
            total_despesas += info['valor']
            labels.append(nome)
            valores.append(info['valor'])
        
        # Cálculo do valor que sobra
        sobra = orçamento - total_despesas
        st.write(f"**Total de despesas:** R${total_despesas:.2f}")
        st.write(f"**Sobra do orçamento:** R${sobra:.2f}")
        
        # Gráfico de pizza
        if total_despesas > 0:
            fig, ax = plt.subplots()
            ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Para deixar o gráfico em formato circular
            st.pyplot(fig)
    else:
        st.write("Nenhuma despesa adicionada ainda.")

    


def SMG_main(): 
    # Função para calcular a parcela mensal e o total a ser pago
    def calcular_parcela(valor_emprestimo, taxa_juros, numero_parcelas):
        # Converter a taxa de juros anual para mensal (percentual)
        juros_mensal = taxa_juros / 100 / 12
        # Fórmula do cálculo da parcela mensal (Sistema de Amortização Francês)
        parcela = valor_emprestimo * (juros_mensal * (1 + juros_mensal)**numero_parcelas) / ((1 + juros_mensal)**numero_parcelas - 1)
        total_pago = parcela * numero_parcelas
        return parcela, total_pago

    # Função para gerar a amortização
    def gerar_amortizacao(valor_emprestimo, taxa_juros, numero_parcelas):
        juros_mensal = taxa_juros / 100 / 12
        saldo_devedor = valor_emprestimo
        parcelas = []
        amortizacoes = []
        juros = []
        
        for i in range(numero_parcelas):
            valor_juros = saldo_devedor * juros_mensal
            valor_amortizacao = calcular_parcela(valor_emprestimo, taxa_juros, numero_parcelas)[0] - valor_juros
            saldo_devedor -= valor_amortizacao
            
            parcelas.append(calcular_parcela(valor_emprestimo, taxa_juros, numero_parcelas)[0])
            amortizacoes.append(valor_amortizacao)
            juros.append(valor_juros)
        
        return parcelas, amortizacoes, juros


    # Interface do Streamlit
    st.title("Simulador de Empréstimos")

    # Entrada de dados do usuário
    valor_emprestimo = st.number_input("Valor do Empréstimo (R$)", min_value=1000.0, value=10000.0, step=1000.0)
    taxa_juros = st.number_input("Taxa de Juros Anual (%)", min_value=0.1, value=5.0, step=0.1)
    numero_parcelas = st.number_input("Número de Parcelas (meses)", min_value=1, value=12, step=1)

    # Cálculo das parcelas
    parcela, total_pago = calcular_parcela(valor_emprestimo, taxa_juros, numero_parcelas)

    # Exibir os resultados
    st.write(f"### Valor da parcela mensal: R$ {parcela:.2f}")
    st.write(f"### Total a ser pago: R$ {total_pago:.2f}")

    # Gerar dados para o gráfico de amortização
    parcelas, amortizacoes, juros = gerar_amortizacao(valor_emprestimo, taxa_juros, numero_parcelas)

    # Gráfico de amortização
    st.write("## Gráfico de Amortização")
    fig, ax = plt.subplots()

    ax.plot(range(1, numero_parcelas + 1), amortizacoes, label="Amortização", marker='o')
    ax.plot(range(1, numero_parcelas + 1), juros, label="Juros", marker='x')
    ax.set_xlabel("Número da Parcela")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Amortização e Juros ao Longo do Tempo")
    ax.legend()

    st.pyplot(fig)


def coracao_plot():
    st.title("Coração plot")
    st.latex(r"x(t) = 16 \sin^3(t)")
    st.latex(r"y(t) = 13 \cos(t) - 5 \cos(2t) - 2 \cos(3t) - \cos(4t)")
    
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16*np.sin(t)**3
    y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)

    plt.plot(x,y,color='black')
    plt.fill(x,y,color='r')
    
    plt.axis("equal")
    st.pyplot(plt)

def AnaliseDeEntrada():
    st.title("Anlise de sequencia Numérica")
    stringNumeros = st.text_input('Entre com uma sequencia de Numeros sepadas por espaço: ',placeholder="1 2 34 2 5 1 2") 
    if stringNumeros:
        numeros = np.array(stringNumeros.split(" "),dtype=float)
        st.markdown(f"""
                    A sequencia de números : {numeros}  
                    Soma: {numeros.sum()}  
                    Media: {numeros.mean()}  
                    median: {np.median(numeros)}
                    moda: {stats.mode(numeros).mode[0]}
                    Desvio padrão: {np.std(numeros)}  
                    Valor Max: {numeros.max()}  
                    Valor Min: {numeros.min()} 

                    """)
        # Exibindo as fórmulas em LaTeX
        st.write("## Fórmulas")
        st.latex(r"\text{Média: } \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i")
        st.latex(r"\text{Mediana: } \text{Mediana} = \text{valor central se ímpar, média dos dois valores centrais se par}")
        st.latex(r"\text{Moda: } \text{Moda é o valor que mais se repete}")
        st.latex(r"\text{Desvio Padrão: } \sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2}")
        st.latex(r"\text{Máximo: } \max(x)")
        st.latex(r"\text{Mínimo: } \min(x)")
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

with st.expander("Coração"):
    coracao_plot()

with st.expander("Despesas Mensais"):
    DespesasMensais()

with st.expander("Custos"):
    SMG_main()

with st.expander("Jogo da Velha"):
    JogoDaVelha()