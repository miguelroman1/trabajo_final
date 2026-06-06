-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-06-2026 a las 19:06:03
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Base de datos: `sistema_calificaciones`
CREATE DATABASE IF NOT EXISTS `sistema_calificaciones`;
USE `sistema_calificaciones`;

-- --------------------------------------------------------
-- Tabla `especialidades`
-- --------------------------------------------------------
CREATE TABLE `especialidades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `especialidades` (`id`, `nombre`) VALUES
(1, 'Programación'),
(2, 'Contabilidad'),
(3, 'Electricidad'),
(4, 'Electrónica'),
(5, 'Recursos Humanos'),
(6, 'Secretariado Bilingüe');

-- --------------------------------------------------------
-- Tabla `usuarios`
-- --------------------------------------------------------
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(200) NOT NULL,
  `curp` varchar(18) NOT NULL,
  `matricula` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `celular` varchar(20) DEFAULT NULL,
  `foto_perfil` varchar(500) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `especialidad_id` int(11) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `curp` (`curp`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `matricula` (`matricula`),
  KEY `especialidad_id` (`especialidad_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`especialidad_id`) REFERENCES `especialidades` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `materias`
-- --------------------------------------------------------
CREATE TABLE `materias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `semestre` int(11) NOT NULL CHECK (`semestre` between 1 and 6),
  `especialidad_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_materia_semestre` (`nombre`,`semestre`,`especialidad_id`),
  KEY `idx_materia_especialidad` (`especialidad_id`,`semestre`),
  CONSTRAINT `materias_ibfk_1` FOREIGN KEY (`especialidad_id`) REFERENCES `especialidades` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Materias para Programación (especialidad_id = 1)
INSERT INTO `materias` (`nombre`, `semestre`, `especialidad_id`) VALUES
('Fundamentos de Programación', 1, 1),
('Matemáticas Discretas', 1, 1),
('Introducción a Bases de Datos', 1, 1),
('Programación Estructurada', 2, 1),
('Cálculo Diferencial', 2, 1),
('SQL Avanzado', 2, 1),
('Programación Orientada a Objetos', 3, 1),
('Álgebra Lineal', 3, 1),
('Estructura de Datos', 3, 1),
('Desarrollo Web', 4, 1),
('Bases de Datos Avanzadas', 4, 1),
('Estadística', 4, 1),
('Frameworks JavaScript', 5, 1),
('Metodologías Ágiles', 5, 1),
('Redes de Computadoras', 5, 1),
('Desarrollo Móvil', 6, 1),
('Proyecto de Titulación', 6, 1),
('Ética Profesional', 6, 1);

-- --------------------------------------------------------
-- Tabla `calificaciones`
-- --------------------------------------------------------
CREATE TABLE `calificaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `materia_id` int(11) NOT NULL,
  `semestre` int(11) NOT NULL CHECK (`semestre` between 1 and 6),
  `unidad1` decimal(4,2) DEFAULT NULL CHECK (`unidad1` between 0 and 10),
  `unidad2` decimal(4,2) DEFAULT NULL CHECK (`unidad2` between 0 and 10),
  `unidad3` decimal(4,2) DEFAULT NULL CHECK (`unidad3` between 0 and 10),
  `promedio` decimal(4,2) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_calificacion` (`usuario_id`,`materia_id`,`semestre`),
  KEY `materia_id` (`materia_id`),
  KEY `idx_usuario_semestre` (`usuario_id`,`semestre`),
  CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Usuario de prueba
INSERT INTO `usuarios` (`id`, `nombre_completo`, `curp`, `matricula`, `correo`, `celular`, `username`, `password`, `especialidad_id`) VALUES
(1, 'Miguel Angel Roman Padilla', 'ROPM010101HDFNRN01', '23308060610314', 'miguel.roman@cetis61.edu.mx', '6861234567', 'miguel', '9b7af877e7ad4c237a87d38a767e4975ec90b978886e117f1952638a970db4f9', 1);

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;