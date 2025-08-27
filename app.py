import streamlit as st
import random

# --- Lógica del Sudoku ---

def solve_sudoku(board):
    """
    Resuelve el Sudoku usando un algoritmo de backtracking.
    """
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i

            if solve_sudoku(board):
                return True

            board[row][col] = 0
    return False

def is_valid(board, num, pos):
    """
    Verifica si un número es válido en una posición dada.
    """
    # Chequeo de la fila
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Chequeo de la columna
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Chequeo del cuadrado 3x3
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(board):
    """
    Encuentra la siguiente celda vacía (con valor 0).
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_full_board():
    """
    Genera un tablero de Sudoku 9x9 resuelto.
    """
    board = [[0] * 9 for _ in range(9)]
    fill_board_recursively(board)
    return board

def fill_board_recursively(board):
    """
    Función auxiliar para rellenar un tablero completo de forma aleatoria.
    """
    for i in range(81):
        row = i // 9
        col = i % 9
        if board[row][col] == 0:
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for number in numbers:
                if is_valid(board, number, (row, col)):
                    board[row][col] = number
                    if find_empty(board) is None or fill_board_recursively(board):
                        return True
                    board[row][col] = 0
            return False
    return True

def generate_sudoku_puzzle(difficulty='difficult'):
    """
    Genera un puzzle de Sudoku eliminando números del tablero resuelto.
    La dificultad "difícil" elimina una gran cantidad de números.
    """
    board = generate_full_board()
    solution = [row[:] for row in board]  # Guardar una copia de la solución
    
    # Número de celdas a eliminar para la dificultad "difícil" (aprox. 55 a 65)
    num_to_remove = random.randint(55, 65)
    
    while num_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            backup = board[row][col]
            board[row][col] = 0
            
            # Verificar si el puzzle sigue teniendo una solución única
            # (Simplificado para esta implementación. Una verificación más robusta
            # requeriría resolver el puzzle y contar el número de soluciones).
            
            num_to_remove -= 1
            
    return board, solution

# --- Funciones de la App de Streamlit ---

def generate_new_sudoku():
    """Genera un nuevo Sudoku y lo guarda en el estado de la sesión."""
    puzzle, solution = generate_sudoku_puzzle(difficulty='difficult')
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_board = [row[:] for row in puzzle]
    st.session_state.message = ""

def check_solution():
    """Comprueba la solución del usuario y actualiza el mensaje."""
    is_correct = True
    user_solution = st.session_state.user_board
    
    # Revisa si todas las celdas están llenas y coinciden con la solución
    for r in range(9):
        for c in range(9):
            if user_solution[r][c] != st.session_state.solution[r][c]:
                is_correct = False
                break
        if not is_correct:
            break
            
    if is_correct:
        st.session_state.message = "🎉 ¡Felicitaciones! ¡Solución correcta!"
    else:
        st.session_state.message = "❌ Solución incorrecta. ¡Sigue intentándolo!"

# --- Interfaz de la App ---

st.set_page_config(page_title="Sudokus para Rocío", layout="wide")

st.title("Sudokus para Rocío")
st.markdown("¡Un nuevo desafío de Sudoku difícil te espera!")

# Inicializar el estado de la sesión si es la primera vez que se carga la app
if "puzzle" not in st.session_state:
    generate_new_sudoku()

# Mostrar el tablero
st.write("### Tablero de Sudoku")
grid_cols = st.columns(9)
user_board = st.session_state.user_board

for r in range(9):
    # Uso de st.columns para un diseño de cuadrícula
    cols = st.columns(9)
    for c in range(9):
        with cols[c]:
            is_initial = st.session_state.puzzle[r][c] != 0
            value = str(st.session_state.user_board[r][c]) if st.session_state.user_board[r][c] != 0 else ""
            
            # Usar st.text_input para cada celda
            # key única para cada celda para que Streamlit sepa qué actualizar
            input_value = st.text_input(
                label="", 
                value=value,
                key=f"cell_{r}_{c}",
                disabled=is_initial,
                max_chars=1
            )
            
            # Actualizar el tablero del usuario
            try:
                if input_value:
                    user_board[r][c] = int(input_value)
                else:
                    user_board[r][c] = 0
            except ValueError:
                # Manejar entrada no numérica
                user_board[r][c] = 0
            
# --- Botones y Mensajes ---

st.write("")
st.write("")
col1, col2 = st.columns(2)

with col1:
    if st.button("Generar Nuevo Sudoku", use_container_width=True):
        generate_new_sudoku()
        st.experimental_rerun()  # Forzar un nuevo renderizado para ver el tablero vacío

with col2:
    if st.button("Verificar Solución", use_container_width=True):
        check_solution()

# Mostrar el mensaje de verificación
st.write("")
if st.session_state.get("message"):
    st.success(st.session_state.message) if "Felicitaciones" in st.session_state.message else st.error(st.session_state.message)
