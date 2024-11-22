import tkinter as tk  # Importa o módulo tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa messagebox para exibir caixas de diálogo (alertas, erros, etc.)
import mysql.connector  # Importa o módulo mysql.connector para conexão com o banco de dados MySQL
from consulta_mercado_livre import open_main_screen  # Importe a função para abrir a interface de métricas do arquivo consulta_mercado_livre

# Configurações do banco de dados MySQL
db_config = {
    'host': 'srv1446.hstgr.io',
    'user': 'u462387354_komforta',
    'password': 'Komforta@123',
    'database': 'u462387354_90dias'
}

GERENTE_SENHA = "acesso@"  # Define a senha do gerente de acessos

# Função para verificar login no banco de dados por email e senha
def check_user_login(email, password):
    try:
        connection = mysql.connector.connect(**db_config)  # Estabelece a conexão com o banco de dados MySQL usando as credenciais definidas em db_config
        cursor = connection.cursor()  # Cria um cursor para executar consultas SQL
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"  # Define a query SQL para verificar o email e senha
        cursor.execute(query, (email, password))  # Executa a consulta passando os valores de email e senha
        result = cursor.fetchone()  # Busca o primeiro resultado da consulta
        cursor.close()  # Fecha o cursor
        connection.close()  # Fecha a conexão com o banco de dados
        return result is not None  # Retorna True se o usuário foi encontrado, senão retorna False
    except mysql.connector.Error as err:  # Captura possíveis erros na conexão ou execução
        messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {err}")  # Exibe uma caixa de erro caso haja um problema
        return False  # Retorna False se houver erro

# Função para cadastrar novo usuário no banco de dados
def add_user(cpf, nome, email, senha):
    try:
        connection = mysql.connector.connect(**db_config)  # Estabelece a conexão com o banco de dados MySQL
        cursor = connection.cursor()  # Cria um cursor para executar a inserção
        query = "INSERT INTO usuarios (cpf, nome, email, senha) VALUES (%s, %s, %s, %s)"  # Define a query SQL para inserir o usuário
        cursor.execute(query, (cpf, nome, email, senha))  # Executa a query passando os valores fornecidos
        connection.commit()  # Confirma a transação no banco de dados
        cursor.close()  # Fecha o cursor
        connection.close()  # Fecha a conexão com o banco de dados
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")  # Exibe uma mensagem informando que o cadastro foi bem-sucedido
    except mysql.connector.Error as err:  # Captura possíveis erros na execução
        messagebox.showerror("Erro", f"Erro ao cadastrar o usuário: {err}")  # Exibe uma mensagem de erro

# Função para sair do modo de tela cheia
def exit_fullscreen(event=None):
    event.widget.attributes("-fullscreen", False)  # Desativa o modo de tela cheia

# Função para validar a senha do gerente antes de abrir a tela de cadastro
def validate_manager_password():
    def verify_password():
        if entry_password.get() == GERENTE_SENHA:
            password_window.destroy()  # Fecha a janela de senha do gerente
            open_register_screen()  # Chama a função para abrir a tela de cadastro
        else:
            messagebox.showerror("Erro", "Senha do gerente incorreta!")  # Exibe uma mensagem de erro se a senha estiver incorreta

    password_window = tk.Toplevel()  # Cria uma nova janela para solicitar a senha do gerente
    password_window.title("Senha do Gerente")
    tk.Label(password_window, text="Digite a senha do gerente de acessos:", font=("Arial", 14)).pack(pady=10)
    entry_password = tk.Entry(password_window, font=("Arial", 14), show="*")  # Campo para inserir a senha
    entry_password.pack(pady=10)
    tk.Button(password_window, text="Confirmar", command=verify_password, font=("Arial", 14)).pack(pady=10)

# Função para abrir a tela de cadastro de usuário
def open_register_screen():
    def register_user():
        cpf = entry_cpf.get()  # Obtém o valor inserido no campo CPF
        nome = entry_nome.get()  # Obtém o valor inserido no campo Nome
        email = entry_email.get()  # Obtém o valor inserido no campo Email
        senha = entry_senha.get()  # Obtém o valor inserido no campo Senha
        if cpf and nome and email and senha:  # Verifica se todos os campos estão preenchidos
            add_user(cpf, nome, email, senha)  # Chama a função para adicionar o usuário ao banco de dados
            register_window.destroy()  # Fecha a janela de cadastro após o registro
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios para cadastro.")  # Exibe uma mensagem de erro se algum campo estiver vazio

    register_window = tk.Toplevel()  # Cria uma nova janela para o cadastro
    register_window.title("Cadastrar Usuário")  # Define o título da janela
    register_window.attributes('-fullscreen', True)  # Ativa o modo tela cheia
    register_window.bind("<Escape>", exit_fullscreen)  # Permite sair do modo tela cheia com a tecla ESC

    frame = tk.Frame(register_window, bg="#E3F6F5", padx=20, pady=20)  # Cria um frame com padding e cor de fundo
    frame.pack(fill="both", expand=True)  # Adiciona o frame à janela

    tk.Label(frame, text="Cadastrar Usuário", font=("Arial", 24, "bold"), bg="#E3F6F5").pack(pady=20)  # Adiciona o título "Cadastrar Usuário"

    tk.Label(frame, text="CPF:", font=("Arial", 14), bg="#E3F6F5").pack(pady=5)  # Adiciona o label "CPF"
    entry_cpf = tk.Entry(frame, font=("Arial", 14), width=30, relief="solid")  # Adiciona um campo de entrada para CPF
    entry_cpf.pack(pady=10)  # Posiciona o campo na janela

    tk.Label(frame, text="Nome:", font=("Arial", 14), bg="#E3F6F5").pack(pady=5)  # Adiciona o label "Nome"
    entry_nome = tk.Entry(frame, font=("Arial", 14), width=30, relief="solid")  # Adiciona um campo de entrada para Nome
    entry_nome.pack(pady=10)

    tk.Label(frame, text="Email:", font=("Arial", 14), bg="#E3F6F5").pack(pady=5)  # Adiciona o label "Email"
    entry_email = tk.Entry(frame, font=("Arial", 14), width=30, relief="solid")  # Adiciona um campo de entrada para Email
    entry_email.pack(pady=10)

    tk.Label(frame, text="Senha:", font=("Arial", 14), bg="#E3F6F5").pack(pady=5)  # Adiciona o label "Senha"
    entry_senha = tk.Entry(frame, font=("Arial", 14), show="*", width=30, relief="solid")  # Adiciona um campo de entrada para Senha com caracteres escondidos
    entry_senha.pack(pady=10)

    tk.Button(frame, text="Cadastrar", command=register_user, font=("Arial", 14), bg="#00aaff", fg="white", cursor="hand2", width=15, relief="flat").pack(pady=20)  # Adiciona um botão para o cadastro

# Função para iniciar a tela de login com email e senha
def show_login_screen():
    def login():
        email = entry_email.get()  # Obtém o valor do campo Email
        password = entry_password.get()  # Obtém o valor do campo Senha
        if check_user_login(email, password):  # Verifica se o login é válido
            login_window.destroy()  # Fecha a janela de login se o login for bem-sucedido
            open_main_screen()  # Chama a função para abrir a interface principal de métricas
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos! Se você não estiver cadastrado, clique em 'Cadastrar Usuário'.")  # Exibe mensagem de erro se o login falhar

    login_window = tk.Tk()  # Cria a janela principal para login
    login_window.title("Login")  # Define o título da janela
    login_window.attributes('-fullscreen', True)  # Ativa o modo tela cheia
    login_window.bind("<Escape>", exit_fullscreen)  # Permite sair do modo tela cheia com ESC

    frame = tk.Frame(login_window, bg="#E3F6F5", padx=20, pady=20)  # Cria um frame dentro da janela
    frame.pack(fill="both", expand=True)  # Posiciona o frame

    tk.Label(frame, text="Login", font=("Arial", 24, "bold"), bg="#E3F6F5").pack(pady=20)  # Adiciona o título "Login"

    tk.Label(frame, text="Email:", font=("Arial", 14), bg="#E3F6F5").pack(pady=10)  # Adiciona o label "Email"
    entry_email = tk.Entry(frame, font=("Arial", 14), width=30, relief="solid")  # Adiciona o campo de entrada para Email
    entry_email.pack(pady=10)

    tk.Label(frame, text="Senha:", font=("Arial", 14), bg="#E3F6F5").pack(pady=10)  # Adiciona o label "Senha"
    entry_password = tk.Entry(frame, font=("Arial", 14), show="*", width=30, relief="solid")  # Adiciona o campo de entrada para Senha
    entry_password.pack(pady=10)

    tk.Button(frame, text="Entrar", command=login, font=("Arial", 14), bg="#00aaff", fg="white", cursor="hand2", width=15, relief="flat").pack(pady=20)  # Adiciona o botão de login
    tk.Button(frame, text="Cadastrar Usuário", command=validate_manager_password, font=("Arial", 14), bg="#00b4d8", fg="white", cursor="hand2", width=15, relief="flat").pack(pady=10)  # Adiciona o botão para abrir a tela de cadastro

    login_window.mainloop()  # Inicia o loop principal da interface gráfica

# Iniciar a tela de login
show_login_screen()  # Chama a função para exibir a tela de login