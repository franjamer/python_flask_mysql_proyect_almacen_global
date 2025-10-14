CREATE DATABASE  IF NOT EXISTS `almacenrepuestos` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_es_trad_0900_as_cs */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `almacenrepuestos`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: almacenrepuestos
-- ------------------------------------------------------
-- Server version	8.4.4

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
-- Table structure for table `categorias_repuestos_tabla`
--

DROP TABLE IF EXISTS `categorias_repuestos_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_repuestos_tabla` (
  `idcategorias_repuestos_tabla` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `codigo_categoria` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `subcategoria` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`idcategorias_repuestos_tabla`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_repuestos_tabla`
--

LOCK TABLES `categorias_repuestos_tabla` WRITE;
/*!40000 ALTER TABLE `categorias_repuestos_tabla` DISABLE KEYS */;
INSERT INTO `categorias_repuestos_tabla` VALUES (1,'MECANICO','MEC',NULL),(2,'ELECTRICO','ELEC',NULL),(3,'FONTANERIA','FONT',NULL);
/*!40000 ALTER TABLE `categorias_repuestos_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabricante_tabla`
--

DROP TABLE IF EXISTS `fabricante_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fabricante_tabla` (
  `idfabricante` int NOT NULL AUTO_INCREMENT,
  `nombre_fabricante` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `proveedor` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `categoria` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`idfabricante`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fabricante_tabla`
--

LOCK TABLES `fabricante_tabla` WRITE;
/*!40000 ALTER TABLE `fabricante_tabla` DISABLE KEYS */;
INSERT INTO `fabricante_tabla` VALUES (1,'fabricante1',NULL,NULL),(2,'fabricante2',NULL,NULL),(3,'fabricante3',NULL,NULL);
/*!40000 ALTER TABLE `fabricante_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_tabla`
--

DROP TABLE IF EXISTS `inventario_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_tabla` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `referencia` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `subcategoria` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `caracteristicas_medidas` varchar(25) COLLATE utf8mb4_spanish2_ci DEFAULT NULL,
  `fotos_planos` varchar(255) COLLATE utf8mb4_spanish2_ci DEFAULT NULL,
  `empaquetado` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `stock` int DEFAULT '0',
  `stock_minimo` int DEFAULT '0',
  `stock_maximo` int DEFAULT '0',
  `id_situacion_tabla` int DEFAULT NULL,
  `id_prov` int DEFAULT NULL,
  PRIMARY KEY (`id`,`referencia`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `referencia_UNIQUE` (`referencia`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `referencia` (`referencia`),
  KEY `idx_situacion` (`id_situacion_tabla`),
  KEY `fk_inventario_proveedor` (`id_prov`),
  CONSTRAINT `fk_inventario_proveedor` FOREIGN KEY (`id_prov`) REFERENCES `proveedores` (`id_prov`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_tabla`
--

LOCK TABLES `inventario_tabla` WRITE;
/*!40000 ALTER TABLE `inventario_tabla` DISABLE KEYS */;
INSERT INTO `inventario_tabla` VALUES (38,'c191626','6mm 5.5mm Round button 50 mA surface Mount,vertical 6mm SPST','Pulsadores','smd','6x5.5','a','unitario',6,1,1,1,NULL),(39,'c328592','1n4007w 1A Independient 1kV 1.1v@1A sod-123fl Diodes-general Purpose ROHS','Diodos','General','1','','unidad',38,10,50,2,NULL),(40,'c20616319','2n222A 40V 625mW 600mA NPN TO-92 Bipolar bjt ROHS','Transistores','BJT_NPN','TO_92','A','unitario',36,10,100,4,NULL),(41,'c136460','Resistencia 10KOhms 200V+-5 1206','Resistencias','SMD','1206','A','Reel',90,10,200,5,NULL),(42,'c2907440','Resistencia 1 KOhms 200V','Resistencias','SMD','1206','A','Reel',90,10,200,4,NULL),(43,'c976324','DIP Switch 2 bit spst slide KF1001-02P-R0-FL-ON-01B 2Bit SPST Slide(Standard),Plugin DIPsWITCHES ROHS','Interruptores','TH','PLUGIN DIP','A','UNITARIO',6,1,10,13,NULL),(44,'C311517','Capacitor 100uF 10V','Condensador','SMD','A-3216','A','REEL',19,5,20,13,NULL),(45,'c7187','Capacitor 4.7uF 16v +-10%','Condensador','SMD','A-3216','A','Reel',11,1,100,2,NULL),(46,'c2688239','ams1117-3.3v 1A positive 12v sot223-3l','Regulador de Voltaje','reel','SOT-223-3L','A','Reel',8,1,20,4,1),(47,'c310817','interruptor 100mA 3polos-1fila','Interruptor','TH','streiht','a','1',13,1,10,4,1),(48,'c2921034','bc817-10','TRANSISTOR','BJT_NPN','SOT-23','A','SMD',42,10,100,4,1),(49,'C489160','BC817-40 45V 300mW 250@100mA, 1V 500 mASOT-23 Bipolar Transistors-BJT ROHS','Transistor BJT','SMD','SOT-23','A','REEL',16,1,20,2,1),(50,'C84681','CH340C 2Mps Transceiver USB 2.0 SOP-16 USB ICs ROHS','TRANSCEPTOR','SMD','SOP-16','A','REEL',3,1,20,13,1),(51,'C128319','CAPACITOR 1uF 25V+-10% TANTALIO','Condensador','smd','A-3216','A','REEL',8,1,20,6,1),(52,'c17702043','AMS1117-3.3V 1A 12V','Regulador de Voltaje','SMD','SOT-223','A','REEL',9,1,20,20,1),(55,'C313517','Condensador Tantalio 100uFTLJA 107M010R1400 100uF 10V 1.4 Ohms@100kH +-20% CASE-A-3216  Tantalum Capacitors ROHS','Condensador','smd','3216','a','reel',13,2,20,20,1);
/*!40000 ALTER TABLE `inventario_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lineas_pedido_tabla`
--

DROP TABLE IF EXISTS `lineas_pedido_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lineas_pedido_tabla` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `referencia_articulo` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `nombre_articulo` varchar(255) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `cantidad_pedida` int NOT NULL,
  `cantidad_recibida` int DEFAULT '0',
  `fecha_recibido` date DEFAULT NULL,
  `completo` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `lineas_pedido_tabla_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos_global_tabla` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lineas_pedido_tabla`
--

LOCK TABLES `lineas_pedido_tabla` WRITE;
/*!40000 ALTER TABLE `lineas_pedido_tabla` DISABLE KEYS */;
INSERT INTO `lineas_pedido_tabla` VALUES (12,20,'c2921034','bc817-10',5,9,'2025-10-01',0);
/*!40000 ALTER TABLE `lineas_pedido_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lineas_produccion`
--

DROP TABLE IF EXISTS `lineas_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lineas_produccion` (
  `idsubcategorias` int NOT NULL AUTO_INCREMENT,
  `subcategoriasnombre` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `categoria` varchar(45) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`idsubcategorias`),
  UNIQUE KEY `idsubcategorias_UNIQUE` (`idsubcategorias`),
  CONSTRAINT `categorias_fk` FOREIGN KEY (`idsubcategorias`) REFERENCES `categorias_repuestos_tabla` (`idcategorias_repuestos_tabla`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs COMMENT='indica un segundo nivel de clasificación dentro de categorias';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lineas_produccion`
--

LOCK TABLES `lineas_produccion` WRITE;
/*!40000 ALTER TABLE `lineas_produccion` DISABLE KEYS */;
INSERT INTO `lineas_produccion` VALUES (1,'IPI',NULL),(2,'COMBI',NULL),(3,'TETRAPAK',NULL);
/*!40000 ALTER TABLE `lineas_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_tabla`
--

DROP TABLE IF EXISTS `movimientos_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_tabla` (
  `idmovimientos` int NOT NULL AUTO_INCREMENT,
  `nombre_pieza_repuesto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_de_movimiento` enum('salida','entrada','inventario') CHARACTER SET utf8mb4 COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `cantidad` int NOT NULL,
  `unidad_de_cantidad` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT 'UNIDAD',
  `codigo_operador` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `fecha_movimiento` date DEFAULT NULL,
  `stock_tras_movimiento` int DEFAULT NULL,
  `referencia_pieza_repuesto` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idmovimientos`,`codigo_operador`),
  KEY `fk_nombre_pieza_repuesto` (`nombre_pieza_repuesto`) /*!80000 INVISIBLE */,
  KEY `fk_referencia_pieza` (`referencia_pieza_repuesto`),
  CONSTRAINT `fk_nombre_pieza_repuesto` FOREIGN KEY (`nombre_pieza_repuesto`) REFERENCES `inventario_tabla` (`nombre`),
  CONSTRAINT `fk_referencia_pieza` FOREIGN KEY (`referencia_pieza_repuesto`) REFERENCES `inventario_tabla` (`referencia`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_tabla`
--

LOCK TABLES `movimientos_tabla` WRITE;
/*!40000 ALTER TABLE `movimientos_tabla` DISABLE KEYS */;
INSERT INTO `movimientos_tabla` VALUES (4,'Capacitor 4.7uF 16v +-10%','entrada',8,'','FJMR','2025-09-23',11,'c7187'),(5,'Capacitor 100uF 10V','entrada',6,'','FJMR','2025-09-23',19,'C311517'),(6,'interruptor 100mA 3polos-1fila','entrada',9,'','FJMR','2025-09-23',13,'c310817');
/*!40000 ALTER TABLE `movimientos_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operadores`
--

DROP TABLE IF EXISTS `operadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operadores` (
  `id_operador` int NOT NULL AUTO_INCREMENT,
  `codigo_operador` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nombre_completo` varchar(45) DEFAULT NULL,
  `puesto` enum('electricista','mecánico','almacen') DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_operador`,`codigo_operador`),
  UNIQUE KEY `codigo_operador_UNIQUE` (`codigo_operador`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operadores`
--

LOCK TABLES `operadores` WRITE;
/*!40000 ALTER TABLE `operadores` DISABLE KEYS */;
INSERT INTO `operadores` VALUES (20,'FJMR','Francisco Javier Menayo Ramos','electricista',NULL),(21,'JCR','Juan Carlos Rincón Díaz','mecánico',NULL),(22,'JDLO','Juan De La O','mecánico',NULL),(23,'FerDi','Fernando Díaz','electricista',NULL),(25,'JG','Javier Gutierrez','electricista',NULL),(26,'Antonio','Antonio Borreguero','mecánico',NULL),(27,'Sergio','Sergio','electricista',NULL),(28,'JAPI','Jose Antonio Pitón','mecánico',NULL),(29,'Vicen','Vicente','mecánico',NULL),(30,'Manolo','Manolo','mecánico',NULL),(31,'Roberto','Roberto','electricista',NULL);
/*!40000 ALTER TABLE `operadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos_global_tabla`
--

DROP TABLE IF EXISTS `pedidos_global_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_global_tabla` (
  `id` int NOT NULL AUTO_INCREMENT,
  `referencia_pedido` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `fecha_creacion` date NOT NULL,
  `completo` tinyint(1) DEFAULT '0',
  `id_prov` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pedidos_proveedor` (`id_prov`),
  CONSTRAINT `fk_pedidos_proveedor` FOREIGN KEY (`id_prov`) REFERENCES `proveedores` (`id_prov`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_global_tabla`
--

LOCK TABLES `pedidos_global_tabla` WRITE;
/*!40000 ALTER TABLE `pedidos_global_tabla` DISABLE KEYS */;
INSERT INTO `pedidos_global_tabla` VALUES (20,'0001','2025-09-22',0,1);
/*!40000 ALTER TABLE `pedidos_global_tabla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfiles`
--

DROP TABLE IF EXISTS `perfiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfiles` (
  `id_perfil` int NOT NULL AUTO_INCREMENT,
  `perfil` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `rol` varchar(20) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL DEFAULT 'usuario',
  PRIMARY KEY (`id_perfil`),
  UNIQUE KEY `usuario` (`perfil`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfiles`
--

LOCK TABLES `perfiles` WRITE;
/*!40000 ALTER TABLE `perfiles` DISABLE KEYS */;
INSERT INTO `perfiles` VALUES (1,'Admin','Admin','admin'),(2,'Mañana','Mañana','operador'),(3,'Tarde','Tarde','operador'),(4,'Noche','Noche','operador'),(5,'Central','Central','operador'),(6,'Pedidos','Pedidos','pedidos'),(15,'Externa','Externa','operador'),(17,'Superadmin','superadmin','admin');
/*!40000 ALTER TABLE `perfiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_prov` int NOT NULL AUTO_INCREMENT,
  `nombre_prov` varchar(100) COLLATE utf8mb4_es_trad_0900_as_cs NOT NULL,
  `email_prov` varchar(100) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `telefono_prov` varchar(30) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `contacto_prov` varchar(100) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `web_prov` varchar(100) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`id_prov`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'lsc','correo@lsc.com','55555555','Chen Gun','www.lsc.com'),(2,'AlíExpress','','---','---','http://www.aliexpress.com');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `situacion_tabla`
--

DROP TABLE IF EXISTS `situacion_tabla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `situacion_tabla` (
  `id_situacion_tabla` int NOT NULL AUTO_INCREMENT,
  `almacen` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `estanteria` varchar(50) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `lado` varchar(10) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  `columna` int DEFAULT NULL,
  `altura` int DEFAULT NULL,
  `situacion_combinada` varchar(255) COLLATE utf8mb4_es_trad_0900_as_cs DEFAULT NULL,
  PRIMARY KEY (`id_situacion_tabla`),
  KEY `situacion_combinada` (`situacion_combinada`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_es_trad_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `situacion_tabla`
--

LOCK TABLES `situacion_tabla` WRITE;
/*!40000 ALTER TABLE `situacion_tabla` DISABLE KEYS */;
INSERT INTO `situacion_tabla` VALUES (1,'Principal','1','IZQ',1,1,'Principal_1_IZQ_1_1'),(2,'Principal','1','N/A',1,1,'Principal_1_N/A_1_1'),(4,'Principal','11','N/A',1,3,NULL),(5,'Principal','12','N/A',1,4,NULL),(6,'Principal','13','N/A',1,3,NULL),(13,'Principal','13','N/A',1,2,NULL),(20,'CAJA 1','MESITA','N/A',0,0,NULL),(21,'CAJA 2','Estanteria','N/A',1,2,NULL),(22,'CAJA 3','Estanteria','N/A',1,2,NULL),(23,'Oficina','ESTANTERIA','N/A',1,2,NULL),(24,'Principal','2','N/A',1,2,NULL);
/*!40000 ALTER TABLE `situacion_tabla` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 18:26:40
