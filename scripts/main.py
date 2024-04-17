"""Main."""
from pathlib import Path

from etabs_sdk.src import Etabs

# path = Path("C:\\Users\\User\\Desktop\\Modelo en trabajo\\test.EDB")
# path2 = Path("C:\\Users\\User\\Desktop\\Modelo en trabajo\\test123.EDB")

etabs = Etabs(adjuntar_a_instancia=True)
columnas_tabla = etabs.columnas_tabla("Area Assignments - Pier Labels", printable=True)
datos_tabla = etabs.datos_tabla("Area Assignments - Pier Labels")
print(datos_tabla)
# etabs.abrir_modelo(path)
# etabs.cerrar_modelo()
# etabs = Etabs(modelo_nuevo=True)
