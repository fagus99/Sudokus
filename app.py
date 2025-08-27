import streamlit as st
import random

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# === FUNCIONES ===
def generate_sudoku():
    """Genera un sudoku válido y quita algunos números para dejar casillas vacías."""
    base  = 3
    side  = base * base

    # patron para un sudoku válido
    def pattern(r, c): return (base*(r % base)+r//base+c) % side
    # mezclar filas, columnas y números
    def shuffle(s): return random.sample(s, len(s)) 
    rBase = range(base) 
    rows  = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)] 
    cols  = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums  = shuffle(range(1, side+1))

    # generar el tablero completo
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # quitar casillas
    squares = side*side
    empties = random.randint(40, 55)  # dificultad (más alto = más difícil)
    for p in random.sample(range(squares), empties):
        board[p//side][p % side] = 0
    return board

def check_solution(board, solution):
    """Verifica si la solución del usuario es válida."""
    size = 9
    for r in range(size):
        row_nums = set()
        col_nums = set()
        for c in range(size):
            val_row = solution[r][c]
            val_col = solution[c][r]
            if val_row < 1 or val_row > 9 or val_col < 1 or val_col > 9:
                return False
            if val_row in row_nums or val_col in col_nums:
                return False
            row_nums.add(val_row)
            col_nums.add(val_col)
    # verificar subcuadrículas
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for r in range(3):
                for c in range(3):
                    val = solution[br+r][bc+c]
                    if val in seen:
                        return False
                    seen.add(val)
    return True

# === ESTADO ===
if "board" not in st.session_state:
    st.session_state.board = generate_sudoku()

# === BOTONES ===
col1, col2 = st.columns(2)
if col1.button("🎲 Generar uno nuevo"):
    st.session_state.board = generate_sudoku()

# === TABLERO ===
st.write("Completa el Sudoku 👇")

user_solution = []
for i in range(9):
    cols = st.columns(9)
    row = []
    for j in range(9):
        val = st.session_state.board[i][j]
        if val != 0:
            cols[j].text_input("", value=str(val), disabled=True, key=f"fixed-{i}-{j}")
            row.append(val)
        else:
            num = cols[j].text_input("", value="", max_chars=1, key=f"user-{i}-{j}")
            try:
                row.append(int(num)) if num.isdigit() else row.append(0)
            except:
                row.append(0)
    user_solution.append(row)

if col2.button("✅ Verificar solución"):
    if check_solution(st.session_state.board, user_solution):
        st.success("🎉 ¡Correcto! Sudoku resuelto.")
    else:
        st.error("❌ La solución no es válida todavía.")
