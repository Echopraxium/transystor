#!/bin/bash
# Script d'initialisation du projet TranSysTor
# Usage: bash setup_transystor.sh

set -e

PROJECT_NAME="transystor"
PROJECT_DIR="/cygdrive/e/_00_Michel/_00_Lab/_00_GitHub/transystor"

echo "🔷 Initialisation du projet TranSysTor..."

# Créer le répertoire principal
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialiser Git
git init
echo "✓ Git initialisé"

# Créer la structure de dossiers
echo "📁 Création de la structure..."
mkdir -p config
mkdir -p models/schemas
mkdir -p models/tscp
mkdir -p transystor/core
mkdir -p transystor/math
mkdir -p transystor/visualization
mkdir -p transystor/assistant
mkdir -p transystor/cli
mkdir -p notebooks
mkdir -p examples/systems
mkdir -p examples/principles
mkdir -p tests
mkdir -p docs
mkdir -p assets/images
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

# Créer les fichiers __init__.py
touch transystor/__init__.py
touch transystor/core/__init__.py
touch transystor/math/__init__.py
touch transystor/visualization/__init__.py
touch transystor/assistant/__init__.py
touch transystor/cli/__init__.py
touch tests/__init__.py

# LICENSE (BSD-3-Clause)
cat > LICENSE << 'EOF'
BSD 3-Clause License

Copyright (c) 2024, TranSysTor Framework
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
EOF
echo "✓ LICENSE créé"

# .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Documentation
site/
docs/_build/

# TranSysTor specific
*.tst.backup
temp_models/
EOF
echo "✓ .gitignore créé"

# requirements.txt
cat > requirements.txt << 'EOF'
# Core dependencies
numpy>=1.24.0
scipy>=1.10.0
sympy>=1.12
networkx>=3.0

# Visualization
plotly>=5.14.0
matplotlib>=3.7.0

# Parsing
lark>=1.1.5

# Validation
jsonschema>=4.17.0
pyyaml>=6.0

# Jupyter
jupyter>=1.0.0
jupyterlab>=4.0.0
ipywidgets>=8.0.0

# Development
pytest>=7.3.0
pytest-cov>=4.1.0
black>=23.3.0
flake8>=6.0.0
mypy>=1.3.0

# Documentation
mkdocs>=1.4.0
mkdocs-material>=9.1.0
EOF
echo "✓ requirements.txt créé"

# README.md
cat > README.md << 'EOF'
# TranSysTor 🔷

**Framework TSCP - Principes Transdisciplinaires de Construction de Systèmes**

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Vision

TranSysTor est un langage de modélisation et un environnement de développement intégré (IDE) pour l'analyse, la conception et la validation de systèmes complexes à travers une approche transdisciplinaire.

## 🏗️ Architecture

Le framework TSCP s'organise en **4 couches** :

- **CM0** : Meta-métamodèle (Meta-metaclasses et Méta-traits)
- **CM1** : Métamodèle (Metaclasses et Traits)
- **CM2** : Modèle - Cube 4×4×4 (64 classes organisées)
- **CM3** : User Model - Cube 5×5×5 (125 instances pour systèmes réels)

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/transystor.git
cd transystor

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

## 📖 Démarrage rapide

```bash
jupyter lab
# Ouvrir notebooks/00_quickstart.ipynb
```

## 📄 Licence

Ce projet est sous licence BSD-3-Clause - voir [LICENSE](LICENSE).

---

*"From elements to systems, through principles"* 🔷→🔶→🟦→🟩
EOF
echo "✓ README.md créé"

# setup.py minimal
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="transystor",
    version="0.1.0",
    author="TranSysTor Framework",
    description="Framework TSCP - Principes Transdisciplinaires de Construction de Systèmes",
    url="https://github.com/yourusername/transystor",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "sympy>=1.12",
        "networkx>=3.0",
        "plotly>=5.14.0",
        "lark>=1.1.5",
        "jsonschema>=4.17.0",
        "pyyaml>=6.0",
    ],
)
EOF
echo "✓ setup.py créé"

# Modèle CM0 initial (JSON)
cat > models/tscp/cm0.json << 'EOF'
{
  "layer": "CM0",
  "version": "0.1.0",
  "meta_metaclasses": [
    {
      "name": "Processus",
      "type": "MetaMetaClass",
      "description": "Transformation dans le temps",
      "stability": "validated"
    },
    {
      "name": "Structure",
      "type": "MetaMetaClass",
      "description": "Organisation spatiale ou conceptuelle",
      "stability": "validated"
    },
    {
      "name": "Échange",
      "type": "MetaMetaClass",
      "description": "Transfert d'information, matière ou énergie",
      "stability": "validated"
    }
  ],
  "meta_traits": [
    {
      "name": "Polarité",
      "type": "MetaTrait",
      "value_type": "categorical",
      "description": "Attracteurs dans un Espace des États",
      "arity": "N-polaire",
      "stability": "validated"
    },
    {
      "name": "Substrat",
      "type": "MetaTrait",
      "value_type": "categorical",
      "description": "Support permettant la manifestation d'un principe",
      "stability": "validated"
    },
    {
      "name": "Domaine",
      "type": "MetaTrait",
      "value_type": "categorical",
      "examples": ["Urbain", "Informatique", "Biologique", "Social"],
      "stability": "validated"
    }
  ]
}
EOF
echo "✓ Modèle CM0 créé"

# Git: premier commit
git add .
git commit -m "🔷 Initial commit - TranSysTor Framework v0.1.0"
echo "✓ Premier commit Git effectué"

echo ""
echo "✅ Projet TranSysTor initialisé avec succès !"
echo ""
echo "📍 Emplacement: $PROJECT_DIR"
echo ""
echo "🚀 Prochaines étapes:"
echo "   1. cd $PROJECT_DIR"
echo "   2. Créer un dépôt sur GitHub"
echo "   3. git remote add origin https://github.com/VOTRE_USERNAME/transystor.git"
echo "   4. git branch -M main"
echo "   5. git push -u origin main"
echo ""
echo "   Ou pour créer un environnement virtuel:"
echo "   python -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""