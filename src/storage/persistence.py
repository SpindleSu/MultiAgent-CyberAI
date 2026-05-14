from __future__ import annotations

from security.validator import validar_codigo_python

import logging
import os
import re
from typing import Final

logger = logging.getLogger("multiagent.persistence")

TOOLS_PATH: Final = os.path.join(
    "src",
    "generated",
    "tool_output.py"
)

def guardar_codigo_generado(texto_veredicto: str) -> None:
    """
    Extrae bloques de código de forma segura y los persiste.
    Mejora: Validación de seguridad antes de escribir en disco.
    """
    # Regex mejorada para capturar bloques de código con o sin nombre de lenguaje
    pattern = r"```(?:python|py)?\s*\n(.*?)\n```"
    match = re.search(pattern, texto_veredicto, re.DOTALL | re.IGNORECASE)
    
    if not match:
        logger.warning("No se detectó un bloque de código válido en el veredicto.")
        print("\n⚠️ [SISTEMA] No se detectó código funcional para persistir.")
        return

    codigo = match.group(1).strip()
    
        # --- VALIDACIÓN AST ---
    if not validar_codigo_python(codigo):
        print("\n[SEGURIDAD] Código bloqueado por validación AST.")
        logger.warning("Código bloqueado por AST validator.")
        return

    # --- SEGURIDAD DEFENSIVA ---
    # Evitamos que la IA guarde archivos vacíos o extremadamente peligrosos
    if len(codigo) < 10:
        print("\n⚠️ [SISTEMA] Código demasiado corto o inválido. Abortando guardado.")
        return

    # Verificación de palabras prohibidas (Blacklist básica)
    peligrosos = ["os.remove", "shutil.rmtree", "os.system('rm"]
    if any(p in codigo for p in peligrosos):
        logger.critical("INTENTO DE INYECCIÓN DE CÓDIGO MALICIOSO DETECTADO")
        print("\n❌ [SEGURIDAD] El código generado contiene comandos prohibidos. Bloqueado.")
        return

    try:
        # Aseguramos que el directorio exista
        os.makedirs(os.path.dirname(TOOLS_PATH), exist_ok=True)
        
        with open(TOOLS_PATH, "w", encoding="utf-8") as f:
            f.write("# Archivo generado automáticamente por Auditoría IA\n")
            f.write(f"# Fecha: {os.path.getmtime(TOOLS_PATH) if os.path.exists(TOOLS_PATH) else 'Nueva'}\n\n")
            f.write(codigo)
            
        print(f"\n💾 [SISTEMA] Código blindado persistido en: {TOOLS_PATH}")
        logger.info(f"Código guardado exitosamente en {TOOLS_PATH}")
    except IOError as e:
        logger.error(f"Error de E/S al guardar herramientas: {e}")
        print(f"\n⚠️ [SISTEMA] Error crítico al escribir archivo: {e}")