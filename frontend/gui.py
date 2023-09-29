import typing
import ctypes
from collections import abc
from tkinter import (
    CENTER,
    DISABLED,
    END,
    NORMAL,
    BooleanVar,
    IntVar,
    Misc,
    StringVar,
    Text,
    Tk,
    Toplevel,
    Variable,
    W,
    X,
    filedialog,
    font,
    scrolledtext,
)
from tkinter.ttk import Button, Entry, Frame, Label, Style

import rsa

OPCOES_SELETOR: dict[str, typing.Any] = {
    "filetypes": (("Documentos de texto", "*.txt"), ("Todos os arquivos", "*")),
    "initialdir": ".",
}


def configurar_tk(raiz: Tk) -> None:
    fonte = font.nametofont("TkDefaultFont")
    fonte.configure(size=13)

    estilo = Style(raiz)
    estilo.configure("TEntry", padding=4)

    if hasattr(ctypes, "windll"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


def mostrar_opcoes(container: Tk) -> None:
    container.title("Projeto RSA")
    container.geometry("700x650")

    frame = Frame(container)
    frame.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.75)

    acoes = (
        ("Gerar chave pública", mostrar_gerar_chave_publica),
        ("Encriptar mensagem", mostrar_encriptar),
        ("Desencriptar mensagem", mostrar_desencriptar),
    )

    for texto, funcao in acoes:
        comando = lambda funcao=funcao: funcao(frame)
        botao = Button(frame, text=texto, command=comando)
        botao.pack(fill=X, pady=5)


def mostrar_gerar_chave_publica(container: Misc) -> None:
    v_p = IntVar()
    v_q = IntVar()
    v_e = IntVar()

    def gerar_chave_publica() -> tuple[bool, str]:
        e = v_e.get()
        n = rsa.gerar_chave_publica(v_p.get(), v_q.get(), e)
        return (True, f"{n} {e}") if n else (False, "Entrada inválida")

    campos = (("Primo p", v_p), ("Primo q", v_q), ("Expoente e", v_e))

    mostrar_formulario(
        container,
        "Gerar chave pública",
        campos,
        "Chave pública",
        "chave_publica",
        "Ainda não gerada",
        "Gerar",
        gerar_chave_publica,
    )


def mostrar_encriptar(container: Misc) -> None:
    v_msg = StringVar()
    v_n = IntVar()
    v_e = IntVar()

    def encriptar_mensagem() -> tuple[bool, str]:
        n = v_n.get()
        e = v_e.get()

        if n and e:
            msg_cripto = rsa.encriptar(v_msg.get().encode(), n, e)
            return True, " ".join(map(str, msg_cripto))
        else:
            return False, "Números inválidos"

    campos = (("Mensagem", v_msg), ("Chave pública", v_n), ("Expoente e", v_e))

    mostrar_formulario(
        container,
        "Encriptar mensagem",
        campos,
        "Mensagem encriptada",
        "encriptado",
        "Ainda não encriptada",
        "Encriptar",
        encriptar_mensagem,
        True,
    )


def mostrar_desencriptar(container: Misc) -> None:
    v_msg_cripto = StringVar()
    v_p = IntVar()
    v_q = IntVar()
    v_e = IntVar()

    def desencriptar_mensagem() -> tuple[bool, str]:
        p = v_p.get()
        q = v_q.get()
        e = v_e.get()

        if p and q and e:
            msg_cripto = list(map(int, v_msg_cripto.get().split()))
            msg = rsa.desencriptar(msg_cripto, p, q, e)
            return True, msg.decode()
        else:
            return False, "Números inválidos"

    campos = (
        ("Mensagem encriptada", v_msg_cripto),
        ("Primo p", v_p),
        ("Primo q", v_q),
        ("Expoente e", v_e),
    )

    mostrar_formulario(
        container,
        "Desencriptar mensagem",
        campos,
        "Mensagem",
        "desencriptado",
        "Ainda não desencriptada",
        "Desencriptar",
        desencriptar_mensagem,
        True,
    )


def mostrar_formulario(
    container: Misc,
    titulo: str,
    campos: tuple[tuple[str, Variable], ...],
    nome_saida: str,
    nome_arquivo: str,
    saida_padrao: str,
    nome_botao: str,
    gerar_saida: abc.Callable[[], tuple[bool, str]],
    primeiro_multilinha: bool = False,
) -> None:
    v_valido = BooleanVar()

    def comando_gerar() -> None:
        valido, saida = gerar_saida()
        v_valido.set(valido)
        texto_saida.configure(state=NORMAL)
        texto_saida.replace("1.0", END, saida)
        texto_saida.configure(state=DISABLED)

    def comando_carregar(entrada: Text) -> None:
        arquivo = filedialog.askopenfile(**OPCOES_SELETOR)
        if not arquivo:
            return

        with arquivo:
            entrada.replace("1.0", END, arquivo.read().strip())

    def comando_salvar() -> None:
        if not v_valido.get():
            return

        caminho = nome_arquivo + ".txt"
        arquivo = filedialog.asksaveasfile(initialfile=caminho, **OPCOES_SELETOR)
        if not arquivo:
            return

        with arquivo:
            arquivo.write(texto_saida.get("1.0", END))

    janela = Toplevel(container)
    janela.title(titulo)
    janela.geometry("700x650")
    janela.grab_set()

    frame = Frame(janela)
    frame.place(anchor=CENTER, relx=0.5, rely=0.5, relwidth=0.85)

    entrada: Entry | Text
    primeiro = True

    for nome, var in campos:
        rotulo = Label(frame, text=nome + ": ")
        rotulo.pack(anchor=W)

        if primeiro_multilinha and primeiro:
            primeiro = False
            entrada = criar_componente_texto(frame, typing.cast(StringVar, var))
            entrada.pack(fill=X)
            comando_carregar_c = lambda entrada=entrada: comando_carregar(entrada)
            botao_carregar = Button(frame, text="Carregar", command=comando_carregar_c)
            botao_carregar.pack(fill=X, pady=(5, 20))
        else:
            entrada = Entry(frame, textvariable=var, width=40)
            entrada.pack(fill=X, pady=(0, 20))

    rotulo_nome_saida = Label(frame, text=nome_saida + ": ")
    rotulo_nome_saida.pack(anchor=W)

    texto_saida = scrolledtext.ScrolledText(frame, height=5, padx=4, pady=4)
    texto_saida.insert(END, saida_padrao)
    texto_saida.configure(state=DISABLED)
    texto_saida.pack(fill=X, pady=(0, 20))

    botao_gerar = Button(frame, text=nome_botao, command=comando_gerar)
    botao_gerar.pack(side="left")

    botao_salvar = Button(frame, text="Salvar", command=comando_salvar)
    botao_salvar.pack(side="right")


def criar_componente_texto(container: Misc, var: StringVar) -> Text:
    def conectar_var_a_text(nome: str, indice: str, modo: str) -> None:
        var.set(entrada.get("1.0", END).rstrip("\n"))

    entrada = scrolledtext.ScrolledText(container, height=5, padx=4, pady=4)
    entrada.insert(END, var.get())
    var.trace_add("read", conectar_var_a_text)
    return entrada


def main() -> None:
    raiz = Tk()
    configurar_tk(raiz)
    mostrar_opcoes(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
