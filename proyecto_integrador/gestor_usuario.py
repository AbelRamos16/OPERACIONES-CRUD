"""
==========================================================
PROYECTO INTEGRADOR - BASE DE DATOS II
Clase GestorUsuario: encapsula la conexión a SQL Server
y las operaciones CRUD sobre la tabla Operacion.Usuario
de la base de datos SoundStreamDB.

Las operaciones CRUD se realizan invocando Stored Procedures
desde Python con pyodbc.

Dirigido a:  Ing. Geovanni Aucancela Soliz, MSc.
Grupo:       grupo1
==========================================================
"""

import json
import pyodbc


class GestorUsuario:
    """Gestor CRUD para la tabla Operacion.Usuario."""

    # ------------------------------------------------------
    # Constructor: inicializa la conexión desde config.json
    # ------------------------------------------------------
    def __init__(self, ruta_config='config.json'):
        try:
            # 1) Leer credenciales del archivo JSON externo
            with open(ruta_config, 'r', encoding='utf-8') as archivo_config:
                config = json.load(archivo_config)

            name_server      = config['name_server']
            database         = config['database']
            username         = config['username']
            password         = config['password']
            controlador_odbc = config['controlador_odbc']

            # 2) Construir cadena de conexión
            self.connection_string = (
                f'DRIVER={{{controlador_odbc}}};'
                f'SERVER={name_server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )

            # 3) Establecer la conexión (parte del objeto, no se pasa como parámetro)
            self.conexion = pyodbc.connect(self.connection_string)
            print("\nOk ... Conexión Exitosa a SQL Server:", database, "\n")

        except FileNotFoundError:
            print(f"\n\t Error: no se encuentra el archivo de configuración '{ruta_config}'")
            self.conexion = None
        except Exception as e:
            print("\n \t Ocurrió un error al conectar a SQL Server: \n\n", e)
            self.conexion = None

    # ------------------------------------------------------
    # Método CRUD: Consultar todos los usuarios (READ)
    # Invoca el SP Operacion.sp_ConsultarUsuarios
    # ------------------------------------------------------
    def consultar_usuarios(self):
        try:
            print("\n\t\tCONSULTA DE USUARIOS:\n")
            micursor = self.conexion.cursor()

            # Invocar Stored Procedure (sin parámetros)
            SENTENCIA_SQL = "{CALL Operacion.sp_ConsultarUsuarios}"
            micursor.execute(SENTENCIA_SQL)
            records = micursor.fetchall()

            # Cabecera
            print("\tID\tNombre\tApellido\tEmail\tPais\tFechaRegistro\tEstado")
            print("\t--\t------\t--------\t-----\t----\t-------------\t------")
            for r in records:
                print(f"\t{r.idUsuario}\t{r.primerNombre}\t{r.primerApellido}\t{r.email}\t{r.pais}\t{r.fechaRegistro}\t{r.estadoCuenta}")

            print(f"\n\tTotal de registros: {len(records)}")
            print("\nOk ... Consulta Culminada con Exito: \n")

        except Exception as e:
            print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)

    # ------------------------------------------------------
    # Método CRUD: Insertar usuario (CREATE)
    # Invoca el SP Operacion.sp_InsertarUsuario
    # ------------------------------------------------------
    def insertar_usuario(self):
        try:
            print("\n\t\tINSERTAR NUEVO USUARIO:\n")

            # Solicitar parámetros por INPUT
            l_primerNombre   = input("\tIngrese Primer Nombre:    \t")
            l_primerApellido = input("\tIngrese Primer Apellido:  \t")
            l_email          = input("\tIngrese Email:            \t")
            l_password       = input("\tIngrese Contraseña:       \t")
            l_pais           = input("\tIngrese País:             \t")
            l_estadoCuenta   = input("\tIngrese Estado (Activo/Inactivo): \t")

            micursor = self.conexion.cursor()
            SENTENCIA_SQL = "{CALL Operacion.sp_InsertarUsuario(?,?,?,?,?,?)}"
            micursor.execute(
                SENTENCIA_SQL,
                (l_primerNombre, l_primerApellido, l_email, l_password, l_pais, l_estadoCuenta)
            )

            # El SP devuelve el nuevo ID generado por IDENTITY
            fila = micursor.fetchone()
            nuevo_id = int(fila.NuevoID) if fila else None

            self.conexion.commit()
            print(f"\nOk ... Inserción Exitosa. Nuevo idUsuario asignado: {nuevo_id}\n")

        except Exception as e:
            print("\n \t Ocurrió un error al insertar con SQL Server: \n\n", e)

    # ------------------------------------------------------
    # Método CRUD: Actualizar usuario (UPDATE)
    # Invoca el SP Operacion.sp_ActualizarUsuario
    # ------------------------------------------------------
    def actualizar_usuario(self):
        try:
            print("\n\t\tACTUALIZAR USUARIO:\n")

            l_idUsuario    = int(input("\tIngrese ID del Usuario a actualizar: \t"))
            l_email        = input("\tIngrese Nuevo Email:                  \t")
            l_estadoCuenta = input("\tIngrese Nuevo Estado (Activo/Inactivo): \t")

            micursor = self.conexion.cursor()
            SENTENCIA_SQL = "{CALL Operacion.sp_ActualizarUsuario(?,?,?)}"
            micursor.execute(SENTENCIA_SQL, (l_idUsuario, l_email, l_estadoCuenta))

            fila = micursor.fetchone()
            filas_afectadas = int(fila.FilasAfectadas) if fila else 0

            self.conexion.commit()
            print(f"\nOk ... Actualización Exitosa. Filas afectadas: {filas_afectadas}\n")

        except Exception as e:
            print("\n \t Ocurrió un error al Actualizar con SQL Server: \n\n", e)

    # ------------------------------------------------------
    # Método CRUD: Eliminar usuario (DELETE)
    # Invoca el SP Operacion.sp_EliminarUsuario
    # ------------------------------------------------------
    def eliminar_usuario(self):
        try:
            print("\n\t\tELIMINAR USUARIO:\n")

            l_idUsuario = int(input("\tIngrese ID del Usuario a Eliminar: \t"))

            micursor = self.conexion.cursor()
            SENTENCIA_SQL = "{CALL Operacion.sp_EliminarUsuario(?)}"
            micursor.execute(SENTENCIA_SQL, (l_idUsuario,))

            fila = micursor.fetchone()
            filas_afectadas = int(fila.FilasAfectadas) if fila else 0

            self.conexion.commit()
            print(f"\nOk ... Eliminación Exitosa. Filas afectadas: {filas_afectadas}\n")

        except Exception as e:
            print("\n \t Ocurrió un error al Eliminar con SQL Server: \n\n", e)

    # ------------------------------------------------------
    # Método: Mostrar el menú principal
    # ------------------------------------------------------
    def mostrar_menu(self):
        print("\n\t****************************************")
        print("\t**  SISTEMA CRUD - SoundStreamDB      **")
        print("\t**  Tabla: Operacion.Usuario          **")
        print("\t****************************************")
        print("\tOpciones CRUD:\n")
        print("\t1. Crear registro (Insertar Usuario)")
        print("\t2. Consultar registros (Listar Usuarios)")
        print("\t3. Actualizar registro")
        print("\t4. Eliminar registro")
        print("\t5. Salir\n")

    # ------------------------------------------------------
    # Método: Bucle principal del menú CRUD
    # ------------------------------------------------------
    def ejecutar_menu(self):
        if self.conexion is None:
            print("\n\t No se puede ejecutar el menú porque no hay conexión.\n")
            return

        while True:
            self.mostrar_menu()
            opcion = input("\tSeleccione una opción 1-5: \t")

            if opcion == '1':
                self.insertar_usuario()
            elif opcion == '2':
                self.consultar_usuarios()
            elif opcion == '3':
                self.actualizar_usuario()
            elif opcion == '4':
                self.eliminar_usuario()
            elif opcion == '5':
                print("\n\tSaliendo del programa...\n")
                break
            else:
                print("\n\tOpción no válida. Intente nuevamente.\n")

        self.cerrar_conexion()

    # ------------------------------------------------------
    # Método: Cerrar la conexión
    # ------------------------------------------------------
    def cerrar_conexion(self):
        if self.conexion is not None:
            self.conexion.close()
            print("\nConexión Cerrada: \n")
