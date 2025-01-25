import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import banco
from ttkthemes import ThemedTk


def carregar_cartas():
    #"""Carrega as cartas do banco de dados."""
    global baralho, baralho_nomes
    cartas = banco.carregar_cartas()
    for carta in cartas:
        baralho_nomes.append(carta)
        imagem = Image.open(carta)
        imagem.thumbnail((100, 150))
        foto = ImageTk.PhotoImage(imagem)
        baralho.append(foto)
    atualizar_lista_baralho()


def selecionar_cartas():
    #"""Seleciona múltiplos arquivos de imagem e atualiza o baralho."""
    global baralho, baralho_nomes
    arquivos_imagem = filedialog.askopenfilenames(
        title="Selecione as cartas",
        filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.gif")],
    )
    for arquivo in arquivos_imagem:
        if arquivo not in baralho_nomes:
            baralho_nomes.append(arquivo)
            banco.salvar_carta(arquivo)
            imagem = Image.open(arquivo)
            imagem.thumbnail((100, 150))
            foto = ImageTk.PhotoImage(imagem)
            baralho.append(foto)
    atualizar_lista_baralho()


def atualizar_lista_baralho():
    #"""Atualiza o painel do baralho com os nomes dos arquivos."""
    lista_baralho.delete(0, tk.END)
    for nome in baralho_nomes:
        lista_baralho.insert(tk.END, nome.split("/")[-1])


def criar_deck_aleatorio():
    global deck, carta_selecionada, limite_deck

    try:
        qtd_cartas = int(entry_qtd_cartas.get())  # Valor obtido do campo de entrada
        if qtd_cartas <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de cartas.")
        return

    # Definir o limite de cartas do deck com base no valor da entrada
    limite_deck = qtd_cartas

    if len(deck) >= qtd_cartas:
        messagebox.showwarning("Aviso", f"O deck já tem {qtd_cartas} cartas ou mais.")
        return
    if len(baralho) < qtd_cartas - len(deck):
        messagebox.showwarning("Aviso", "Cartas insuficientes no baralho para completar o deck.")
        return

    # Embaralhar o baralho antes de retirar as cartas
    random.shuffle(baralho)

    # Adicionar as cartas de forma aleatória ao deck
    for _ in range(qtd_cartas - len(deck)):
        carta = baralho.pop(0)
        baralho_nomes.pop(0)  # Remove o nome correspondente
        deck.append(carta)

    carta_selecionada = None
    atualizar_lista_baralho()
    atualizar_painel_deck()




def atualizar_painel_deck():
    """Atualiza o painel de cartas com base na página atual."""
    for widget in painel_deck.winfo_children():
        widget.destroy()  # Limpar o painel atual

    inicio = pagina_deck * cartas_por_pagina_deck  # Calcular o índice inicial para a página
    fim = inicio + cartas_por_pagina_deck  # Calcular o índice final para a página
    cartas_na_pagina = deck[inicio:fim]  # Obter as cartas da página atual

    # Exibir as cartas no painel
    for idx, carta in enumerate(cartas_na_pagina):
        lbl_carta = tk.Label(painel_deck, image=carta, relief=tk.RAISED, bd=2)
        lbl_carta.grid(row=0, column=idx, padx=5, pady=5)

        # Passar o índice real de cada carta para o bind
        lbl_carta.bind("<Button-1>", lambda e, idx_real=inicio + idx: selecionar_carta_deck(idx_real))  # Calcular o índice real

    # Botão Anterior (se não estiver na primeira página)
    if pagina_deck > 0:
        btn_anterior = ttk.Button(painel_deck, text="Anterior", command=lambda: navegar_pagina("anterior", "deck"), style="BotaoNav.TButton")
        btn_anterior.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)

    # Botão Próxima (se não estiver na última página)
    if fim < len(deck):
        btn_proxima = ttk.Button(painel_deck, text="Próxima", command=lambda: navegar_pagina("proxima", "deck"), style="BotaoNav.TButton")
        btn_proxima.grid(row=1, column=4, sticky=tk.E, pady=5, padx=10)




def selecionar_carta_deck(idx_real):
    """Função para selecionar uma carta do deck e destacar com borda azul."""
    global carta_selecionada

    carta_selecionada = idx_real  # Armazena o índice da carta selecionada
    atualizar_painel_deck()

    # Resetar estilo das cartas
    for widget in painel_deck.winfo_children():
        if isinstance(widget, tk.Label):  # Verificar se o widget é do tipo tk.Label
            widget.config(relief=tk.RAISED, bd=2, bg="white")  # Resetar borda e fundo de todas as cartas

    # Destacar a carta selecionada com borda azul e fundo azul
    painel_deck.winfo_children()[idx_real - (pagina_deck * cartas_por_pagina_deck)].config(relief=tk.SUNKEN, bd=6, bg="blue")






def descartar_carta():
    """Descarta a carta selecionada no deck."""
    global deck, descartadas, carta_selecionada

    if carta_selecionada is None:
        messagebox.showwarning("Aviso", "Selecione uma carta para descartar.")
        return

    # Remover a carta do deck
    descartadas.append(deck.pop(carta_selecionada))
    carta_selecionada = None  # Limpar a seleção

    # Atualizar o painel de cartas e o painel de descartes
    atualizar_painel_deck()
    atualizar_painel_descartes()






def atualizar_painel_descartes():
    for widget in painel_descartes.winfo_children():
        widget.destroy()

    descartadas_invertido = list(reversed(descartadas))
    inicio = pagina_descarte * cartas_por_pagina
    fim = inicio + cartas_por_pagina
    cartas_na_pagina = descartadas_invertido[inicio:fim]

    for idx, carta in enumerate(cartas_na_pagina):
        lbl_carta = tk.Label(painel_descartes, image=carta, relief=tk.RAISED, bd=2)
        lbl_carta.grid(row=0, column=idx, padx=5, pady=5)

    if pagina_descarte > 0:
        btn_anterior = ttk.Button(painel_descartes, text="Anterior", command=lambda: navegar_pagina("anterior", "descartes"), style="BotaoNav.TButton")
        btn_anterior.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)

    if fim < len(descartadas):
        btn_proxima = ttk.Button(painel_descartes, text="Próxima", command=lambda: navegar_pagina("proxima", "descartes"), style="BotaoNav.TButton")
        btn_proxima.grid(row=1, column=4, sticky=tk.E, pady=5, padx=10)




def incluir_carta():
    #"""Inclui uma carta aleatória do baralho no deck, respeitando o limite configurado."""
    global deck, limite_deck

    if len(deck) >= limite_deck:
        messagebox.showwarning("Aviso", f"O deck já está completo com {limite_deck} cartas.")
        return

    if not baralho:
        messagebox.showwarning("Aviso", "Não há cartas no baralho.")
        return

    # Embaralhar o baralho antes de retirar uma carta aleatória
    random.shuffle(baralho)

    # Adicionar uma carta aleatória ao deck
    carta = baralho.pop(0)
    baralho_nomes.pop(0)
    deck.append(carta)

    atualizar_lista_baralho()
    atualizar_painel_deck()

def navegar_pagina(direcao, tipo):
    global pagina_deck, pagina_descarte

    if tipo == "deck":
        if direcao == "anterior" and pagina_deck > 0:
            pagina_deck -= 1
        elif direcao == "proxima" and (pagina_deck + 1) * cartas_por_pagina_deck < len(deck):
            pagina_deck += 1
    elif tipo == "descartes":
        if direcao == "anterior" and pagina_descarte > 0:
            pagina_descarte -= 1
        elif direcao == "proxima" and (pagina_descarte + 1) * cartas_por_pagina < len(descartadas):
            pagina_descarte += 1

    if tipo == "deck":
        atualizar_painel_deck()
    elif tipo == "descartes":
        atualizar_painel_descartes()

def excluir_todas_as_cartas():
    #"""Exclui todas as cartas do banco de dados, limpa os painéis e atualiza a interface."""
    # Exibe a caixa de confirmação
    resposta = messagebox.askyesno(
        "Confirmar Exclusão", "Você tem certeza que deseja excluir todas as cartas?"
    )

    if resposta:  # Se o usuário confirmar a exclusão
        # Chama a função para excluir todas as cartas do banco de dados
        banco.excluir_todas_as_cartas()

        # Limpa as listas de baralho e baralho_nomes
        global baralho, baralho_nomes
        baralho.clear()
        baralho_nomes.clear()

        # Limpa as imagens nos painéis de deck e descarte
        for painel in [painel_deck, painel_descartes]:  # Para os painéis de deck e descarte
            for widget in painel.winfo_children():
                widget.destroy()  # Remove todos os widgets do painel (inclusive imagens e labels)

        # Atualiza a interface do usuário
        atualizar_lista_baralho()

        # Exibe uma mensagem de sucesso
        messagebox.showinfo("Sucesso", "Todas as cartas foram excluídas com sucesso.")



# Configurações iniciais com tema
root = ThemedTk()
root.get_themes()
root.set_theme("clam")
root.title("Gerenciador de Baralho")
root.geometry("850x700")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton",
                font=("Arial", 10, "bold"),
                padding=10,
                relief="raised",
                background="#4CAF50",
                foreground="black",
                focuscolor="none")

style.configure("TLabel",
                font=("Arial", 12, "bold"),
                background="#f0f0f0",
                foreground="black",
                relief="flat")

style.configure("TListbox",
                font=("Arial", 10),
                height=20,
                width=40)

style = ttk.Style()
style.configure("BotaoNav.TButton",
                background="#00BFFF",  # Cor de fundo desejada (exemplo: vermelho)
                foreground="black",    # Cor do texto (exemplo: branco)
                padding=10,            # Ajuste do preenchimento do botão
                font=("Arial", 10, "bold"),
                relief="raised")

style = ttk.Style()
style.configure("BotaoUsarCarta.TButton",
                background="#D2691E",  # Cor de fundo desejada (exemplo: vermelho)
                foreground="black",    # Cor do texto (exemplo: branco)
                padding=10,            # Ajuste do preenchimento do botão
                font=("Arial", 10, "bold"),
                relief="raised")

style = ttk.Style()
style.configure("BotaoIncluirCarta.TButton",
                background="#00FFFF",  # Cor de fundo desejada (exemplo: vermelho)
                foreground="black",    # Cor do texto (exemplo: branco)
                padding=10,            # Ajuste do preenchimento do botão
                font=("Arial", 10, "bold"),
                relief="raised")

style = ttk.Style()
style.configure("BotaoExcluirCarta.TButton",
                background="#800000",  # Cor de fundo desejada (exemplo: vermelho)
                foreground="black",    # Cor do texto (exemplo: branco)
                padding=10,            # Ajuste do preenchimento do botão
                font=("Arial", 10, "bold"),
                relief="raised")

# Inicialize as variáveis globais
pagina_atual = 1
baralho = []  # Lista de imagens das cartas
baralho_nomes = []  # Lista de nomes das cartas
deck = []  # Cartas no deck
descartadas = []  # Cartas descartadas
carta_selecionada = None  # Índice da carta selecionada no deck
cartas_por_pagina = 5  # Número máximo de cartas visíveis no painel de descarte
pagina_descarte = 0  # Página atual no painel de descarte
pagina_deck = 0  # Página atual do deck
cartas_por_pagina_deck = 5  # Número de cartas por página
limite_deck = 0


# Painéis

frame_qtd_cartas = tk.Frame(root)
frame_qtd_cartas.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

lbl_qtd_cartas = tk.Label(frame_qtd_cartas, text="Quantidade de cartas no deck:")
lbl_qtd_cartas.pack(side=tk.LEFT, padx=5)

entry_qtd_cartas = tk.Entry(frame_qtd_cartas, width=10)
entry_qtd_cartas.insert(0, "10")  # Valor padrão
entry_qtd_cartas.pack(side=tk.LEFT, padx=5)

frame_baralho = tk.Frame(root)
frame_baralho.pack(side=tk.LEFT, fill=tk.Y)

lbl_baralho = tk.Label(frame_baralho, text="Cartas do Baralho")
lbl_baralho.pack()

lista_baralho = tk.Listbox(frame_baralho, height=20, width=30)  # Ajuste a largura para 40 colunas
lista_baralho.pack(padx=10, pady=0)

painel_deck = tk.LabelFrame(root, text="Deck", bd=3, relief=tk.GROOVE)
painel_deck.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

painel_descartes = tk.LabelFrame(root, text="Cartas Usadas", bd=3, relief=tk.GROOVE)
painel_descartes.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

# Botões
frame_opcoes = tk.Frame(root)
frame_opcoes.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

btn_selecionar_cartas = ttk.Button(frame_baralho, text="Selecionar Cartas", command=selecionar_cartas)
btn_selecionar_cartas.pack(pady=10)

btn_criar_deck = ttk.Button(frame_qtd_cartas, text="Criar Deck Aleatório", command=criar_deck_aleatorio)
btn_criar_deck.pack(side=tk.LEFT, padx=10, pady=10)

btn_descartar = ttk.Button(frame_opcoes, text="Usar Carta", command=descartar_carta, style="BotaoUsarCarta.TButton")
btn_descartar.pack(side=tk.LEFT, padx=5, pady=5)

btn_incluir = ttk.Button(frame_opcoes, text="Incluir Carta", command=incluir_carta, style="BotaoIncluirCarta.TButton")
btn_incluir.pack(side=tk.LEFT, padx=5, pady=5)

btn_excluir_todas = ttk.Button(frame_opcoes, text="Excluir Todas as Cartas", command=excluir_todas_as_cartas, style="BotaoExcluirCarta.TButton")
btn_excluir_todas.pack(side=tk.RIGHT, padx=0, pady=0)

# Inicializa o banco de dados
banco.inicializar_bd()
carregar_cartas()

root.mainloop()