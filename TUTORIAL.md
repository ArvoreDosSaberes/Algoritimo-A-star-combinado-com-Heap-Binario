# Algoritmo A* combinado com heap binário

Este tutorial explica o que é o Algoritmo A* (A-estrela), como ele funciona, e por que é comum combiná-lo com um heap binário para implementar a fila de prioridade do conjunto aberto (open set).

## Visão geral do A*

O A* é um algoritmo de busca de caminho ótimo e completo em grafos quando utiliza uma heurística admissível e consistente. Ele seleciona o próximo nó a expandir com base em uma função de custo:

- f(n) = g(n) + h(n)
  - g(n): custo real acumulado do nó inicial até n
  - h(n): heurística (estimativa) do custo de n até o objetivo

Se a heurística for:
- Admissível (nunca superestima o custo restante), e
- Consistente/monótona (h(n) ≤ custo(n, n') + h(n') para toda aresta (n, n')),

então o A* encontra um caminho ótimo (de menor custo).

## Estrutura de dados: por que usar um heap binário

Durante a execução do A*, mantemos um conjunto de nós a serem explorados (open set), ordenados pelo menor valor de f(n). A forma eficiente de fazer isso é usar uma fila de prioridade. Um heap binário é uma implementação simples e rápida para essa fila:

- Inserção: O(log N)
- Extração do mínimo (retirar o nó com menor f): O(log N)

Isso torna a etapa crítica do A* eficiente. Com heap binário, a complexidade típica de tempo fica em torno de O(E log V), onde cada relaxamento/atualização de aresta pode envolver operações no heap.

### Observação sobre decrease-key

Heaps binários simples (como `heapq` do Python) não oferecem uma operação explícita de decrease-key. Prática comum:
- Inserir novamente o mesmo nó com o novo custo menor e marcar a entrada antiga como obsoleta (lazy deletion). Ao extrair do heap, se a entrada não corresponder ao melhor custo atual do nó, ela é ignorada.

## Alternativas ao heap binário

- Heap de Fibonacci: melhor complexidade amortizada para decrease-key, porém mais complexo e nem sempre mais rápido na prática.
- Pairing heap: boa alternativa prática, com implementação mais simples que Fibonacci.
- Bucket queues/radix heaps: eficazes quando os pesos são inteiros e limitados em faixa.

## Exemplo prático (Python com `heapq`)

O exemplo abaixo ilustra um A* genérico usando `heapq` como heap binário e a técnica de lazy deletion. Ajuste `neighbors_fn`, `cost_fn` e `h_fn` ao seu problema.

```python
import heapq

def a_star(start, goal, neighbors_fn, cost_fn, h_fn):
    open_heap = []  # elementos: (f, seq, node)
    g = {start: 0.0}
    came_from = {}

    f0 = h_fn(start, goal)
    heapq.heappush(open_heap, (f0, 0, start))
    best_f = {start: f0}
    counter = 1

    while open_heap:
        f_curr, _, curr = heapq.heappop(open_heap)
        # Lazy deletion: ignora entradas superadas
        if best_f.get(curr, float('inf')) < f_curr:
            continue

        if curr == goal:
            # Reconstrução do caminho
            path = [curr]
            while curr in came_from:
                curr = came_from[curr]
                path.append(curr)
            path.reverse()
            return path, g[goal]

        for nxt in neighbors_fn(curr):
            tentative_g = g[curr] + cost_fn(curr, nxt)
            if tentative_g < g.get(nxt, float('inf')):
                g[nxt] = tentative_g
                came_from[nxt] = curr
                fn = tentative_g + h_fn(nxt, goal)
                best_f[nxt] = fn
                heapq.heappush(open_heap, (fn, counter, nxt))
                counter += 1

    return None, float('inf')  # nenhum caminho encontrado
```

## Quando usar A*

- Roteamento e menor caminho em grafos (mapas, redes, GPS).
- Planejamento de movimento (robótica, jogos).
- Qualquer problema em que exista custo real acumulado e uma boa heurística para o custo restante.

## Boas práticas

- Escolha heurísticas admissíveis e, preferencialmente, consistentes (por exemplo, distância euclidiana/manhattan em grades).
- Mantenha estruturas auxiliares para verificar se um nó já foi expandido ou para registrar o melhor custo até o momento.
- Trate empates no heap com um segundo critério estável (como um contador incremental), evitando comparação direta de nós.

## Complexidade

- Tempo: tipicamente O(E log V) com heap binário (E arestas, V vértices).
- Espaço: O(V), devido ao armazenamento de `g`, `came_from` e do conjunto aberto.

## Referências

- Hart, Nilsson, Raphael (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths".
- Russell & Norvig. "Artificial Intelligence: A Modern Approach".
- Implementações práticas: `heapq` (Python), `std::priority_queue` (C++), `PriorityQueue` (Java).
