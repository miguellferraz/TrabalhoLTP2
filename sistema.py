import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def criar_banco():
    conn = sqlite3.connect("clientes_pedidos.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()

def inserir_cliente(nome, telefone):
    try:
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

def buscar_clientes():
    conn = sqlite3.connect("clientes_pedidos.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_cliente(id_, nome, telefone):
    try:
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("UPDATE clientes SET nome=?, telefone=? WHERE id=?", (nome, telefone, id_))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

def deletar_cliente(id_):
    try:
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("DELETE FROM clientes WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

def inserir_pedido(cliente_id, produto, quantidade):
    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("INSERT INTO pedidos (cliente_id, produto, quantidade) VALUES (?, ?, ?)",
                  (cliente_id, produto, quantidade))
        conn.commit()
        conn.close()
        return True
    except ValueError as ve:
        messagebox.showerror("Erro de valor", str(ve))
        return False
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

def buscar_pedidos(cliente_id=None):
    conn = sqlite3.connect("clientes_pedidos.db")
    c = conn.cursor()
    if cliente_id:
        c.execute("SELECT id, produto, quantidade FROM pedidos WHERE cliente_id=?", (cliente_id,))
    else:
        c.execute("SELECT id, cliente_id, produto, quantidade FROM pedidos")
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_pedido(id_, produto, quantidade):
    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("UPDATE pedidos SET produto=?, quantidade=? WHERE id=?", (produto, quantidade, id_))
        conn.commit()
        conn.close()
        return True
    except ValueError as ve:
        messagebox.showerror("Erro de valor", str(ve))
        return False
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

def deletar_pedido(id_):
    try:
        conn = sqlite3.connect("clientes_pedidos.db")
        c = conn.cursor()
        c.execute("DELETE FROM pedidos WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return False

class App:
    def __init__(self, root):
        self.root = root
        root.title("Clientes e Pedidos")

        self.frame_clientes = tk.LabelFrame(root, text="Clientes")
        self.frame_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_pedidos = tk.LabelFrame(root, text="Pedidos do Cliente")
        self.frame_pedidos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(self.frame_clientes, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = tk.Entry(self.frame_clientes)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.frame_clientes, text="Telefone:").grid(row=1, column=0, sticky="w")
        self.entry_telefone = tk.Entry(self.frame_clientes)
        self.entry_telefone.grid(row=1, column=1)

        self.btn_inserir_cliente = tk.Button(self.frame_clientes, text="Inserir Cliente", command=self.inserir_cliente)
        self.btn_inserir_cliente.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.tree_clientes = ttk.Treeview(self.frame_clientes, columns=("id", "nome", "telefone"), show="headings", height=8)
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nome", text="Nome")
        self.tree_clientes.heading("telefone", text="Telefone")
        self.tree_clientes.column("id", width=30)
        self.tree_clientes.grid(row=3, column=0, columnspan=2)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.selecionar_cliente)

        self.btn_atualizar_cliente = tk.Button(self.frame_clientes, text="Atualizar Cliente", command=self.atualizar_cliente)
        self.btn_atualizar_cliente.grid(row=4, column=0, pady=5, sticky="ew")

        self.btn_deletar_cliente = tk.Button(self.frame_clientes, text="Excluir Cliente", command=self.deletar_cliente)
        self.btn_deletar_cliente.grid(row=4, column=1, pady=5, sticky="ew")

        tk.Label(self.frame_pedidos, text="Produto:").grid(row=0, column=0, sticky="w")
        self.entry_produto = tk.Entry(self.frame_pedidos)
        self.entry_produto.grid(row=0, column=1)

        tk.Label(self.frame_pedidos, text="Quantidade:").grid(row=1, column=0, sticky="w")
        self.entry_quantidade = tk.Entry(self.frame_pedidos)
        self.entry_quantidade.grid(row=1, column=1)

        self.btn_inserir_pedido = tk.Button(self.frame_pedidos, text="Inserir Pedido", command=self.inserir_pedido)
        self.btn_inserir_pedido.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.tree_pedidos = ttk.Treeview(self.frame_pedidos, columns=("id", "produto", "quantidade"), show="headings", height=8)
        self.tree_pedidos.heading("id", text="ID")
        self.tree_pedidos.heading("produto", text="Produto")
        self.tree_pedidos.heading("quantidade", text="Quantidade")
        self.tree_pedidos.column("id", width=30)
        self.tree_pedidos.grid(row=3, column=0, columnspan=2)
        self.tree_pedidos.bind("<<TreeviewSelect>>", self.selecionar_pedido)

        self.btn_atualizar_pedido = tk.Button(self.frame_pedidos, text="Atualizar Pedido", command=self.atualizar_pedido)
        self.btn_atualizar_pedido.grid(row=4, column=0, pady=5, sticky="ew")

        self.btn_deletar_pedido = tk.Button(self.frame_pedidos, text="Excluir Pedido", command=self.deletar_pedido)
        self.btn_deletar_pedido.grid(row=4, column=1, pady=5, sticky="ew")

        self.cliente_selecionado_id = None
        self.pedido_selecionado_id = None

        self.atualizar_lista_clientes()

    def inserir_cliente(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório.")
            return
        if inserir_cliente(nome, telefone):
            self.limpar_campos_cliente()
            self.atualizar_lista_clientes()

    def atualizar_lista_clientes(self):
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)
        for cliente in buscar_clientes():
            self.tree_clientes.insert("", "end", values=cliente)
        self.limpar_campos_cliente()
        self.limpar_lista_pedidos()

    def selecionar_cliente(self, event):
        selecionado = self.tree_clientes.focus()
        if selecionado:
            valores = self.tree_clientes.item(selecionado, "values")
            self.cliente_selecionado_id = valores[0]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, valores[1])
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, valores[2])
            self.atualizar_lista_pedidos(cliente_id=self.cliente_selecionado_id)

    def atualizar_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")
            return
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório.")
            return
        if atualizar_cliente(self.cliente_selecionado_id, nome, telefone):
            self.atualizar_lista_clientes()

    def deletar_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Confirma exclusão do cliente e seus pedidos?"):
            if deletar_cliente(self.cliente_selecionado_id):
                self.cliente_selecionado_id = None
                self.atualizar_lista_clientes()
                self.limpar_lista_pedidos()

    def limpar_campos_cliente(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.cliente_selecionado_id = None

    def inserir_pedido(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um cliente antes de inserir pedidos.")
            return
        produto = self.entry_produto.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        if not produto or not quantidade:
            messagebox.showwarning("Aviso", "Produto e quantidade são obrigatórios.")
            return
        if inserir_pedido(self.cliente_selecionado_id, produto, quantidade):
            self.limpar_campos_pedido()
            self.atualizar_lista_pedidos(cliente_id=self.cliente_selecionado_id)

    def atualizar_lista_pedidos(self, cliente_id=None):
        for i in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(i)
        if cliente_id:
            pedidos = buscar_pedidos(cliente_id=cliente_id)
        else:
            pedidos = buscar_pedidos()
        for pedido in pedidos:
            self.tree_pedidos.insert("", "end", values=pedido)
        self.limpar_campos_pedido()

    def selecionar_pedido(self, event):
        selecionado = self.tree_pedidos.focus()
        if selecionado:
            valores = self.tree_pedidos.item(selecionado, "values")
            self.pedido_selecionado_id = valores[0]
            self.entry_produto.delete(0, tk.END)
            self.entry_produto.insert(0, valores[1])
            self.entry_quantidade.delete(0, tk.END)
            self.entry_quantidade.insert(0, valores[2])

    def atualizar_pedido(self):
        if not self.pedido_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um pedido para atualizar.")
            return
        produto = self.entry_produto.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        if not produto or not quantidade:
            messagebox.showwarning("Aviso", "Produto e quantidade são obrigatórios.")
            return
        if atualizar_pedido(self.pedido_selecionado_id, produto, quantidade):
            self.atualizar_lista_pedidos(cliente_id=self.cliente_selecionado_id)

    def deletar_pedido(self):
        if not self.pedido_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um pedido para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Confirma exclusão do pedido?"):
            if deletar_pedido(self.pedido_selecionado_id):
                self.pedido_selecionado_id = None
                self.atualizar_lista_pedidos(cliente_id=self.cliente_selecionado_id)

    def limpar_campos_pedido(self):
        self.entry_produto.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.pedido_selecionado_id = None

    def limpar_lista_pedidos(self):
        for i in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(i)
        self.limpar_campos_pedido()

if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
