
import sys
import os

# --- ARQUITECTURA DE RUTAS (BLINDAJE SENIOR) ---
# Localizamos la ruta absoluta de la carpeta 'src' para evitar conflictos de importación.
# 'sys.path.insert(0, ...)' garantiza que el orquestador se localice antes que cualquier otro módulo.
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

try:
    # Importación absoluta optimizada para ejecución directa y futuro empaquetado (.exe)
    from orchestrator.engine import iniciar_auditoria

except ImportError as e:
    print(f"❌ Error crítico de arquitectura: No se pudo localizar el orquestador. {e}")
    sys.exit(1)

def ejecutar_consola():
    """
    Interfaz de línea de comandos (CLI) para la interacción con la Triada de Agentes.
    Gestiona el ciclo de vida de la consulta y el control de excepciones.
    """
    print("\n" + "█" * 60)
    print("🛡️  SISTEMA MULTI-AGENTE DE AUDITORÍA TÉCNICA (Llama 3 + AutoGen)")
    print("█" * 60)
    print("Enfoque: Ciberseguridad Defensiva y Programación Robusta.")
    print("Escribe 'salir' para finalizar la sesión.\n")

    while True:
        try:
            # Captura de la duda técnica o código a auditar
            pregunta = input("Consulta > ").strip()
            
            if not pregunta:
                continue

            if pregunta.lower() in ["salir", "exit", "q"]:
                print("\n[!] Cerrando el laboratorio. Auditoría finalizada.")
                break

            # Lanzamiento del debate entre DevExpert, SecurityShadow y ChiefArchitect
            iniciar_auditoria(pregunta)
            
            print("\n" + "─" * 60)
            print("Auditores en espera de la siguiente consulta...")
            
        except ConnectionError:
            print("\n❌ ERROR: Sin respuesta de Ollama. Asegúrate de que el servidor esté activo.")
        except KeyboardInterrupt:
            print("\n\n[!] Interrupción manual detectada. Saliendo de forma segura...")
            break
        except Exception as e:
            print(f"\n❌ ERROR INESPERADO: {e}")

if __name__ == "__main__":
    ejecutar_consola()


