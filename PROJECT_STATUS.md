# Estado actual del refactor

## Arquitectura nueva creada

src/
├── core/
├── generated/
├── security/
├── storage/

## Refactors completados

- Separada persistencia fuera de engine.py
- Creado storage/persistence.py
- Creado generated/tool_output.py
- Imports modulares funcionando
- VS Code limpiado (.venv oculto)

## Pendiente

- Crear security/validator.py
- Integrar validación AST
- Extraer llamadas LLM a llm.py
- Mejorar configuración centralizada
- Hardening de ejecución

# Estado actual del refactor — Última sesión

## Refactors completados

### Arquitectura modular inicial
- Creadas carpetas:
  - `core/`
  - `security/`
  - `storage/`
  - `generated/`

### Modularización
- Creado `storage/persistence.py`
- Movida función `guardar_codigo_generado()` fuera de `engine.py`
- Import modular funcionando:
  - `from storage.persistence import guardar_codigo_generado`

### Seguridad
- Creado `security/validator.py`
- Implementada validación AST real usando:
  - `ast.parse()`
  - bloqueo de imports peligrosos
  - bloqueo de `eval`, `exec`, `compile`

### Pipeline defensivo
Flujo actual:

LLM Generation
→ extracción de código
→ validación AST
→ persistencia segura

### Persistencia segura
- Ya NO se sobrescribe `tools.py`
- Nuevo destino:
  - `src/generated/tool_output.py`

### VS Code
- Ocultados:
  - `.venv`
  - `__pycache__`
  - `.pyc`

## Estado funcional

✅ Proyecto arranca correctamente

Comando probado:

python src/main.py

✅ Refactor modular funcionando

## Problema detectado

Error Ollama:

model requires more system memory than is available

El pipeline sigue vivo pero el modelo actual consume demasiada RAM.

## Próximo paso al continuar

1. Ejecutar:
   ollama list

2. Elegir modelo más ligero:
   - phi3:mini
   - gemma3:1b
   - u otro disponible

3. Mejorar manejo de errores LLM:
   - abortar pipeline cuando falle Ollama

4. Siguiente evolución arquitectónica:
   - extraer `llm.py`
   - separar llamadas IA del engine