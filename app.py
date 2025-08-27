import streamlit as st
import numpy as np
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="Sudokus para Rocio", layout="centered")
st.title("🧩 Sudokus para Rocio")

# === Generador simple de Sudoku completo y tablero con celdas vacías ===
def pattern(r, c): return (3*(r % 3) + r//3 + c) % 9
def shuffled(s): return random.sample(s, len(s))

def generate_board():
    rBase = range(3)
    rows = [g*3 + r for g in shuffled(rBase) for r in shuffled(rBase)]
    cols = [g*3 + c for g in shuffled(rBase) for c in shuffled(rBase)]
    nums = shuffled(list(range(1,10)))
    board = [[nums[pattern(r,c)] for c in cols] for r in rows]
    empties = random.randint(40,55)
    for p in random.sample(range(81), empties):
        board[p//9][p % 9] = 0
    return np.array(board)

# Generar el sudoku si no existe en estado
if "board" not in st.session_state:
    st.session_state.board = generate_board()
    st.session_state.solution = None

# Botón para reiniciar
if st.button("🎲 Generar uno nuevo"):
    st.session_state.board = generate_board()

# Estilo y HTML del tablero editable
def render_sudoku_html(board):
    style = """
    <style>
        .sudoku { border-collapse: collapse; margin: auto; }
        .sudoku td { border: 1px solid black; width: 2em; height: 2em; padding: 0; }
        .sudoku td:nth-child(3n) { border-right: 3px solid black; }
        .sudoku tr:nth-child(3n) td { border-bottom: 3px solid black; }
        .sudoku-input { width: 100%; height: 100%; text-align: center; font-size: 1.2em; border: none; }
        .sudoku-input:focus { outline: none; background-color: #e8f0fe; }
    </style>
    """
    table = "<table class='sudoku'>"
    for i in range(9):
        table += "<tr>"
        for j in range(9):
            val = board[i, j]
            cell = f"<input class='sudoku-input' maxlength='1' value='{val if val != 0 else ''}'>"
            if val != 0:
                table += f"<td style='background-color:#ddd'>{val}</td>"
            else:
                table += f"<td>{cell}</td>"
        table += "</tr>"
    table += "</table>"
    return style + table

# Mostrar el tablero
board = st.session_state.board
components.html(render_sudoku_html(board), height=390)

# Aquí podríamos desarrollar lógica extra con JavaScript para recoger inputs,
# pero por simplicidad dejaremos sólo visualización y generación nueva.
st.write("Tablero generado. Para verificar, vamos a agregar lógica manualmente si querés.")

