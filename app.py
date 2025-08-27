import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# ========================
# Generador Sudoku 9x9
# ========================
def pattern(r, c): return (3*(r % 3) + r//3 + c) % 9
def shuffled(s): return random.sample(s, len(s))

def generate_sudoku():
    rBase = range(3)
    rows = [g*3 + r for g in shuffled(rBase) for r in shuffled(rBase)]
    cols = [g*3 + c for g in shuffled(rBase) for c in shuffled(rBase)]
    nums = shuffled(list(range(1,10)))
    board = [[nums[pattern(r,c)] for c in cols] for r in rows]
    empties = random.randint(40,55)
    for p in random.sample(range(81), empties):
        board[p//9][p%9] = 0
    return np.array(board)

if "board" not in st.session_state:
    st.session_state.board = generate_sudoku()

if st.button("🎲 Generar uno nuevo"):
    st.session_state.board = generate_sudoku()

board = st.session_state.board

# ========================
# Mostrar tablero con st.columns
# ========================
st.write("Completa el Sudoku 👇")

user_solution = []
for i in range(9):
    cols = st.columns(9)
    row = []
    for j in range(9):
        val = board[i,j]
        style = {"background-color": "#ddd"} if val != 0 else {"background-color": "#fff"}
        if val != 0:
            cols[j].text_input("", value=str(val), disabled=True, key=f"fixed-{i}-{j}")
            row.append(val)
        else:
            num = cols[j].text_input("", value="", max_chars=1, key=f"user-{i}-{j}")
            row.append(int(num) if num.isdigit() else 0)
    user_solution.append(row)

user_solution = np.array(user_solution)

# ========================
# Verificar solución
# ========================
def check_solution(board, solution):
    # fila
    for r in range(9):
        if len(set(solution[r,:])) != 9 or not all(1 <= n <= 9 for n in solution[r,:]):
            return False
    # columna
    for c in range(9):
        if len(set(solution[:,c])) != 9:
            return False
    # subcuadrícula 3x3
    for r in range(0,9,3):
        for c in range(0,9,3):
            block = solution[r:r+3, c:c+3].flatten()
            if len(set(block)) != 9:
                return False
    return True

if st.button("✅ Verificar solución"):
    if check_solution(board, user_solution):
        st.success("🎉 ¡Correcto! Sudoku resuelto")
    else:
        st.error("❌ Todavía hay errores o casillas incompletas")
