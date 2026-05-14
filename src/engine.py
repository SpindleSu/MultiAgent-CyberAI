from __future__ import annotations

import logging
from security.validator import validar_codigo_python
from typing import Dict, Any
from core.code_extractor import extraer_codigo
from dotenv import load_dotenv

from agents import obtener_roles
from core.llm import generar_respuesta
from storage.persistence import guardar_codigo_generado


# --- CONFIGURACIÓN ---
load_dotenv()

logger = logging.getLogger("multiagent.engine")


def construir_prompt(
    rol: Dict[str, str],
    contexto: str,
    consulta: str
) -> str:
    """
    Construye prompts estandarizados para el pipeline.
    """

    return (
        f"CONTEXTO DE ROL:\n{rol['instrucciones']}\n\n"
        f"HISTORIAL: {contexto}\n\n"
        f"TAREA ACTUAL: {consulta}\n\n"
        "RESPUESTA TÉCNICA EN ESPAÑOL:"
    )


def iniciar_auditoria(consulta: str) -> None:
    """
    Orquestador del flujo de trabajo multi-agente.
    """

    roles = obtener_roles()

    # =========================================================
    # FASE 1 — GENERACIÓN
    # =========================================================

    print(f"\n👨‍💻 [{roles['desarrollador']['nombre']}] Generando arquitectura...")

    prompt_propuesta = construir_prompt(
        roles['desarrollador'],
        "Inicio de cadena de mando.",
        consulta
    )

    try:
        propuesta = generar_respuesta(prompt_propuesta)

    except RuntimeError as e:
        logger.error(f"Abortando pipeline: {e}")
        return

    print(f"--- PROPUESTA ---\n{propuesta[:500]}...\n")

    # =========================================================
    # FASE 2 — AUDITORÍA
    # =========================================================

    print(f"\n🕵️ [{roles['auditor']['nombre']}] Analizando vulnerabilidades...")

    prompt_auditoria = construir_prompt(
        roles['auditor'],
        f"Audita rigurosamente esta propuesta: {propuesta}",
        consulta
    )

    try:
        critica = generar_respuesta(prompt_auditoria)

    except RuntimeError as e:
        logger.error(f"Abortando pipeline: {e}")
        return

    print(f"--- ANÁLISIS DE RIESGOS ---\n{critica}\n")

    # =========================================================
    # FASE 3 — VEREDICTO FINAL
    # =========================================================

    print(f"\n⚖️ [{roles['juez']['nombre']}] Consolidando solución final...")

    contexto_final = (
        f"Entrada original: {consulta}\n"
        f"Propuesta previa: {propuesta}\n"
        f"Crítica técnica: {critica}"
    )

    prompt_veredicto = construir_prompt(
        roles['juez'],
        contexto_final,
        "Genera el código final blindado."
    )

    try:
        veredicto = generar_respuesta(prompt_veredicto)

    except RuntimeError as e:
        logger.error(f"Abortando pipeline: {e}")
        return

    print(f"--- SOLUCIÓN FINAL ---\n{veredicto}\n")

    # =========================================================
    # FASE 4 — PERSISTENCIA
    # =========================================================

    codigo_final = extraer_codigo(veredicto)

    if not validar_codigo_python(codigo_final):
        logger.error("Código bloqueado por validación AST.")
        return

    guardar_codigo_generado(codigo_final)
