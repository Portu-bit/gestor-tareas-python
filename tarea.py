from datetime import datetime


class Tarea:
    """Representa una tarea individual."""

    PRIORIDADES = ["alta", "media", "baja"]

    def __init__(self, id: int, titulo: str, descripcion: str = "", prioridad: str = "media"):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad if prioridad in self.PRIORIDADES else "media"
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
        tarea = cls(
            id=datos["id"],
            titulo=datos["titulo"],
            descripcion=datos.get("descripcion", ""),
            prioridad=datos.get("prioridad", "media"),
        )
        tarea.completada = datos.get("completada", False)
        tarea.fecha_creacion = datos.get("fecha_creacion", "")
        return tarea

    def __str__(self) -> str:
        estado = "✔" if self.completada else "○"
        iconos = {"alta": "🔴", "media": "🟡", "baja": "🟢"}
        icono = iconos.get(self.prioridad, "⚪")
        return f"[{estado}] #{self.id} {icono} {self.titulo} ({self.prioridad})"