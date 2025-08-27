import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# ========================
# Generador de Sudoku 9x9
# ========================
def pattern(r, c): return (3*(r % 3) + r//3 + c) % 9
def shuffled(s): return random.sample(s, len(s))

def generate_sudoku(empty_min=40, empty_max=55):
    rBase = range(3)
    rows = [g*3 + r for g in shuffled(rBase) for r in shuffled(rBase)]
    cols = [g*3 + c for g in shuffled(rBase) for c in shuffled(rBase)]
    nums = shuffled(list(range(1,10)))
    board = [[nums[pattern(r,c)] for c in cols] for r in rows]

    # Borrar algunas celdas
    empties = random.randint(empty_min, empty_max)
    for p in random.sample(range(81), empties):
        board[p//9][p%9] = 0
    return np.array(board)

# ========================
# Estado del Sudoku
# ========================
if "board" not in st.session_state:
    st.session_state.board = generate_sudoku()
    st.session_state.solution = None

# ========================
# Botón para generar nuevo
# ========================
if st.button("🎲 Generar uno nuevo"):
    st.session_state.board = generate_sudoku()

# ========================
# Preparar DataFrame para mostrar
# ========================
board = st.session_state.board
df = pd.DataFrame(board, columns=[f"{i+1}" for i in range(9)])

# Mostrar celdas fijas como no editables, vacías como editables
editable_mask = (board == 0)

# ========================
# Data Editor de Streamlit
# ========================
edited_df = st.experimental_data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    disabled=~editable_mask,  # solo editable donde sea 0
)

# ========================
# Verificar solución
# ========================
def check_solution(user_board, solution_board):
    return np.array_equal(user_board, solution_board)

if st.button("✅ Verificar solución"):
    # Solución completa
    # Usamos backtracking simple para rellenar board
    def is_valid(b, r, c, n):
        if n in b[r,:]: return False
        if n in b[:,c]: return False
        r0, c0 = 3*(r//3), 3*(c//3)
        if n in b[r0:r0+3, c0:c0+3]: return False
        return True

    def solve(b):
        for r in range(9):
            for c in range(9):
                if b[r,c] == 0:
                    for n in range(1,10):
                        if is_valid(b,r,c,n):
                            b[r,c] = n
                            if solve(b):
                                return True
                            b[r,c] = 0
                    return False
        return True

    solution = board.copy()
    solve(solution)

    user_board = edited_df.to_numpy()
    if check_solution(user_board, solution):
        st.success("🎉 ¡Correcto! Sudoku resuelto")
    else:
        st.error("❌ Todavía hay errores o casillas incompletas")
