from datetime import datetime
from entities.domain_models import Livro, Avaliacao, ReciboFiscal
from use_cases.ports import PersistenciaLivrariaPort

class LivrariaUseCaseInteractor:
    def __init__(self, persistencia_port: PersistenciaLivrariaPort):
        # O Caso de Uso recebe a abstração por Injeção de Dependência (DIP)
        self.repo = persistencia_port
        self.catalogo = [
            Livro(1, "1984", "George Orwell", "Ficção Científica", "9780451524935", 45.00),
            Livro(2, "O Guia do Mochileiro das Galáxias", "Douglas Adams", "Ficção Científica", "9788530601492", 39.90),
            Livro(3, "Código Limpo (Clean Code)", "Robert C. Martin", "Tecnologia", "9788576082675", 89.90),
            Livro(4, "Arquitetura Limpa", "Robert C. Martin", "Tecnologia", "9788550804606", 79.50),
            Livro(5, "O Senhor dos Anéis", "J.R.R. Tolkien", "Fantasia", "9788595084742", 110.00)
        ]
        self.carrinho: list[Livro] = []
        self.ultimo_qr_gerado = None

    def listar_catalogo(self, termo: str = "") -> list[Livro]:
        if not termo:
            return self.catalogo
        t = termo.lower()
        return [l for l in self.catalogo if t in l.titulo.lower() or t in l.autor.lower()]

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return next((l for l in self.catalogo if l.id == int(livro_id)), None)

    def adicionar_ao_carrinho_id(self, livro_id: int) -> Livro | None:
        livro = self.buscar_por_id(livro_id)
        if livro:
            self.carrinho.append(livro)
            self.ultimo_qr_gerado = None
        return livro

    def scan_and_go_isbn(self, isbn: str) -> Livro | None:
        livro = next((l for l in self.catalogo if l.isbn == isbn.strip()), None)
        if livro:
            self.carrinho.append(livro)
            self.ultimo_qr_gerado = None
        return livro

    def remover_do_carrinho(self, indice: int) -> None:
        if 0 <= indice < len(self.carrinho):
            self.carrinho.pop(indice)

    def calcular_subtotal(self) -> float:
        return sum(item.preco for item in self.carrinho)

    # Nova Feature (Ex. 7.4): Registar Avaliações de Clientes e Persistir
    def registar_avaliacao_livro(self, livro_id: int, utilizador: str, nota: int, comentario: str) -> Avaliacao:
        livro = self.buscar_por_id(livro_id)
        if not livro:
            raise ValueError("Livro não encontrado para avaliação.")
        nova_avaliacao = Avaliacao(
            livro_id=livro.id,
            titulo_livro=livro.titulo,
            utilizador=utilizador,
            nota=int(nota),
            comentario=comentario
        )
        self.repo.guardar_avaliacao(nova_avaliacao)
        return nova_avaliacao

    def calcular_media_avaliacoes(self, livro_id: int) -> float:
        avaliacoes = [a for a in self.repo.ler_todas_avaliacoes() if a.livro_id == int(livro_id)]
        if not avaliacoes:
            return 5.0  # Nota padrão inicial
        return round(sum(a.nota for a in avaliacoes) / len(avaliacoes), 1)

    # Checkout com Persistência de Recibo Fiscal (CPF na Nota)
    def finalizar_compra_pix(self, cpf_cliente: str = "") -> ReciboFiscal | None:
        if not self.carrinho:
            return None
        total = self.calcular_subtotal()
        nomes_itens = ", ".join(i.titulo for i in self.carrinho)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        qr_code = f"QR-CLEAN-{int(datetime.now().timestamp())}"

        recibo = ReciboFiscal(
            data_hora=timestamp,
            cpf_cliente=cpf_cliente.strip(),
            itens_resumo=nomes_itens,
            valor_total=total,
            codigo_qr=qr_code
        )
        # Invoca a porta de persistência sem conhecer o ficheiro TXT
        self.repo.guardar_recibo(recibo)
        self.carrinho.clear()
        self.ultimo_qr_gerado = recibo.formatar_para_registo()
        return recibo
