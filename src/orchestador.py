
import autogen
from agents import ROLES

# --- CONFIGURACIÓN DE INFRAESTRUCTURA LLM ---
# Centralizamos la conexión con Ollama para garantizar la soberanía del dato.
# Se utiliza el modelo Llama 3 (8B) por su alta capacidad de razonamiento técnico.
config_list = [
    {
        "model": "llama3", 
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama", # Requerido por el estándar de AutoGen
    }
]

def iniciar_auditoria(pregunta_usuario):
    """
    Orquesta un debate técnico asíncrono entre agentes especializados.
    Utiliza el framework AutoGen para gestionar la confrontación de ideas.
    """

    # 1. AGENTE DE CONTROL (ADMIN): Representa al usuario y lanza el debate.
    admin = autogen.UserProxyAgent(
        name="Admin", 
        human_input_mode="NEVER", 
        code_execution_config=False,
        max_consecutive_auto_reply=1
    )

    # 2. AGENTE DESARROLLADOR (DEV): Genera la propuesta técnica inicial.
    programador = autogen.AssistantAgent(
        name="DevExpert",
        llm_config={"config_list": config_list},
        system_message=ROLES["desarrollador"]["instrucciones"]
    )

    # 3. AGENTE AUDITOR (SECURITY): Busca vulnerabilidades (Red Team).
    auditor = autogen.AssistantAgent(
        name="SecurityShadow",
        llm_config={"config_list": config_list},
        system_message=ROLES["auditor"]["instrucciones"]
    )

    # 4. AGENTE ARQUITECTO (JUDGE): Consolida la solución final segura.
    juez = autogen.AssistantAgent(
        name="ChiefArchitect",
        llm_config={"config_list": config_list},
        system_message=ROLES["juez"]["instrucciones"]
    )

    # --- LÓGICA DE GRUPO (MULTI-AGENT ORCHESTRATION) ---
    # Definimos un chat grupal para que los agentes interactúen dinámicamente.
    # El límite de 6 rondas previene bucles infinitos y optimiza la RAM local.
    groupchat = autogen.GroupChat(
        agents=[admin, programador, auditor, juez], 
        messages=[], 
        max_round=6 
    )
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat, 
        llm_config={"config_list": config_list}
    )

    # Iniciamos la sesión de auditoría con la entrada del usuario
    admin.initiate_chat(manager, message=pregunta_usuario)


