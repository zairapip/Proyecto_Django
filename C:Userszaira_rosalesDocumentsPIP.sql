-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: PIP
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `Taddress`
--

DROP TABLE IF EXISTS `Taddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Taddress` (
  `code_address` varchar(20) NOT NULL,
  `street` varchar(50) NOT NULL,
  `gate` varchar(50) NOT NULL,
  `floor` varchar(10) NOT NULL,
  `door` varchar(10) NOT NULL,
  `local` varchar(10) NOT NULL,
  `cpostal` varchar(10) NOT NULL,
  `wo_lift` tinyint(1) NOT NULL,
  PRIMARY KEY (`code_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Taddress`
--

LOCK TABLES `Taddress` WRITE;
/*!40000 ALTER TABLE `Taddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `Taddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tconnect`
--

DROP TABLE IF EXISTS `Tconnect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tconnect` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `token_ph` varchar(200) NOT NULL,
  `connect` tinyint(1) NOT NULL,
  `position` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tconnect`
--

LOCK TABLES `Tconnect` WRITE;
/*!40000 ALTER TABLE `Tconnect` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tconnect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Torders`
--

DROP TABLE IF EXISTS `Torders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Torders` (
  `code_order` varchar(20) NOT NULL,
  `pay` double NOT NULL,
  `application` datetime(6) NOT NULL,
  `pickup` datetime(6) NOT NULL,
  `delivery` datetime(6) NOT NULL,
  `code_address_id` varchar(20) DEFAULT NULL,
  `code_rider_id` varchar(20) DEFAULT NULL,
  `code_sender_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`code_order`),
  UNIQUE KEY `code_address_id` (`code_address_id`),
  KEY `Torders_code_rider_id_bf7b3f8c_fk_Triders_code_rider` (`code_rider_id`),
  KEY `Torders_code_sender_id_12d96767_fk_Tsenders_code_sender` (`code_sender_id`),
  CONSTRAINT `Torders_code_address_id_7752d44a_fk_Taddress_code_address` FOREIGN KEY (`code_address_id`) REFERENCES `Taddress` (`code_address`),
  CONSTRAINT `Torders_code_rider_id_bf7b3f8c_fk_Triders_code_rider` FOREIGN KEY (`code_rider_id`) REFERENCES `Triders` (`code_rider`),
  CONSTRAINT `Torders_code_sender_id_12d96767_fk_Tsenders_code_sender` FOREIGN KEY (`code_sender_id`) REFERENCES `Tsenders` (`code_sender`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Torders`
--

LOCK TABLES `Torders` WRITE;
/*!40000 ALTER TABLE `Torders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Torders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Triders`
--

DROP TABLE IF EXISTS `Triders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Triders` (
  `code_rider` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surnames` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  `telephone` int NOT NULL,
  `token_ph` varchar(200) NOT NULL,
  `connect` tinyint(1) NOT NULL,
  `code_address_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`code_rider`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `code_address_id` (`code_address_id`),
  CONSTRAINT `Triders_code_address_id_4b4d9d8c_fk_Taddress_code_address` FOREIGN KEY (`code_address_id`) REFERENCES `Taddress` (`code_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Triders`
--

LOCK TABLES `Triders` WRITE;
/*!40000 ALTER TABLE `Triders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Triders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tsenders`
--

DROP TABLE IF EXISTS `Tsenders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tsenders` (
  `code_sender` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  `telephone` int NOT NULL,
  `token_ph` varchar(200) NOT NULL,
  `qualification` int NOT NULL,
  `code_address_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`code_sender`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `code_address_id` (`code_address_id`),
  CONSTRAINT `Tsenders_code_address_id_05101d8c_fk_Taddress_code_address` FOREIGN KEY (`code_address_id`) REFERENCES `Taddress` (`code_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tsenders`
--

LOCK TABLES `Tsenders` WRITE;
/*!40000 ALTER TABLE `Tsenders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tsenders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tsessions`
--

DROP TABLE IF EXISTS `Tsessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tsessions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `token_access` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tsessions`
--

LOCK TABLES `Tsessions` WRITE;
/*!40000 ALTER TABLE `Tsessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tsessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Twolifts`
--

DROP TABLE IF EXISTS `Twolifts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Twolifts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gate` varchar(50) NOT NULL,
  `street` varchar(200) NOT NULL,
  `lift` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Twolifts`
--

LOCK TABLES `Twolifts` WRITE;
/*!40000 ALTER TABLE `Twolifts` DISABLE KEYS */;
/*!40000 ALTER TABLE `Twolifts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add tconnect',7,'add_tconnect'),(26,'Can change tconnect',7,'change_tconnect'),(27,'Can delete tconnect',7,'delete_tconnect'),(28,'Can view tconnect',7,'view_tconnect'),(29,'Can add tsession',8,'add_tsession'),(30,'Can change tsession',8,'change_tsession'),(31,'Can delete tsession',8,'delete_tsession'),(32,'Can view tsession',8,'view_tsession'),(33,'Can add twolifts',9,'add_twolifts'),(34,'Can change twolifts',9,'change_twolifts'),(35,'Can delete twolifts',9,'delete_twolifts'),(36,'Can view twolifts',9,'view_twolifts'),(37,'Can add taddress',10,'add_taddress'),(38,'Can change taddress',10,'change_taddress'),(39,'Can delete taddress',10,'delete_taddress'),(40,'Can view taddress',10,'view_taddress'),(41,'Can add triders',11,'add_triders'),(42,'Can change triders',11,'change_triders'),(43,'Can delete triders',11,'delete_triders'),(44,'Can view triders',11,'view_triders'),(45,'Can add torders',12,'add_torders'),(46,'Can change torders',12,'change_torders'),(47,'Can delete torders',12,'delete_torders'),(48,'Can view torders',12,'view_torders'),(49,'Can add tsenders',13,'add_tsenders'),(50,'Can change tsenders',13,'change_tsenders'),(51,'Can delete tsenders',13,'delete_tsenders'),(52,'Can view tsenders',13,'view_tsenders');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$MFdyrc6PDnz9WgvUKEbfpy$7/M85fDpVysM7ZC3zRqLG+ZzUiL0nEpmEVhZP5wqvVI=',NULL,1,'zaira','','','',1,1,'2024-02-24 15:34:06.405400');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(10,'PIP01app','taddress'),(7,'PIP01app','tconnect'),(12,'PIP01app','torders'),(11,'PIP01app','triders'),(13,'PIP01app','tsenders'),(8,'PIP01app','tsession'),(9,'PIP01app','twolifts'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-02-24 15:29:24.344861'),(2,'auth','0001_initial','2024-02-24 15:29:25.144651'),(3,'admin','0001_initial','2024-02-24 15:29:25.348869'),(4,'admin','0002_logentry_remove_auto_add','2024-02-24 15:29:25.367153'),(5,'admin','0003_logentry_add_action_flag_choices','2024-02-24 15:29:25.384895'),(6,'contenttypes','0002_remove_content_type_name','2024-02-24 15:29:25.522158'),(7,'auth','0002_alter_permission_name_max_length','2024-02-24 15:29:25.617729'),(8,'auth','0003_alter_user_email_max_length','2024-02-24 15:29:25.664705'),(9,'auth','0004_alter_user_username_opts','2024-02-24 15:29:25.686997'),(10,'auth','0005_alter_user_last_login_null','2024-02-24 15:29:25.766770'),(11,'auth','0006_require_contenttypes_0002','2024-02-24 15:29:25.774676'),(12,'auth','0007_alter_validators_add_error_messages','2024-02-24 15:29:25.795751'),(13,'auth','0008_alter_user_username_max_length','2024-02-24 15:29:25.897922'),(14,'auth','0009_alter_user_last_name_max_length','2024-02-24 15:29:26.003175'),(15,'auth','0010_alter_group_name_max_length','2024-02-24 15:29:26.042477'),(16,'auth','0011_update_proxy_permissions','2024-02-24 15:29:26.063841'),(17,'auth','0012_alter_user_first_name_max_length','2024-02-24 15:29:26.159535'),(18,'sessions','0001_initial','2024-02-24 15:29:26.223178'),(19,'PIP01app','0001_initial','2024-03-03 10:28:11.135168');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-03 13:40:46
