import tkinter as tk  # Importa a biblioteca tkinter para criação de interfaces gráficas
from tkinter import messagebox  # Importa o messagebox para exibir caixas de diálogo de erro e informação
from tkinter import ttk  # Importa ttk para widgets aprimorados do tkinter
from datetime import datetime  # Importa a classe datetime para trabalhar com datas
import requests  # Importa requests para fazer requisições HTTP
import mysql.connector  # Importa mysql.connector para conectar-se a um banco de dados MySQL

# Configurações da planilha onde o token está armazenado
sheet_id = "1mCloyHpRasZK-jer2QwOGLEHa5FxDv4sz40ejnIwS8Y"  # ID da planilha do Google Sheets
range_name = "access!B2"  # Intervalo da célula onde o token de acesso está localizado
api_key = "AIzaSyDYMPaJrPnT8xrHPWPpGHOTSCYAJhtw8Nk"  # Chave da API do Google para acessar o Google Sheets

# Configurações do banco de dados MySQL
db_config = {
    'host': 'srv1446.hstgr.io',  # Endereço do host MySQL
    'user': 'u462387354_komforta',  # Nome do usuário do banco de dados
    'password': 'Komforta@123',  # Senha do banco de dados
    'database': 'u462387354_90dias'  # Nome do banco de dados
}

# URL da API do Google Sheets para obter o Access Token
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}"  # Monta a URL para acessar o valor da célula do Google Sheets

# Função para obter o access token do Google Sheets
def get_access_token():
    response = requests.get(url)  # Faz uma requisição GET para a URL configurada
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        data = response.json()  # Converte a resposta em JSON
        access_token = data.get("values", [[]])[0][0]  # Extrai o token de acesso da resposta
        return access_token  # Retorna o token de acesso
    else:
        show_custom_error("Erro ao acessar a planilha do Google Sheets.")  # Exibe uma mensagem de erro
        return None  # Retorna None em caso de falha

# Função para exibir uma mensagem personalizada de informação
def show_custom_info(title, message):
    info_window = tk.Toplevel(app)  # Cria uma nova janela de nível superior
    info_window.title(title)  # Define o título da janela
    info_window.geometry("350x180")  # Define o tamanho da janela
    info_window.configure(bg="white")  # Define a cor de fundo da janela

    # Adiciona um label de mensagem
    message_label = tk.Label(
        info_window, text=message, font=("Arial", 14, "bold"), fg="#333", bg="white", wraplength=300, justify="center"
    )
    message_label.pack(expand=True, padx=20, pady=(30, 10))  # Posiciona o label

    # Adiciona um botão de "OK" para fechar a janela
    ok_button = tk.Button(
        info_window, text="OK", command=info_window.destroy,
        bg="#00b4d8", fg="white", font=("Arial", 12, "bold"),
        bd=0, relief="flat", width=10, height=2, cursor="hand2"
    )
    ok_button.pack(pady=(0, 20))

    # Ajusta as propriedades da janela para ficar no topo e semi-transparente
    info_window.overrideredirect(True)
    info_window.lift()
    info_window.wm_attributes("-topmost", True)
    info_window.wm_attributes("-alpha", 0.95)

# Função para exibir uma mensagem de erro personalizada
def show_custom_error(message):
    error_window = tk.Toplevel(app)  # Cria uma janela de erro
    error_window.title("Erro")  # Define o título
    error_window.geometry("300x150")  # Define o tamanho da janela
    error_window.configure(bg="white")  # Define a cor de fundo da janela

    # Adiciona o label de erro
    tk.Label(error_window, text=message, font=("Arial", 11), fg="#cc0000").pack(expand=True, padx=20, pady=20)

    # Adiciona um botão de "Fechar" para fechar a janela
    tk.Button(error_window, text="Fechar", command=error_window.destroy, bg="#ff6961", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat").pack(pady=10)

# Função que atualiza os campos de entrada com base na métrica selecionada
def update_fields():
    selected_metric = metric_var.get()  # Obtém a métrica selecionada

    # Desativa todos os campos de entrada
    entry_user.configure(state="disabled", bg="#f0f0f0")
    product_entry.configure(state="disabled", bg="#f0f0f0")
    product_button.config(state="disabled")
    entry_start_date.configure(state="disabled", bg="#f0f0f0")
    entry_end_date.configure(state="disabled", bg="#f0f0f0")

    # Habilita os campos necessários de acordo com a métrica selecionada
    if selected_metric == "Reputação":
        entry_user.configure(state="normal", bg="white")
    elif selected_metric == "Visitas":
        product_entry.configure(state="normal", bg="white")
        product_button.config(state="normal")
        entry_start_date.configure(state="normal", bg="white")
        entry_end_date.configure(state="normal", bg="white")
    elif selected_metric == "Estoque":
        product_entry.configure(state="normal", bg="white")
        product_button.config(state="normal")
    elif selected_metric in ["Faturamento", "Quantidade de Vendas", "Unidades Vendidas"]:
        product_entry.configure(state="normal", bg="white")
        product_button.config(state="normal")
        entry_start_date.configure(state="normal", bg="white")

# Função para abrir a janela de seleção de produto
def open_product_selection():
    product_window = tk.Toplevel(app)  # Cria uma nova janela para a seleção do produto
    product_window.title("Selecione o Código do Produto")  # Define o título da janela
    product_window.geometry("300x200")  # Define o tamanho da janela
    
    # Frame para lista de produtos
    listbox_frame = tk.Frame(product_window, bg="white")
    listbox_frame.pack(fill="x", pady=5)

    # Cria a lista de códigos de produtos
    product_code_listbox = tk.Listbox(listbox_frame, font=("Arial", 10, "bold"), bg="white", fg="black", selectmode="single", height=6, bd=1, relief="solid")
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    scrollbar.config(command=product_code_listbox.yview)
    product_code_listbox.config(yscrollcommand=scrollbar.set)
    
    product_codes = get_product_codes()  # Obtém os códigos de produto do banco de dados
    for code in product_codes:
        product_code_listbox.insert(tk.END, code)  # Insere cada código na lista

    product_code_listbox.pack(side="left", fill="x", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Função para selecionar o código do produto
    def select_product():
        selected_product_index = product_code_listbox.curselection()  # Obtém o índice do item selecionado
        if selected_product_index:
            selected_code = product_code_listbox.get(selected_product_index[0])  # Obtém o código selecionado
            product_code_var.set(selected_code)  # Define o valor selecionado no campo
            product_window.destroy()  # Fecha a janela de seleção
        else:
            messagebox.showwarning("Aviso", "Nenhum produto foi selecionado.")  # Exibe uma mensagem se nenhum produto for selecionado

    # Botão para confirmar a seleção do produto
    select_button = tk.Button(product_window, text="Selecionar", command=select_product, bg="#00aaff", fg="white", font=("Arial", 10, "bold"))
    select_button.pack(pady=10)

# Função que busca as métricas de acordo com a seleção
def fetch_metric_data():
    selected_metric = metric_var.get()  # Obtém a métrica selecionada
    product_code = product_code_var.get()  # Obtém o valor do código de produto
    
    start_date = entry_start_date.get()  # Obtém a data de início
    access_token = get_access_token()  # Obtém o token de acesso
    
    if not access_token:
        show_custom_error("Erro ao obter o access token.")  # Exibe erro caso não consiga obter o token
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}"  # Define o token no cabeçalho da requisição
    }
    
    # Lógica de acordo com a métrica selecionada
    if selected_metric == "Reputação":
        user_id = entry_user.get()
        if not user_id:
            show_custom_error("O campo 'Código do Usuário' é obrigatório para Reputação.")  # Exige que o código de usuário seja preenchido
            return
        url = f"https://api.mercadolibre.com/users/{user_id}"  # Monta a URL para buscar a reputação do usuário
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
            data = response.json()
            level_id = data.get("seller_reputation", {}).get("level_id", "Não disponível")  # Obtém o nível de reputação
            show_custom_info("Reputação", f"Nível de Reputação: {level_id}")  # Exibe o nível de reputação
        else:
            show_custom_error(f"Falha ao obter a métrica de Reputação.\nStatus Code: {response.status_code}")  # Exibe erro em caso de falha

    elif selected_metric == "Visitas":
        if not product_code or not start_date:
            show_custom_error("Os campos 'Código do Produto' e 'Data de Início' são obrigatórios para Visitas.")  # Exige que os campos sejam preenchidos
            return
        try:
            start_date_formatted = datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")  # Formata a data
            end_date_formatted = entry_end_date.get()
            end_date_formatted = datetime.strptime(end_date_formatted, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            show_custom_error("Datas devem estar no formato dd/mm/aaaa.")  # Exibe erro se o formato da data estiver incorreto
            return
        
        url = f"https://api.mercadolibre.com/items/visits?ids={product_code}&date_from={start_date_formatted}&date_to={end_date_formatted}"  # Monta a URL para buscar visitas
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                total_visits = data[0].get("total_visits", "Não disponível")  # Obtém o número total de visitas
                show_custom_info("Visitas", f"Total de Visitas: {total_visits}")  # Exibe o total de visitas
            else:
                show_custom_info("Visitas", "Não foi possível obter o total de visitas.")  # Exibe erro caso não haja visitas disponíveis
        else:
            show_custom_error(f"Falha ao obter a métrica de Visitas.\nStatus Code: {response.status_code}")  # Exibe erro em caso de falha
    
    elif selected_metric == "Estoque":
        if not product_code:
            show_custom_error("O campo 'Código do Produto' é obrigatório para Estoque.")  # Exige que o código do produto seja preenchido
            return
        url = f"https://api.mercadolibre.com/items/{product_code}"  # Monta a URL para buscar a quantidade de estoque
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            available_quantity = data.get("available_quantity", "Não disponível")  # Obtém a quantidade disponível
            show_custom_info("Estoque", f"Quantidade em Estoque: {available_quantity}")  # Exibe a quantidade disponível
        else:
            show_custom_error(f"Falha ao obter a métrica de Estoque.\nStatus Code: {response.status_code}")  # Exibe erro em caso de falha

    elif selected_metric in ["Faturamento", "Quantidade de Vendas", "Unidades Vendidas"]:
        if not product_code or not start_date:
            show_custom_error("Os campos 'Código do Produto' e 'Data de Início' são obrigatórios.")  # Exige que os campos sejam preenchidos
            return
        
        try:
            start_date_formatted = datetime.strptime(start_date, "%d/%m/%Y").strftime("%d/%m/%Y")  # Formata a data de início
            primary_key = f"{product_code}{start_date_formatted}"  # Define a chave primária para a busca
            
            connection = mysql.connector.connect(**db_config)  # Conecta ao banco de dados MySQL
            cursor = connection.cursor()

            column_name = ""
            if selected_metric == "Faturamento":
                column_name = "total_amount"  # Define a coluna correta para Faturamento
            elif selected_metric == "Quantidade de Vendas":
                column_name = "total_transacoes"  # Define a coluna correta para Quantidade de Vendas
            elif selected_metric == "Unidades Vendidas":
                column_name = "total_unidades"  # Define a coluna correta para Unidades Vendidas

            # Query SQL para obter os dados da métrica selecionada
            query = f"SELECT {column_name} FROM tF_ml_vendasAcumuladas WHERE chave_primaria = %s"
            cursor.execute(query, (primary_key,))
            
            result = cursor.fetchone()  # Busca o primeiro resultado
            if result:
                metric_value = result[0]  # Obtém o valor da métrica
                show_custom_info(selected_metric, f"{selected_metric}: {metric_value}")  # Exibe o valor da métrica
            else:
                show_custom_info(selected_metric, "Nenhum dado encontrado para os parâmetros fornecidos.")  # Exibe mensagem se nenhum dado for encontrado
            
            cursor.close()
            connection.close()  # Fecha a conexão com o banco de dados
        
        except mysql.connector.Error as err:
            show_custom_error(f"Erro ao acessar o banco de dados: {err}")  # Exibe erro em caso de falha no banco de dados

# Função para obter os códigos dos produtos da tabela 'anuncios'
def get_product_codes():
    try:
        connection = mysql.connector.connect(**db_config)  # Conecta ao banco de dados MySQL
        cursor = connection.cursor()
        query = "SELECT codigo FROM anuncios"  # Query para buscar os códigos dos produtos
        cursor.execute(query)
        product_codes = [row[0] for row in cursor.fetchall()]  # Armazena os códigos em uma lista
        cursor.close()
        connection.close()  # Fecha a conexão com o banco de dados
        return product_codes  # Retorna a lista de códigos de produto
    except mysql.connector.Error as err:
        show_custom_error(f"Erro ao acessar o banco de dados: {err}")  # Exibe erro em caso de falha no banco de dados
        return []  # Retorna uma lista vazia em caso de erro

# Função para abrir a tela principal da aplicação
def open_main_screen():
    global app, metric_var, product_code_var, entry_user, product_entry, product_button, entry_start_date, entry_end_date  # Declarando as variáveis como globais
    app = tk.Tk()  # Cria a janela principal da aplicação
    app.title("Consulta de Métricas do Mercado Livre")  # Define o título da janela
    app.attributes("-fullscreen", True)  # Define a janela para abrir em tela cheia
    app.configure(bg="#f4f4f4")  # Define a cor de fundo da janela

    # Cria o cabeçalho da janela
    header = tk.Frame(app, bg="#00b4d8", height=70)
    header.pack(fill="x")
    header_label = tk.Label(header, text="Consulta de Métricas", font=("Arial", 16, "bold"), fg="white", bg="#00b4d8")
    header_label.pack(pady=20)

    # Cria o cartão para as opções
    card = tk.Frame(app, bg="#ffffff", bd=1, highlightthickness=1, highlightbackground="#d0d0d0", relief="solid")
    card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=575)

    # Seção para escolher a métrica
    metric_section = tk.Frame(card, bg="white", padx=20, pady=10)
    metric_section.pack(pady=(10, 5), fill="x")
    tk.Label(metric_section, text="Selecione a Métrica:", font=("Arial", 11, "bold"), bg="white", fg="#333").pack(pady=5)
    metric_var = tk.StringVar(value="Reputação")  # Variável para armazenar a métrica selecionada
    metrics = [
        ("Reputação", "Reputação"), 
        ("Visitas", "Visitas"), 
        ("Estoque", "Estoque"), 
        ("Faturamento", "Faturamento"),
        ("Quantidade de Vendas", "Quantidade de Vendas"),
        ("Unidades Vendidas", "Unidades Vendidas")
    ]
    for text, metric in metrics:
        tk.Radiobutton(metric_section, text=text, variable=metric_var, value=metric, command=update_fields, font=("Arial", 10), bg="white").pack(anchor="w")  # Adiciona opções de métricas como radiobuttons

    # Seção de entrada de dados
    input_section = tk.Frame(card, bg="white", padx=20, pady=10)
    input_section.pack(pady=(5, 10), fill="x")

    # Função auxiliar para criar entradas de texto
    def create_entry(parent, label_text):
        frame = tk.Frame(parent, bg="white")
        frame.pack(pady=5, fill="x")
        label = tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), bg="white", fg="#333")
        label.pack(anchor="w")
        entry = tk.Entry(frame, font=("Arial", 10), bd=1, relief="solid")
        entry.pack(pady=5, ipadx=5, ipady=5, fill="x")
        return entry

    global entry_start_date, entry_end_date
    entry_user = create_entry(input_section, "Código do usuário:")  # Cria campo de entrada para o código do usuário
    
    # Botão para abrir o menu de seleção de produtos
    tk.Label(input_section, text="Código do Produto:", font=("Arial", 10, "bold"), bg="white", fg="#333").pack(anchor="w")
    product_code_var = tk.StringVar()

    product_selection_frame = tk.Frame(input_section, bg="white")
    product_selection_frame.pack(pady=5, fill="x")

    product_entry = tk.Entry(product_selection_frame, textvariable=product_code_var, font=("Arial", 10), bd=1, relief="solid", state="readonly")  # Campo de entrada para o código do produto
    product_entry.pack(side="left", fill="x", expand=True)

    product_button = tk.Button(product_selection_frame, text="🔽", command=open_product_selection, bg="white", fg="black", relief="solid")  # Botão para abrir a seleção de produtos
    product_button.pack(side="right")

    entry_start_date = create_entry(input_section, "Data de Início (dd/mm/aaaa):")  # Campo de entrada para a data de início
    entry_end_date = create_entry(input_section, "Data de Fim (dd/mm/aaaa):")  # Campo de entrada para a data de fim

    # Funções para alterar o botão ao passar o mouse
    def on_enter(e):
        button_fetch_metric.config(bg="#0077b6")

    def on_leave(e):
        button_fetch_metric.config(bg="#00aaff")

    # Botão para consultar a métrica
    button_fetch_metric = tk.Button(card, text="🔍 Consultar Métrica", command=fetch_metric_data, bg="#00aaff", fg="white", font=("Arial", 12, "bold"), bd=0, relief="flat", cursor="hand2")
    button_fetch_metric.place(relx=0.5, rely=1, anchor="s", y=-20)
    button_fetch_metric.bind("<Enter>", on_enter)
    button_fetch_metric.bind("<Leave>", on_leave)

    update_fields()  # Atualiza os campos de entrada de acordo com a métrica selecionada

    # Função para sair do modo tela cheia
    def exit_fullscreen(event=None):
        app.attributes("-fullscreen", False)

    app.bind("<Escape>", exit_fullscreen)  # Permite sair do modo tela cheia pressionando a tecla Esc
    app.mainloop()  # Inicia o loop principal da interface gráfica