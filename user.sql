CREATE DATABASE  IF NOT EXISTS `user` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `user`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: user
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `airplanes`
--

DROP TABLE IF EXISTS `airplanes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airplanes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `departure_time` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airplanes`
--

LOCK TABLES `airplanes` WRITE;
/*!40000 ALTER TABLE `airplanes` DISABLE KEYS */;
INSERT INTO `airplanes` VALUES (1,'Airplane Option 1',500.00,'08:00:00'),(2,'Airplane Option 2',700.00,'10:00:00');
/*!40000 ALTER TABLE `airplanes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `available_dates`
--

DROP TABLE IF EXISTS `available_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `available_dates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_dates`
--

LOCK TABLES `available_dates` WRITE;
/*!40000 ALTER TABLE `available_dates` DISABLE KEYS */;
INSERT INTO `available_dates` VALUES (1,1,'2024-04-01','2024-04-07');
/*!40000 ALTER TABLE `available_dates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `package_id` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `booking_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `booking_status` varchar(20) DEFAULT 'booked',
  `guest_count` int DEFAULT NULL,
  `booked_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `package_id` (`package_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (17,2,1,'2024-04-01','2024-04-07','2024-04-02 10:13:28','booked',NULL,NULL),(18,2,1,'2024-04-01','2024-04-07','2024-04-03 15:27:57','booked',NULL,NULL),(20,2,1,'2024-04-01','2024-04-07','2024-04-04 13:00:07','booked',NULL,NULL),(22,4,1,NULL,NULL,'2024-04-05 05:39:03','booked',NULL,NULL),(23,4,1,'2024-04-01','2024-04-07','2024-04-05 05:43:08','booked',NULL,NULL),(24,4,1,'2024-04-01','2024-04-07','2024-04-05 05:48:37','booked',NULL,NULL),(25,2,1,'2024-04-01','2024-04-07','2024-04-05 06:14:56','booked',NULL,NULL),(26,2,1,'2024-04-01','2024-04-07','2024-04-05 06:17:41','booked',NULL,NULL),(27,2,1,'2024-04-01','2024-04-07','2024-04-05 06:18:58','booked',NULL,NULL),(28,2,1,'2024-04-01','2024-04-07','2024-04-05 06:21:04','booked',NULL,NULL),(29,2,1,'2024-04-01','2024-04-07','2024-04-05 06:22:56','booked',NULL,NULL),(30,2,1,'2024-04-01','2024-04-07','2024-04-05 06:23:39','booked',NULL,NULL),(31,2,1,'2024-04-01','2024-04-07','2024-04-06 04:08:09','booked',NULL,NULL),(32,2,1,'2024-04-01','2024-04-07','2024-04-06 04:08:11','booked',NULL,NULL),(36,2,1,'2024-04-01','2024-04-07','2024-04-06 14:36:28','booked',NULL,NULL),(37,2,1,'2024-04-01','2024-04-07','2024-04-06 14:39:58','booked',NULL,NULL),(39,2,1,'2024-04-01','2024-04-07','2024-04-06 15:09:51','booked',NULL,NULL),(40,2,1,'2024-04-01','2024-04-07','2024-04-06 16:28:16','booked',NULL,NULL),(41,2,1,'2024-04-01','2024-04-07','2024-04-06 16:29:53','booked',NULL,NULL),(42,2,1,'2024-04-01','2024-04-07','2024-04-06 16:30:38','booked',NULL,NULL),(43,2,1,'2024-04-01','2024-04-07','2024-04-06 17:08:29','booked',NULL,NULL),(44,2,1,'2024-04-01','2024-04-07','2024-04-06 18:07:13','booked',NULL,NULL),(45,2,1,'2024-04-01','2024-04-07','2024-04-06 18:48:16','booked',NULL,NULL),(46,2,1,'2024-04-01','2024-04-07','2024-04-07 07:06:28','booked',NULL,NULL),(47,2,1,'2024-04-01','2024-04-07','2024-04-07 07:36:59','booked',NULL,NULL),(48,2,1,'2024-04-01','2024-04-07','2024-04-07 07:45:02','booked',NULL,NULL),(49,2,1,'2024-04-01','2024-04-07','2024-04-07 07:47:20','booked',NULL,NULL),(50,2,1,'2024-04-01','2024-04-07','2024-04-07 07:47:51','booked',NULL,NULL),(51,2,1,'2024-04-01','2024-04-07','2024-04-07 08:31:13','booked',NULL,NULL),(53,2,1,'2024-04-01','2024-04-07','2024-04-07 18:16:46','booked',NULL,NULL),(54,2,1,'2024-04-01','2024-04-07','2024-04-08 06:04:07','booked',NULL,NULL),(55,2,1,'2024-04-01','2024-04-07','2024-04-08 11:57:59','booked',NULL,NULL),(56,2,1,'2024-04-01','2024-04-07','2024-04-08 14:06:55','booked',NULL,NULL),(58,2,1,'2024-04-01','2024-04-07','2024-04-08 16:46:38','booked',NULL,NULL),(60,2,1,NULL,NULL,'2024-04-19 18:30:40','booked',2,2);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `budgets`
--

DROP TABLE IF EXISTS `budgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budgets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `price_per_person` decimal(10,2) DEFAULT NULL,
  `total_budget` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`),
  CONSTRAINT `budgets_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgets`
--

LOCK TABLES `budgets` WRITE;
/*!40000 ALTER TABLE `budgets` DISABLE KEYS */;
INSERT INTO `budgets` VALUES (16,1,200000.00,10000.00,NULL),(17,1,250000.00,NULL,NULL),(18,1,180000.00,NULL,NULL),(19,2,220000.00,NULL,NULL),(20,2,190000.00,NULL,NULL),(21,2,300000.00,NULL,NULL),(22,3,230000.00,NULL,NULL),(23,3,210000.00,NULL,NULL),(24,3,170000.00,NULL,NULL),(25,4,240000.00,NULL,NULL),(26,4,260000.00,NULL,NULL),(27,4,200000.00,NULL,NULL),(28,5,270000.00,NULL,NULL),(29,5,220000.00,NULL,NULL),(30,5,180000.00,NULL,NULL);
/*!40000 ALTER TABLE `budgets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carousel_items`
--

DROP TABLE IF EXISTS `carousel_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carousel_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_url` varchar(255) NOT NULL,
  `caption` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carousel_items`
--

LOCK TABLES `carousel_items` WRITE;
/*!40000 ALTER TABLE `carousel_items` DISABLE KEYS */;
INSERT INTO `carousel_items` VALUES (1,'static/maldives.jpg','Land of Smiles, Timeless Charm'),(2,'static/maldives-1.jpg','Paradise Found, Serene Bliss'),(3,'static/carousel-1.jpg',NULL),(4,'static/austrilia.jpg',NULL),(5,'static/carousel-2.jpg',NULL);
/*!40000 ALTER TABLE `carousel_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatbot_responses`
--

DROP TABLE IF EXISTS `chatbot_responses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatbot_responses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_message` varchar(255) NOT NULL,
  `response` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatbot_responses`
--

LOCK TABLES `chatbot_responses` WRITE;
/*!40000 ALTER TABLE `chatbot_responses` DISABLE KEYS */;
INSERT INTO `chatbot_responses` VALUES (1,'hello','Hi there! How can I help you today?'),(2,'bye','Goodbye! Have a great day!'),(3,'help','I am a simple chatbot. Feel free to ask me anything!'),(4,'maldives','');
/*!40000 ALTER TABLE `chatbot_responses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `destination_lists`
--

DROP TABLE IF EXISTS `destination_lists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destination_lists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `top_destination_id` int DEFAULT NULL,
  `place_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `top_destination_id` (`top_destination_id`),
  CONSTRAINT `destination_lists_ibfk_1` FOREIGN KEY (`top_destination_id`) REFERENCES `top_destinations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destination_lists`
--

LOCK TABLES `destination_lists` WRITE;
/*!40000 ALTER TABLE `destination_lists` DISABLE KEYS */;
INSERT INTO `destination_lists` VALUES (1,1,'New York'),(2,1,'Los Angeles'),(3,1,'Chicago'),(4,2,'London'),(5,2,'Manchester'),(6,2,'Edinburgh'),(7,3,'Sydney'),(8,3,'Melbourne'),(9,3,'Brisbane'),(10,4,'Delhi'),(11,4,'Mumbai'),(12,4,'Bangalore'),(13,5,'Cape Town'),(14,5,'Johannesburg'),(15,5,'Durban'),(16,6,'Jakarta'),(17,6,'Bali'),(18,6,'Yogyakarta');
/*!40000 ALTER TABLE `destination_lists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `destinations`
--

DROP TABLE IF EXISTS `destinations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destinations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destinations`
--

LOCK TABLES `destinations` WRITE;
/*!40000 ALTER TABLE `destinations` DISABLE KEYS */;
INSERT INTO `destinations` VALUES (0,'Select Destination',NULL),(1,'Paris','City of lights and romance'),(2,'Tokyo','Vibrant metropolis with rich culture'),(3,'Sydney','Harbor city with stunning beaches'),(4,'Rome','Historical city with ancient ruins'),(5,'Cancun','Tropical paradise with white sandy beaches');
/*!40000 ALTER TABLE `destinations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `hotel` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `guest` int DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `adult_price` decimal(10,2) DEFAULT '0.00',
  `child_price` decimal(10,2) DEFAULT '0.00',
  `airplane_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`),
  CONSTRAINT `packages_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--

LOCK TABLES `packages` WRITE;
/*!40000 ALTER TABLE `packages` DISABLE KEYS */;
INSERT INTO `packages` VALUES (1,1,'Eiffel Tower Hotel','Champs-Elysées',200000.00,2,'static/package-1.jpg','2024-04-01','2024-04-07',10000.00,10000.00,NULL),(2,1,'Louvre Palace Hotel','Le Marais',250000.00,2,'https://example.com/paris2.jpg','2024-05-10','2024-05-18',0.00,0.00,NULL),(3,1,'Seine River Resort','Saint-Germain-des-Prés',180000.00,2,'https://example.com/paris3.jpg','2024-06-15','2024-06-25',0.00,0.00,NULL),(4,2,'Sakura Palace Hotel','Shibuya',220000.00,2,'https://example.com/tokyo1.jpg','2024-07-20','2024-07-28',0.00,0.00,NULL),(5,2,'Imperial Gardens Resort','Ginza',190000.00,2,'https://example.com/tokyo2.jpg','2024-08-05','2024-08-12',0.00,0.00,NULL),(6,2,'Mount Fuji Retreat','Fuji-Hakone-Izu National Park',300000.00,2,'https://example.com/tokyo3.jpg','2024-09-15','2024-09-23',0.00,0.00,NULL),(7,3,'Harborview Resort','Bondi Beach',230000.00,2,'https://example.com/sydney1.jpg','2024-10-10','2024-10-18',0.00,0.00,NULL),(8,3,'Opera House Hotel','Circular Quay',210000.00,2,'https://example.com/sydney2.jpg','2024-11-20','2024-11-28',0.00,0.00,NULL),(9,3,'Sydney Tower Suites','Darling Harbour',170000.00,2,'https://example.com/sydney3.jpg','2025-01-05','2025-01-12',0.00,0.00,NULL),(10,4,'Colosseum Grand Hotel','Colosseum',240000.00,2,'https://example.com/rome1.jpg','2025-02-15','2025-02-22',0.00,0.00,NULL),(11,4,'Pantheon Plaza','Piazza Navona',260000.00,2,'https://example.com/rome2.jpg','2025-03-10','2025-03-17',0.00,0.00,NULL),(12,4,'Vatican View Resort','Vatican City',200000.00,2,'https://example.com/rome3.jpg','2025-04-20','2025-04-27',0.00,0.00,NULL),(13,5,'Azure Shores Resort','Playa Delfines',270000.00,2,'https://example.com/cancun1.jpg','2025-05-15','2025-05-22',0.00,0.00,NULL),(14,5,'Mayan Riviera Resort','Tulum',220000.00,2,'https://example.com/cancun2.jpg','2025-06-10','2025-06-17',0.00,0.00,NULL),(15,5,'Cancun Sunset Suites','Playa del Carmen',180000.00,2,'https://example.com/cancun3.jpg','2025-07-20','2025-07-27',0.00,0.00,NULL);
/*!40000 ALTER TABLE `packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_status`
--

DROP TABLE IF EXISTS `payment_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `payment_status` varchar(255) DEFAULT NULL,
  `transaction_id` varchar(255) DEFAULT NULL,
  `payment_date` datetime DEFAULT NULL,
  `package_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `package_id` (`package_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `payment_status_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`),
  CONSTRAINT `payment_status_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_status`
--

LOCK TABLES `payment_status` WRITE;
/*!40000 ALTER TABLE `payment_status` DISABLE KEYS */;
INSERT INTO `payment_status` VALUES (1,'pending',NULL,'2024-03-28 21:35:58',1,NULL),(2,'success','TRANS202403282136072527','2024-03-28 21:36:07',1,2),(3,'pending',NULL,'2024-03-28 21:39:37',1,NULL),(4,'pending',NULL,'2024-03-28 21:43:04',NULL,NULL),(5,'pending',NULL,'2024-03-28 21:43:57',1,NULL),(6,'pending',NULL,'2024-03-28 21:47:49',1,NULL),(7,'success',NULL,'2024-03-28 21:56:55',1,2),(8,'success','TRANS202403282202373879','2024-03-28 22:02:37',1,2),(9,'pending',NULL,'2024-03-28 22:08:10',1,NULL),(10,'pending',NULL,'2024-03-28 22:09:22',1,NULL),(11,'pending',NULL,'2024-03-28 22:14:34',1,NULL),(12,'pending',NULL,'2024-03-28 22:37:42',1,NULL),(13,'pending',NULL,'2024-03-28 22:37:46',1,NULL),(14,'success','TRANS202403282241049255','2024-03-28 22:41:04',1,2),(15,'success','TRANS202403282330592344','2024-03-28 23:30:59',1,2),(16,'success','TRANS202403282358253610','2024-03-28 23:58:25',1,2),(17,'success','TRANS202403290935532799','2024-03-29 09:35:53',1,2),(18,'success','TRANS202403290936161834','2024-03-29 09:36:16',1,2),(19,'success','TRANS202403290938446082','2024-03-29 09:38:44',1,2),(20,'success','TRANS202403291101218147','2024-03-29 11:01:21',1,2),(21,'success','TRANS202403291109095626','2024-03-29 11:09:09',1,2),(22,'success','TRANS202403291112527260','2024-03-29 11:12:52',1,2),(23,'success','TRANS202403291114539151','2024-03-29 11:14:53',1,2),(24,'pending',NULL,'2024-03-29 11:29:48',1,NULL),(25,'pending',NULL,'2024-03-29 12:09:16',1,NULL),(26,'success','TRANS202403291211408837','2024-03-29 12:11:40',1,2),(27,'success','TRANS202403291215247637','2024-03-29 12:15:24',1,2),(28,'success','TRANS202403291216581903','2024-03-29 12:16:58',1,2),(29,'success','TRANS202403291221485078','2024-03-29 12:21:48',1,2),(30,'success','TRANS202403291227329593','2024-03-29 12:27:32',1,2),(31,'pending',NULL,'2024-03-29 13:20:08',1,NULL),(32,'pending',NULL,'2024-03-29 13:20:16',1,NULL),(33,'success','TRANS202403291322321946','2024-03-29 13:22:32',1,2),(34,'pending',NULL,'2024-03-29 18:40:35',1,NULL),(35,'pending',NULL,'2024-03-29 23:57:00',NULL,NULL),(36,'pending',NULL,'2024-03-29 23:57:01',NULL,NULL),(37,'pending',NULL,'2024-03-29 23:57:01',NULL,NULL),(38,'pending',NULL,'2024-03-29 23:57:02',NULL,NULL),(39,'pending',NULL,'2024-03-29 23:57:02',NULL,NULL),(40,'pending',NULL,'2024-03-29 23:57:03',NULL,NULL),(41,'pending',NULL,'2024-03-29 23:57:03',NULL,NULL),(42,'success','TRANS202403300059179918','2024-03-30 00:59:17',1,2),(43,'pending',NULL,'2024-03-30 01:17:53',1,NULL),(44,'pending',NULL,'2024-03-30 01:32:51',1,NULL),(45,'success','TRANS202403300301033829','2024-03-30 03:01:03',1,2),(46,'success','TRANS202403300824543866','2024-03-30 08:24:54',1,2),(47,'success','TRANS202403301826495963','2024-03-30 18:26:49',1,2),(48,'pending',NULL,'2024-03-30 18:38:19',1,NULL),(49,'pending',NULL,'2024-03-30 19:10:31',1,NULL),(50,'pending',NULL,'2024-03-30 19:24:29',1,NULL),(51,'success','TRANS202403311215332573','2024-03-31 12:15:33',1,2),(52,'success','TRANS202403311237478000','2024-03-31 12:37:47',1,2),(53,'success','TRANS202403311241542664','2024-03-31 12:41:54',1,2),(54,'success','TRANS202403311244325098','2024-03-31 12:44:32',1,2),(55,'success','TRANS202403311245259628','2024-03-31 12:45:25',1,2),(56,'success','TRANS202403311258411701','2024-03-31 12:58:41',1,2),(57,'pending',NULL,'2024-04-01 12:54:18',1,NULL),(58,'success','TRANS202404011303307360','2024-04-01 13:03:30',1,2),(59,'success','TRANS202404011920215369','2024-04-01 19:20:21',1,2),(60,'success','TRANS202404011928547303','2024-04-01 19:28:54',1,2),(61,'success','TRANS202404011940047576','2024-04-01 19:40:04',1,2),(62,'success','TRANS202404011945491786','2024-04-01 19:45:49',1,2),(63,'success','TRANS202404011947051708','2024-04-01 19:47:05',1,2),(64,'success','TRANS202404011949148114','2024-04-01 19:49:14',1,2),(65,'success','TRANS202404011952165292','2024-04-01 19:52:16',1,2),(66,'success','TRANS202404012005017134','2024-04-01 20:05:01',1,2),(67,'success','TRANS202404012149479360','2024-04-01 21:49:47',1,2),(68,'success','TRANS202404012157018396','2024-04-01 21:57:01',1,2),(69,'success','TRANS202404021539582500','2024-04-02 15:39:58',1,2),(70,'success','TRANS202404021543161982','2024-04-02 15:43:16',1,2),(71,'success','TRANS202404032057492561','2024-04-03 20:57:49',1,2),(72,'success','TRANS202404041829597048','2024-04-04 18:29:59',1,2),(73,'success','TRANS202404051106213591','2024-04-05 11:06:21',1,4),(74,'pending',NULL,'2024-04-05 11:08:02',1,NULL),(75,'success','TRANS202404051112544482','2024-04-05 11:12:54',1,4),(76,'success','TRANS202404051118204795','2024-04-05 11:18:20',1,4),(77,'success','TRANS202404051127363458','2024-04-05 11:27:36',1,2),(78,'success','TRANS202404051128593782','2024-04-05 11:29:00',1,2),(79,'success','TRANS202404051130007752','2024-04-05 11:30:00',1,2),(80,'success','TRANS202404051131015026','2024-04-05 11:31:01',1,2),(81,'success','TRANS202404051133444043','2024-04-05 11:33:44',1,2),(82,'success','TRANS202404051136376587','2024-04-05 11:36:37',1,2),(83,'success','TRANS202404051136496721','2024-04-05 11:36:49',1,2),(84,'success','TRANS202404051136578700','2024-04-05 11:36:57',1,2),(85,'success','TRANS202404051136579470','2024-04-05 11:36:57',1,2),(86,'success','TRANS202404051136586954','2024-04-05 11:36:58',1,2),(87,'success','TRANS202404051140352833','2024-04-05 11:40:35',1,2),(88,'success','TRANS202404051144464019','2024-04-05 11:44:46',1,2),(89,'success','TRANS202404051147237663','2024-04-05 11:47:23',1,2),(90,'success','TRANS202404051148465507','2024-04-05 11:48:46',1,2),(91,'pending',NULL,'2024-04-05 11:50:16',1,NULL),(92,'success','TRANS202404051150396199','2024-04-05 11:50:39',1,2),(93,'success','TRANS202404051152363677','2024-04-05 11:52:36',1,2),(94,'success','TRANS202404051153213124','2024-04-05 11:53:21',1,2),(95,'pending',NULL,'2024-04-06 07:45:34',1,NULL),(96,'pending',NULL,'2024-04-06 08:01:45',1,NULL),(97,'success','TRANS202404060937118990','2024-04-06 09:37:11',1,2),(98,'success','TRANS202404060937515936','2024-04-06 09:37:51',1,2),(99,'pending',NULL,'2024-04-06 10:29:59',1,NULL),(100,'pending',NULL,'2024-04-06 11:53:01',1,NULL),(101,'pending',NULL,'2024-04-06 12:11:17',1,NULL),(102,'success','TRANS202404061951312703','2024-04-06 19:51:31',1,2),(103,'success','TRANS202404061956291048','2024-04-06 19:56:29',1,2),(104,'success','TRANS202404062000154330','2024-04-06 20:00:15',1,2),(105,'success','TRANS202404062002355853','2024-04-06 20:02:35',1,2),(106,'success','TRANS202404062006165670','2024-04-06 20:06:16',1,2),(107,'success','TRANS202404062009437936','2024-04-06 20:09:43',1,2),(108,'success','TRANS202404062012519746','2024-04-06 20:12:51',1,2),(109,'success','TRANS202404062039447529','2024-04-06 20:39:44',1,2),(110,'success','TRANS202404062110323733','2024-04-06 21:10:32',1,2),(111,'success','TRANS202404062111441157','2024-04-06 21:11:44',1,2),(112,'success','TRANS202404062114549467','2024-04-06 21:14:54',1,2),(113,'success','TRANS202404062116049304','2024-04-06 21:16:04',1,2),(114,'success','TRANS202404062120588448','2024-04-06 21:20:58',1,2),(115,'success','TRANS202404062158148160','2024-04-06 21:58:14',1,2),(116,'success','TRANS202404062159512040','2024-04-06 21:59:51',1,2),(117,'success','TRANS202404062200284837','2024-04-06 22:00:28',1,2),(118,'success','TRANS202404062238209820','2024-04-06 22:38:20',1,2),(119,'success','TRANS202404062337052052','2024-04-06 23:37:05',1,2),(120,'success','TRANS202404070018096112','2024-04-07 00:18:09',1,2),(121,'pending',NULL,'2024-04-07 01:37:58',1,NULL),(122,'pending',NULL,'2024-04-07 11:26:26',1,NULL),(123,'success','TRANS202404071235581296','2024-04-07 12:35:58',1,2),(124,'pending',NULL,'2024-04-07 13:04:08',1,NULL),(125,'success','TRANS202404071306536986','2024-04-07 13:06:53',1,2),(126,'pending',NULL,'2024-04-07 13:11:50',1,NULL),(127,'success','TRANS202404071314556438','2024-04-07 13:14:55',1,2),(128,'success','TRANS202404071316396441','2024-04-07 13:16:39',1,2),(129,'success','TRANS202404071317467217','2024-04-07 13:17:46',1,2),(130,'success','TRANS202404071401067950','2024-04-07 14:01:06',1,2),(131,'success','TRANS202404071950007019','2024-04-07 19:50:00',1,2),(132,'success','TRANS202404072346402096','2024-04-07 23:46:40',1,2),(133,'success','TRANS202404081133461888','2024-04-08 11:33:46',1,2),(134,'success','TRANS202404081727536286','2024-04-08 17:27:53',1,2),(135,'success','TRANS202404081936482755','2024-04-08 19:36:48',1,2),(136,'success','TRANS202404082216327058','2024-04-08 22:16:32',1,2),(137,'pending',NULL,'2024-04-09 18:44:16',1,NULL),(138,'success','TRANS202404192358561331','2024-04-19 23:58:56',1,2);
/*!40000 ALTER TABLE `payment_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_number` varchar(16) NOT NULL,
  `expiry_date` varchar(7) NOT NULL,
  `cvv` varchar(3) NOT NULL,
  `payment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,'679585850','86858','675','2024-03-27 17:29:37'),(2,'679585850','86858','675','2024-03-27 17:32:05'),(3,'678747473746','577564','657','2024-03-27 17:32:32'),(4,'8364353745','833468','926','2024-03-27 17:38:04'),(5,'384575324','79468','747','2024-03-27 17:48:10'),(6,'384575324','79468','747','2024-03-27 17:48:16'),(7,'78468326','264479','793','2024-03-27 17:50:40'),(8,'78468326','264479','793','2024-03-27 17:53:08'),(9,'794586863','89347','793','2024-03-27 17:53:33'),(10,'794586863','89347','793','2024-03-27 17:54:15'),(11,'57589955869','086857','786','2024-03-27 17:59:34'),(12,'656859556','467575','456','2024-03-27 18:03:03'),(13,'76486869','64565','575','2024-03-27 18:04:28'),(14,'76486869','64565','575','2024-03-27 18:05:18'),(15,'46545686','546575','356','2024-03-27 18:05:50'),(16,'6834575','728223','783','2024-03-27 18:09:20'),(17,'6856846343','793464','343','2024-03-27 18:11:57'),(18,'6856846343','793464','343','2024-03-27 18:14:46'),(19,'79234682','493493','793','2024-03-27 18:15:15'),(20,'784639694','73846','793','2024-03-27 18:17:24'),(21,'738468','739648','794','2024-03-27 18:19:30'),(22,'738463567983','7836','793','2024-03-27 18:27:01'),(23,'36856358','79344','794','2024-03-27 18:29:26'),(24,'73946836','934793','848','2024-03-27 18:38:34'),(25,'73946836','934793','848','2024-03-27 18:39:18'),(26,'937583684','79346','794','2024-03-27 18:39:41'),(27,'78364834','79349','797','2024-03-27 18:40:45'),(28,'7936483648','037493','937','2024-03-27 18:42:12'),(29,'94783648','792494','234','2024-03-27 18:44:03'),(30,'7926482548','729479','123','2024-03-27 18:46:08'),(31,'82648254','7924682','123','2024-03-27 18:46:48'),(32,'7936493696','68246','234','2024-03-27 18:50:39'),(33,'57577474','868585','686','2024-03-27 18:57:22'),(34,'683463854','794692','434','2024-03-27 19:23:51'),(35,'793658396','79347','793','2024-03-27 19:41:36'),(36,'793658396','79347','793','2024-03-27 19:41:36'),(37,'79364869','803743','343','2024-03-27 19:43:44'),(38,'79364869','803743','343','2024-03-27 19:43:44'),(39,'79364869','803743','343','2024-03-27 19:46:52'),(40,'79364869','803743','343','2024-03-27 19:46:52'),(41,'686958585','7869','787','2024-03-27 19:48:44'),(42,'785764674','6868','868','2024-03-27 19:58:43'),(43,'79579347','3974','793','2024-03-27 20:05:19'),(44,'68585','7943','794','2024-03-27 20:08:14'),(45,'6836583','7397','793','2024-03-27 20:11:48'),(46,'6836483','79347','243','2024-03-27 20:14:09'),(47,'6836483','79347','243','2024-03-27 20:14:48'),(48,'683468364','68364','738','2024-03-27 20:25:17'),(49,'683468364','68364','738','2024-03-27 20:30:02'),(50,'79356396','79374','834','2024-03-27 20:30:30'),(51,'6834638463','739474','243','2024-03-27 20:35:52'),(52,'6834638463','739474','243','2024-03-27 20:36:27'),(53,'783658','93759','856','2024-03-27 20:37:01'),(54,'6868683','79479','343','2024-03-27 20:39:26'),(55,'6868683','79479','343','2024-03-27 20:40:04'),(56,'7386384','347397','739','2024-03-27 20:40:33'),(57,'68483628','7944','793','2024-03-27 20:45:43');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `refund_status`
--

DROP TABLE IF EXISTS `refund_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `refund_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transaction_id` varchar(255) DEFAULT NULL,
  `bank_account` varchar(255) DEFAULT NULL,
  `account_name` varchar(255) DEFAULT NULL,
  `account_number` varchar(255) DEFAULT NULL,
  `retype_account_number` varchar(255) DEFAULT NULL,
  `ifsc_code` varchar(20) DEFAULT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refund_status`
--

LOCK TABLES `refund_status` WRITE;
/*!40000 ALTER TABLE `refund_status` DISABLE KEYS */;
INSERT INTO `refund_status` VALUES (1,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-04 14:24:41'),(2,'8','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 04:40:50'),(3,'7','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 04:44:38'),(4,'2','682672554756',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 04:49:27'),(5,'2','682672554756',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 04:51:28'),(6,'2','862864836423',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 04:53:58'),(7,'TRANS202403282136072527','67458528583',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:26:16'),(8,'TRANS202403282136072527','6785658484648',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:29:40'),(9,'TRANS202403282136072527','6785658484648',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:38:25'),(10,'TRANS202403282202373879','67458528583',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:38:31'),(11,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:39:35'),(12,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:39:42'),(13,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:41:26'),(14,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:43:33'),(15,'TRANS202403282202373879','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:44:19'),(16,'TRANS202403282136072527','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 05:44:58'),(17,'TRANS202403282136072527','68676437674',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 13:46:38'),(18,'TRANS202404082216327058','67957684574',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-08 16:47:16'),(19,'','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-09 06:52:20'),(20,'TRANS202403282202373879','6357455375726',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-09 06:52:33'),(21,'TRANS202404192358561331','6785658484648',NULL,NULL,NULL,NULL,NULL,NULL,'pending','2024-04-19 18:29:50');
/*!40000 ALTER TABLE `refund_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `top_destinations`
--

DROP TABLE IF EXISTS `top_destinations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `top_destinations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_name` varchar(255) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `top_destinations`
--

LOCK TABLES `top_destinations` WRITE;
/*!40000 ALTER TABLE `top_destinations` DISABLE KEYS */;
INSERT INTO `top_destinations` VALUES (1,'United States','static\\destination-1.jpg'),(2,'United Kingdom','static/destination-2.jpg'),(3,'Australia','static/destination-3.jpg'),(4,'India','static/destination-4.jpg'),(5,'South Africa','static/destination-5.jpg'),(6,'Indonesia','static/destination-6.jpg');
/*!40000 ALTER TABLE `top_destinations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tour_packages`
--

DROP TABLE IF EXISTS `tour_packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour_packages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `days` int NOT NULL,
  `ratings` decimal(3,2) DEFAULT '0.00',
  `price` decimal(10,2) NOT NULL,
  `guest_count` int DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour_packages`
--

LOCK TABLES `tour_packages` WRITE;
/*!40000 ALTER TABLE `tour_packages` DISABLE KEYS */;
INSERT INTO `tour_packages` VALUES (1,'Thailand','static/package-1.jpg',3,4.50,75000.00,2),(2,'France','static/package-2.jpg',5,4.80,60000.00,4),(3,'Japan','static/package-3.jpg',7,4.70,250000.00,3),(4,'Italy','static/package-4.jpg',4,4.60,145000.00,2),(5,'Australia','static/package-5.jpg',6,4.90,190000.00,5),(6,'Canada','static/package-6.jpg',8,4.40,145000.00,6);
/*!40000 ALTER TABLE `tour_packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `otp` varchar(6) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `login_status` enum('logged_in','logged_out') DEFAULT 'logged_out',
  `total_budget` decimal(10,2) DEFAULT NULL,
  `total_guests` int DEFAULT '0',
  `profile_picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Abhi','abhi123','','785024','2024-03-18 12:26:24','2024-03-27 06:25:47','logged_in',NULL,0,NULL),(2,'abhi1','abhi1234','','862932','2024-03-18 13:08:55','2024-06-18 05:44:56','logged_in',200000.00,0,NULL),(3,'123','123','',NULL,'2024-03-18 21:24:32','2024-03-18 21:24:40','logged_in',NULL,0,NULL),(4,'abhi123','Abhi123','',NULL,'2024-04-05 05:34:54','2024-04-05 05:42:06','logged_in',NULL,0,NULL),(5,'abhi1234','abhi1234','','862932','2024-04-08 06:53:31','2024-04-08 16:35:42','logged_out',NULL,0,NULL),(6,'abhi1234','abhi12345','','862932','2024-04-08 07:42:15','2024-04-08 16:35:42','logged_out',NULL,0,NULL),(7,'abhi1234','abhi1234','','862932','2024-04-08 13:47:33','2024-04-08 16:35:42','logged_out',NULL,0,NULL),(8,'abhi123','abhi134','a',NULL,'2024-04-08 14:05:56','2024-04-08 14:05:56','logged_out',NULL,0,NULL),(9,'abhi123','abhi12','a',NULL,'2024-04-08 15:27:55','2024-04-08 15:37:28','logged_out',NULL,0,'blob'),(10,'abhi10','abhi1','a',NULL,'2024-04-08 15:38:45','2024-04-08 15:50:54','logged_in',NULL,0,'UPLOAD_FOLDER\\blob'),(11,'abhi10','abhi1','a',NULL,'2024-04-08 15:42:44','2024-04-08 15:42:44','logged_out',NULL,0,'UPLOAD_FOLDER/blob'),(12,'abhi123','abhi12345','a',NULL,'2024-04-08 15:52:31','2024-04-08 15:52:31','logged_out',NULL,0,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-20  8:14:05
