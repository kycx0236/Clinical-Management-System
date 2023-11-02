-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ssis_v1
DROP DATABASE IF EXISTS 'cms_2k23';
CREATE DATABASE IF NOT EXISTS 'cms_2k23' /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE 'cms_2k23';

-- Dumping structure for table 'students'
DROP TABLE IF EXISTS 'appointment';
CREATE TABLE IF NOT EXISTS 'appointment'(
	  'reference_number' varchar(50) NOT NULL PRIMARY KEY,
    'date_appointment' DATE,
    'time_appointment' varchar(255) DEFAULT NOT NULL,
    'status_' varchar(20) DEFAULT NOT NULL,
    'book_date' varchar(255) DEFAULT NOT NULL,
    'first_name' varchar(255) DEFAULT NOT NULL,
    'middle_name' varchar(50) DEFAULT NOT NULL,
    'last_name' varchar(50) DEFAULT NOT NULL,
    'sex' varchar(10) DEFAULT NOT NULL,
    'birth_date' DATE NOT NULL,
    'contact_number' varchar(50) DEFAULT NULL,
    'email' varchar(100) DEFAULT NULL,
    'address' varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci0;

-- Data exporting was unselected.


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
