"""Analisa logs JSONL de uma API sem carregar o arquivo inteiro em memória."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def analisar(caminho):
    status = Counter()
    rotas = Counter()
    total_ms = 0.0
    validos = invalidos = 0
    with Path(caminho).open(encoding='utf-8-sig') as arquivo:
        for linha in arquivo:
            if not linha.strip():
                continue
            try:
                registro = json.loads(linha)
                codigo = registro['status']
                rota = registro['rota']
                duracao = registro['duracao_ms']
                if (type(codigo) is not int or not 100 <= codigo <= 599
                        or not isinstance(rota, str) or not rota.startswith('/')
                        or type(duracao) not in (int, float)
                        or not math.isfinite(duracao) or duracao < 0):
                    raise ValueError('Registro inválido')
                novo_total = total_ms + duracao
                if not math.isfinite(novo_total):
                    raise ValueError('Duração acumulada fora do limite')
            except (json.JSONDecodeError, KeyError, TypeError, ValueError, OverflowError):
                invalidos += 1
                continue
            validos += 1
            total_ms = novo_total
            status[str(codigo)] += 1
            rotas[rota] += 1
    erros = sum(contagem for codigo, contagem in status.items() if int(codigo) >= 400)
    erros_servidor = sum(contagem for codigo, contagem in status.items() if int(codigo) >= 500)
    return {
        'requisicoes_validas': validos,
        'linhas_invalidas': invalidos,
        'respostas_4xx_5xx': erros,
        'respostas_5xx': erros_servidor,
        'percentual_4xx_5xx': round(100 * erros / validos, 2) if validos else 0.0,
        'latencia_media_ms': round(total_ms / validos, 2) if validos else 0.0,
        'status_http': dict(sorted(status.items())),
        'rotas': dict(sorted(rotas.items())),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arquivo', help='Log JSONL, com um objeto JSON por linha')
    parser.add_argument('--saida', default='relatorio.json')
    argumentos = parser.parse_args()
    if Path(argumentos.arquivo).resolve() == Path(argumentos.saida).resolve():
        parser.error('Entrada e saída devem ser arquivos diferentes')
    relatorio = analisar(argumentos.arquivo)
    texto = json.dumps(relatorio, ensure_ascii=False, indent=2)
    Path(argumentos.saida).write_text(texto + '\n', encoding='utf-8')
    print(texto)
