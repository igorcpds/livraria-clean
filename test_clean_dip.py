import os
from entities.domain_models import Avaliacao, ReciboFiscal
from use_cases.ports import PersistenciaLivrariaPort
from use_cases.interactors import LivrariaUseCaseInteractor
from frameworks_drivers.txt_repository import TxtFileRepository


class FakeInMemoryRepository(PersistenciaLivrariaPort):
    """Repositório falso em memória para provar que o núcleo não depende do TXT (DIP)."""
    def __init__(self):
        self.recibos = []
        self.avaliacoes = []

    def guardar_recibo(self, recibo: ReciboFiscal) -> None:
        self.recibos.append(recibo.formatar_para_registo())

    def ler_todos_recibos(self) -> list[str]:
        return self.recibos

    def guardar_avaliacao(self, avaliacao: Avaliacao) -> None:
        self.avaliacoes.append(avaliacao)

    def ler_todas_avaliacoes(self) -> list[Avaliacao]:
        return self.avaliacoes


def test_nucleo_independente_de_tecnologia_dip():
    repo_memoria = FakeInMemoryRepository()
    interactor = LivrariaUseCaseInteractor(persistencia_port=repo_memoria)

    interactor.adicionar_ao_carrinho_id(1)
    recibo = interactor.finalizar_compra_pix(cpf_cliente="111.222.333-44")

    assert recibo is not None
    assert len(repo_memoria.ler_todos_recibos()) == 1


def test_persistencia_real_em_ficheiro_txt(tmp_path):
    ficheiro_teste = tmp_path / "teste_bd.txt"
    repo_txt = TxtFileRepository(str(ficheiro_teste))
    interactor = LivrariaUseCaseInteractor(persistencia_port=repo_txt)

    interactor.registar_avaliacao_livro(1, "Igor", 5, "Excelente arquitetura!")
    interactor.scan_and_go_isbn("9780451524935")
    interactor.finalizar_compra_pix("999.888.777-66")

    assert os.path.exists(ficheiro_teste)
    assert len(repo_txt.ler_todas_avaliacoes()) == 1
    assert len(repo_txt.ler_todos_recibos()) == 1
