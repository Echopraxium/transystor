"""
TranSysTor IDE - Application Streamlit
Version standalone complète avec visualisation 3D
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import json
from pathlib import Path
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="TranSysTor IDE",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chemins
BASE_DIR = Path.cwd()
MODEL_DIR = BASE_DIR / "models" / "tscp"
EXPORT_DIR = BASE_DIR / "exports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# État de l'application (session state)
# ============================================================================

if 'language' not in st.session_state:
    st.session_state.language = 'fr'

if 'visible_layers' not in st.session_state:
    st.session_state.visible_layers = {
        'CM0': False,
        'CM1': True,
        'CM2': True,
        'CM3': False
    }

if 'exclusive_layer' not in st.session_state:
    st.session_state.exclusive_layer = 'CM2'

if 'show_grid' not in st.session_state:
    st.session_state.show_grid = True

if 'show_axes' not in st.session_state:
    st.session_state.show_axes = True

if 'principles' not in st.session_state:
    # Données initiales
    st.session_state.principles = [
        # CM0
        {'name': 'Processus', 'layer': 'CM0', 'position': [1, 1, -0.5], 'color': '#ef4444',
         'description': 'Meta-metaclasse : Transformation dans le temps'},
        {'name': 'Structure', 'layer': 'CM0', 'position': [2, 2, -0.5], 'color': '#f59e0b',
         'description': 'Meta-metaclasse : Organisation spatiale'},
        {'name': 'Échange', 'layer': 'CM0', 'position': [3, 3, -0.5], 'color': '#10b981',
         'description': 'Meta-metaclasse : Transfert d\'information'},
        # CM1
        {'name': 'Observateur', 'layer': 'CM1', 'position': [1.5, 1.5, 1.5], 'color': '#3b82f6',
         'description': 'Point de départ anthropocentrique'},
        {'name': 'Interface', 'layer': 'CM1', 'position': [2, 1.5, 2], 'color': '#10b981',
         'description': 'Médiation entre systèmes'},
        {'name': 'Langage', 'layer': 'CM1', 'position': [2, 2, 1.5], 'color': '#8b5cf6',
         'description': 'Interface d\'échange'},
        {'name': 'Relation', 'layer': 'CM1', 'position': [2.5, 1.5, 2], 'color': '#f59e0b',
         'description': 'Principe structurant'},
        {'name': 'Réseau', 'layer': 'CM1', 'position': [2.5, 2, 2.5], 'color': '#ef4444',
         'description': 'Structure organisationnelle'},
        {'name': 'Agent', 'layer': 'CM1', 'position': [2, 2.5, 2.5], 'color': '#06b6d4',
         'description': 'Entité active'},
        {'name': 'Distribution', 'layer': 'CM1', 'position': [1, 2, 2.5], 'color': '#ec4899',
         'description': 'Processus de dispersion'},
        {'name': 'Communication', 'layer': 'CM1', 'position': [2.5, 2.5, 2], 'color': '#14b8a6',
         'description': 'Échange informationnel'},
        # CM2
        {'name': 'Protocole', 'layer': 'CM2', 'position': [2, 1, 1], 'color': '#a855f7',
         'description': 'Instance d\'Interface avec règles'},
        {'name': 'Bus', 'layer': 'CM2', 'position': [1, 3, 3], 'color': '#f97316',
         'description': 'Bus = Processus ⊗ Distribution'},
    ]

# ============================================================================
# Fonctions utilitaires
# ============================================================================

def create_visualization():
    """Crée la visualisation 3D Plotly"""
    
    fig = go.Figure()
    
    principles = st.session_state.principles
    visible_layers = st.session_state.visible_layers
    exclusive_layer = st.session_state.exclusive_layer
    show_grid = st.session_state.show_grid
    show_axes = st.session_state.show_axes
    
    # Plan CM0
    if visible_layers.get('CM0') and (not exclusive_layer or exclusive_layer == 'CM0'):
        z = -0.5
        for i in range(6):
            # Lignes horizontales
            fig.add_trace(go.Scatter3d(
                x=[0, 5], y=[i, i], z=[z, z],
                mode='lines',
                line=dict(color='gray', width=2),
                opacity=0.3,
                showlegend=False,
                hoverinfo='skip'
            ))
            # Lignes verticales
            fig.add_trace(go.Scatter3d(
                x=[i, i], y=[0, 5], z=[z, z],
                mode='lines',
                line=dict(color='gray', width=2),
                opacity=0.3,
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Fonction pour dessiner un cube
    def draw_cube(size, center, color, layer_name, show):
        if not show or (exclusive_layer and exclusive_layer != layer_name):
            return
        
        half = size / 2
        cx, cy, cz = center
        
        # Sommets
        v = [
            [cx-half, cy-half, cz-half], [cx+half, cy-half, cz-half],
            [cx+half, cy+half, cz-half], [cx-half, cy+half, cz-half],
            [cx-half, cy-half, cz+half], [cx+half, cy-half, cz+half],
            [cx+half, cy+half, cz+half], [cx-half, cy+half, cz+half]
        ]
        
        # Arêtes
        edges = [
            [0,1],[1,2],[2,3],[3,0],
            [4,5],[5,6],[6,7],[7,4],
            [0,4],[1,5],[2,6],[3,7]
        ]
        
        lines = []
        for e in edges:
            lines.extend([v[e[0]], v[e[1]], [None, None, None]])
        
        x, y, z = zip(*lines)
        
        # Arêtes
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=color, width=3),
            opacity=0.6,
            name=f'{layer_name} ({size}×{size}×{size})',
            hoverinfo='name'
        ))
        
        # Faces transparentes avec Mesh3d
        vertices_x = [v[i][0] for i in range(8)]
        vertices_y = [v[i][1] for i in range(8)]
        vertices_z = [v[i][2] for i in range(8)]
        
        faces_i = [0,0,4,4,0,2, 1,1,5,5,1,3, 2,2,6,6,4,0, 3,3,7,7,5,1]
        faces_j = [1,3,5,7,4,6, 2,0,6,4,5,7, 3,1,7,5,6,2, 0,2,4,6,7,3]
        faces_k = [2,2,6,6,5,5, 3,3,7,7,6,6, 1,1,5,5,7,7, 2,2,6,6,4,4]
        
        fig.add_trace(go.Mesh3d(
            x=vertices_x, y=vertices_y, z=vertices_z,
            i=faces_i, j=faces_j, k=faces_k,
            color=color,
            opacity=0.08,
            flatshading=True,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Dessiner les cubes
    cube_configs = {
        'CM1': {'size': 3, 'center': [2, 2, 2], 'color': '#3b82f6'},
        'CM2': {'size': 4, 'center': [2, 2, 2], 'color': '#10b981'},
        'CM3': {'size': 5, 'center': [2, 2, 2], 'color': '#8b5cf6'}
    }
    
    for layer, config in cube_configs.items():
        draw_cube(
            config['size'],
            config['center'],
            config['color'],
            layer,
            visible_layers.get(layer, False)
        )
    
    # Axes IJK
    if show_axes:
        for axis, color, end, label in [
            ('I', 'red', [5.5, 0, 0], 'I'),
            ('J', 'green', [0, 5.5, 0], 'J'),
            ('K', 'blue', [0, 0, 5.5], 'K')
        ]:
            fig.add_trace(go.Scatter3d(
                x=[0, end[0]], y=[0, end[1]], z=[0, end[2]],
                mode='lines+text',
                line=dict(color=color, width=4),
                text=['', label],
                textfont=dict(size=14, color=color),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Principes
    for p in principles:
        if exclusive_layer and p['layer'] != exclusive_layer:
            continue
        if not exclusive_layer and not visible_layers.get(p['layer'], False):
            continue
        
        pos = p['position']
        
        hover_text = f"<b>{p['name']}</b><br>"
        hover_text += f"Couche: {p['layer']}<br>"
        hover_text += f"Position: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]<br>"
        hover_text += f"{p['description']}"
        
        fig.add_trace(go.Scatter3d(
            x=[pos[0]], y=[pos[1]], z=[pos[2]],
            mode='markers+text',
            marker=dict(
                size=10,
                color=p['color'],
                line=dict(color='white', width=2),
                opacity=0.9
            ),
            text=[p['name']],
            textposition='top center',
            textfont=dict(size=9, color=p['color']),
            name=p['name'],
            hovertext=hover_text,
            hoverinfo='text'
        ))
    
    # Mise en page
    fig.update_layout(
        title='TranSysTor - Cubes Imbriqués',
        scene=dict(
            xaxis=dict(title='I', range=[-0.5, 5.5], showgrid=False),
            yaxis=dict(title='J', range=[-0.5, 5.5], showgrid=False),
            zaxis=dict(title='K', range=[-1, 5.5], showgrid=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3)),
            aspectmode='cube',
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        height=700,
        paper_bgcolor='#1f2937',
        plot_bgcolor='#1f2937',
        font=dict(color='white')
    )
    
    return fig


def compute_orthogonality():
    """Calcule l'orthogonalité"""
    principles = st.session_state.principles
    vectors = np.array([p['position'] for p in principles])
    
    if len(vectors) < 2:
        return 1.0
    
    n = len(vectors)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                v1 = vectors[i] / (np.linalg.norm(vectors[i]) + 1e-6)
                v2 = vectors[j] / (np.linalg.norm(vectors[j]) + 1e-6)
                matrix[i, j] = abs(np.dot(v1, v2))
    
    score = 1 - np.mean(matrix[matrix > 0]) if matrix.any() else 1.0
    return score


def export_owl():
    """Génère export OWL"""
    principles = st.session_state.principles
    
    owl = """@prefix : <http://transystor.org/ontology/tscp#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:TSCP rdf:type owl:Ontology ;
    rdfs:label "TSCP Ontology" ;
    owl:versionInfo "0.2.0" .

"""
    for p in principles:
        name = p['name'].replace(' ', '_')
        owl += f"\n:{name} rdf:type :CM{p['layer'][-1]}_Class ;\n"
        owl += f'    rdfs:label "{p["name"]}" ;\n'
        owl += f'    :hasPosition "{p["position"]}" .\n'
    
    filename = f"tscp_owl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ttl"
    filepath = EXPORT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(owl)
    
    return filepath, owl


# ============================================================================
# Interface Streamlit
# ============================================================================

# Header
st.title("🔷 TranSysTor IDE")
st.markdown("**Framework TSCP v0.2.0** - Application Streamlit")

# Sidebar - Contrôles
with st.sidebar:
    st.header("⚙️ Contrôles")
    
    # Langue
    lang = st.radio("🌐 Langue", ['🇫🇷 Français', '🇬🇧 English'], index=0)
    st.session_state.language = 'fr' if 'Français' in lang else 'en'
    
    st.markdown("---")  # Remplace st.divider()
    
    # Mode d'affichage
    st.subheader("Mode d'affichage")
    mode = st.selectbox(
        "Mode",
        ['Superposé', 'CM0 uniquement', 'CM1 uniquement', 'CM2 uniquement', 'CM3 uniquement']
    )
    
    if mode == 'Superposé':
        st.session_state.exclusive_layer = None
    else:
        st.session_state.exclusive_layer = mode.split()[0]
    
    st.markdown("---")
    
    # Couches visibles
    st.subheader("Couches visibles")
    for layer in ['CM0', 'CM1', 'CM2', 'CM3']:
        st.session_state.visible_layers[layer] = st.checkbox(
            f"{layer}",
            value=st.session_state.visible_layers[layer],
            key=f"layer_{layer}"
        )
    
    st.markdown("---")
    
    # Options
    st.subheader("Options")
    st.session_state.show_grid = st.checkbox("Grille 3D", value=True)
    st.session_state.show_axes = st.checkbox("Axes IJK", value=True)
    
    st.markdown("---")
    
    # Statistiques
    st.subheader("📊 Statistiques")
    principles = st.session_state.principles
    by_layer = {}
    for p in principles:
        by_layer.setdefault(p['layer'], []).append(p)
    
    for layer in ['CM0', 'CM1', 'CM2', 'CM3']:
        count = len(by_layer.get(layer, []))
        st.metric(layer, count)
    
    st.metric("Total", len(principles))

# Layout principal à 2 colonnes
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📊 Visualisation 3D")
    
    # Boutons d'action
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()
    
    with btn_col2:
        if st.button("✅ Valider", use_container_width=True):
            score = compute_orthogonality()
            if score > 0.6:
                st.success(f"✅ Orthogonalité: {score:.3f} - PASS")
            else:
                st.warning(f"⚠️ Orthogonalité: {score:.3f} - À REVOIR")
    
    with btn_col3:
        if st.button("📥 Export OWL", use_container_width=True):
            filepath, content = export_owl()
            st.success(f"✅ Exporté: {filepath.name}")
            with st.expander("Voir le contenu"):
                st.code(content[:500] + "...", language="turtle")
    
    # Visualisation
    fig = create_visualization()
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🗂️ Explorateur")
    
    principles = st.session_state.principles
    by_layer = {}
    for p in principles:
        by_layer.setdefault(p['layer'], []).append(p)
    
    for layer in ['CM0', 'CM1', 'CM2', 'CM3']:
        with st.expander(f"**{layer}** ({len(by_layer.get(layer, []))})"):
            for p in by_layer.get(layer, []):
                st.markdown(
                    f"<div style='padding: 5px; border-left: 3px solid {p['color']};'>"
                    f"{p['name']}</div>",
                    unsafe_allow_html=True
                )

# Footer
st.markdown("---")
st.markdown("*TranSysTor IDE v0.2.0 - Streamlit Edition*")