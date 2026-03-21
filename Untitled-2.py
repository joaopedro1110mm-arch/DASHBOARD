import pandas as pd
import plotly.graph_objects as go
import streamlit as st
alunos = pd.read_excel("Vendas.xlsx")
st.set_page_config("dashboards","💎",layout=("wide"))
st.title("ola bem vindos a pagina de relatorios")
alunos = pd.DataFrame(alunos)
st.dataframe(alunos, use_container_width=True)
