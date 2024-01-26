"""Etabs api."""
import contextlib
from pathlib import Path
from typing import Any, Literal

import comtypes
import comtypes.client

from .enums import Unidades
from .excepciones import InstanciaActivaNoEncontradaError, ModeloNoEncontradoError, NuevoModeloError

UnidadLiteral = Literal[
    "LB_IN_F",
    "LB_FT_F",
    "KIP_IN_F",
    "KIP_FT_F",
    "KN_MM_C",
    "KN_M_C",
    "KGF_MM_C",
    "KGF_M_C",
    "N_MM_C",
    "N_M_C",
    "TON_MM_C",
    "TON_M_C",
    "KN_CM_C",
    "KGF_CM_C",
    "N_CM_C",
    "TON_CM_C",
]


class Etabs:
    """Maneja la comunicación con la API de Etabs."""

    def __init__(
        self, path: Path | None = None, modelo_nuevo: bool = False, cerrar_intancia_abierta: bool = True
    ) -> None:
        """Método init para la case Etabs."""
        self.path = path
        self.etabs_object = self._conectar_etabs(modelo_nuevo, cerrar_intancia_abierta)
        self.model = self.etabs_object.SapModel

        if modelo_nuevo:
            self.iniciar_modelo("TON_M_C")

        self.unidades_del_modelo("TON_M_C")

    def _conectar_etabs(self, modelo_nuevo: bool, cerrar_instancia_abierta: bool) -> Any:
        """Conectar al modelo indicado o a la instancia activa."""
        if cerrar_instancia_abierta:
            with contextlib.suppress(OSError, comtypes.COMError):
                etabs_object = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
                if etabs_object is not None:
                    etabs_object.ApplicationExit(True)

        helper = comtypes.client.CreateObject("ETABSv1.Helper")
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        if self.path:
            try:
                return helper.CreateObject(self.path)
            except Exception as error:
                raise ModeloNoEncontradoError(self.path, error) from error

        elif modelo_nuevo:
            return helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")

        try:
            return comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        except Exception as error:
            raise InstanciaActivaNoEncontradaError(error) from error

    def unidades_del_modelo(self, unidad: UnidadLiteral) -> None:
        """Configura las unidades internas del modelo."""
        try:
            self.model.SetPresentUnits(Unidades[unidad].value)
        except KeyError as error:
            raise ValueError(f"Unidad '{unidad}' no es válida.") from error

    def iniciar_modelo(self, unidad: UnidadLiteral) -> None:
        """Inicial el modelo nuevo."""
        try:
            self.etabs_object.ApplicationStart()
            self.model.InitializeNewModel(Unidades[unidad].value)
            self.model.File.NewBlank()
        except Exception as error:
            raise NuevoModeloError(error) from error

    def cerrar_modelo(self, guardar: bool = True) -> None:
        """Cerrar modelo."""
        self.etabs_object.ApplicationExit(guardar)  # llave true es para guardar antes de salir
