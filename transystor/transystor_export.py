"""
TranSysTor Export Module
Export sémantique : OWL, RDFS, SHACL
"""

from datetime import datetime
from pathlib import Path

# Import relatif ou absolu
try:
    from transystor.transystor_core import EXPORT_DIR
except ImportError:
    from transystor_core import EXPORT_DIR


def export_to_owl(principles_data, model_name="TSCP"):
    """
    Génère une ontologie OWL du modèle
    
    Args:
        principles_data: Liste des principes
        model_name: Nom du modèle
    
    Returns:
        Contenu OWL en format Turtle
    """
    
    owl_content = f"""@prefix : <http://transystor.org/ontology/{model_name.lower()}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:{model_name} rdf:type owl:Ontology ;
    rdfs:label "{model_name} Ontology"@en ;
    rdfs:label "Ontologie {model_name}"@fr ;
    rdfs:comment "Framework TSCP - Principes Transdisciplinaires de Construction de Systèmes"@fr ;
    rdfs:comment "TSCP Framework - Transdisciplinary Principles for System Construction"@en ;
    owl:versionInfo "0.2.0" ;
    owl:versionIRI <http://transystor.org/ontology/{model_name.lower()}/0.2.0> .

# ============================================================================
# Classes pour les couches
# ============================================================================

:CM0_MetaMetaClass rdf:type owl:Class ;
    rdfs:label "Meta-Metaclasse"@fr, "Meta-Metaclass"@en ;
    rdfs:comment "Couche CM0 - Meta-métamodèle"@fr ;
    rdfs:comment "Layer CM0 - Meta-metamodel"@en .

:CM1_MetaClass rdf:type owl:Class ;
    rdfs:label "Metaclasse"@fr, "Metaclass"@en ;
    rdfs:comment "Couche CM1 - Métamodèle (Cube 3×3×3)"@fr ;
    rdfs:comment "Layer CM1 - Metamodel (Cube 3×3×3)"@en .

:CM2_Class rdf:type owl:Class ;
    rdfs:label "Classe"@fr, "Class"@en ;
    rdfs:comment "Couche CM2 - Modèle (Cube 4×4×4)"@fr ;
    rdfs:comment "Layer CM2 - Model (Cube 4×4×4)"@en .

:CM3_Instance rdf:type owl:Class ;
    rdfs:label "Instance"@fr, "Instance"@en ;
    rdfs:comment "Couche CM3 - Systèmes réels (Cube 5×5×5)"@fr ;
    rdfs:comment "Layer CM3 - Real systems (Cube 5×5×5)"@en .

# ============================================================================
# Propriétés de données
# ============================================================================

:hasPosition rdf:type owl:DatatypeProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range xsd:string ;
    rdfs:label "a pour position"@fr, "has position"@en ;
    rdfs:comment "Position [I, J, K] dans le cube"@fr .

:hasDescription rdf:type owl:DatatypeProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range xsd:string ;
    rdfs:label "a pour description"@fr, "has description"@en .

:hasColor rdf:type owl:DatatypeProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range xsd:string ;
    rdfs:label "a pour couleur"@fr, "has color"@en .

# ============================================================================
# Propriétés d'objets
# ============================================================================

:belongsToLayer rdf:type owl:ObjectProperty ;
    rdfs:domain owl:Thing ;
    rdfs:label "appartient à la couche"@fr, "belongs to layer"@en .

:tensorProduct rdf:type owl:ObjectProperty ;
    rdfs:label "produit tensoriel"@fr, "tensor product"@en ;
    rdfs:comment "Combinaison de principes (opérateur ⊗)"@fr ;
    rdfs:comment "Combination of principles (operator ⊗)"@en .

:derivesFrom rdf:type owl:ObjectProperty ;
    rdfs:label "dérive de"@fr, "derives from"@en ;
    rdfs:comment "Héritage ou sous-classe (⊂)"@fr .

:hasRelation rdf:type owl:ObjectProperty ;
    rdfs:label "a pour relation"@fr, "has relation"@en .

# ============================================================================
# Principes
# ============================================================================

"""
    
    # Ajouter chaque principe
    for p in principles_data:
        safe_name = p['name'].replace(' ', '_').replace("'", '')
        layer = p.get('layer', 'CM1')
        
        layer_class_map = {
            'CM0': ':CM0_MetaMetaClass',
            'CM1': ':CM1_MetaClass',
            'CM2': ':CM2_Class',
            'CM3': ':CM3_Instance'
        }
        
        layer_class = layer_class_map.get(layer, ':CM1_MetaClass')
        
        owl_content += f"\n:{safe_name} rdf:type {layer_class} ;\n"
        owl_content += f'    rdfs:label "{p["name"]}"@fr ;\n'
        owl_content += f'    :hasPosition "{p.get("position", [])}" ;\n'
        owl_content += f'    :hasColor "{p.get("color", "#000000")}" ;\n'
        owl_content += f'    :belongsToLayer :{layer} ;\n'
        
        if 'description' in p:
            desc = p['description'].replace('"', '\\"')
            owl_content += f'    :hasDescription "{desc}"@fr ;\n'
        
        if 'derives' in p and p['derives']:
            for derive in p['derives']:
                derive_safe = derive.split()[0].replace(' ', '_')
                owl_content += f'    :derivesFrom :{derive_safe} ;\n'
        
        if 'combination' in p:
            owl_content += f'    rdfs:comment "Combinaison: {p["combination"]}"@fr ;\n'
        
        owl_content += "    .\n"
    
    return owl_content


def export_to_shacl(principles_data):
    """
    Génère des contraintes SHACL pour validation
    
    Args:
        principles_data: Liste des principes
    
    Returns:
        Contenu SHACL en format Turtle
    """
    
    shacl_content = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix tscp: <http://transystor.org/ontology/tscp#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# ============================================================================
# Shapes pour les contraintes du modèle TSCP
# ============================================================================

# Shape pour vérifier les positions dans les cubes
tscp:CubePositionShape a sh:NodeShape ;
    sh:targetClass tscp:CM2_Class ;
    sh:property [
        sh:path tscp:hasPosition ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:pattern "^\\\\[\\\\d+\\\\.?\\\\d*,\\\\s*\\\\d+\\\\.?\\\\d*,\\\\s*\\\\d+\\\\.?\\\\d*\\\\]$" ;
        sh:message "La position doit être au format [I, J, K]"@fr ;
    ] .

# Shape pour l'appartenance à une couche
tscp:LayerShape a sh:NodeShape ;
    sh:targetClass tscp:CM1_MetaClass, tscp:CM2_Class, tscp:CM3_Instance ;
    sh:property [
        sh:path tscp:belongsToLayer ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "Chaque principe doit appartenir à exactement une couche"@fr ;
    ] .

# Shape pour orthogonalité (validation sémantique)
tscp:OrthogonalityShape a sh:NodeShape ;
    sh:targetClass tscp:CM2_Class ;
    sh:sparql [
        sh:message "Principe trop proche d'un autre (orthogonalité < 0.6)"@fr ;
        sh:select \"\"\"
            PREFIX tscp: <http://transystor.org/ontology/tscp#>
            SELECT ?this
            WHERE {
                ?this tscp:orthogonalityScore ?score .
                FILTER (?score < 0.6)
            }
        \"\"\" ;
    ] .

# Shape pour les combinaisons tensorielle
tscp:CombinationShape a sh:NodeShape ;
    sh:targetClass tscp:CM2_Class ;
    sh:sparql [
        sh:message "Les composants d'une combinaison doivent être rangés"@fr ;
        sh:select \"\"\"
            PREFIX tscp: <http://transystor.org/ontology/tscp#>
            SELECT ?this
            WHERE {
                ?this tscp:tensorProduct ?component .
                FILTER NOT EXISTS { ?component rdf:type ?anyClass }
            }
        \"\"\" ;
    ] .

# Shape pour les relations
tscp:RelationShape a sh:NodeShape ;
    sh:targetClass tscp:CM1_MetaClass ;
    sh:property [
        sh:path tscp:hasRelation ;
        sh:nodeKind sh:IRI ;
        sh:message "Les relations doivent pointer vers des principes valides"@fr ;
    ] .

# Shape pour les descriptions
tscp:DescriptionShape a sh:NodeShape ;
    sh:targetClass tscp:CM0_MetaMetaClass, tscp:CM1_MetaClass, tscp:CM2_Class ;
    sh:property [
        sh:path tscp:hasDescription ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 10 ;
        sh:message "Chaque principe doit avoir une description d'au moins 10 caractères"@fr ;
    ] .
"""
    
    return shacl_content


def export_to_rdfs(principles_data):
    """
    Génère un schéma RDFS simplifié
    
    Args:
        principles_data: Liste des principes
    
    Returns:
        Contenu RDFS en format Turtle
    """
    
    rdfs_content = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tscp: <http://transystor.org/ontology/tscp#> .

# Classes de base
tscp:Principle rdf:type rdfs:Class ;
    rdfs:label "Principe TSCP"@fr ;
    rdfs:comment "Classe racine pour tous les principes"@fr .

tscp:CM0_MetaMetaClass rdfs:subClassOf tscp:Principle .
tscp:CM1_MetaClass rdfs:subClassOf tscp:Principle .
tscp:CM2_Class rdfs:subClassOf tscp:Principle .
tscp:CM3_Instance rdfs:subClassOf tscp:Principle .

# Propriétés
tscp:hasPosition rdf:type rdf:Property ;
    rdfs:domain tscp:Principle ;
    rdfs:range rdfs:Literal .

tscp:belongsToLayer rdf:type rdf:Property ;
    rdfs:domain tscp:Principle .
"""
    
    return rdfs_content


def save_export(content, format_name, model_name="tscp"):
    """
    Sauvegarde un export dans le répertoire exports/
    
    Args:
        content: Contenu à sauvegarder
        format_name: Format (owl, shacl, rdfs)
        model_name: Nom du modèle
    
    Returns:
        Path du fichier sauvegardé
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{model_name}_{format_name}_{timestamp}.ttl"
    filepath = EXPORT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Export {format_name.upper()} sauvegardé: {filepath}")
    return filepath


print("✅ Module TranSysTor Export chargé")