-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: bank
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `bank`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `bank` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `bank`;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `Account_num` char(11) NOT NULL,
  `Balance` int NOT NULL DEFAULT '0',
  `Password` char(6) NOT NULL,
  `Open_date` date DEFAULT NULL,
  `Ussn` char(13) NOT NULL,
  PRIMARY KEY (`Account_num`,`Ussn`),
  KEY `Ussn` (`Ussn`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`Ussn`) REFERENCES `user` (`Ssn`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('13498766245',3000000,'123456','2019-12-06','9010171333445'),('19362276145',3180,'222333','2021-11-01','0104244321321'),('29871928643',10000000,'333222','2020-06-30','0104244321321'),('35713894011',11290,'654321','2021-07-05','8311291222334'),('38947154027',980000,'222333','2021-09-18','0104244321321'),('45183099823',620000,'321654','2020-11-11','8902071444556'),('51782023048',100000,'222333','2021-11-22','0104244321321'),('64529366489',5000000,'654321','2020-05-04','8311291222334'),('71390006323',4000000,'321654','2021-10-27','8902071444556'),('83492015649',210000,'654321','2020-12-04','8311291222334');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Admin_num` char(9) NOT NULL,
  `Fname` varchar(5) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Usercount` int DEFAULT NULL,
  PRIMARY KEY (`Admin_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('111111111','Kim','Godae',2),('123123123','Lee','Yoon',0),('222233334','Yoo','Jiwon',1),('777777777','Jeong','Sehoon',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dw_information`
--

DROP TABLE IF EXISTS `dw_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dw_information` (
  `Idx` int NOT NULL,
  `Deposit_withdraw` char(1) NOT NULL,
  `Dw_date` date DEFAULT NULL,
  `Amount` int DEFAULT NULL,
  `Message` varchar(20) DEFAULT NULL,
  `This_account` char(11) NOT NULL,
  PRIMARY KEY (`Idx`,`This_account`),
  KEY `This_account` (`This_account`),
  CONSTRAINT `dw_information_ibfk_1` FOREIGN KEY (`This_account`) REFERENCES `account` (`Account_num`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dw_information`
--

LOCK TABLES `dw_information` WRITE;
/*!40000 ALTER TABLE `dw_information` DISABLE KEYS */;
INSERT INTO `dw_information` VALUES (1,'d','2019-12-06',3000000,'Open','13498766245'),(1,'d','2021-11-01',5000,'Open','19362276145'),(1,'d','2020-06-30',10000000,'Open','29871928643'),(1,'d','2021-07-05',50000,'Open','35713894011'),(1,'d','2021-09-18',1000000,'Open','38947154027'),(1,'d','2020-11-11',1000000,'Open','45183099823'),(1,'d','2021-11-22',100000,'Open','51782023048'),(1,'d','2020-05-04',2000000,'Open','64529366489'),(1,'d','2021-10-27',4000000,'Open','71390006323'),(1,'d','2020-12-04',100000,'Open','83492015649'),(2,'w','2021-11-03',1820,'snack','19362276145'),(2,'w','2021-09-08',38710,'Kim','35713894011'),(2,'w','2021-09-30',200000,'dudu','38947154027'),(2,'w','2020-12-31',380000,'Parkhaewoong','45183099823'),(2,'d','2020-08-10',3000000,'Kimhaejin','64529366489'),(2,'w','2021-01-01',50000,'Kim','83492015649'),(3,'w','2021-06-24',29000,'Kimhaejin','83492015649'),(7,'e','2022-01-01',0,'asdf','29871928643');
/*!40000 ALTER TABLE `dw_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `Ssn` char(13) NOT NULL,
  `Fname` varchar(5) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Address` varchar(30) DEFAULT NULL,
  `Phonecall` char(11) DEFAULT NULL,
  `Max_account` int DEFAULT NULL,
  `Cur_account` int DEFAULT NULL,
  `Adnum` char(9) NOT NULL,
  PRIMARY KEY (`Ssn`),
  KEY `Adnum` (`Adnum`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`Adnum`) REFERENCES `admin` (`Admin_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('0104244321321','Ha','Subin','Daegu','01044445555',4,4,'777777777'),('8311291222334','Kim','Haejin','Seoul','01011112222',7,3,'111111111'),('8902071444556','Park','Haewoong','Incheon','01033334444',4,2,'111111111'),('9010171333445','Lee','Sundong','Busan','01022223333',4,1,'222233334');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-03 22:02:37
