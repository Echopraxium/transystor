"""
TranSysTor Chatbot Module
Assistant IA pour validation et critique
"""


def create_chatbot_interface(state):
    """
    Crée l'interface du chatbot
    
    Args:
        state: Instance de IDEState
    
    Returns:
        Tuple (provider_widget, api_key_widget, chat_input, chat_button, chat_output)
    """
    import ipywidgets as widgets
    from IPython.display import clear_output
    
    # Widgets
    chatbot_provider = widgets.Dropdown(
        options=['Anthropic (Claude)', 'OpenAI (GPT)', 'Local (Ollama)', 'Désactivé'],
        value='Désactivé',
        description='Provider:',
        style={'description_width': 'initial'}
    )
    
    api_key_input = widgets.Password(
        placeholder='Entrez votre clé API',
        description='API Key:',
        disabled=True,
        style={'description_width': 'initial'}
    )
    
    chat_input = widgets.Textarea(
        placeholder='Posez votre question sur le framework TSCP...',
        description='Question:',
        layout=widgets.Layout(width='100%', height='100px')
    )
    
    chat_button = widgets.Button(
        description='Envoyer',
        button_style='info',
        icon='paper-plane',
        disabled=True
    )
    
    chat_output = widgets.Output()
    
    # Callbacks
    def on_provider_change(change):
        if change['new'] in ['Anthropic (Claude)', 'OpenAI (GPT)']:
            api_key_input.disabled = False
            chat_button.disabled = False
        elif change['new'] == 'Local (Ollama)':
            api_key_input.disabled = True
            chat_button.disabled = False
        else:
            api_key_input.disabled = True
            chat_button.disabled = True
        
        state.chatbot_config['provider'] = change['new']
    
    chatbot_provider.observe(on_provider_change, names='value')
    
    def on_chat_send(b):
        with chat_output:
            clear_output(wait=True)
            
            question = chat_input.value
            if not question:
                print("⚠️ Veuillez entrer une question")
                return
            
            print(f"💬 Vous: {question}\n")
            print("🤖 Assistant:\n")
            
            provider = chatbot_provider.value
            
            if provider == 'Anthropic (Claude)':
                response = send_to_anthropic(question, api_key_input.value, state)
                print(response)
            
            elif provider == 'OpenAI (GPT)':
                response = send_to_openai(question, api_key_input.value, state)
                print(response)
            
            elif provider == 'Local (Ollama)':
                response = send_to_ollama(question, state)
                print(response)
            
            else:
                print("Chatbot désactivé")
    
    chat_button.on_click(on_chat_send)
    
    return chatbot_provider, api_key_input, chat_input, chat_button, chat_output


def send_to_anthropic(question, api_key, state):
    """
    Envoie une question à l'API Anthropic
    
    Args:
        question: Question de l'utilisateur
        api_key: Clé API
        state: Instance de IDEState
    
    Returns:
        Réponse du modèle
    """
    if not api_key:
        return "❌ Veuillez configurer votre clé API Anthropic"
    
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        system_prompt = """Tu es un expert du framework TSCP (Principes Transdisciplinaires de Construction de Systèmes).

Le framework TSCP organise les principes en 4 couches :
- CM0 : Meta-métamodèle (plan 5×5) - Meta-metaclasses et Méta-traits
- CM1 : Métamodèle (cube 3×3×3) - Metaclasses et Traits
- CM2 : Modèle (cube 4×4×4) - Classes organisées dans un cube
- CM3 : Systèmes réels (cube 5×5×5) - Instances concrètes

Opérateurs :
- ⊗ : Produit tensoriel (combinaison)
- ∈ : Instance de
- ⊂ : Sous-classe de / Dérive de

Ton rôle : valider les principes, détecter les incohérences, proposer des améliorations, vérifier l'orthogonalité."""
        
        message = client.messages.create(
            model=state.chatbot_config['model'],
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        
        return message.content[0].text
        
    except ImportError:
        return """❌ Module 'anthropic' non installé.

Pour installer :
    pip install anthropic

Puis relancez cette cellule."""
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def send_to_openai(question, api_key, state):
    """
    Envoie une question à l'API OpenAI
    
    Args:
        question: Question de l'utilisateur
        api_key: Clé API
        state: Instance de IDEState
    
    Returns:
        Réponse du modèle
    """
    if not api_key:
        return "❌ Veuillez configurer votre clé API OpenAI"
    
    try:
        import openai
        
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert du framework TSCP."},
                {"role": "user", "content": question}
            ]
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        return """❌ Module 'openai' non installé.

Pour installer :
    pip install openai

Puis relancez cette cellule."""
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def send_to_ollama(question, state):
    """
    Envoie une question à Ollama local
    
    Args:
        question: Question de l'utilisateur
        state: Instance de IDEState
    
    Returns:
        Réponse du modèle
    """
    try:
        import ollama
        
        response = ollama.chat(model='llama2', messages=[
            {'role': 'system', 'content': 'Tu es un expert du framework TSCP.'},
            {'role': 'user', 'content': question}
        ])
        
        return response['message']['content']
        
    except ImportError:
        return """❌ Module 'ollama' non installé.

Pour installer :
    pip install ollama

Assurez-vous également que le serveur Ollama est lancé localement."""
    
    except Exception as e:
        return f"❌ Erreur: {str(e)}"


def get_predefined_questions():
    """
    Retourne une liste de questions prédéfinies
    
    Returns:
        Liste de tuples (label, question)
    """
    return [
        ("Vérifier orthogonalité", "Vérifie l'orthogonalité de tous les principes de CM2 et identifie les conflits potentiels."),
        ("Proposer contre-arguments", "Propose 3 contre-arguments pour ranger 'Métabolisme' en CM1 plutôt qu'en CM2."),
        ("Dépendances manquantes", "Quelles sont les dépendances manquantes pour que le principe 'Communication' soit complet ?"),
        ("Formule tensorielle", "Génère une formule tensorielle pour combiner 'Agent' et 'Comportement'."),
        ("Validation isotopie", "Est-ce que 'Symétrie/Asymétrie' forme une isotopie valide ? Justifie."),
        ("Restructuration suggérée", "Analyse la structure actuelle du cube CM2 et propose des améliorations."),
    ]


print("✅ Module TranSysTor Chatbot chargé")