import json
import pathlib
from typing import Dict, List, Union


class CarregadorDados:
    def __init__(self, diretorio_dados: str = None):
        if diretorio_dados is None:
            # Subir um nível para acessar o diretório actions
            diretorio_base = pathlib.Path(__file__).parent.parent.parent
            self.diretorio_dados = diretorio_base / "actions" / "json"
        else:
            self.diretorio_dados = pathlib.Path(diretorio_dados)

        if not self.diretorio_dados.exists():
            print(f"AVISO: Diretório não encontrado: {self.diretorio_dados}")
            print(f"Diretório atual: {pathlib.Path.cwd()}")

    def carregar_json(self, nome_arquivo: str) -> Union[Dict, List]:
        caminho_arquivo = self.diretorio_dados / nome_arquivo

        if not caminho_arquivo.exists():
            return {} if nome_arquivo == "compras.json" else []

        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def listar_arquivos_despesas(self) -> List[str]:
        return [f.name for f in self.diretorio_dados.glob("despesas_*.json")]

    def listar_arquivos_renuncias(self) -> List[str]:
        return [f.name for f in self.diretorio_dados.glob("renuncias_*.json")]

    def carregar_dados_compras(self) -> Dict:
        return self.carregar_json("compras.json")

    def carregar_dados_despesas(self, arquivo: str) -> List:
        return self.carregar_json(arquivo)

    def carregar_dados_bolsa_familia(self) -> Dict:
        return self.carregar_json("bolsafamilia.json")

    def carregar_dados_renuncia(self, arquivo: str) -> List:
        return self.carregar_json(arquivo)
