# Analisador de logs de API em Python

Projeto de portfólio para analisar logs JSONL e gerar um resumo de códigos HTTP, rotas e latência média. Os dados da demonstração são fictícios.

## Executar

Python 3.10 ou superior, sem dependências externas:

    python analisador.py exemplo.jsonl --saida relatorio.json
    python -m unittest -v

Cada linha precisa conter: rota (texto iniciado em /), status (inteiro entre 100 e 599) e duracao_ms (número finito, maior ou igual a zero). Linhas vazias são ignoradas; registros inválidos são contados separadamente e não interrompem o processamento.

## Resultado do exemplo

10 registros válidos, 1 linha inválida, latência média de 190 ms, 3 respostas 4xx/5xx (30%) e 1 resposta 5xx. A taxa de 30% descreve apenas o arquivo fictício; não representa um serviço real.

## Limites

Ferramenta local de análise de arquivos, sem monitoramento ao vivo, autenticação ou integração com plataformas de observabilidade. Não calcula percentis de latência. A leitura é linha a linha, mas o uso de memória dos contadores cresce com o número de rotas distintas. Não coloque tokens, endereços de clientes ou dados pessoais nos logs compartilhados.
