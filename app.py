import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# ====== GENERADOR PROPIO DE SUDOKUS ======
def is_valid(board, row, col, num):
    # Verifica si num puede ir en (row, col)
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve(board):
    # Backtracking para resolver sudoku
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku(empty_cells=40):
    # Crea un sudoku válido y borra celdas
    board = np.zeros((9,9), dtype=int)
    solve(board)  # llena un sudoku completo
    # borrar celdas aleatoriamente
    cells = list(range(81))
    random.shuffle(cells)
    for i in range(empty_cells):
        row, col = divmod(cells[i], 9)
        board[row][col] = 0
    return board

# ====== INTERFAZ STREAMLIT ======
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_sudoku()
    st.session_state.solution = None

col1, col2 = st.columns([3,1])

with col1:
    st.subheader("Sudoku actual")
    user_input = np.zeros((9,9), dtype=int)
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            if st.session_state.puzzle[i][j] != 0:
                cols[j].write(f"**{st.session_state.puzzle[i][j]}**")
                user_input[i][j] = st.session_state.puzzle[i][j]
            else:
                val = cols[j].number_input("", min_value=0, max_value=9, step=1, key=f"cell_{i}_{j}")
                user_input[i][j] = val

with col2:
    if st.button("🔄 Nuevo Sudoku"):
        st.session_state.puzzle = generate_sudoku()
        st.rerun()

    if st.button("✅ Verificar solución"):
        puzzle_copy = st.session_state.puzzle.copy()
        solve(puzzle_copy)
        if np.array_equal(user_input, puzzle_copy):
            st.success("🎉 ¡Correcto! Sudoku resuelto")
        else:
            st.error("❌ Aún no está correcto")

