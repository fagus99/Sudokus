import streamlit as st
import pandas as pd
import random
from sudoku import Sudoku

# ==============================
# Configuración inicial
# ==============================
st.set_page_config(page_title="Sudokus para Rocio", layout="wide")
st.title("🎲 Sudokus para Rocio")

st.markdown("Elige la **dificultad** y el **tipo de Sudoku** para jugar. Cada vez que entres, se generará uno nuevo 🎉")

# ==============================
# Base de sudokus precargados
# ==============================
# Representamos los tableros como strings (0 = celda vacía)
precargados = {
    "X": [
        {
            "puzzle": "400000805030000000000700000020000060000080400000010000000603070500200000104000000",
            "solution": "419652837837149652265738941521974368673581429948213765192865374586327194374496218"
        }
    ],
    "Irregular": [
        {
            "puzzle": "009000000080605020501078000000040706000000000104060000000720805090501030000000600",
            "solution": "349152687287645139561978342635894726972316458814263975126739854498521763753486291"
        }
    ],
    "Killer": [
        {
            "puzzle": "300200000000107000706030500070009080900020004010800050009040301000702000000008006",
            "solution": "345286179892157463716934528574369182968521734123874659659418327481762395237695841"
        }
    ]
}
# Aquí podrías cargar más (hasta 50 por tipo) desde un JSON o CSV

# ==============================
# Selección de dificultad y tipo
# ==============================
dificultad = st.selectbox("Elige dificultad", ["medio/alto", "alto"])
tipo = st.selectbox("Elige tipo de Sudoku", ["clásico", "X", "Irregular", "Killer"])

# ==============================
# Obtener tablero según tipo
# ==============================
if tipo == "clásico":
    if dificultad == "medio/alto":
        puzzle = Sudoku(3).difficulty(0.5)   # nivel medio-alto
    else:
        puzzle = Sudoku(3).difficulty(0.7)   # nivel alto
    board = puzzle.board
    solution = puzzle.solve().board
else:
    elegido = random.choice(precargados[tipo])
    puzzle_str = elegido["puzzle"]
    sol_str = elegido["solution"]

    # convertir a listas 9x9
    board = [
        [int(puzzle_str[r*9 + c]) if puzzle_str[r*9 + c] != "0" else None for c in range(9)]
        for r in range(9)
    ]
    solution = [
        [int(sol_str[r*9 + c]) for c in range(9)]
        for r in range(9)
    ]

# ==============================
# Mostrar grilla interactiva
# ==============================
st.write(f"### Sudoku {tipo} - dificultad {dificultad}")

with st.form("sudoku_form"):
    user_grid = []
    for r in range(9):
        cols = st.columns(9)
        row = []
        for c in range(9):
            val = board[r][c]
            if val is None:  # celda vacía → input
                cell_value = cols[c].text_input(
                    "",
                    key=f"cell_{r}_{c}",
                    max_chars=1,
                    value=""
                )
                row.append(int(cell_value) if cell_value.isdigit() else None)
            else:  # celda fija
                cols[c].markdown(f"**{val}**")
                row.append(val)
        user_grid.append(row)

    submitted = st.form_submit_button("✅ Verificar Sudoku")

# ==============================
# Verificación
# ==============================
if submitted:
    if user_grid == solution:
        st.success("🎉 ¡Felicitaciones Rocio! Sudoku resuelto correctamente ✅")
    else:
        st.error("❌ Aún hay errores o celdas incompletas. Seguí intentando 😉")

if st.button("📌 Mostrar solución"):
    sol_df = pd.DataFrame(solution)
    st.write("✅ Aquí está la solución completa:")
    st.dataframe(sol_df, height=400)
