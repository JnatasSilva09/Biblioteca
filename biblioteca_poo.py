import json
import os


class Livro:

    def __init__(self, titulo, autor, ano, isbn, disponivel=True, usuario=None):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.disponivel = disponivel
        self.usuario_emprestimo = usuario

    def para_dicionario(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "isbn": self.isbn,
            "disponivel": self.disponivel,
            "usuario_emprestimo": self.usuario_emprestimo,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            titulo=dados.get("titulo", ""),
            autor=dados.get("autor", ""),
            ano=dados.get("ano", 0),
            isbn=dados.get("isbn", ""),
            disponivel=dados.get("disponivel", True),
            usuario=dados.get("usuario_emprestimo") or dados.get("usuario"),
        )


class Biblioteca:

    def __init__(self, arquivo_dados="biblioteca_dados.json"):
        self.arquivo_dados = arquivo_dados
        self.acervo = {}
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for item in dados.get("livros", []):
                    livro = Livro.de_dicionario(item)
                    self.acervo[livro.isbn] = livro

    def salvar_dados(self):
        dados = {"livros": [livro.para_dicionario() for livro in self.acervo.values()]}
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def cadastrar_livro(self, titulo, autor, ano, isbn):
        if isbn in self.acervo:
            print(f"[Erro] Já existe um livro cadastrado com o ISBN {isbn}.")
            return
        novo_livro = Livro(titulo, autor, ano, isbn)
        self.acervo[isbn] = novo_livro
        self.salvar_dados()
        print(f"Livro '{titulo}' cadastrado com sucesso (POO)!")

    def listar_livros(self):
        print("\n--- ACERVO DE LIVROS (POO) ---")
        if not self.acervo:
            print("Nenhum livro cadastrado.")
            return
        for livro in self.acervo.values():
            status = (
                "Disponível"
                if livro.disponivel
                else f"Emprestado para {livro.usuario_emprestimo}"
            )
            print(
                f"ISBN: {livro.isbn} | Título: {livro.titulo} | Autor: {livro.autor} | Status: {status}"
            )

    def emprestar_livro(self, isbn, nome_usuario):
        if isbn in self.acervo:
            livro = self.acervo[isbn]
            if livro.disponivel:
                livro.disponivel = False
                livro.usuario_emprestimo = nome_usuario
                self.salvar_dados()
                print(
                    f"Livro '{livro.titulo}' emprestado para {nome_usuario}!"
                )
            else:
                print(
                    f"[Erro] Livro já está emprestado para {livro.usuario_emprestimo}."
                )
        else:
            print(f"[Erro] ISBN {isbn} não encontrado.")

    def devolver_livro(self, isbn):
        if isbn in self.acervo:
            livro = self.acervo[isbn]
            if not livro.disponivel:
                usuario = livro.usuario_emprestimo
                livro.disponivel = True
                livro.usuario_emprestimo = None
                self.salvar_dados()
                print(
                    f"Livro '{livro.titulo}' devolvido por {usuario} com sucesso!"
                )
            else:
                print(f"[Aviso] O livro '{livro.titulo}' já está disponível.")
        else:
            print(f"[Erro] ISBN {isbn} não encontrado.")

    def listar_disponiveis(self):
        print("\n--- LIVROS DISPONÍVEIS (POO) ---")
        disponiveis = [l for l in self.acervo.values() if l.disponivel]
        if not disponiveis:
            print("Nenhum livro disponível no momento.")
            return
        for livro in disponiveis:
            print(
                f"ISBN: {livro.isbn} | Título: {livro.titulo} | Autor: {livro.autor}"
            )


if __name__ == "__main__":
    bib = Biblioteca()
    print("=== TESTE PARADIGMA ORIENTADO A OBJETOS ===")
    bib.cadastrar_livro(
        "Dom Casmurro", "Machado de Assis", 1899, "9788535902778"
    )
    bib.listar_livros()
    bib.emprestar_livro("9788535902778", "Jônatas")
    bib.listar_disponiveis()
    bib.devolver_livro("9788535902778")