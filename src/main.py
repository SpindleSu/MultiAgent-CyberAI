
import sys
import os

# --- LÓGICA DE RUTAS (BOILERPLATE PROFESIONAL) ---
# Añadimos la carpeta 'src' al path de búsqueda para que Python
# encuentre los módulos internos independientemente de dónde se ejecute.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importación absoluta una vez configurado el entorno
from orchestrator import iniciar_auditoria

def ejecutar_consola():
    """
    Interfaz de línea de comandos para interactuar con el sistema de auditoría.
    """
    print("\n" + "="*60)
    print("🛡️  SISTEMA MULTI-AGENTE DE AUDITORÍA TÉCNICA (Python/Sec)")
    print("="*60)
    print("Ingresa tu duda técnica (o escribe 'salir' para finalizar).")
    print("-"*60 + "\n")

    while True:
        try:
            pregunta = input("Consulta > ")
            
            if pregunta.lower() in ["salir", "exit", "q"]:
                print("\nCerrando el auditor. Sesión finalizada.")
                break
            
            if not pregunta.strip():
                continue

            # Disparo del orquestador multi-agente
            iniciar_auditoria(pregunta)
            
            print("\n" + "-"*60)
            print("Esperando nueva consulta...")
            
        except ConnectionError:
            print("\n❌ Error: No se pudo conectar con Ollama. Verifica que el servidor esté activo.")
        except Exception as e:
            print(f"\n❌ Se produjo un error inesperado: {e}")
        except KeyboardInterrupt:
            print("\n\nInterrupción manual detectada. Saliendo...")
            break

if __name__ == "__main__":
    ejecutar_consola()
