-- --------------------------------------------------------
-- Anfitrião:                    sql11.freesqldatabase.com
-- Versão do servidor:           5.5.62-0ubuntu0.14.04.1 - (Ubuntu)
-- SO do servidor:               debian-linux-gnu
-- HeidiSQL Versão:              12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- A despejar estrutura da base de dados para sql11696357
CREATE DATABASE IF NOT EXISTS `sql11696357` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `sql11696357`;

-- A despejar estrutura para tabela sql11696357.doctors
CREATE TABLE IF NOT EXISTS `doctors` (
  `doctor_id` bigint(255) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telephone` int(9) NOT NULL,
  `sex` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthdate` date NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `speciality` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `salt_pass` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`doctor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exportação de dados não seleccionada.

-- A despejar estrutura para tabela sql11696357.modules
CREATE TABLE IF NOT EXISTS `modules` (
  `module_id` bigint(255) NOT NULL AUTO_INCREMENT,
  `patient_id` bigint(255) NOT NULL,
  `episode` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `module` char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('Finished','In Progress','Paused') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`module_id`),
  KEY `patient_module` (`patient_id`),
  CONSTRAINT `patient_module` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exportação de dados não seleccionada.

-- A despejar estrutura para tabela sql11696357.patients
CREATE TABLE IF NOT EXISTS `patients` (
  `patient_id` bigint(255) NOT NULL AUTO_INCREMENT,
  `doctor_id` bigint(255) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` int(9) NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sex` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthdate` date NOT NULL,
  `processnumber` int(80) NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `postalcode` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `town` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nif` int(9) DEFAULT NULL,
  `sns` int(9) DEFAULT NULL,
  `STATUS` enum('In Treatment','Awaiting Treatment','Completed Treatment') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  KEY `doctor_patient` (`doctor_id`),
  CONSTRAINT `doctor_patient` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exportação de dados não seleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
