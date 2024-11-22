import unittest
from main import criar_consumo_aleatorio, criar_grafico_consumo, colecao


class TestBancoDeDados(unittest.TestCase):
    def test_criar_consumo_aleatorio(self):
        """
        Testa se a função criar_consumo_aleatorio insere corretamente no banco de dados.
        """
        documentos_antes = colecao.count_documents({})
        criar_consumo_aleatorio()
        documentos_depois = colecao.count_documents({})
        self.assertEqual(documentos_depois, documentos_antes + 1)

    def test_criar_grafico(self):
        """
        Testa se a função criar_grafico_consumo não gera erros durante a execução.
        """
        try:
            criar_grafico_consumo()
        except Exception as e:
            self.fail(f"Erro ao criar gráfico: {e}")


if __name__ == "__main__":
    unittest.main()
