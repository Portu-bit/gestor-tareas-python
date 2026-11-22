from datetime import datetime


class Tarea:
    """Representa una tarea individual."""

    PRIORIDADES = ("alta", "media", "baja")

    def __init__(
        self,
        id: int,
        titulo: str,
        descripcion: str = "",
        prioridad: str = "media",
    ):
        if isinstance(id, bool) or not isinstance(id, int) or id < 1:
            raise ValueError("El ID debe ser un entero positivo.")
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        if not isinstance(descripcion, str):
            raise ValueError("La descripción debe ser texto.")
        if prioridad not in self.PRIORIDADES:
            raise ValueError(f"Prioridad inválida: {prioridad!r}.")

        self.id = id
        self.titulo = titulo.strip()
        self.descripcion = descripcion.strip()
        self.prioridad = prioridad
        self.completada = False
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M")

    def completar(self):
        self.completada = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "completada": self.completada,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Tarea":
        if not isinstance(datos, dict):
            raise ValueError("Cada tarea guardada debe ser un objeto JSON.")
        tarea = cls(
            id=datos.get("id"),
            titulo=datos.get("titulo"),
            descripcion=datos.get("descripcion", ""),
            prioridad=datos.get("prioridad", "media"),
        )
        completada = datos.get("completada", False)
        if not isinstance(completada, bool):
            raise ValueError("El estado de la tarea debe ser verdadero o falso.")
        fecha = datos.get("fecha_creacion", "")
        if not isinstance(fecha, str):
            raise ValueError("La fecha de creación debe ser texto.")
        tarea.completada = completada
        tarea.fecha_creacion = fecha
        return tarea

    def __str__(self) -> str:
        estado = "✔" if self.completada else "○"
        iconos = {"alta": "🔴", "media": "🟡", "baja": "🟢"}
        return f"[{estado}] #{self.id} {iconos[self.prioridad]} {self.titulo} ({self.prioridad})"
