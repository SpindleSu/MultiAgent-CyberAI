
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Configuración de conexión con el motor de IA local (Ollama)
# Se utiliza el endpoint compatible con OpenAI para máxima compatibilidad.
config_list = [
    {
        "model": "llama3", 
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama", # Requerido por la sintaxis de AutoGen
    }
]

def iniciar_auditoria(pregunta_usuario):
    """
    Orquesta un debate dinámico entre agentes especializados para
    validar la seguridad y eficiencia de una solución técnica.
    """
    from agents import ROLES  # Importación local para evitar dependencias circulares

    # Representa al usuario. Modo 'NEVER' para que la IA debata de forma autónoma.
    admin = UserProxyAgent(
        name="Admin", 
        human_input_mode="NEVER", 
        code_execution_config=False,
        max_consecutive_auto_reply=1
    )

    # Inicialización de los tres agentes con sus respectivas personalidades
    programador = AssistantAgent(
        name="DevExpert",
        llm_config={"config_list": config_list},
        system_message=ROLES["desarrollador"]["instrucciones"]
    )

    auditor = AssistantAgent(
        name="SecurityShadow",
        llm_config={"config_list": config_list},
        system_message=ROLES["auditor"]["instrucciones"]
    )

    juez = AssistantAgent(
        name="ChiefArchitect",
        llm_config={"config_list": config_list},
        system_message=ROLES["juez"]["instrucciones"]
    )

    # Gestión de la charla grupal (GroupChat)
    # Se limita a 6 rondas para optimizar el procesamiento local y evitar bucles.
    groupchat = GroupChat(
        agents=[admin, programador, auditor, juez], 
        messages=[], 
        max_round=6 
    )
    
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

    # Lanzamiento del flujo de trabajo multi-agente
    admin.initiate_chat(manager, message=pregunta_usuario)
