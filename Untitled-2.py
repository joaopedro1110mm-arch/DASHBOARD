import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import base64

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="StreamFlix - Sua Plataforma de Streaming",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    /* Tema escuro */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Header */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    
    .logo {
        font-size: 2rem;
        font-weight: 800;
        color: white;
    }
    
    .logo-highlight {
        color: #E50914;
    }
    
    /* Cards dos filmes */
    .movie-card {
        background: #1a1a1a;
        border-radius: 15px;
        padding: 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.3);
        border-color: #E50914;
    }
    
    .movie-poster {
        width: 100%;
        border-radius: 15px 15px 0 0;
    }
    
    .movie-info {
        padding: 1rem;
    }
    
    .movie-title {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    
    .movie-year {
        color: #b3b3b3;
        font-size: 0.9rem;
    }
    
    .movie-rating {
        color: #ffd700;
        font-weight: bold;
    }
    
    /* Botões */
    .btn-assistir {
        background: #E50914;
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.1rem;
        width: 100%;
    }
    
    .btn-assistir:hover {
        background: #b20710;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(229, 9, 20, 0.4);
    }
    
    /* Player de vídeo */
    .video-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        margin: 1rem 0;
    }
    
    /* Seções */
    .section-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E50914;
        display: inline-block;
    }
    
    /* Informações */
    .info-box {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
    }
    
    /* Tags */
    .cast-tag {
        display: inline-block;
        background: rgba(229, 9, 20, 0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        color: white;
        font-size: 0.9rem;
    }
    
    /* Player modal */
    .player-overlay {
        background: rgba(0,0,0,0.95);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #0a0a0a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BANCO DE DADOS DOS FILMES
# ============================================
movies_database = [
    {
        "id": "capitao_america",
        "titulo": "Capitão América: Guerra Civil",
        "ano": "2016",
        "avaliacao": 8.5,
        "duracao": "2h 27min",
        "categoria": "Heróis",
        "genero": ["Ação", "Aventura", "Heróis"],
        # ⚠️ COLOQUE AQUI O LINK DO SEU VÍDEO
        "video_url": "https://drive.google.com/uc?export=download&id=SEU_ID_DO_ARQUIVO",
        # Ou link direto:
        # "video_url": "https://seusite.com/videos/capitao-america.mp4",
        "poster": "https://image.tmdb.org/t/p/w500/rAGiXaUfPzY7CDEyNKUofk3Kw2e.jpg",
        "descricao": "Steve Rogers e Tony Stark lideram times opostos de Vingadores em uma batalha épica que vai dividir o universo Marvel.",
        "elenco": ["Chris Evans", "Robert Downey Jr.", "Scarlett Johansson", "Sebastian Stan", "Anthony Mackie"],
        "diretor": "Anthony Russo, Joe Russo"
    },
    
    # EXEMPLO DE NOVOS FILMES (descomente e adicione seus links):
    # {
    #     "id": "vingadores_ultimato",
    #     "titulo": "Vingadores: Ultimato",
    #     "ano": "2019",
    #     "avaliacao": 9.2,
    #     "duracao": "3h 01min",
    #     "categoria": "Heróis",
    #     "genero": ["Ação", "Aventura", "Heróis"],
    #     "video_url": "https://drive.google.com/uc?export=download&id=SEU_ID_AQUI",
    #     "poster": "https://image.tmdb.org/t/p/w500/q6725aR8Zs4IwGMXzZT8aC8lh41.jpg",
    #     "descricao": "Os Vingadores se unem para reverter as ações de Thanos e salvar o universo.",
    #     "elenco": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo", "Chris Hemsworth"],
    #     "diretor": "Anthony Russo, Joe Russo"
    # },
    # {
    #     "id": "missao_impossivel",
    #     "titulo": "Missão Impossível: Acerto de Contas",
    #     "ano": "2023",
    #     "avaliacao": 8.0,
    #     "duracao": "2h 43min",
    #     "categoria": "Ação",
    #     "genero": ["Ação", "Espionagem"],
    #     "video_url": "https://drive.google.com/uc?export=download&id=SEU_ID_AQUI",
    #     "poster": "https://image.tmdb.org/t/p/w500/nnqj8h9qWvZ0Jq0qWvZ0Jq0qWvZ0.jpg",
    #     "descricao": "Ethan Hunt enfrenta sua missão mais perigosa até agora.",
    #     "elenco": ["Tom Cruise", "Hayley Atwell", "Ving Rhames", "Simon Pegg"],
    #     "diretor": "Christopher McQuarrie"
    # },
]

# ============================================
# INICIALIZAR SESSÃO
# ============================================
if 'filme_selecionado' not in st.session_state:
    st.session_state.filme_selecionado = None
if 'mostrar_player' not in st.session_state:
    st.session_state.mostrar_player = False
if 'filtro_categoria' not in st.session_state:
    st.session_state.filtro_categoria = "Todos"

# ============================================
# FUNÇÕES
# ============================================

def selecionar_filme(filme_id):
    """Seleciona um filme para assistir"""
    st.session_state.filme_selecionado = filme_id
    st.session_state.mostrar_player = True

def fechar_player():
    """Fecha o player de vídeo"""
    st.session_state.mostrar_player = False
    st.session_state.filme_selecionado = None

def filtrar_filmes(categoria):
    """Filtra filmes por categoria"""
    st.session_state.filtro_categoria = categoria

def get_filme_por_id(filme_id):
    """Retorna o filme pelo ID"""
    for filme in movies_database:
        if filme["id"] == filme_id:
            return filme
    return None

# ============================================
# HEADER
# ============================================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
        <div class="header">
            <div class="logo">
                🎬 Stream<span class="logo-highlight">Flix</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR - MENU DE NAVEGAÇÃO
# ============================================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    st.markdown("---")
    
    # Busca
    busca = st.text_input("🔍 Buscar filmes...", placeholder="Digite o nome do filme...")
    
    st.markdown("---")
    
    # Categorias
    st.markdown("### 📂 Categorias")
    
    categorias = ["Todos"] + list(set([f["categoria"] for f in movies_database]))
    
    for categoria in categorias:
        if st.button(
            categoria, 
            key=f"cat_{categoria}",
            use_container_width=True,
            type="primary" if st.session_state.filtro_categoria == categoria else "secondary"
        ):
            filtrar_filmes(categoria)
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.markdown("StreamFlix - Sua plataforma de streaming pessoal")
    st.markdown("Filmes armazenados na nuvem para você assistir de qualquer lugar!")

# ============================================
# CONTEÚDO PRINCIPAL
# ============================================

# Se o player estiver aberto, mostrar o player
if st.session_state.mostrar_player and st.session_state.filme_selecionado:
    filme = get_filme_por_id(st.session_state.filme_selecionado)
    
    if filme:
        # Botão voltar
        if st.button("← Voltar para filmes", type="secondary"):
            fechar_player()
            st.rerun()
        
        st.markdown(f'<div class="section-title">🎥 {filme["titulo"]}</div>', unsafe_allow_html=True)
        
        # Player de vídeo
        st.markdown('<div class="player-overlay">', unsafe_allow_html=True)
        
        # Mostrar vídeo
        st.video(filme["video_url"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações do filme
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {filme['titulo']} ({filme['ano']})")
            st.markdown(f"⭐ **{filme['avaliacao']}/10** • ⏱️ **{filme['duracao']}**")
            st.markdown(f"🎬 **Diretor:** {filme['diretor']}")
            st.markdown(f"📝 {filme['descricao']}")
            
            # Elenco
            st.markdown("**👥 Elenco:**")
            elenco_html = " ".join([f'<span class="cast-tag">{ator}</span>' for ator in filme['elenco']])
            st.markdown(elenco_html, unsafe_allow_html=True)
        
        with col2:
            # Poster
            try:
                st.image(filme["poster"], use_container_width=True)
            except:
                st.image("https://placehold.co/500x750/1a1a1a/ffffff?text=Poster", use_container_width=True)
            
            # Gêneros
            st.markdown("**Gêneros:**")
            for genero in filme["genero"]:
                st.markdown(f"• {genero}")

else:
    # Página inicial com grade de filmes
    
    # Banner principal
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <h1 style="color: white; font-size: 3rem; margin: 0;">StreamFlix</h1>
            <p style="color: #b3b3b3; font-size: 1.2rem;">Sua plataforma de streaming na nuvem</p>
            <p style="color: #b3b3b3;">Assista seus filmes de qualquer lugar, a qualquer hora!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filme em destaque (Capitão América)
    filme_destaque = get_filme_por_id("capitao_america")
    
    if filme_destaque:
        st.markdown(f'<div class="section-title">⭐ Em Destaque</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"## {filme_destaque['titulo']}")
            st.markdown(f"⭐ **{filme_destaque['avaliacao']}/10** • {filme_destaque['ano']} • {filme_destaque['duracao']}")
            st.markdown(filme_destaque['descricao'])
            
            if st.button("▶️ Assistir Agora", key="assistir_destaque", type="primary"):
                selecionar_filme(filme_destaque['id'])
                st.rerun()
        
        with col2:
            try:
                st.image(filme_destaque["poster"], use_container_width=True)
            except:
                st.image("https://placehold.co/500x750/1a1a1a/ffffff?text=Capitao+America", use_container_width=True)
    
    # Grade de filmes
    st.markdown(f'<div class="section-title">🎬 Todos os Filmes</div>', unsafe_allow_html=True)
    
    # Filtrar filmes
    if busca:
        filmes_filtrados = [f for f in movies_database if busca.lower() in f["titulo"].lower()]
    elif st.session_state.filtro_categoria != "Todos":
        filmes_filtrados = [f for f in movies_database if f["categoria"] == st.session_state.filtro_categoria]
    else:
        filmes_filtrados = movies_database
    
    # Exibir filmes em grid
    if filmes_filtrados:
        # Criar grid de 4 colunas
        cols = st.columns(4)
        
        for i, filme in enumerate(filmes_filtrados):
            with cols[i % 4]:
                # Card do filme
                st.markdown(f"""
                    <div style="
                        background: #1a1a1a;
                        border-radius: 15px;
                        overflow: hidden;
                        margin-bottom: 1rem;
                        border: 1px solid rgba(255,255,255,0.1);
                        transition: transform 0.3s;
                        cursor: pointer;
                    ">
                """, unsafe_allow_html=True)
                
                # Poster
                try:
                    st.image(filme["poster"], use_container_width=True)
                except:
                    st.image(f"https://placehold.co/500x750/1a1a1a/ffffff?text={filme['titulo']}", use_container_width=True)
                
                # Informações
                st.markdown(f"""
                    <div style="padding: 1rem;">
                        <div style="color: white; font-weight: 600; margin-bottom: 0.3rem;">{filme['titulo']}</div>
                        <div style="color: #b3b3b3; font-size: 0.9rem;">{filme['ano']} • {filme['duracao']}</div>
                        <div style="color: #ffd700;">⭐ {filme['avaliacao']}/10</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botão assistir
                if st.button("▶️ Assistir", key=f"btn_{filme['id']}", use_container_width=True):
                    selecionar_filme(filme['id'])
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #b3b3b3;">
                <h3>😕 Nenhum filme encontrado</h3>
                <p>Tente buscar por outro nome ou categoria</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #b3b3b3; padding: 2rem 0;">
        <p>🎬 StreamFlix - Sua plataforma de streaming pessoal</p>
        <p style="font-size: 0.9rem;">© 2024 Todos os direitos reservados</p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# COMO USAR:
# ============================================
# 1. Instale o Streamlit: pip install streamlit
# 2. Salve este arquivo como app.py
# 3. Execute: streamlit run app.py
# 4. Substitua "SEU_ID_DO_ARQUIVO" pelo ID real do seu vídeo no Google Drive