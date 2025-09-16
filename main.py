"""Aplicativo interativo (Pygame) demonstrando o algoritmo A* com heap binário.

- Edite o grid com o mouse (False=livre, True=obstáculo).
- O agente persegue o cursor usando A* com heurística Manhattan e lazy deletion.
- Implementação usa `heapq` como fila de prioridade (heap binário).
"""
import sys
import math
import pygame
import heapq
from collections import deque

# Configurações da janela
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
BACKGROUND_COLOR = (30, 30, 36)
GRID_COLOR = (70, 70, 80)
CELL_COLOR = (60, 170, 90)
BORDER_COLOR = (200, 200, 220)
MOUSE_SQUARE_COLOR = (240, 180, 60)
AGENT_COLOR = (80, 180, 240)
PATH_COLOR = (200, 120, 200)

# Configurações do tabuleiro
CELL_SIZE = 16  # cada célula é 16x16 pixels
BOARD_SCALE = 0.8  # tabuleiro ocupa 80% da janela

# Agente perseguidor
AGENT_SPEED_PX_S = 220.0  # velocidade em pixels/segundo


def compute_board_rect(window_width: int, window_height: int, cell_size: int, scale: float) -> pygame.Rect:
    """Computa o retângulo do tabuleiro centralizado ocupando 'scale' da janela.
    Ajusta para múltiplos de cell_size e retorna um pygame.Rect.
    """
    board_w = int(window_width * scale)
    board_h = int(window_height * scale)

    # Ajusta para múltiplos de cell_size
    board_w -= board_w % cell_size
    board_h -= board_h % cell_size

    # Garante pelo menos 1 célula
    board_w = max(cell_size, board_w)
    board_h = max(cell_size, board_h)

    x = (window_width - board_w) // 2
    y = (window_height - board_h) // 2
    return pygame.Rect(x, y, board_w, board_h)


def create_grid(board_rect: pygame.Rect, cell_size: int):
    """Cria a matriz de células (grid) booleana alinhada ao retângulo do tabuleiro.

    Cada célula representa um bloco navegável (False) ou bloqueado/obstáculo (True).

    Parâmetros:
    - board_rect: área retangular ocupada pelo tabuleiro na janela.
    - cell_size: tamanho de cada célula, em pixels (lado do quadrado).

    Retorna:
    - Uma lista de listas de booleanos com dimensões `rows x cols`.
    """
    cols = board_rect.width // cell_size
    rows = board_rect.height // cell_size
    # Matriz de booleanos: False = vazio, True = marcado
    return [[False for _ in range(cols)] for _ in range(rows)]


def pos_to_cell(board_rect: pygame.Rect, cell_size: int, pos: tuple[int, int]):
    """Converte uma posição em pixels na janela para coordenadas de célula (linha, coluna).

    Se a posição estiver fora do `board_rect`, retorna None.

    Parâmetros:
    - board_rect: área do tabuleiro.
    - cell_size: tamanho da célula em pixels.
    - pos: tupla (x, y) em pixels, no espaço da janela.

    Retorna:
    - (row, col) como inteiros, ou None se fora do tabuleiro.
    """
    x, y = pos
    # Verifica se está dentro do tabuleiro
    if not board_rect.collidepoint(x, y):
        return None
    rel_x = x - board_rect.left
    rel_y = y - board_rect.top
    col = rel_x // cell_size
    row = rel_y // cell_size
    return int(row), int(col)


def nearest_free_cell(grid, start_rc: tuple[int, int]):
    """Encontra a célula livre mais próxima a partir de `start_rc` (inclusive ela mesma).
    
    A busca usa BFS em 4 direções (cima, baixo, esquerda, direita), o que
    garante encontrar a célula livre mais próxima em termos de distância Manhattan.
    Caso não exista célula livre acessível, retorna None.

    Parâmetros:
    - grid: matriz booleana com obstáculos.
    - start_rc: tupla (row, col) a partir da qual se inicia a expansão.

    Retorna:
    - Tupla (row, col) da célula livre mais próxima ou None.
    """
    if start_rc is None:
        return None
    sr, sc = start_rc
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return None
    if valid_cell(grid, sr, sc):
        return start_rc
    q = deque()
    q.append(start_rc)
    seen = {start_rc}
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                if valid_cell(grid, nr, nc):
                    return (nr, nc)
                seen.add((nr, nc))
                q.append((nr, nc))
    return None


def toggle_cell(grid, cell):
    """Alterna o estado de uma célula no grid entre livre (False) e bloqueado (True)."""
    r, c = cell
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        grid[r][c] = not grid[r][c]


def draw_board(surface: pygame.Surface, board_rect: pygame.Rect, grid, cell_size: int):
    """Desenha o tabuleiro, as células marcadas e a malha de grade na `surface`.

    - O contorno do tabuleiro é desenhado com `BORDER_COLOR`.
    - Células marcadas (bloqueadas) são preenchidas com `CELL_COLOR`.
    - Linhas da grade são traçadas para orientar a edição com o mouse.
    """
    # Fundo do tabuleiro
    pygame.draw.rect(surface, BORDER_COLOR, board_rect, width=2)

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Preenche células marcadas
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]:
                x = board_rect.left + c * cell_size
                y = board_rect.top + r * cell_size
                rect = pygame.Rect(x + 1, y + 1, cell_size - 2, cell_size - 2)
                pygame.draw.rect(surface, CELL_COLOR, rect)

    # Desenha linhas da grade
    # Linhas verticais
    for c in range(cols + 1):
        x = board_rect.left + c * cell_size
        pygame.draw.line(surface, GRID_COLOR, (x, board_rect.top), (x, board_rect.bottom), 1)
    # Linhas horizontais
    for r in range(rows + 1):
        y = board_rect.top + r * cell_size
        pygame.draw.line(surface, GRID_COLOR, (board_rect.left, y), (board_rect.right, y), 1)


# ---------- Utilidades de Grid/Coordenadas ----------
def cell_center_px(board_rect: pygame.Rect, cell_size: int, rc: tuple[int, int]) -> tuple[int, int]:
    """Retorna a posição (x, y) em pixels do centro da célula `rc` dentro do tabuleiro."""
    r, c = rc
    x = board_rect.left + c * cell_size + cell_size // 2
    y = board_rect.top + r * cell_size + cell_size // 2
    return x, y


def valid_cell(grid, r: int, c: int) -> bool:
    """Verifica se a célula (r, c) está dentro dos limites e é livre (não bloqueada)."""
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and not grid[r][c]


# ---------- A* com heap binário ----------
def a_star_grid(grid, start: tuple[int, int], goal: tuple[int, int]):
    """Executa o algoritmo A* em um grid ortogonal (4 vizinhos) com `heapq`.

    Este A* usa a distância Manhattan como heurística e custo uniforme (1 por passo).
    A fila de prioridade é implementada com `heapq` (heap binário) e utiliza a
    técnica de lazy deletion: quando um nó recebe um custo melhor, empilhamos uma
    nova entrada com f menor e não removemos a antiga; ao desempilhar, ignoramos
    entradas obsoletas comparando `f_curr` com `best_f[curr]`.

    Parâmetros:
    - grid: matriz booleana com obstáculos.
    - start: célula de partida (row, col), deve ser válida/livre.
    - goal: célula objetivo (row, col), deve ser válida/livre.

    Retorna:
    - Uma lista de células do caminho de `start` até `goal` (inclusive), ou None se
      não houver caminho.
    """
    if start is None or goal is None:
        return None

    if not valid_cell(grid, start[0], start[1]) or not valid_cell(grid, goal[0], goal[1]):
        return None

    def neighbors(rc):
        r, c = rc
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if valid_cell(grid, nr, nc):
                yield (nr, nc)

    def h(rc):
        # Manhattan
        return abs(rc[0] - goal[0]) + abs(rc[1] - goal[1])

    open_heap = []
    g = {start: 0}
    came = {}
    f0 = h(start)
    heapq.heappush(open_heap, (f0, 0, start))
    best_f = {start: f0}
    counter = 1

    while open_heap:
        f_curr, _, curr = heapq.heappop(open_heap)
        if best_f.get(curr, float('inf')) < f_curr:
            continue
        if curr == goal:
            # reconstrói caminho
            path = [curr]
            while curr in came:
                curr = came[curr]
                path.append(curr)
            path.reverse()
            return path
        for nb in neighbors(curr):
            tg = g[curr] + 1
            if tg < g.get(nb, float('inf')):
                g[nb] = tg
                came[nb] = curr
                fn = tg + h(nb)
                best_f[nb] = fn
                heapq.heappush(open_heap, (fn, counter, nb))
                counter += 1
    return None


def main():
    """Aplicativo Pygame: edição de grid e perseguição do cursor com A*.

    O programa abre uma janela onde o tabuleiro ocupa ~80% do espaço. O usuário
    pode marcar/desmarcar células clicando e arrastando com o botão esquerdo do
    mouse. Um agente (círculo) tenta perseguir a célula sob o cursor, planejando
    um caminho A* até a célula livre mais próxima ao cursor (e também lidando
    com o caso do agente iniciar dentro de um bloco, via `nearest_free_cell`).

    O movimento do agente até o próximo waypoint é suave e limitado por
    `AGENT_SPEED_PX_S`. Sempre que o objetivo muda (ou a grade muda), o caminho
    é replanejado.
    """
    pygame.init()
    try:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    except pygame.error as e:
        print(f"Erro ao inicializar a janela: {e}")
        pygame.quit()
        sys.exit(1)

    pygame.display.set_caption("Tabuleiro 80% - Desenho com Mouse (16x16)")
    clock = pygame.time.Clock()

    board_rect = compute_board_rect(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, BOARD_SCALE)
    grid = create_grid(board_rect, CELL_SIZE)

    drawing = False  # estado do botão esquerdo
    last_cell = None  # evita toggles repetidos dentro da mesma célula durante o arrasto
    grid_dirty = False

    # Agente (circunferência) inicia no centro do tabuleiro
    start_rc = ( (board_rect.height // CELL_SIZE) // 2, (board_rect.width // CELL_SIZE) // 2 )
    agent_x, agent_y = cell_center_px(board_rect, CELL_SIZE, start_rc)
    agent_path = None  # lista de células
    agent_path_index = 0
    last_goal = None

    running = True
    prev_ticks = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # esquerdo
                    drawing = True
                    cell = pos_to_cell(board_rect, CELL_SIZE, event.pos)
                    if cell is not None:
                        toggle_cell(grid, cell)
                        last_cell = cell
                        grid_dirty = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    last_cell = None

            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    cell = pos_to_cell(board_rect, CELL_SIZE, event.pos)
                    if cell is not None and cell != last_cell:
                        toggle_cell(grid, cell)
                        last_cell = cell
                        grid_dirty = True

        # Renderização
        screen.fill(BACKGROUND_COLOR)
        draw_board(screen, board_rect, grid, CELL_SIZE)

        # Atualiza alvo (quadrado do mouse) com base na posição atual do mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_cell = pos_to_cell(board_rect, CELL_SIZE, mouse_pos)
        if mouse_cell is not None:
            # desenha quadrado alinhado à célula do mouse
            mcx = board_rect.left + mouse_cell[1] * CELL_SIZE
            mcy = board_rect.top + mouse_cell[0] * CELL_SIZE
            pygame.draw.rect(screen, MOUSE_SQUARE_COLOR, pygame.Rect(mcx + 2, mcy + 2, CELL_SIZE - 4, CELL_SIZE - 4), width=2)

        # A* planejamento de caminho do agente até a célula do mouse (ou célula livre mais próxima)
        if mouse_cell is not None:
            # célula atual do agente (se bloqueada, substitui por célula livre mais próxima)
            agent_cell_raw = pos_to_cell(board_rect, CELL_SIZE, (agent_x, agent_y))
            agent_cell = agent_cell_raw
            if agent_cell is not None and not valid_cell(grid, agent_cell[0], agent_cell[1]):
                agent_cell = nearest_free_cell(grid, agent_cell)

            # alvo planejado: célula livre mais próxima do mouse
            plan_goal = nearest_free_cell(grid, mouse_cell)

            # se alvo mudou (em termos de plan_goal) ou grid mudou ou não há caminho, replana
            if (last_goal != plan_goal) or grid_dirty or (agent_path is None):
                if agent_cell is not None and plan_goal is not None:
                    agent_path = a_star_grid(grid, agent_cell, plan_goal)
                else:
                    agent_path = None
                agent_path_index = 0
                last_goal = plan_goal
                grid_dirty = False

        # Movimento suave do agente ao longo do caminho
        now_ticks = pygame.time.get_ticks()
        dt = max(0.0, (now_ticks - prev_ticks) / 1000.0)
        prev_ticks = now_ticks

        if agent_path and len(agent_path) > 1 and mouse_cell is not None:
            # proximo waypoint (pule a primeira célula que é a atual)
            if agent_path_index < len(agent_path) - 1:
                next_rc = agent_path[agent_path_index + 1]
                target_px = cell_center_px(board_rect, CELL_SIZE, next_rc)
                vx = target_px[0] - agent_x
                vy = target_px[1] - agent_y
                dist = math.hypot(vx, vy)
                if dist > 1e-6:
                    step = AGENT_SPEED_PX_S * dt
                    if step >= dist:
                        # alcançou o waypoint
                        agent_x, agent_y = target_px
                        agent_path_index += 1
                    else:
                        agent_x += vx / dist * step
                        agent_y += vy / dist * step
                else:
                    agent_path_index += 1

        # Desenha agente (circunferência) e linha até o quadrado do mouse
        agent_pos_int = (int(agent_x), int(agent_y))
        pygame.draw.circle(screen, AGENT_COLOR, agent_pos_int, max(4, CELL_SIZE // 2), width=2)

        if mouse_cell is not None:
            mouse_center = cell_center_px(board_rect, CELL_SIZE, mouse_cell)
            pygame.draw.line(screen, PATH_COLOR, agent_pos_int, mouse_center, 1)

        # Opcional: desenhe o caminho planejado
        if agent_path and len(agent_path) > 1:
            points = [cell_center_px(board_rect, CELL_SIZE, rc) for rc in agent_path]
            if len(points) >= 2:
                pygame.draw.lines(screen, PATH_COLOR, False, points, 1)

        pygame.display.flip()
        clock.tick(120)  # limita FPS

    pygame.quit()


if __name__ == "__main__":
    main()
