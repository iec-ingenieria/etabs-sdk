"""Módulo para excepciones personalizadas."""
from pathlib import Path


class ModeloNoEncontradoError(Exception):
    """Excepción lanzada cuando no se puede encontrar o abrir el modelo de ETABS."""

    def __init__(self, path: Path, error: Exception, message: str = "Modelo no encontrado o no se pudo abrir"):
        """Método init."""
        self.path = path
        self.message = f"{message}: {path}. Causa: {error}"
        super().__init__(self.message)


class InstanciaActivaNoEncontradaError(Exception):
    """Excepción lanzada cuando no se encuentra una instancia activa de Etabs."""

    def __init__(self, error: Exception, message: str = "Modelo no encontrado o no se pudo abrir"):
        """Método init."""
        self.message = f"{message}. Causa: {error}"
        super().__init__(self.message)


class NuevoModeloError(Exception):
    """Excepción lanzada cuando no se puede crear un nuevo modelo Etabs."""

    def __init__(self, error: Exception, message: str = "Modelo no pudo ser creado"):
        """Método init."""
        self.message = f"{message}. Causa: {error}"
        super().__init__(self.message)
