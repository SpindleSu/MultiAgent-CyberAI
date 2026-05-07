import ollama
import time
import os
import re
from agents import obtener_roles

def guardar_codigo_generado(texto_veredicto):
    """Extrae el bloque de código del veredicto y lo guarda en src/tools.py"""
    match = re.search(r"```(?:python)?\n(.*?)\n```", texto_veredicto, re.DOTALL)
    if match:
        codigo = match.group(1)
        ruta = os.path.join("src", "tools.py")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(codigo)
            print(f"\n💾 [SISTEMA] Código blindado extraído y guardado en: {ruta}")
        except Exception as e:
            print(f"\n⚠️ [SISTEMA] Error al escribir el archivo: {e}")
    else:
        print("\n⚠️ [SISTEMA] No se detectó un bloque de código completo para persistir.")

def llamar_a_llama(rol, contexto, consulta):
    """Conecta con Llama 3 forzando el uso de CPU/RAM para estabilidad."""
    prompt = (
        f"Actúa como: {rol['nombre']}\n"
        f"Instrucciones: {rol['instrucciones']}\n"
        f"Contexto actual: {contexto}\n"
        f"Petición del usuario: {consulta}\n"
        f"Responde de forma concisa y técnica en español."
    )
    
    try:
        # Configuración forzada para evitar errores de CUDA en GPUs de 2GB
        response = ollama.chat(
            model='llama3', 
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'num_gpu': 0  # <--- FUERZA USO DE RAM (CPU) SIEMPRE
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"Error conectando con Ollama: {e}"

def iniciar_auditoria(consulta):
    roles = obtener_roles()
    
    # 1. Desarrollo
    print(f"\n👨‍💻 [{roles['desarrollador']['nombre']}] generando solución técnica...")
    propuesta = llamar_a_llama(roles['desarrollador'], "Eres el primero en intervenir.", consulta)
    print(f"--- PROPUESTA ---\n{propuesta}\n-----------------")

    # 2. Auditoría
    print(f"\n🕵️ [{roles['auditor']['nombre']}] ejecutando auditoría de seguridad...")
    critica = llamar_a_llama(roles['auditor'], f"Debes auditar este código: {propuesta}", consulta)
    print(f"--- ANÁLISIS DE RIESGOS ---\n{critica}\n---------------------------")

    # 3. Veredicto y Blindaje
    print(f"\n⚖️  [{roles['juez']['nombre']}] evaluando veredicto y blindando código...")
    contexto_final = (
        f"Debate previo: Dev propuso {propuesta} y Auditor criticó {critica}. "
        "Genera un código ÚNICO, COMPLETO y sin verificaciones de hash innecesarias."
    )
    veredicto = llamar_a_llama(roles['juez'], contexto_final, consulta)
    print(f"--- SOLUCIÓN FINAL ROBUSTA ---\n{veredicto}\n-----------------------")

    # 4. Persistencia automática
    guardar_codigo_generado(veredicto)

