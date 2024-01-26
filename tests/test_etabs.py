"""Tests para clase Etabs."""
from pathlib import Path

import pytest

from etabs_sdk import Etabs
from etabs_sdk.enums import Unidades
from etabs_sdk.excepciones import ModeloNoEncontradoError


@pytest.fixture(scope="module")
def etabs_fixture() -> None:
    """Fixture para crear y cerrar un objeto Etabs."""
    etabs = Etabs(path=None, modelo_nuevo=True, cerrar_intancia_abierta=True)
    yield etabs
    etabs.cerrar_modelo(guardar=False)


def test_iniciar_modelo(etabs_fixture: Etabs) -> None:
    """Test."""
    assert etabs_fixture.model is not None


def test_set_unidades(etabs_fixture: Etabs) -> None:
    """Test."""
    assert etabs_fixture.model.GetPresentUnits() == Unidades.TON_M_C.value
    etabs_fixture.unidades_del_modelo("KGF_CM_C")
    assert etabs_fixture.model.GetPresentUnits() == Unidades.KGF_CM_C.value


def test_error_modelo_no_encontrado() -> None:
    """Test."""
    with pytest.raises(ModeloNoEncontradoError):
        Etabs(path=Path("ruta/incorrecta/al/modelo"))
