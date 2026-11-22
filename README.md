# Gestor de tareas en Python

Aplicación de consola para administrar tareas con título, descripción, prioridad y estado.

## Funcionalidades
- Crear, listar, editar, completar y eliminar tareas.
- Filtrar tareas pendientes y completadas.
- Consultar estadísticas generales y por prioridad.
- Guardar los datos en un archivo JSON local.

## Requisitos
Python 3.10 o superior. No requiere dependencias externas.

## Ejecutar
```bash
python main.py
```

El archivo `tareas.json` se crea junto a los módulos del proyecto, independientemente de la carpeta desde la que se ejecute el programa. Está excluido de Git para no publicar tareas personales.

La escritura del JSON es atómica para reducir el riesgo de perder datos si el proceso se interrumpe. Si el archivo está dañado, el programa informa del problema y no lo sobrescribe automáticamente.

## Pruebas
```bash
python -m pip install pytest
python -m pytest -q
```
