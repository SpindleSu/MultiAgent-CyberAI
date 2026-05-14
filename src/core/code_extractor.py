import re


def extraer_codigo(texto: str) -> str:
    """
    Extrae bloques de código Markdown.
    """

    bloques = re.findall(
        r"```(?:python)?\n(.*?)```",
        texto,
        re.DOTALL
    )

    if bloques:
        return "\n\n".join(bloques)

    return texto.strip()