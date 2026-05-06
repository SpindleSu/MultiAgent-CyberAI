# src/main.py
from orchestrator import iniciar_auditoria

def ejecutar_consola():
    """
    Punto de entrada principal para la interfaz de usuario.
    Permite realizar consultas de forma iterativa.
    """
    print("\n" + "="*60)
    print("🛡️  SISTEMA MULTI-AGENTE DE AUDITORÍA TÉCNICA")
    print("="*60)
    print("Ingresa tu duda de programación o ciberseguridad.")
    print("(Escribe 'salir' para finalizar el programa)\n")

    while True:
        try:
            pregunta = input("Consulta > ")
            
            if pregunta.lower() in ["salir", "exit", "q"]:
                print("\nCerrando el auditor. Hasta pronto.")
                break
            
            if not pregunta.strip():
                continue

            # Iniciamos el flujo de los 3 agentes (Dev, Security, Architect)
            iniciar_auditoria(pregunta)
            
            print("\n" + "-"*60)
            print("Auditoría finalizada. Esperando nueva consulta...")
            
        except ConnectionError:
            print("\n❌ Error: No se pudo conectar con Ollama. Asegúrate de que el servidor esté activo.")
        except KeyboardInterrupt:
            print("\n\nInterrupción detectada. Saliendo...")
            break

if __name__ == "__main__":
    ejecutar_consola()
