/* =========================================================
   PROYECTO INTEGRADOR - Stored Procedures
   Base de Datos:  SoundStreamDB
   Tabla:          Operacion.Usuario
   ========================================================= */

USE [SoundStreamDB];
GO

-- ---------------------------------------------------------
-- 1) SP CONSULTAR - Devuelve todos los usuarios
-- ---------------------------------------------------------
CREATE OR ALTER PROCEDURE [Operacion].[sp_ConsultarUsuarios]
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        idUsuario,
        primerNombre,
        primerApellido,
        email,
        pais,
        fechaRegistro,
        estadoCuenta
    FROM Operacion.Usuario
    ORDER BY idUsuario;
END
GO

-- ---------------------------------------------------------
-- 2) SP INSERTAR - Crea un nuevo usuario
--    (idUsuario es IDENTITY: lo genera SQL Server automáticamente)
--    (fechaRegistro se asigna con GETDATE())
-- ---------------------------------------------------------
CREATE OR ALTER PROCEDURE [Operacion].[sp_InsertarUsuario]
    @primerNombre   NVARCHAR(35),
    @primerApellido NVARCHAR(35),
    @email          NVARCHAR(80),
    @password       NVARCHAR(100),
    @pais           NVARCHAR(30),
    @estadoCuenta   NVARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Operacion.Usuario
        (primerNombre, primerApellido, email, password, pais, fechaRegistro, estadoCuenta)
    VALUES
        (@primerNombre, @primerApellido, @email, @password, @pais, GETDATE(), @estadoCuenta);

    -- Devolver el ID generado
    SELECT SCOPE_IDENTITY() AS NuevoID;
END
GO

-- ---------------------------------------------------------
-- 3) SP ACTUALIZAR - Modifica email y estadoCuenta de un usuario
-- ---------------------------------------------------------
CREATE OR ALTER PROCEDURE [Operacion].[sp_ActualizarUsuario]
    @idUsuario    INT,
    @email        NVARCHAR(80),
    @estadoCuenta NVARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Operacion.Usuario
    SET email = @email,
        estadoCuenta = @estadoCuenta
    WHERE idUsuario = @idUsuario;

    SELECT @@ROWCOUNT AS FilasAfectadas;
END
GO

-- ---------------------------------------------------------
-- 4) SP ELIMINAR - Borra un usuario por su ID
-- ---------------------------------------------------------
CREATE OR ALTER PROCEDURE [Operacion].[sp_EliminarUsuario]
    @idUsuario INT
AS
BEGIN
    SET NOCOUNT ON;
    DELETE FROM Operacion.Usuario
    WHERE idUsuario = @idUsuario;

    SELECT @@ROWCOUNT AS FilasAfectadas;
END
GO
