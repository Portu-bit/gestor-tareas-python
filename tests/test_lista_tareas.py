import json

import pytest

from lista_tareas import ListaDeTareas
from tarea import Tarea


def test_add_task_persists_and_assigns_next_id(tmp_path):
    data_file = tmp_path / "tareas.json"
    tasks = ListaDeTareas(data_file)
    first = tasks.agregar("  Estudiar Python  ", "Practicar", "alta")
    second = tasks.agregar("Leer", prioridad="baja")

    reloaded = ListaDeTareas(data_file)
    assert first.id == 1
    assert first.titulo == "Estudiar Python"
    assert second.id == 2
    assert [task.titulo for task in reloaded.listar()] == ["Estudiar Python", "Leer"]


def test_complete_edit_delete_and_statistics(tmp_path):
    tasks = ListaDeTareas(tmp_path / "tareas.json")
    task = tasks.agregar("Proyecto", prioridad="alta")
    assert tasks.completar(task.id)
    assert tasks.editar(task.id, titulo="Proyecto terminado", descripcion="Listo")
    stats = tasks.estadisticas()
    assert stats["total"] == 1
    assert stats["completadas"] == 1
    assert stats["pendientes"] == 0
    assert tasks.eliminar(task.id)
    assert tasks.estadisticas()["total"] == 0


def test_filters_and_missing_ids(tmp_path):
    tasks = ListaDeTareas(tmp_path / "tareas.json")
    pending = tasks.agregar("Pendiente")
    done = tasks.agregar("Hecha")
    tasks.completar(done.id)
    assert [task.id for task in tasks.listar("pendientes")] == [pending.id]
    assert [task.id for task in tasks.listar("completadas")] == [done.id]
    assert not tasks.completar(999)
    assert not tasks.editar(999, titulo="No existe")
    assert not tasks.eliminar(999)


def test_invalid_task_data_is_rejected(tmp_path):
    tasks = ListaDeTareas(tmp_path / "tareas.json")
    with pytest.raises(ValueError):
        tasks.agregar("   ")
    with pytest.raises(ValueError):
        tasks.agregar("Tarea", prioridad="urgente")
    with pytest.raises(ValueError):
        tasks.editar(1, titulo=" ")


def test_corrupt_json_is_not_overwritten(tmp_path):
    data_file = tmp_path / "tareas.json"
    original = "{ archivo dañado"
    data_file.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError, match="JSON inválido"):
        ListaDeTareas(data_file)
    assert data_file.read_text(encoding="utf-8") == original


def test_duplicate_ids_are_rejected(tmp_path):
    data_file = tmp_path / "tareas.json"
    record = Tarea(1, "Tarea").to_dict()
    data_file.write_text(json.dumps([record, record]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicados"):
        ListaDeTareas(data_file)


def test_task_from_dict_validates_completion_flag():
    record = Tarea(1, "Tarea").to_dict()
    record["completada"] = "false"
    with pytest.raises(ValueError):
        Tarea.from_dict(record)
