-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.16 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for examination_attendance
CREATE DATABASE IF NOT EXISTS `examination_attendance` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `examination_attendance`;

-- Dumping structure for table examination_attendance.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `no` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table examination_attendance.admin: ~0 rows (approximately)
INSERT INTO `admin` (`no`, `username`, `password`, `creation_date`) VALUES
	(1, 'admin', 'admin', '2022-07-26 03:12:32');

-- Dumping structure for table examination_attendance.attendance_records
CREATE TABLE IF NOT EXISTS `attendance_records` (
  `attendance_id` int(10) NOT NULL AUTO_INCREMENT,
  `student_id` int(10) NOT NULL,
  `time` time NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `student_id` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table examination_attendance.attendance_records: ~59 rows (approximately)
INSERT INTO `attendance_records` (`attendance_id`, `student_id`, `time`, `date`) VALUES
	(1, 1, '15:18:10', '2022-08-09'),
	(4, 1, '12:43:40', '2022-08-11'),
	(5, 1, '15:18:15', '2022-08-12'),
	(6, 1, '09:01:24', '2022-08-15'),
	(7, 2, '15:51:53', '2022-08-15'),
	(10, 3, '16:00:29', '2022-08-15'),
	(11, 2, '09:11:58', '2022-08-16'),
	(12, 1, '09:12:54', '2022-08-16'),
	(14, 1, '09:32:10', '2022-08-30'),
	(15, 2, '09:33:13', '2022-08-30'),
	(17, 3, '11:40:06', '2022-08-30'),
	(18, 1, '17:41:39', '2022-08-31'),
	(19, 4, '17:58:16', '2022-08-31'),
	(20, 2, '18:03:01', '2022-08-31'),
	(21, 5, '18:18:23', '2022-08-31'),
	(22, 6, '18:26:52', '2022-08-31'),
	(23, 6, '07:48:11', '2022-09-01'),
	(24, 5, '07:53:07', '2022-09-01'),
	(25, 7, '18:57:15', '2022-09-01'),
	(27, 5, '08:44:45', '2022-09-02'),
	(28, 6, '10:26:01', '2022-09-02'),
	(29, 7, '19:39:57', '2022-09-02'),
	(30, 6, '15:46:01', '2022-09-08'),
	(31, 6, '08:47:03', '2022-09-12'),
	(32, 6, '11:10:16', '2022-09-23'),
	(33, 5, '11:12:07', '2022-09-23'),
	(34, 6, '20:43:58', '2022-09-26'),
	(35, 7, '20:44:04', '2022-09-26'),
	(36, 5, '20:44:25', '2022-09-26'),
	(37, 6, '17:36:21', '2022-09-27'),
	(38, 5, '18:10:23', '2022-09-27'),
	(39, 6, '10:26:25', '2022-09-29'),
	(40, 5, '10:26:47', '2022-09-29'),
	(41, 6, '09:26:53', '2022-10-03'),
	(42, 5, '09:28:50', '2022-10-03'),
	(43, 6, '16:15:17', '2022-10-06'),
	(44, 5, '16:46:22', '2022-10-06'),
	(45, 7, '17:20:58', '2022-10-06'),
	(50, 6, '08:51:26', '2022-10-19'),
	(51, 10, '09:32:20', '2022-10-19'),
	(52, 5, '10:04:32', '2022-10-19'),
	(53, 6, '21:47:07', '2022-10-25'),
	(54, 5, '10:26:36', '2022-10-28'),
	(55, 6, '10:29:03', '2022-10-28'),
	(56, 6, '12:08:47', '2022-11-02'),
	(57, 6, '16:08:12', '2022-11-03'),
	(58, 6, '17:59:20', '2022-11-08'),
	(59, 10, '18:04:09', '2022-11-08'),
	(60, 6, '18:02:13', '2022-11-29'),
	(61, 6, '16:24:07', '2022-12-08'),
	(62, 10, '09:42:47', '2023-02-02'),
	(63, 5, '09:43:08', '2023-02-02'),
	(64, 6, '09:45:06', '2023-02-15'),
	(65, 13, '22:03:13', '2023-02-15'),
	(66, 5, '14:24:33', '2023-02-15'),
	(67, 12, '20:35:37', '2023-02-15'),
	(68, 6, '15:52:38', '2023-02-16'),
	(69, 7, '16:04:53', '2023-02-16'),
	(71, 5, '16:14:37', '2023-02-16'),
	(72, 10, '16:30:20', '2023-02-16');

-- Dumping structure for table examination_attendance.student_examination_list
CREATE TABLE IF NOT EXISTS `student_examination_list` (
  `student_id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `programme` varchar(50) NOT NULL,
  `course` varchar(50) NOT NULL,
  `hall` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `seat` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `available` int(10) NOT NULL,
  PRIMARY KEY (`student_id`) USING BTREE,
  UNIQUE KEY `seat` (`seat`),
  KEY `course_id` (`course`) USING BTREE,
  KEY `hall_id` (`hall`) USING BTREE,
  KEY `programme_id` (`programme`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table examination_attendance.student_examination_list: ~9 rows (approximately)
INSERT INTO `student_examination_list` (`student_id`, `name`, `gender`, `phone`, `email`, `programme`, `course`, `hall`, `seat`, `available`) VALUES
	(5, 'Lim Peng Aun ', 'Male', '0123456789', 'pengaun@gmail.com', 'Software Engineering', 'System Security', 'Hall A', 'A1', 1),
	(6, 'Janice Lim', 'Female', '187924603', 'janicelim@gmail.com', 'Psychology', 'Biological Psychology', 'Hall A', 'A2', 1),
	(7, 'zekai', 'Male', '0183624819', 'zekai0221@gmail.com', 'Psychology', 'Social Psychology', 'Hall A', 'A3', 1),
	(8, 'Xiao Jia Qi ', 'Female', '0198745632', 'jiaqi@gmail.com', 'Psychology', 'Biological Psychology', 'Hall A', 'A4', 1),
	(10, 'May Tan', 'Female', '164885416', 'mary@gmail.com ', 'Music', 'Musicology', NULL, NULL, 0),
	(11, 'GabTan', 'Male', '2587425845', 'gab@gmail.com', 'Software Engineering', 'Computational Logic', NULL, NULL, 0),
	(12, 'Gab', 'Male', '25874587458', 'gab@gmail.com', 'Software Engineering', 'System Security', 'Hall B', 'B1', 1),
	(13, 'John Wong', 'Male', '52442424', 'fdvfvfdbgg', 'Music', 'Musicology', 'Hall C', 'C1', 1),
	(14, 'ddsds', 'Female', '542845', 'xdfgbvcxasdcfv', 'Psychology', 'Social Psychology', NULL, NULL, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
