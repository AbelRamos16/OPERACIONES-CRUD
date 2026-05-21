"""
==========================================================
PROYECTO INTEGRADOR - BASE DE DATOS II
Punto de entrada del programa.

Instancia la clase GestorUsuario y ejecuta el menú CRUD.
==========================================================
"""

import sys
from gestor_usuario import GestorUsuario

# Forzar UTF-8 en la consola (acentos correctos en Windows)
sys.stdout.reconfigure(encoding='utf-8')


def main():
    # Instanciar el gestor (lee config.json y abre la conexión)
    gestor = GestorUsuario('config.json')

    # Ejecutar el menú CRUD interactivo
    gestor.ejecutar_menu()


if __name__ == '__main__':
    main()
