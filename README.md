# 🛡️ Sistema Multi-Agente de Auditoría Técnica (Llama 3 + Local LLM)

Este repositorio alberga un framework de **orquestación de agentes de IA** especializado en auditoría automatizada y hardening de código para entornos de ciberseguridad.

## 🚀 Arquitectura: Tríada de Confrontación
El sistema no solo genera código; ejecuta un proceso de **Code Review** dialéctico antes de entregar una solución:

*   **👨‍💻 DevExpert:** Programador Senior enfocado en funcionalidad, limpieza y eficiencia del código Python.
*   **🕵️ SecurityShadow:** Auditor con mentalidad *Red Team*. Su misión es el "breaking code", detectando RCE, inyecciones y fugas de información.
*   **⚖️ ChiefArchitect:** Juez de infraestructura que arbitra el debate y entrega una **solución final blindada** con persistencia automática en disco.

## 🛠️ Innovación y Blindaje Técnico
*   **Soberanía del Dato:** Ejecución 100% local mediante **Ollama**, garantizando que la lógica de negocio y las vulnerabilidades nunca salgan del entorno controlado.
*   **Gestión de Secretos:** Integración con `python-dotenv` y `getpass` para evitar la exposición de credenciales en el código fuente.
*   **Persistencia Inteligente:** El sistema extrae automáticamente el código validado y lo guarda en `src/tools.py` para su uso inmediato.
*   **Optimización de Recursos:** Configurado para funcionar en entornos con limitaciones de VRAM mediante descarga a RAM sistémica.

## 📦 Instalación y Despliegue

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd Orquestación-Multi-Agente
   ```

2. **Configurar el entorno virtual:**
   ```bash
   python -m venv venv
   .\(\venv\Scripts\Activate.\)ps1
   pip install -r requirements.txt
   ```

3. **Preparar el motor de IA (Ollama):**
   ```bash
   ollama pull llama3
   ```

4. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz con tus parámetros de conexión (opcional para ejecución dinámica).

## 🖥️ Uso
Ejecuta el orquestador principal:
```bash
python src/main.py

## 📝 Últimas Mejoras (v2.0)
- **Hardening de Agentes:** Se añadieron instrucciones de "Whitelist" y validación de comandos para evitar inyecciones (RCE).
- **Persistencia Automática:** El orquestador ahora extrae el código del veredicto final y lo guarda dinámicamente en `src/tools.py` mediante Regex.
- **Gestión de Secretos Dinámica:** Integración de `getpass` e `input` interactivo para manejar credenciales SSH sin almacenarlas en disco.
- **Optimización de Ejecución:** Refactorización de las rutas de sistema (`sys.path`) para garantizar la portabilidad del módulo `orchestrator`.
- **Compatibilidad de Hardware:** Configuración documentada para ejecución en RAM (CPU) evitando errores de memoria en GPUs con menos de 4GB (GTX 1050).

```
## 🚀 Actualizaciones Recientes (v2.1)

### Optimización de Infraestructura y Lógica
- **Compatibilidad Universal de Hardware:** Implementación de inferencia forzada en **CPU/RAM** (`num_gpu: 0`) para evitar bloqueos por falta de VRAM en equipos con GPUs limitadas.
- **Auditoría de Código Pragmática:** Refactorización del rol del **Juez (ChiefArchitect)** para priorizar la ejecución inmediata, eliminando validaciones de integridad (hashes) que causaban bucles de error.
- **Persistencia de Scripts de Alta Integridad:** Mejora en el motor de extracción para asegurar que `src/tools.py` reciba scripts 100% autocontenidos y funcionales.
- **Seguridad de Archivos:** Saneamiento de rutas para mitigar riesgos de *Path Traversal* en las herramientas generadas.

---
*Enfoque: Ciberseguridad Defensiva y Programación Robusta.*


---

> [!IMPORTANT]
> **Aviso Legal y Uso Ético**
>
> Este proyecto ha sido desarrollado exclusivamente con **fines didácticos y de investigación**. El autor no se hace responsable del uso indebido, ilegal o malintencionado de este código. 
> 
> Queda estrictamente prohibido su uso en actividades que vulneren la privacidad de terceros o la seguridad de sistemas sin autorización expresa. Al utilizar este repositorio, el usuario acepta que es el único responsable de cumplir con la legislación vigente.

Este proyecto está bajo la licencia [MIT](LICENSE).

