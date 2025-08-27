import streamlit as st
import numpy as np
import random
import streamlit.components.v1 as components

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
# Render HTML tablero 9x9 con cuadrantes
# ========================
def render_sudoku_html(board):
    style = """
    <style>
    table.sudoku {border-collapse: collapse; margin: auto;}
    table.sudoku td {
        width: 50px; height: 50px; text-align:center; font-size:20px; padding:0;
        border:1px solid #999;
    }
    /* Bordes gruesos para cuadrantes 3x3 */
    table.sudoku tr:nth-child(3n) td {border-bottom:3px solid black;}
    table.sudoku td:nth-child(3n) {border-right:3px solid black;}
    table.sudoku tr:first-child td {border-top:3px solid black;}
    table.sudoku td:first-child {border-left:3px solid black;}
    .fixed {background-color:#ddd; font-weight:bold;}
    input.sudoku-cell {width:100%; height:100%; text-align:center; border:none; font-size:20px;}
    input.sudoku-cell:focus {outline:2px solid #4a90e2; background-color:#e8f0fe;}
    </style>
    """

    table = "<table class='sudoku'>"
    for i in range(9):
        table += "<tr>"
        for j in range(9):
            val = board[i,j]
            if val != 0:
                table += f"<td class='fixed'>{val}</td>"
            else:
                table += f"<td><input class='sudoku-cell' maxlength='1' id='cell-{i}-{j}'></td>"
        table += "</tr>"
    table += "</table>"
    return style + table

components.html(render_sudoku_html(board), height=480)

# ========================
# Captura los inputs con st.session_state
# ========================
st.write("💡 Las casillas grises son fijas, blancas son para completar.")

# Lógica para capturar y validar inputs:
# Cada input tiene key='cell-i-j', podemos usar st.session_state si usamos st.text_input en lugar de html,
# pero por visual se mantiene el tablero clásico. La validación se hace con un formulario opcional.
