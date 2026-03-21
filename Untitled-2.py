import pandas as pd
import streamlit as st
import plotly
alunos = pd.read_excel(r"C:\Users\Aluno\Pictures\__pycache__\Vendas.xlsx")
st.set_page_config("dashboards","💎",layout=("wide"))
st.title("ola bem vindos a pagina de relatorios")
alunos = pd.DataFrame(alunos)
print(alunos)
st.title('DASHBOARDS DE VENDAS ')
st.dataframe(alunos, use_container_width=True)
