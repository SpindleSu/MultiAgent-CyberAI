import ollama
import time
import os
import re
from agents import obtener_roles

def guardar_codigo_generado(texto_veredicto):
    """Extrae el bloque de código del veredicto y lo guarda en src/tools.py"""
    # Busca bloques de código delimitados por ```python o simplemente ```
    match = re.search(r"```(?:python)?\n(.*?)\n```", texto_veredicto, re.DOTALL)
    if match:
        codigo = match.group(1)
        # Aseguramos que la ruta sea src/tools.py
        ruta = os.path.join("src", "tools.py")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(codigo)
            print(f"\n💾 [SISTEMA] Código blindado extraído y guardado en: {ruta}")
        except Exception as e:
            print(f"\n⚠️ [SISTEMA] Error al escribir el archivo: {e}")
    else:
        print("\n⚠️ [SISTEMA] No se detectó un bloque de código final para persistir.")

def llamar_a_llama(rol, contexto, consulta):
    """Conecta con Llama 3 pasándole la personalidad del agente."""
    prompt = (
        f"Actúa como: {rol['nombre']}\n"
        f"Instrucciones: {rol['instrucciones']}\n"
        f"Contexto actual: {contexto}\n"
        f"Petición del usuario: {consulta}\n"
        f"Responde de forma concisa y técnica en español."
    )
    
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error conectando con Ollama: {e}"

def iniciar_auditoria(consulta):
    roles = obtener_roles()
    
    # 1. El Desarrollador propone el código
    print(f"\n👨‍💻 [{roles['desarrollador']['nombre']}] generando solución técnica...")
    propuesta = llamar_a_llama(roles['desarrollador'], "Eres el primero en intervenir.", consulta)
    print(f"--- PROPUESTA ---\n{propuesta}\n-----------------")

    # 2. El Auditor busca fallos
    print(f"\n🕵️ [{roles['auditor']['nombre']}] ejecutando auditoría de seguridad...")
    critica = llamar_a_llama(roles['auditor'], f"Debes auditar este código: {propuesta}", consulta)
    print(f"--- ANÁLISIS DE RIESGOS ---\n{critica}\n---------------------------")

    # 3. El Juez dicta sentencia y revisa
    print(f"\n⚖️  [{roles['juez']['nombre']}] evaluando veredicto y blindando código...")
    contexto_final = (
        f"Debate previo: Dev propuso {propuesta} y Auditor criticó {critica}. "
        "Asegúrate de incluir todos los imports y aplicar Whitelist de comandos."
    )
    veredicto = llamar_a_llama(roles['juez'], contexto_final, consulta)
    print(f"--- SOLUCIÓN FINAL ROBUSTA ---\n{veredicto}\n-----------------------")

    # 4. Persistencia automática
    guardar_codigo_generado(veredicto)
