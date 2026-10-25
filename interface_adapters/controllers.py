from use_cases.interactors import LivrariaUseCaseInteractor

class LivrariaAdapterController:
    def __init__(self, interactor: LivrariaUseCaseInteractor):
        self.interactor = interactor

    def construir_view_model(self, termo_busca: str = "") -> dict:
        livros = self.interactor.listar_catalogo(termo_busca)
        catalogo_formatado = []
        for l in livros:
            catalogo_formatado.append({
                "id": l.id,
                "titulo": l.titulo,
                "autor": l.autor,
                "genero": l.genero,
                "isbn": l.isbn,
                "preco": l.preco,
                "media_estrelas": self.interactor.calcular_media_avaliacoes(l.id)
            })

        return {
            "livros": catalogo_formatado,
            "carrinho": self.interactor.carrinho,
            "subtotal": self.interactor.calcular_subtotal(),
            "ultimo_qr": self.interactor.ultimo_qr_gerado,
            "recibos_persistidos": self.interactor.repo.ler_todos_recibos(),
            "avaliacoes_persistidas": self.interactor.repo.ler_todas_avaliacoes(),
            "termo_atual": termo_busca
        }

    def adicionar_livro(self, livro_id: int):
        return self.interactor.adicionar_ao_carrinho_id(livro_id)

    def escanear_codigo(self, isbn: str):
        return self.interactor.scan_and_go_isbn(isbn)

    def remover_item(self, indice: int):
        self.interactor.remover_do_carrinho(indice)

    def submeter_avaliacao(self, livro_id: str, utilizador: str, nota: str, comentario: str):
        return self.interactor.registar_avaliacao_livro(
            livro_id=int(livro_id),
            utilizador=utilizador,
            nota=int(nota),
            comentario=comentario
        )

    def concluir_pagamento(self, cpf: str):
        return self.interactor.finalizar_compra_pix(cpf)
