from dataclasses import dataclass

@dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    genero: str
    isbn: str
    preco: float


@dataclass
class Avaliacao:
    livro_id: int
    titulo_livro: str
    utilizador: str
    nota: int
    comentario: str

    def __post_init__(self):
        if not (1 <= int(self.nota) <= 5):
            raise ValueError("A nota da avaliação deve ser entre 1 e 5 estrelas.")
        if not self.utilizador.strip():
            raise ValueError("O nome do utilizador é obrigatório.")


@dataclass
class ReciboFiscal:
    data_hora: str
    cpf_cliente: str
    itens_resumo: str
    valor_total: float
    codigo_qr: str

    def formatar_para_registo(self) -> str:
        cpf_exibicao = self.cpf_cliente if self.cpf_cliente else "Não informado"
        return (
            f"[{self.data_hora}] CPF: {cpf_exibicao} | "
            f"Itens: {self.itens_resumo} | Total PIX: R$ {self.valor_total:.2f} | "
            f"QR: {self.codigo_qr}"
        )
