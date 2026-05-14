from __future__ import annotations

import logging
import sys
import re  # Para saneamiento de entrada
from typing import Optional, Final

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import settings
from engine import iniciar_auditoria
from logger import setup_logging

# --- CONFIGURACIÓN Y CONSTANTES ---
setup_logging()
logger = logging.getLogger("multiagent.cli")
console = Console()

# Constantes para evitar números mágicos
EXIT_COMMANDS: Final = {"salir", "exit", "quit", "q"}
MIN_INPUT_LENGTH: Final = 3


class CLIException(Exception):
    """Excepción base para errores controlados de la interfaz."""
    pass


def sanear_entrada(texto: str) -> str:
    """
    Limpia la entrada para evitar caracteres de control o inyecciones básicas.
    Seguridad defensiva: Solo permite caracteres alfanuméricos y puntuación básica.
    """
    # Eliminamos caracteres no deseados (ej. caracteres de control de terminal)
    # Solo permitimos letras, números, espacios y puntuación común
    return re.sub(r'[^\w\s.,?!\-]', '', texto)


def validar_entrada(pregunta: Optional[str]) -> str:
    """
    Valida y normaliza la entrada del usuario con enfoque en seguridad.
    """
    if not pregunta or not pregunta.strip():
        raise CLIException("La consulta no puede estar vacía.")

    entrada = pregunta.strip()
    
    # Verificación de salida inmediata
    if entrada.lower() in EXIT_COMMANDS:
        raise CLIException("Cierre solicitado")

    # Saneamiento de caracteres peligrosos
    entrada = sanear_entrada(entrada)

    # Validación de longitud mínima y máxima
    if len(entrada) < MIN_INPUT_LENGTH:
        raise CLIException(f"Consulta demasiado corta. Mínimo {MIN_INPUT_LENGTH} caracteres.")
        
    if len(entrada) > settings.MAX_INPUT_LENGTH:
        raise CLIException(
            f"Consulta demasiado extensa (Máximo: {settings.MAX_INPUT_LENGTH})."
        )
        
    return entrada


def mostrar_banner() -> None:
    """Muestra el banner de identidad del sistema."""
    banner = Panel.fit(
        "[bold cyan]🛡️  SISTEMA MULTI-AGENTE DE AUDITORÍA[/bold cyan]\n"
        "[dim]Seguridad Defensiva | Análisis de Código | IA Offline[/dim]\n\n"
        "[yellow]Comando:[/yellow] Escribe 'salir' para finalizar",
        title="[bold green]Laboratorio v1.0[/bold green]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(banner)


def ejecutar_auditoria_con_progreso(consulta: str) -> None:
    """Encapsula la ejecución de la auditoría con manejo de progreso."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True  # El progreso desaparece al terminar para limpiar la pantalla
    ) as progress:
        task = progress.add_task("[cyan]Analizando vectores de ataque...", total=None)
        
        try:
            # La lógica pesada ocurre aquí
            iniciar_auditoria(consulta)
            progress.update(task, completed=True)
        except Exception as e:
            logger.error(f"Fallo en motor de auditoría: {e}")
            raise CLIException(f"Error en el motor: {str(e)}")


def ejecutar_consola() -> None:
    """Bucle principal de la CLI con manejo robusto de estados."""
    mostrar_banner()
    
    while True:
        try:
            # Mejoramos questionary para que no falle si el usuario cancela (Ctrl+C)
            pregunta = questionary.text(
                "🔍 Consulta de seguridad:",
                qmark=">",
                instruction="(Escribe 'salir' para terminar)"
            ).ask()

            # Manejo de Ctrl+C o salida nula en questionary
            if pregunta is None:
                raise KeyboardInterrupt

            entrada_validada = validar_entrada(pregunta)
            
            logger.info(f"Sesión activa: Iniciando análisis para '{entrada_validada[:20]}...'")
            ejecutar_auditoria_con_progreso(entrada_validada)
            
            console.print("\n" + "[dim]─" * 50 + "[/dim]")
            console.print("[bold green]✓[/bold green] [dim]Auditoría completada. Esperando nueva orden...[/dim]\n")
            
        except CLIException as e:
            mensaje = str(e)
            if "Cierre solicitado" in mensaje:
                console.print("\n[yellow]👋 Cerrando sesión de auditoría de forma segura...[/yellow]")
                break
            console.print(f"[bold red]⚠️  Entrada no válida:[/bold red] {mensaje}")
                
        except ConnectionError:
            logger.error("Servicio LLM (Ollama) no detectado")
            console.print("\n[bold red]❌ ERROR DE CONEXIÓN:[/bold red] Ollama no responde.")
            console.print("[yellow]Verifica que el servicio esté activo y el modelo cargado.[/yellow]\n")
            
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]⚠️  Interrupción detectada. Finalizando procesos...[/bold yellow]")
            break
        except Exception:
            logger.exception("Excepción no controlada en el bucle principal")
            console.print("\n[bold red]❌ ERROR INTERNO DEL SISTEMA[/bold red]")
            console.print("[dim]Consulta logs/cli.log para detalles técnicos[/dim]\n")


def main() -> int:
    """Punto de entrada con gestión de códigos de salida del sistema."""
    try:
        ejecutar_consola()
        return 0
    except Exception as e:
        logger.critical(f"Fallo catastrófico: {e}", exc_info=True)
        console.print("\n[bold white on red] FATAL ERROR [/bold white on red]")
        console.print(f"[red]{str(e)}[/red]")
        return 1


if __name__ == "__main__":
    # Aseguramos que la codificación de salida sea UTF-8 para iconos de Rich
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    sys.exit(main())
