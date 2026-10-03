import json
import os

ARQUIVO_DADOS = "biblioteca_dados.json"


def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"livros": []}


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def cadastrar_livro(dados, titulo, autor, ano, isbn):
    for livro in dados["livros"]:
        if livro["isbn"] == isbn:
            print(f"[Erro] Já existe um livro cadastrado com o ISBN {isbn}.")
            return

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "disponivel": True,
        "usuario_emprestimo": None,
    }
    dados["livros"].append(novo_livro)
    salvar_dados(dados)
    print(f"Livro '{titulo}' cadastrado com sucesso!")


def listar_livros(dados):
    print("\n--- ACERVO DE LIVROS ---")
    if not dados["livros"]:
        print("Nenhum livro cadastrado.")
        return
    for livro in dados["livros"]:
        status = (
            "Disponível"
            if livro["disponivel"]
            else f"Emprestado para {livro['usuario_emprestimo']}"
        )
        print(
            f"ISBN: {livro['isbn']} | Título: {livro['titulo']} | Autor: {livro['autor']} | Ano: {livro['ano']} | Status: {status}"
        )


def emprestar_livro(dados, isbn, nome_usuario):
    for livro in dados["livros"]:
        if livro["isbn"] == isbn:
            if livro["disponivel"]:
                livro["disponivel"] = False
                livro["usuario_emprestimo"] = nome_usuario
                salvar_dados(dados)
                print(
                    f"Livro '{livro['titulo']}' emprestado para {nome_usuario}!"
                )
                return
            else:
                print(
                    f"[Erro] O livro '{livro['titulo']}' já está emprestado."
                )
                return
    print(f"[Erro] Livro com ISBN {isbn} não encontrado.")


def devolver_livro(dados, isbn):
    for livro in dados["livros"]:
        if livro["isbn"] == isbn:
            if not livro["disponivel"]:
                livro["disponivel"] = True
                usuario = livro["usuario_emprestimo"]
                livro["usuario_emprestimo"] = None
                salvar_dados(dados)
                print(
                    f"Livro '{livro['titulo']}' devolvido por {usuario} com sucesso!"
                )
                return
            else:
                print(
                    f"[Aviso] O livro '{livro['titulo']}' já está disponível."
                )
                return
    print(f"[Erro] Livro com ISBN {isbn} não encontrado.")


def listar_disponiveis(dados):
    print("\n--- LIVROS DISPONÍVEIS ---")
    disponiveis = [l for l in dados["livros"] if l["disponivel"]]
    if not disponiveis:
        print("Nenhum livro disponível.")
        return
    for livro in disponiveis:
        print(
            f"ISBN: {livro['isbn']} | Título: {livro['titulo']} | Autor: {livro['autor']}"
        )


if __name__ == "__main__":
    dados = carregar_dados()
    print("=== TESTE PARADIGMA IMPERATIVO ===")
    cadastrar_livro(
        dados, "Dom Casmurro", "Machado de Assis", 1899, "9788535902778"
    )
    cadastrar_livro(dados, "1984", "George Orwell", 1949, "9788535909555")
    listar_livros(dados)
    emprestar_livro(dados, "9788535902778", "Jônatas")
    listar_disponiveis(dados)
    devolver_livro(dados, "9788535902778")