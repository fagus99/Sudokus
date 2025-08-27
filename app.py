import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# ========================
# Generador de Sudoku 9x9
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

# ========================
# Estado del Sudoku
# ========================
if "board" not in st.session_state:
    st.session_state.board = generate_sudoku()

if st.button("🎲 Generar uno nuevo"):
    st.session_state.board = generate_sudoku()

board = st.session_state.board

# ========================
# Crear inputs del usuario
# ========================
st.write("Completa el Sudoku 👇")
user_board = np.zeros((9,9), dtype=int)

for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        val = board[i,j]
        # Definir estilo de bordes
        top = 3 if i%3==0 else 1
        bottom = 3 if i==8 else 0
        left = 3 if j%3==0 else 1
        right = 3 if j==8 else 0
        style = f"border-top:{top}px solid black; border-bottom:{bottom}px solid black; border-left:{left}px solid black; border-right:{right}px solid black; width:50px; height:50px; text-align:center; font-size:20px;"

        if val != 0:
            cols[j].markdown(f"<div style='background-color:#ddd; {style}'>{val}</div>", unsafe_allow_html=True)
            user_board[i,j] = val
        else:
            num = cols[j].text_input("", value="", max_chars=1, key=f"user-{i}-{j}", help="Ingresa un número del 1 al 9")
            user_board[i,j] = int(num) if num.isdigit() else 0

# ========================
# Función para verificar solución
# ========================
def check_solution(board):
    # Filas
    for r in range(9):
        if set(board[r,:]) != set(range(1,10)):
            return False
    # Columnas
    for c in range(9):
        if set(board[:,c]) != set(range(1,10)):
            return False
    # Bloques 3x3
    for r in range(0,9,3):
        for c in range(0,9,3):
            block = board[r:r+3, c:c+3].flatten()
            if set(block) != set(range(1,10)):
                return False
    return True

if st.button("✅ Verificar solución"):
    if check_solution(user_board):
        st.success("🎉 ¡Correcto! Sudoku resuelto")
    else:
        st.error("❌ Todavía hay errores o casillas incompletas")
