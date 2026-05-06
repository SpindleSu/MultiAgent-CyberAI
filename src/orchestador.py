
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Configuración de conexión con el servidor local de modelos (Ollama)
# Se utiliza el endpoint compatible con OpenAI para facilitar la integración
config_list = [
    {
        "model": "llama3", 
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
]

def iniciar_auditoria(pregunta_usuario):
    """
    Orquesta un debate técnico entre tres agentes especializados.
    El objetivo es confrontar la funcionalidad frente a la seguridad
    para obtener una solución técnica validada y robusta.
    """

    # Representa al usuario humano. No interviene (NEVER) para permitir 
    # que la discusión entre los agentes sea autónoma y fluida.
    admin = UserProxyAgent(
        name="Admin", 
        human_input_mode="NEVER", 
        code_execution_config=False,
        max_consecutive_auto_reply=1
    )

    # Perfil enfocado en la entrega de resultados funcionales y eficientes.
    programador = AssistantAgent(
        name="DevExpert",
        llm_config={"config_list": config_list},
        system_message="Eres un programador senior de Python. Tu prioridad es ofrecer código ejecutable y eficiente."
    )

    # Perfil con mentalidad de 'Red Team'. Su misión es encontrar vulnerabilidades,
    # malas prácticas y riesgos de seguridad en el código propuesto.
    auditor = AssistantAgent(
        name="SecurityShadow",
        llm_config={"config_list": config_list},
        system_message="Eres un experto en ciberseguridad. Sé ácido y crítico. Busca fallos de seguridad en cada propuesta."
    )

    # El punto de equilibrio. Filtra el ruido de la discusión y redacta 
    # la versión definitiva aplicando los parches de seguridad necesarios.
    juez = AssistantAgent(
        name="ChiefArchitect",
        llm_config={"config_list": config_list},
        system_message="Eres un Arquitecto de Sistemas veterano. Tu meta es dictar la solución final que sea segura y funcional."
    )

    # El GroupChat permite la interacción dinámica (no lineal) entre agentes.
    # Limitamos a 6 rondas para optimizar el consumo de recursos locales.
    groupchat = GroupChat(
        agents=[admin, programador, auditor, juez], 
        messages=[], 
        max_round=6 
    )
    
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

    # Punto de inicio del flujo de trabajo multi-agente
    admin.initiate_chat(manager, message=pregunta_usuario)
