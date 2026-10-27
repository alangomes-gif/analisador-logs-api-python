"""Gera um relatório HTML estático a partir do resumo JSON do analisador."""
import argparse
import html
import json
from pathlib import Path


def renderizar(resumo):
    def escapar(valor):
        return html.escape(str(valor), quote=True)

    def tabela(titulo, dados):
        linhas = ''.join('<tr><td>' + escapar(chave) + '</td><td>' + escapar(valor) + '</td></tr>' for chave, valor in dados.items())
        return '<h2>' + titulo + '</h2><table><thead><tr><th>Item</th><th>Quantidade</th></tr></thead><tbody>' + linhas + '</tbody></table>'

    campos = [('Requisições válidas', 'requisicoes_validas'), ('Linhas inválidas', 'linhas_invalidas'), ('Latência média (ms)', 'latencia_media_ms'), ('Respostas 4xx/5xx', 'respostas_4xx_5xx')]
    indicadores = ''.join('<li><strong>' + titulo + ':</strong> ' + escapar(resumo[chave]) + '</li>' for titulo, chave in campos)
    return ('<!doctype html><html lang="pt-BR"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Relatório de logs de API</title>'
            '<style>body{font:18px system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#15283b}table{border-collapse:collapse;width:100%}th,td{padding:12px;border:1px solid #ccd4dc;text-align:left}th{background:#edf4fa}li{margin:12px 0}</style>'
            '<h1>Relatório de logs de API</h1><p>Resumo estático do arquivo analisado.</p><ul>' + indicadores + '</ul>'
            + tabela('Códigos HTTP', resumo['status_http']) + tabela('Rotas', resumo['rotas']) + '</html>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resumo', help='Arquivo JSON gerado por analisador.py')
    parser.add_argument('--saida', default='relatorio.html')
    args = parser.parse_args()
    if Path(args.resumo).resolve() == Path(args.saida).resolve():
        parser.error('Entrada e saída devem ser diferentes')
    dados = json.loads(Path(args.resumo).read_text(encoding='utf-8-sig'))
    Path(args.saida).write_text(renderizar(dados), encoding='utf-8')
