import json
import os
from typing import List
from tarea import Tarea


ARCHIVO_DATOS = "tareas.json"


class ListaDeTareas:
    """Gestiona una colección de tareas con persistencia en JSON."""

    def __init__(self):
        self.tareas: List[Tarea] = []
        self._siguiente_id = 1
        self.cargar()

    # ── Persistencia ──────────────────────────────────────────────────────────

    def cargar(self):
        """Carga las tareas desde el archivo JSON."""
        if not os.path.exists(ARCHIVO_DATOS):
            return
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.tareas = [Tarea.from_dict(t) for t in datos]
            if self.tareas:
                self._siguiente_id = max(t.id for t in self.tareas) + 1
        except (json.JSONDecodeError, KeyError):
            print("⚠️  No se pudo cargar el archivo de tareas. Empezando en blanco.")

    def guardar(self):
        """Guarda las tareas en el archivo JSON."""
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tareas], f, ensure_ascii=False, indent=2)

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def agregar(self, titulo: str, descripcion: str = "", prioridad: str = "media") -> Tarea:
        tarea = Tarea(self._siguiente_id, titulo, descripcion, prioridad)
        self.tareas.append(tarea)
        self._siguiente_id += 1
        self.guardar()
        return tarea

    def completar(self, id: int) -> bool:
        tarea = self._buscar_por_id(id)
        if tarea:
            tarea.completar()
            self.guardar()
            return True
        return False

    def eliminar(self, id: int) -> bool:
        tarea = self._buscar_por_id(id)
        if tarea:
            self.tareas.remove(tarea)
            self.guardar()
            return True
        return False

    def editar(self, id: int, titulo: str = None, descripcion: str = None, prioridad: str = None) -> bool:
        tarea = self._buscar_por_id(id)
        if not tarea:
            return False
        if titulo:
            tarea.titulo = titulo
        if descripcion is not None:
            tarea.descripcion = descripcion
        if prioridad and prioridad in Tarea.PRIORIDADES:
            tarea.prioridad = prioridad
        self.guardar()
        return True

    # ── Consultas ─────────────────────────────────────────────────────────────

    def listar(self, filtro: str = "todas") -> List[Tarea]:
        if filtro == "pendientes":
            return [t for t in self.tareas if not t.completada]
        if filtro == "completadas":
            return [t for t in self.tareas if t.completada]
        return self.tareas

    def _buscar_por_id(self, id: int):
        return next((t for t in self.tareas if t.id == id), None)

    def detalle(self, id: int):
        return self._buscar_por_id(id)

    # ── Estadísticas ──────────────────────────────────────────────────────────

    def estadisticas(self) -> dict:
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t.completada)
        return {
            "total": total,
            "completadas": completadas,
            "pendientes": total - completadas,
            "por_prioridad": {
                p: sum(1 for t in self.tareas if t.prioridad == p and not t.completada)
                for p in Tarea.PRIORIDADES
            },
        }