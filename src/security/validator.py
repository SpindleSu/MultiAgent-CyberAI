import ast
import logging

logger = logging.getLogger("multiagent.security")

BANNED_IMPORTS = {
    "os",
    "subprocess",
    "socket",
    "shutil"
}

BANNED_FUNCTIONS = {
    "eval",
    "exec",
    "compile"
}

def validar_codigo_python(codigo: str) -> bool:
    """
    Analiza código Python usando AST y bloquea
    imports y funciones peligrosas.
    """

    try:
        tree = ast.parse(codigo)

    except SyntaxError:
        logger.warning("Código inválido detectado.")
        return False

    for node in ast.walk(tree):

        # Bloqueo de imports
        if isinstance(node, ast.Import):

            for name in node.names:
                if name.name in BANNED_IMPORTS:
                    logger.warning(f"Import peligroso: {name.name}")
                    return False

        # Bloqueo de from x import y
        elif isinstance(node, ast.ImportFrom):

            if node.module in BANNED_IMPORTS:
                logger.warning(f"ImportFrom peligroso: {node.module}")
                return False

        # Bloqueo de funciones peligrosas
        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id in BANNED_FUNCTIONS:
                    logger.warning(f"Función peligrosa: {node.func.id}")
                    return False

    return True