from abc import ABC, abstractmethod
from entities.domain_models import Avaliacao, ReciboFiscal

class PersistenciaLivrariaPort(ABC):
    """
    Porta de saída (Output Port) definida pelo núcleo da aplicação.
    Aplica o DIP: a camada externa (TXT) é obrigada a implementar este contrato.
    """

    @abstractmethod
    def guardar_recibo(self, recibo: ReciboFiscal) -> None:
        pass

    @abstractmethod
    def ler_todos_recibos(self) -> list[str]:
        pass

    @abstractmethod
    def guardar_avaliacao(self, avaliacao: Avaliacao) -> None:
        pass

    @abstractmethod
    def ler_todas_avaliacoes(self) -> list[Avaliacao]:
        pass
