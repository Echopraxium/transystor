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
