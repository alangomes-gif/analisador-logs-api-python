"""Testes do comando completo, usando arquivos temporários e Python real."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('analisador.py').resolve()


class TestCLI(unittest.TestCase):
    def test_exporta_json_em_pasta_com_espacos(self):
        with tempfile.TemporaryDirectory(prefix='logs api ') as pasta:
            origem = Path(pasta) / 'entrada.jsonl'
            destino = Path(pasta) / 'resultado.json'
            origem.write_text('\ufeff\n' + json.dumps({'rota': '/saúde', 'status': 200, 'duracao_ms': 12.5}, ensure_ascii=False) + '\nlinha inválida\n', encoding='utf-8')
            processo = subprocess.run([sys.executable, str(SCRIPT), str(origem), '--saida', str(destino)], capture_output=True, text=True, encoding='utf-8', env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'}, timeout=15)
            self.assertEqual(processo.returncode, 0, processo.stderr)
            resultado = json.loads(destino.read_text(encoding='utf-8'))
            self.assertEqual(json.loads(processo.stdout), resultado)
            self.assertEqual(resultado['requisicoes_validas'], 1)
            self.assertEqual(resultado['linhas_invalidas'], 1)
            self.assertEqual(resultado['latencia_media_ms'], 12.5)
            self.assertEqual(resultado['rotas'], {'/saúde': 1})

    def test_arquivo_ausente_nao_cria_relatorio(self):
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / 'resultado.json'
            processo = subprocess.run([sys.executable, str(SCRIPT), str(Path(pasta) / 'ausente.jsonl'), '--saida', str(destino)], capture_output=True, timeout=15)
            self.assertNotEqual(processo.returncode, 0)
            self.assertFalse(destino.exists())


if __name__ == '__main__':
    unittest.main()
