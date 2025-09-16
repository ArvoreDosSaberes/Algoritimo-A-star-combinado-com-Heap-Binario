[![CI](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/actions/workflows/ci.yml/badge.svg)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/actions/workflows/ci.yml)
![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.A_star_com_Heap_Binario)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
[![Language-C](https://img.shields.io/badge/language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))
[![CMake](https://img.shields.io/badge/build-CMake-informational.svg)](https://cmake.org/)
[![Raylib](https://img.shields.io/badge/graphics-raylib-2ea44f.svg)](https://www.raylib.com/)
[![Issues](https://img.shields.io/github/issues/ArvoreDosSaberes/A_star_com_Heap_Binario.svg)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/issues)
[![Stars](https://img.shields.io/github/stars/ArvoreDosSaberes/A_star_com_Heap_Binario.svg)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/stargazers)
[![Forks](https://img.shields.io/github/forks/ArvoreDosSaberes/A_star_com_Heap_Binario.svg)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/network/members)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![Watchers](https://img.shields.io/github/watchers/ArvoreDosSaberes/A_star_com_Heap_Binario)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/watchers)
[![Last Commit](https://img.shields.io/github/last-commit/ArvoreDosSaberes/A_star_com_Heap_Binario)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/commits)
[![Contributors](https://img.shields.io/github/contributors/ArvoreDosSaberes/A_star_com_Heap_Binario)](https://github.com/ArvoreDosSaberes/A_star_com_Heap_Binario/graphs/contributors)

# A* com Heap Binário

Este repositório contém uma explicação prática do Algoritmo A* (A-estrela) e de como combiná-lo com um heap binário para implementar de forma eficiente a fila de prioridade do conjunto aberto (open set).

## Resumo

- O A* seleciona o próximo nó a expandir minimizando `f(n) = g(n) + h(n)`, onde:
  - `g(n)` é o custo acumulado do início até `n`.
  - `h(n)` é a heurística (estimativa) do custo de `n` até o objetivo.
- Com heurística admissível e consistente, A* encontra o caminho ótimo.
- O heap binário oferece operações eficientes para a fila de prioridade:
  - Inserção: `O(log N)`
  - Extração do mínimo: `O(log N)`
- Na prática, usa-se lazy deletion para lidar com a ausência de `decrease-key` em heaps binários simples (como `heapq` do Python).

## Conteúdo detalhado

Para uma explicação completa, incluindo código de exemplo em Python, boas práticas e alternativas ao heap binário, consulte o tutorial:

- [TUTORIAL.md](./TUTORIAL.md)

## Executando o tabuleiro (Python/Pygame)

Este projeto inclui um tabuleiro interativo feito em Python com Pygame. O tabuleiro ocupa 80% da janela, utiliza células de 32x32 pixels e permite desenhar/apagar passando o mouse com o botão esquerdo pressionado (toggle por célula).

Passos recomendados (Linux):

1. Crie e ative um ambiente virtual

   ```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências

   ```bash
pip install -r requirements.txt
```

3. Execute o aplicativo

   ```bash
python main.py
```

Controles:
- Botão esquerdo do mouse pressionado: alterna o estado das células ao passar por cima (marca/desmarca).
- Fechar janela para encerrar.

## Referências rápidas

- Hart, Nilsson, Raphael (1968) — "A Formal Basis for the Heuristic Determination of Minimum Cost Paths".
- Russell & Norvig — "Artificial Intelligence: A Modern Approach".
- Implementações: `heapq` (Python), `std::priority_queue` (C++), `PriorityQueue` (Java).

## Licença

Este trabalho está licenciado sob a licença Creative Commons Atribuição-CompartilhaIgual 4.0 Internacional (CC BY-SA 4.0).

- Consulte o arquivo [`LICENSE.md`](./LICENSE.md) para detalhes.
- Resumo (legível por humanos): https://creativecommons.org/licenses/by-sa/4.0/deed.pt_BR
- Texto legal completo: https://creativecommons.org/licenses/by-sa/4.0/legalcode

Ao reutilizar, por favor:
- Atribua crédito apropriado, incluindo link para este repositório e para a licença.
- Indique se foram feitas alterações.
- Distribua obras derivadas sob a mesma licença (CompartilhaIgual).
