-- Primero, crear la base de datos
CREATE DATABASE RoadToFit;
GO

-- Seleccionamos la base de datos para trabajar
USE Road_To_Fit;
GO

-- Ahora creamos las tablas

-- Tabla Planes
CREATE TABLE Planes (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Descripción NVARCHAR(255),
    Costo DECIMAL(10,2) NOT NULL
);

-- Tabla Roles
CREATE TABLE Roles (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Descripción NVARCHAR(100) NOT NULL
);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Apellidos NVARCHAR(100),
    Correo NVARCHAR(150) UNIQUE,
    Peso DECIMAL(5,2),
    Planes INT,
    FOREIGN KEY (Planes) REFERENCES Planes(Id)
);

-- Tabla Usuario-Rol (relación muchos a muchos)
CREATE TABLE UsuarioRol (
    Usuario INT NOT NULL,
    Rol INT NOT NULL,
    PRIMARY KEY (Usuario, Rol),
    FOREIGN KEY (Usuario) REFERENCES Usuarios(Id),
    FOREIGN KEY (Rol) REFERENCES Roles(Id)
);

-- Tabla Cuestionario
CREATE TABLE Cuestionario (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Descripción NVARCHAR(255)
);

-- Tabla Preguntas
CREATE TABLE Preguntas (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Descripción NVARCHAR(255)
);

-- Tabla Cuestionario-Preguntas
CREATE TABLE CuestionarioPreguntas (
    Usuario INT NOT NULL,
    TipoDeCuestionario NVARCHAR(50),
    NumeroDeSesion INT,
    Pregunta INT,
    Respuesta NVARCHAR(500),
    FOREIGN KEY (Usuario) REFERENCES Usuarios(Id),
    FOREIGN KEY (Pregunta) REFERENCES Preguntas(Id)
);

-- Tabla Ejercicios
CREATE TABLE Ejercicios (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Descripción NVARCHAR(255),
    Video NVARCHAR(255),
    Foto NVARCHAR(255),
    Doble BIT
);

-- Tabla Músculos
CREATE TABLE Musculos (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    MusculoPequeño BIT
);

-- Tabla Músculos_1 (parece ser otra categoría de músculos)
CREATE TABLE Musculos_1 (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    MusculoPequeño BIT
);

-- Tabla Ejercicios-Músculos
CREATE TABLE EjerciciosMusculos (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Ejercicio INT NOT NULL,
    MusculoPrincipal INT,
    MusculosSecundarios NVARCHAR(255),
    FOREIGN KEY (Ejercicio) REFERENCES Ejercicios(Id),
    FOREIGN KEY (MusculoPrincipal) REFERENCES Musculos(Id)
);

-- Tabla Sesiones
CREATE TABLE Sesiones (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Usuario INT NOT NULL,
    NumeroDeSesion INT,
    Completado BIT,
    Fecha DATE,
    PesoTotal DECIMAL(6,2),
    Tiempo TIME,
    FOREIGN KEY (Usuario) REFERENCES Usuarios(Id)
);

-- Tabla Maquinas
CREATE TABLE Maquina (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Usuario INT,
    Numero INT,
    Descripción NVARCHAR(255),
    FOREIGN KEY (Usuario) REFERENCES Usuarios(Id)
);

-- Tabla Series
CREATE TABLE Series (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Sesion INT,
    Ejercicio INT,
    Numero INT,
    Medida NVARCHAR(50),
    Peso DECIMAL(6,2),
    Repeticiones INT,
    RIR INT,
    Maquina INT,
    FOREIGN KEY (Sesion) REFERENCES Sesiones(Id),
    FOREIGN KEY (Ejercicio) REFERENCES Ejercicios(Id),
    FOREIGN KEY (Maquina) REFERENCES Maquina(Id)
);

-- Tabla Desempeño
CREATE TABLE Desempeño (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Usuario INT NOT NULL,
    Fecha DATE DEFAULT GETDATE(),
    Comentario NVARCHAR(300),
    FOREIGN KEY (Usuario) REFERENCES Usuarios(Id)
);
