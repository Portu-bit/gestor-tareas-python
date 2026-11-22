import json
import os
import tempfile
from pathlib import Path
from typing import List

from tarea import Tarea


ARCHIVO_DATOS = Path(__file__).resolve().with_name("tareas.json")


class ListaDeTareas:
    """Gestiona tareas con persistencia JSON segura y atómica."""

    def __init__(self, archivo_datos=ARCHIVO_DATOS):
        self.archivo_datos = Path(archivo_datos)
        self.tareas: List[Tarea] = []
        self._siguiente_id = 1
        self.cargar()

    def cargar(self):
        """Carga tareas. Si el archivo está dañado, informa sin sobrescribirlo."""
        if not self.archivo_datos.exists():
            return

        try:
            with self.archivo_datos.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"El archivo {self.archivo_datos} contiene JSON inválido; "
                "no se modificó para proteger los datos."
            ) from exc

        if not isinstance(datos, list):
            raise ValueError("El archivo de tareas debe contener una lista JSON.")

        tareas = [Tarea.from_dict(item) for item in datos]
        ids = [tarea.id for tarea in tareas]
        if len(ids) != len(set(ids)):
            raise ValueError("El archivo contiene IDs de tarea duplicados.")

        self.tareas = tareas
        self._siguiente_id = max(ids, default=0) + 1

    def guardar(self):
        """Escribe primero un archivo temporal y reemplaza el JSON al terminar."""
        self.archivo_datos.parent.mkdir(parents=True, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.archivo_datos.parent,
                prefix=f".{self.archivo_datos.name}.",
                suffix=".tmp",
                delete=False,
            ) as archivo:
                temp_path = Path(archivo.name)
                json.dump(
                    [tarea.to_dict() for tarea in self.tareas],
                    archivo,
                    ensure_ascii=False,
                    indent=2,
                )
                archivo.flush()
                os.fsync(archivo.fileno())
            os.replace(temp_path, self.archivo_datos)
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()

    def agregar(self, titulo: str, descripcion: str = "", prioridad: str = "media") -> Tarea:
        tarea = Tarea(self._siguiente_id, titulo, descripcion, prioridad)
        self.tareas.append(tarea)
        try:
            self.guardar()
        except OSError:
            self.tareas.pop()
            raise
        self._siguiente_id += 1
        return tarea

    def completar(self, id: int) -> bool:
        tarea = self._buscar_por_id(id)
        if tarea is None:
            return False
        estado_anterior = tarea.completada
        tarea.completar()
        try:
            self.guardar()
        except OSError:
            tarea.completada = estado_anterior
            raise
        return True

    def eliminar(self, id: int) -> bool:
        tarea = self._buscar_por_id(id)
        if tarea is None:
            return False
        indice = self.tareas.index(tarea)
        self.tareas.pop(indice)
        try:
            self.guardar()
        except OSError:
            self.tareas.insert(indice, tarea)
            raise
        return True

    def editar(self, id: int, titulo: str = None, descripcion: str = None, prioridad: str = None) -> bool:
        tarea = self._buscar_por_id(id)
        if tarea is None:
            return False

        nuevos_valores = {}
        if titulo is not None:
            if not isinstance(titulo, str) or not titulo.strip():
                raise ValueError("El título no puede estar vacío.")
            nuevos_valores["titulo"] = titulo.strip()
        if descripcion is not None:
            if not isinstance(descripcion, str):
                raise ValueError("La descripción debe ser texto.")
            nuevos_valores["descripcion"] = descripcion.strip()
        if prioridad is not None:
            if prioridad not in Tarea.PRIORIDADES:
                raise ValueError(f"Prioridad inválida: {prioridad!r}.")
            nuevos_valores["prioridad"] = prioridad

        anteriores = {campo: getattr(tarea, campo) for campo in nuevos_valores}
        for campo, valor in nuevos_valores.items():
            setattr(tarea, campo, valor)
        try:
            self.guardar()
        except OSError:
            for campo, valor in anteriores.items():
                setattr(tarea, campo, valor)
            raise
        return True

    def listar(self, filtro: str = "todas") -> List[Tarea]:
        if filtro == "pendientes":
            return [tarea for tarea in self.tareas if not tarea.completada]
        if filtro == "completadas":
            return [tarea for tarea in self.tareas if tarea.completada]
        return list(self.tareas)

    def _buscar_por_id(self, id: int):
        return next((tarea for tarea in self.tareas if tarea.id == id), None)

    def detalle(self, id: int):
        return self._buscar_por_id(id)

    def estadisticas(self) -> dict:
        total = len(self.tareas)
        completadas = sum(1 for tarea in self.tareas if tarea.completada)
        return {
            "total": total,
            "completadas": completadas,
            "pendientes": total - completadas,
            "por_prioridad": {
                prioridad: sum(
                    1 for tarea in self.tareas
                    if tarea.prioridad == prioridad and not tarea.completada
                )
                for prioridad in Tarea.PRIORIDADES
            },
        }
