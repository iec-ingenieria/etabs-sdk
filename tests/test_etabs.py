"""Tests para clase Etabs."""
from pathlib import Path

import pytest

from etabs_sdk import Etabs
from etabs_sdk.excepciones import ModeloNoEncontradoError


def test_iniciar_modelo() -> None:
    """Test."""
    etabs = Etabs(path=None, modelo_nuevo=True, cerrar_intancia_abierta=False)
    assert etabs.model is not None
    etabs.cerrar_modelo(guardar=False)


def test_error_modelo_no_encontrado() -> None:
    """Test."""
    with pytest.raises(ModeloNoEncontradoError):
        Etabs(path=Path("ruta/incorrecta/al/modelo"))
