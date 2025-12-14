"""
TranSysTor Core Module
Configuration, état global et traductions
"""

from pathlib import Path
from datetime import datetime

# Chemins
MODEL_DIR = Path('../models/tscp')
SCHEMA_DIR = Path('../models/schemas')
EXPORT_DIR = Path('../exports')

# État global de l'application
class IDEState:
    """Gestion de l'état global de l'IDE"""
    
    def __init__(self):
        self.language = 'fr'  # 'fr' ou 'en'
        self.visible_layers = {
            'CM0': False,
            'CM1': True,
            'CM2': True,
            'CM3': False
        }
        self.exclusive_layer = 'CM2'  # Couche affichée par défaut
        self.selected_principle = None
        self.show_grid = True
        self.show_axes = True
        self.chatbot_config = {
            'provider': 'anthropic',
            'api_key': None,
            'model': 'claude-sonnet-4-20250514'
        }
    
    def toggle_layer(self, layer):
        """Active/désactive une couche"""
        if layer in self.visible_layers:
            self.visible_layers[layer] = not self.visible_layers[layer]
    
    def set_exclusive_layer(self, layer):
        """Définit la couche exclusive (ou None pour mode superposé)"""
        self.exclusive_layer = layer
    
    def switch_language(self):
        """Bascule entre français et anglais"""
        self.language = 'en' if self.language == 'fr' else 'fr'


# Dictionnaire de traductions complet
TRANSLATIONS = {
    'fr': {
        'title': 'TranSysTor IDE - Cubes Imbriqués',
        'explorer': 'Explorateur de Modèle',
        'visualization': 'Visualisation 3D',
        'info': 'Informations',
        'chatbot': 'Assistant IA',
        'layer': 'Couche',
        'position': 'Position',
        'description': 'Description',
        'formulas': 'Formules',
        'relations': 'Relations',
        'properties': 'Propriétés',
        'validation': 'Validation Mathématique',
        'export': 'Exporter',
        'language': 'Langue',
        'show_grid': 'Afficher grille',
        'show_axes': 'Afficher axes',
        'exclusive_mode': 'Mode exclusif',
        'overlay_mode': 'Mode superposé',
        'update': 'Actualiser',
        'save': 'Sauvegarder',
        'load': 'Charger',
        'send': 'Envoyer',
        'provider': 'Fournisseur',
        'api_key': 'Clé API',
        'question': 'Question',
        'predefined_questions': 'Questions prédéfinies',
        'format': 'Format',
        'generate': 'Générer',
        'principle': 'Principe',
        'name': 'Nom',
        'type': 'Type',
        'identity': 'Identité',
        'mathematical_validation': 'Validation Mathématique',
        'orthogonality': 'Orthogonalité',
        'group_coherence': 'Cohérence de groupe',
        'semantic_distance': 'Distance sémantique'
    },
    'en': {
        'title': 'TranSysTor IDE - Nested Cubes',
        'explorer': 'Model Explorer',
        'visualization': '3D Visualization',
        'info': 'Information',
        'chatbot': 'AI Assistant',
        'layer': 'Layer',
        'position': 'Position',
        'description': 'Description',
        'formulas': 'Formulas',
        'relations': 'Relations',
        'properties': 'Properties',
        'validation': 'Mathematical Validation',
        'export': 'Export',
        'language': 'Language',
        'show_grid': 'Show grid',
        'show_axes': 'Show axes',
        'exclusive_mode': 'Exclusive mode',
        'overlay_mode': 'Overlay mode',
        'update': 'Update',
        'save': 'Save',
        'load': 'Load',
        'send': 'Send',
        'provider': 'Provider',
        'api_key': 'API Key',
        'question': 'Question',
        'predefined_questions': 'Predefined Questions',
        'format': 'Format',
        'generate': 'Generate',
        'principle': 'Principle',
        'name': 'Name',
        'type': 'Type',
        'identity': 'Identity',
        'mathematical_validation': 'Mathematical Validation',
        'orthogonality': 'Orthogonality',
        'group_coherence': 'Group coherence',
        'semantic_distance': 'Semantic distance'
    }
}


def t(key, state):
    """
    Fonction de traduction
    
    Args:
        key: Clé de traduction
        state: Instance de IDEState
    
    Returns:
        Texte traduit
    """
    return TRANSLATIONS[state.language].get(key, key)


# Configuration des cubes imbriqués
CUBE_CONFIGS = {
    'CM0': {
        'type': 'plane',
        'size': [5, 5],
        'z': -0.5,
        'color': '#4b5563',
        'label_fr': 'Meta-métamodèle (Plan 5×5)',
        'label_en': 'Meta-metamodel (Plane 5×5)'
    },
    'CM1': {
        'type': 'cube',
        'size': 3,
        'center': [2, 2, 2],
        'color': '#3b82f6',
        'label_fr': 'Métamodèle (Cube 3×3×3)',
        'label_en': 'Metamodel (Cube 3×3×3)'
    },
    'CM2': {
        'type': 'cube',
        'size': 4,
        'center': [2, 2, 2],
        'color': '#10b981',
        'label_fr': 'Modèle (Cube 4×4×4)',
        'label_en': 'Model (Cube 4×4×4)'
    },
    'CM3': {
        'type': 'cube',
        'size': 5,
        'center': [2, 2, 2],
        'color': '#8b5cf6',
        'label_fr': 'Systèmes réels (Cube 5×5×5)',
        'label_en': 'Real systems (Cube 5×5×5)'
    }
}


def load_model(layer_name):
    """
    Charge un modèle JSON depuis le répertoire models/tscp
    
    Args:
        layer_name: Nom de la couche (CM0, CM1, CM2, CM3)
    
    Returns:
        Dict contenant le modèle chargé
    """
    import json
    
    file_path = MODEL_DIR / f"{layer_name.lower()}.json"
    
    if not file_path.exists():
        print(f"⚠️  Fichier {file_path} non trouvé. Création d'un modèle vide.")
        return {"layer": layer_name, "version": "0.2.0"}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Modèle {layer_name} chargé")
    return data


def save_model(model_data, layer_name):
    """
    Sauvegarde un modèle dans models/tscp/
    
    Args:
        model_data: Données du modèle
        layer_name: Nom de la couche
    """
    import json
    
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    file_path = MODEL_DIR / f"{layer_name.lower()}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Modèle {layer_name} sauvegardé dans {file_path}")


def save_complete_state(state, principles_data):
    """
    Sauvegarde l'état complet de l'IDE
    
    Args:
        state: Instance de IDEState
        principles_data: Liste des principes
    
    Returns:
        Path du fichier sauvegardé
    """
    import json
    
    model_state = {
        'version': '0.2.0',
        'timestamp': datetime.now().isoformat(),
        'language': state.language,
        'principles': principles_data,
        'cube_configs': CUBE_CONFIGS,
        'visible_layers': state.visible_layers,
        'exclusive_layer': state.exclusive_layer
    }
    
    filename = f"tscp_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = MODEL_DIR / filename
    
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(model_state, f, indent=2, ensure_ascii=False)
    
    print(f"✅ État complet sauvegardé: {filepath}")
    return filepath


# Initialisation
print("✅ Module TranSysTor Core chargé")
print(f"📂 Répertoire modèles: {MODEL_DIR.absolute()}")
print(f"📂 Répertoire exports: {EXPORT_DIR.absolute()}")