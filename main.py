import tkinter as tk
import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cria a tabela de produtos se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        quantidade INTEGER
    )
''')
conn.commit()

# Função para adicionar um produto ao banco de dados
def adicionar_produto():
    nome = nome_entry.get()
    preco = float(preco_entry.get())
    quantidade = int(quantidade_entry.get())

    cursor.execute('''
        INSERT INTO produtos (nome, preco, quantidade)
        VALUES (?, ?, ?)
    ''', (nome, preco, quantidade))
    conn.commit()

    status_label["text"] = "Produto adicionado com sucesso!"

    nome_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)

# Função para calcular o total da venda
def calcular_total():
    cursor.execute('SELECT preco, quantidade FROM produtos')
    produtos = cursor.fetchall()

    total = 0
    for produto in produtos:
        preco_total = produto[0] * produto[1]
        total += preco_total

    total_label["text"] = f"Total da venda: R${total:.2f}"

# Função para exibir o recibo da venda
def exibir_recibo():
    cursor.execute('SELECT nome, preco, quantidade FROM produtos')
    produtos = cursor.fetchall()

    recibo_text.delete(1.0, tk.END)
    recibo_text.insert(tk.END, "-------- RECIBO --------\n")
    for produto in produtos:
        recibo_text.insert(tk.END, f"Produto: {produto[0]}\n")
        recibo_text.insert(tk.END, f"Preço: R${produto[1]:.2f}\n")
        recibo_text.insert(tk.END, f"Quantidade: {produto[2]}\n")
        recibo_text.insert(tk.END, "------------------------\n")

# Cria a janela principal
root = tk.Tk()
root.title("Programa de Vendas")

# Frame para adicionar produtos
adicionar_frame = tk.LabelFrame(root, text="Adicionar Produto")
adicionar_frame.pack(padx=10, pady=10)

nome_label = tk.Label(adicionar_frame, text="Nome do Produto:")
nome_label.grid(row=0, column=0, padx=5, pady=5)
nome_entry = tk.Entry(adicionar_frame)
nome_entry.grid(row=0, column=1, padx=5, pady=5)

preco_label = tk.Label(adicionar_frame, text="Preço do Produto:")
preco_label.grid(row=1, column=0, padx=5, pady=5)
preco_entry = tk.Entry(adicionar_frame)
preco_entry.grid(row=1, column=1, padx=5, pady=5)

quantidade_label = tk.Label(adicionar_frame, text="Quantidade:")
quantidade_label.grid(row=2, column=0, padx=5, pady=5)
quantidade_entry = tk.Entry(adicionar_frame)
quantidade_entry.grid(row=2, column=1, padx=5, pady=5)

adicionar_button = tk.Button(adicionar_frame, text="Adicionar", command=adicionar_produto)
adicionar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(adicionar_frame, text="")
status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Frame para calcular total
calcular_frame = tk.LabelFrame(root, text="Calcular Total")
calcular_frame.pack(padx=10, pady=10)

calcular_button = tk.Button(calcular_frame, text="Calcular", command=calcular_total)
calcular_button.pack(padx=5, pady=5)

total_label = tk.Label(calcular_frame, text="")
total_label.pack(padx=5, pady=5)

# Frame para exibir recibo
recibo_frame = tk.LabelFrame(root, text="Recibo")
recibo_frame.pack(padx=10, pady=10)

recibo_text = tk.Text(recibo_frame, width=50, height=10)
recibo_text.pack(padx=5, pady=5)

exibir_button = tk.Button(recibo_frame, text="Exibir Recibo", command=exibir_recibo)
exibir_button.pack(padx=5, pady=5)

# Loop principal do programa
root.mainloop()

# Fecha a conexão com o banco de dados
conn.close()