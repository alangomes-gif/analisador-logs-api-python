import json
import tempfile
import unittest
from pathlib import Path
from analisador import analisar

class TestAnalisador(unittest.TestCase):
    def executar(self, linhas):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as pasta:
            caminho = Path(pasta)/'log.jsonl'
            caminho.write_text(linhas, encoding='utf-8')
            return analisar(caminho)
    def test_contagem_e_latencia(self):
        entradas = [{'rota':'/api','status':200,'duracao_ms':100}, {'rota':'/api','status':500,'duracao_ms':300}]
        resultado = self.executar('\n'.join(json.dumps(x) for x in entradas))
        self.assertEqual(resultado['requisicoes_validas'], 2)
        self.assertEqual(resultado['percentual_4xx_5xx'], 50)
        self.assertEqual(resultado['latencia_media_ms'], 200)
        self.assertEqual(resultado['respostas_5xx'], 1)
    def test_vazio_sem_divisao_por_zero(self):
        resultado = self.executar('\n')
        self.assertEqual(resultado['latencia_media_ms'], 0)
        self.assertEqual(resultado['requisicoes_validas'], 0)
    def test_invalidos_nao_interrompem_o_arquivo(self):
        texto = '\n'.join(['null', '[]', 'nao e json', '{"rota":"/x","status":200,"duracao_ms":NaN}', '{"rota":"/x","status":true,"duracao_ms":2}', '{"rota":"/x","status":200,"duracao_ms":-1}', '{"rota":"/ok","status":200,"duracao_ms":5}'])
        resultado = self.executar(texto)
        self.assertEqual(resultado['linhas_invalidas'], 6)
        self.assertEqual(resultado['requisicoes_validas'], 1)
    def test_demonstracao(self):
        resultado = analisar(Path(__file__).with_name('exemplo.jsonl'))
        self.assertEqual(resultado['requisicoes_validas'], 10)
        self.assertEqual(resultado['linhas_invalidas'], 1)
        self.assertEqual(resultado['percentual_4xx_5xx'], 30)
        self.assertEqual(resultado['latencia_media_ms'], 190)

if __name__=='__main__': unittest.main()
