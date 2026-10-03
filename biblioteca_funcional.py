import json
import os

ARQUIVO_DADOS = "biblioteca_dados.json"


def carregar_dados(arquivo=ARQUIVO_DADOS):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return tuple(json.load(f).get("livros", []))
    return ()


def salvar_dados(acervo, arquivo=ARQUIVO_DADOS):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump({"livros": list(acervo)}, f, indent=4, ensure_ascii=False)


def cadastrar_livro(acervo, titulo, autor, ano, isbn):
    if any(livro["isbn"] == isbn for livro in acervo):
        print(f"Erro: Livro com ISBN {isbn} já existe.")
        return acervo

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "disponivel": True,
        "usuario_emprestimo": None,
    }
    novo_acervo = acervo + (novo_livro,)
    salvar_dados(novo_acervo)
    print(f"Livro '{titulo}' cadastrado no paradigma Funcional!")
    return novo_acervo


def emprestar_livro(acervo, isbn, nome_usuario):
    def atualizar(livro):
        if livro["isbn"] == isbn and livro["disponivel"]:
            return {
                **livro,
                "disponivel": False,
                "usuario_emprestimo": nome_usuario,
            }
        return livro

    novo_acervo = tuple(map(atualizar, acervo))
    salvar_dados(novo_acervo)
    print(f"Empréstimo processado para ISBN: {isbn}")
    return novo_acervo


def devolver_livro(acervo, isbn):
    def atualizar(livro):
        if livro["isbn"] == isbn and not livro["disponivel"]:
            return {**livro, "disponivel": True, "usuario_emprestimo": None}
        return livro

    novo_acervo = tuple(map(atualizar, acervo))
    salvar_dados(novo_acervo)
    print(f"Devolução processada para ISBN: {isbn}")
    return novo_acervo


def filtrar_disponiveis(acervo):
    return tuple(filter(lambda livro: livro["disponivel"], acervo))


def exibir_acervo(acervo, titulo_secao="ACERVO"):
    print(f"\n--- {titulo_secao} (FUNCIONAL) ---")
    if not acervo:
        print("Nenhum livro cadastrado/encontrado.")
        return
    for livro in acervo:
        status = (
            "Disponível"
            if livro["disponivel"]
            else f"Emprestado para {livro['usuario_emprestimo']}"
        )
        print(
            f"ISBN: {livro['isbn']} | Título: {livro['titulo']} | Status: {status}"
        )


if __name__ == "__main__":
    acervo_inicial = carregar_dados()
    acervo1 = cadastrar_livro(
        acervo_inicial, "O Cortiço", "Aluísio Azevedo", 1890, "978-8508041534"
    )  #[cite: 7]
    exibir_acervo(acervo1)  #[cite: 7]

    acervo2 = emprestar_livro(
        acervo1, "978-8508041534", "Jônatas Coutinho"
    )  #[cite: 7, 8]
    exibir_acervo(filtrar_disponiveis(acervo2), "LIVROS DISPONÍVEIS")  #[cite: 7]

    acervo3 = devolver_livro(acervo2, "978-8508041534")  #[cite: 7]
    exibir_acervo(acervo3)  #[cite: 7]