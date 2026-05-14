from __future__ import annotations

import logging

import ollama

from config import settings

logger = logging.getLogger("multiagent.llm")


def generar_respuesta(prompt: str) -> str:
    """
    Cliente centralizado para interacción con Ollama.
    """

    try:
        response = ollama.chat(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "num_gpu": NUM_GPU,
                "top_p": TOP_P,
                "temperature": DEFAULT_TEMP,
            }
        )

        contenido = response["message"]["content"]

        if not contenido:
            raise ValueError("Respuesta vacía del modelo.")

        return str(contenido)

    except Exception as e:
        logger.exception("Fallo crítico comunicando con Ollama")
        raise RuntimeError(f"Error LLM: {str(e)}") from e