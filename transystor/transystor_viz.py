"""
TranSysTor Visualization Module
Fonctions de visualisation 3D des cubes imbriqués
"""

import plotly.graph_objects as go
import numpy as np
from transystor_core import CUBE_CONFIGS, t


def create_nested_cubes_visualization(principles, show_layers, exclusive_layer=None, 
                                     show_grid=True, show_axes=True, state=None):
    """
    Crée une visualisation 3D interactive complète des cubes imbriqués.
    
    Args:
        principles: Liste des principes à afficher
        show_layers: Dict indiquant quelles couches afficher
        exclusive_layer: Si défini, affiche uniquement cette couche
        show_grid: Afficher les grilles internes
        show_axes: Afficher les axes IJK
        state: Instance de IDEState pour traductions
    
    Returns:
        Figure Plotly
    """
    
    fig = go.Figure()
    
    # 1. Plan CM0 (grille 5x5 horizontale)
    if show_layers.get('CM0', False) and (not exclusive_layer or exclusive_layer == 'CM0'):
        z_plane = CUBE_CONFIGS['CM0']['z']
        
        for i in range(6):
            # Lignes horizontales
            fig.add_trace(go.Scatter3d(
                x=[0, 5], y=[i, i], z=[z_plane, z_plane],
                mode='lines',
                line=dict(color='gray', width=2),
                opacity=0.3,
                showlegend=False,
                hoverinfo='skip'
            ))
            # Lignes verticales
            fig.add_trace(go.Scatter3d(
                x=[i, i], y=[0, 5], z=[z_plane, z_plane],
                mode='lines',
                line=dict(color='gray', width=2),
                opacity=0.3,
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # 2. Fonction pour dessiner un cube transparent
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
            [0,1],[1,2],[2,3],[3,0],  # Face inf
            [4,5],[5,6],[6,7],[7,4],  # Face sup
            [0,4],[1,5],[2,6],[3,7]   # Verticales
        ]
        
        lines = []
        for e in edges:
            lines.extend([v[e[0]], v[e[1]], [None, None, None]])
        
        x, y, z = zip(*lines)
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=color, width=3),
            opacity=0.6,
            name=f'{layer_name} ({size}×{size}×{size})',
            hoverinfo='name'
        ))
        
        # Grille interne
        if show_grid and size >= 3:
            for i in range(int(size)+1):
                offset_x = cx - half + i
                offset_y = cy - half + i
                offset_z = cz - half + i
                
                # Lignes // à X
                if i <= size:
                    fig.add_trace(go.Scatter3d(
                        x=[cx-half, cx+half], y=[offset_y, offset_y], z=[cz-half, cz-half],
                        mode='lines', line=dict(color=color, width=0.5),
                        opacity=0.15, showlegend=False, hoverinfo='skip'
                    ))
    
    # Dessiner les cubes
    for layer in ['CM1', 'CM2', 'CM3']:
        config = CUBE_CONFIGS[layer]
        draw_cube(config['size'], config['center'], config['color'], 
                 layer, show_layers.get(layer, False))
    
    # 3. Principes
    for p in principles:
        if exclusive_layer and p['layer'] != exclusive_layer:
            continue
        if not exclusive_layer and not show_layers.get(p['layer'], False):
            continue
        
        pos = p['position']
        
        hover_text = f"<b>{p['name']}</b><br>"
        hover_text += f"Couche: {p['layer']}<br>"
        hover_text += f"Position: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]<br>"
        hover_text += f"Type: {p.get('type', 'N/A')}<br><br>"
        hover_text += p.get('description', '')
        
        if 'combination' in p:
            hover_text += f"<br><br>⊗ {p['combination']}"
        
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
    
    # 4. Axes IJK
    if show_axes:
        # Axe I (rouge)
        fig.add_trace(go.Scatter3d(
            x=[0, 5.5], y=[0, 0], z=[0, 0],
            mode='lines+text',
            line=dict(color='red', width=4),
            text=['', 'I'],
            textposition='middle right',
            textfont=dict(size=14, color='red'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Axe J (vert)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 5.5], z=[0, 0],
            mode='lines+text',
            line=dict(color='green', width=4),
            text=['', 'J'],
            textposition='middle right',
            textfont=dict(size=14, color='green'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Axe K (bleu)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, 5.5],
            mode='lines+text',
            line=dict(color='blue', width=4),
            text=['', 'K'],
            textposition='middle right',
            textfont=dict(size=14, color='blue'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Mise en page
    title_text = t('title', state) if state else 'TranSysTor IDE'
    
    fig.update_layout(
        title={'text': title_text, 'x': 0.5, 'xanchor': 'center'},
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


def compute_orthogonality(principles):
    """
    Calcule une métrique d'orthogonalité simplifiée
    
    Args:
        principles: Liste des principes
    
    Returns:
        Tuple (score, matrice)
    """
    vectors = np.array([p['position'] for p in principles if 'position' in p])
    
    if len(vectors) < 2:
        return 1.0, np.array([[]])
    
    n = len(vectors)
    ortho_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                v1 = vectors[i] / (np.linalg.norm(vectors[i]) + 1e-6)
                v2 = vectors[j] / (np.linalg.norm(vectors[j]) + 1e-6)
                ortho_matrix[i, j] = abs(np.dot(v1, v2))
    
    ortho_score = 1 - np.mean(ortho_matrix[ortho_matrix > 0]) if ortho_matrix.any() else 1.0
    
    return ortho_score, ortho_matrix


print("✅ Module TranSysTor Visualization chargé")