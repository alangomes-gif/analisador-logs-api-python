import unittest
from relatorio_html import renderizar

class TestHTML(unittest.TestCase):
    def resumo(self, rotas):
        return dict(requisicoes_validas=1, linhas_invalidas=0, latencia_media_ms=12.5, respostas_4xx_5xx=0, status_http={'200':1}, rotas=rotas)

    def test_rota_nao_injeta_html(self):
        resultado = renderizar(self.resumo({'/<script>alert("x")</script>': 1}))
        self.assertNotIn('<script>', resultado)
        self.assertIn('&lt;script&gt;', resultado)
        self.assertIn('&quot;x&quot;', resultado)

    def test_indicadores_e_tabelas(self):
        resultado = renderizar(self.resumo({'/api': 1}))
        self.assertIn('12.5', resultado)
        self.assertIn('<td>/api</td><td>1</td>', resultado)
        self.assertEqual(resultado.count('<table>'), 2)
        self.assertIn('lang="pt-BR"', resultado)

if __name__ == '__main__':
    unittest.main()
