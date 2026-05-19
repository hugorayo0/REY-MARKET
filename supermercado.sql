CREATE DATABASE  IF NOT EXISTS `supermercado` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `supermercado`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: supermercado
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL,
  `categoria` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'verduras'),(2,'refrescos'),(3,'lacteos'),(4,'panaderia'),(5,'pasta'),(6,'fruta'),(7,'carne'),(8,'conservas');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `descuentos`
--

DROP TABLE IF EXISTS `descuentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `descuentos` (
  `id_descuento` int NOT NULL AUTO_INCREMENT,
  `descuento` int DEFAULT NULL,
  `tipo_descuento` enum('porcentaje') DEFAULT NULL,
  PRIMARY KEY (`id_descuento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descuentos`
--

LOCK TABLES `descuentos` WRITE;
/*!40000 ALTER TABLE `descuentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `descuentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direcciones`
--

DROP TABLE IF EXISTS `direcciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direcciones` (
  `id_direccion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `calle_entrega` varchar(45) NOT NULL,
  `piso_entrega` int NOT NULL,
  `puerta_entrega` varchar(5) NOT NULL,
  `localidad_entrega` varchar(45) NOT NULL,
  `provincia_entrega` varchar(45) NOT NULL,
  `cp_entrega` int NOT NULL,
  PRIMARY KEY (`id_direccion`),
  KEY `id_usuario_usuarios_idx` (`id_usuario`),
  CONSTRAINT `id_usuario_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones`
--

LOCK TABLES `direcciones` WRITE;
/*!40000 ALTER TABLE `direcciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `direcciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL,
  `id_usuario` int NOT NULL,
  `precio_total` decimal(10,2) DEFAULT NULL,
  `fecha_pedido` datetime DEFAULT NULL,
  `estado` enum('pendiente','enviado','entregado') DEFAULT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_usuario_idx` (`id_usuario`),
  CONSTRAINT `id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `precio_unidad` decimal(10,2) DEFAULT NULL,
  `unidad_medida` enum('kg','unidad','litro','docena','pack') DEFAULT NULL,
  `url_imagen` varchar(100) DEFAULT NULL,
  `id_categoria` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `id_categoria_categorias_idx` (`id_categoria`),
  CONSTRAINT `id_categoria_categorias` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Manzanas',1.50,'kg','manzana.jpg',6),(2,'Pan',0.80,'unidad','barra-de-pan-integral-de-90-gr.jpg',4),(3,'Leche',1.00,'litro','leche.jpg',3),(4,'Docena de Huevos',3.99,'docena','docena-de-huevos-l-12-und.jpg',3),(5,'Macarrones 500g',2.49,'unidad','macarrones.jpg',5),(6,'Coca Cola',2.00,'unidad','coca-cola-2-l.jpg',2),(7,'Plátanos',1.20,'kg','banane-large.jpg',6),(8,'Naranjas',1.80,'unidad','naranjas.webp',6),(9,'Tomates',2.10,'unidad','tomates.jpg',1),(10,'Cebollas',0.90,'kg','cebollas.jpg',1),(11,'Patatas',1.10,'kg','patatas.jpg',1),(12,'Queso Tierno',4.50,'unidad','queso.jpg',3),(13,'Yogur Natural (pack 4)',1.60,'pack','yogur.jpg',3),(14,'Pechuga de Pollo',5.99,'unidad','pechuga-pollo.jpg',7),(15,'Carne Picada 400g',3.80,'unidad','carne-picada.jpg',7),(16,'Croissants (pack 4)',1.90,'pack','curasan.jpg',4),(17,'Espaguetis 500g',1.99,'unidad','spagettis.webp',5),(18,'Agua 1.5L',3.00,'unidad','agua.jpg',2),(19,'Zumo de Naranja 1L',1.75,'unidad','zumo-naranja.jpg',2),(20,'Atún en Lata (pack 3)',6.00,'pack','atun-claro-aceite-oliva-ortiz-pack-3-latas.webp',8),(21,'Tomate Frito 400g',1.20,'unidad','tomate-frito-orlando.jpg',8),(22,'Peras',1.60,'kg','pera-conferencia-product.webp',6),(23,'Fresas 500g',2.50,'unidad','fresas-en-bandeja.jpeg',6),(24,'Melón',1.30,'kg','melon.jpg',6),(25,'Lechuga',0.99,'unidad','lechuga.jpg',1),(26,'Zanahorias 1kg',1.20,'unidad','zanahorias.webp',1),(27,'Pimientos (pack 3)',1.80,'kg','pimientos.jpg',1),(28,'Pepino',0.70,'unidad','pepino.jpg',1),(29,'Mantequilla 250g',2.10,'unidad','mantequilla.jpg',3),(30,'Nata para Cocinar',1.40,'unidad','nata.jpg',3),(31,'Pan de Molde',1.50,'unidad','BIMBO-GRANDE.png',4),(32,'Magdalenas (pack 6)',1.80,'pack','magdalenas.jpg',4),(33,'Arroz 1kg',1.50,'unidad','arroz-sos-1kg.jpg',5),(34,'Avena 500g',1.90,'unidad','copos-de-avena-500g-legumbres-guillermo-scaled.jpg',5),(35,'Salchichas (pack 8)',2.80,'pack','salchicha.jpg',7),(36,'Jamón Cocido 200g',2.50,'unidad','jamon-cocido.avif',7),(37,'Fanta Naranja 2L',1.80,'unidad','Fanta-Naranja-2500ml.jpg',2),(38,'Fuze Tea 1.5L',1.60,'unidad','fuze-tea.jpg',2),(39,'Lentejas en Lata',3.10,'unidad','lentejas.avif',8),(40,'Sardinas en Aceite',3.30,'unidad','sardinas.webp',8),(41,'Uvas',2.20,'kg','uvas.jpg',6),(42,'Garbanzos en Lata 400g',1.05,'unidad','garbanzos-420g.png',8);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_pedidos`
--

DROP TABLE IF EXISTS `productos_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_pedidos` (
  `id_pedido` int NOT NULL,
  `id_producto` int NOT NULL,
  PRIMARY KEY (`id_pedido`,`id_producto`),
  KEY `id_producto_productos_idx` (`id_producto`),
  CONSTRAINT `id_pedido_pedidos` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `id_producto_productos` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_pedidos`
--

LOCK TABLES `productos_pedidos` WRITE;
/*!40000 ALTER TABLE `productos_pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `apellido1` varchar(40) NOT NULL,
  `apellido2` varchar(40) NOT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `contraseña` varchar(128) NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `tipo_usuario` enum('cliente','administrador') NOT NULL DEFAULT 'cliente',
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Paul','Perez','Lopez','prueba@example.com','ea7e66d2cf5ce306d4e475c53bb96dc5a04df4aa459b8c3f74caff09b34fed32','2026-05-15 16:27:57','cliente');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trigger_usuario_before_insert` BEFORE INSERT ON `usuarios` FOR EACH ROW begin
	if char_length(new.contraseña) < 8 or char_length(new.contraseña) > 64 then
		signal sqlstate '45000'
        set message_text = "La contraseña debe tener entre 8 y 64 caracteres";
	end if;
    
	if new.correo is null then
		call generar_correo(new.nombre, new.apellido1, "reymarket.es", @correo_creado);
		set new.correo = @correo_creado;
        set new.tipo_usuario = 'administrador';
    end if;
    if new.tipo_usuario != 'cliente' then
		set new.contraseña = SHA2(new.contraseña, 256);
	end if;
    if new.fecha_registro is null then
		set new.fecha_registro = now();
    end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trigger_usuarios_before_update` BEFORE UPDATE ON `usuarios` FOR EACH ROW begin
	if char_length(new.contraseña) < 8 or char_length(new.contraseña) > 64 then
		signal sqlstate '45000'
        set message_text = "La contraseña debe tener entre 8 y 64 caracteres";
	end if;
    
    set new.contraseña = SHA2(new.contraseña, 256);
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `vista_productos`
--

DROP TABLE IF EXISTS `vista_productos`;
/*!50001 DROP VIEW IF EXISTS `vista_productos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_productos` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre`,
 1 AS `precio_unidad`,
 1 AS `unidad_medida`,
 1 AS `url_imagen`,
 1 AS `categoria`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'supermercado'
--

--
-- Dumping routines for database 'supermercado'
--
/*!50003 DROP FUNCTION IF EXISTS `eliminar_acentos` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `eliminar_acentos`(texto varchar(255)) RETURNS varchar(255) CHARSET utf8mb4
    DETERMINISTIC
begin
	declare resultado varchar(255);
    set resultado = lower(texto);
    set resultado = replace(resultado, "á", "a");
    set resultado = replace(resultado, "é", "e");
    set resultado = replace(resultado, "í", "i");
    set resultado = replace(resultado, "ó", "o");
    set resultado = replace(resultado, "ú", "u");
    
    return resultado;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `generar_correo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `generar_correo`(
in p_nombre varchar(255),
in p_apellido1 varchar(255),
in p_dominio varchar(255),
out p_correo varchar(255))
begin
	set p_nombre = eliminar_acentos(p_nombre);
    set p_apellido1 = eliminar_acentos(p_apellido1);
    set p_correo = concat(lower(concat(left(p_nombre, 1), p_apellido1)), "@", p_dominio);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `vista_productos`
--

/*!50001 DROP VIEW IF EXISTS `vista_productos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_productos` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre`,`p`.`precio_unidad` AS `precio_unidad`,`p`.`unidad_medida` AS `unidad_medida`,`p`.`url_imagen` AS `url_imagen`,`c`.`categoria` AS `categoria` from (`productos` `p` left join `categorias` `c` on((`p`.`id_categoria` = `c`.`id_categoria`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-18 10:36:56
