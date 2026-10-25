import os
from entities.domain_models import Avaliacao, ReciboFiscal
from use_cases.ports import PersistenciaLivrariaPort

class TxtFileRepository(PersistenciaLivrariaPort):
    """
    Adaptador concreto de persistência em ficheiro TXT.
    Implementa PersistenciaLivrariaPort respeitando o DIP.
    """

    def __init__(self, caminho_txt: str = "bd_livraria.txt"):
        self.caminho_txt = caminho_txt
        self._inicializar_ficheiro()

    def _inicializar_ficheiro(self) -> None:
        if not os.path.exists(self.caminho_txt):
            with open(self.caminho_txt, "w", encoding="utf-8") as f:
                f.write("# BASE DE DADOS TXT - LIVRARIA CLEAN ARCHITECTURE\n")

    def guardar_recibo(self, recibo: ReciboFiscal) -> None:
        linha = f"RECIBO|{recibo.formatar_para_registo()}\n"
        with open(self.caminho_txt, "a", encoding="utf-8") as f:
            f.write(linha)

    def ler_todos_recibos(self) -> list[str]:
        recibos = []
        if not os.path.exists(self.caminho_txt):
            return recibos
        with open(self.caminho_txt, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.startswith("RECIBO|"):
                    recibos.append(linha.replace("RECIBO|", "").strip())
        return recibos

    def guardar_avaliacao(self, av: Avaliacao) -> None:
        comentario_limpo = av.comentario.replace("|", "/")
        utilizador_limpo = av.utilizador.replace("|", "/")
        linha = f"AVALIACAO|{av.livro_id}|{av.titulo_livro}|{utilizador_limpo}|{av.nota}|{comentario_limpo}\n"
        with open(self.caminho_txt, "a", encoding="utf-8") as f:
            f.write(linha)

    def ler_todas_avaliacoes(self) -> list[Avaliacao]:
        avaliacoes = []
        if not os.path.exists(self.caminho_txt):
            return avaliacoes
        with open(self.caminho_txt, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.startswith("AVALIACAO|"):
                    partes = linha.strip().split("|")
                    if len(partes) == 6:
                        avaliacoes.append(
                            Avaliacao(
                                livro_id=int(partes[1]),
                                titulo_livro=partes[2],
                                utilizador=partes[3],
                                nota=int(partes[4]),
                                comentario=partes[5]
                            )
                        )
        return avaliacoes
