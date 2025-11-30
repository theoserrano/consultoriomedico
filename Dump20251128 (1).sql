-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: consultoriomedico
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `tabelaclinica`
--

DROP TABLE IF EXISTS `tabelaclinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabelaclinica` (
  `CodCli` char(6) NOT NULL,
  `NomeCli` varchar(100) NOT NULL,
  `Endereco` varchar(255) DEFAULT NULL,
  `Telefone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CodCli`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelaclinica`
--

LOCK TABLES `tabelaclinica` WRITE;
/*!40000 ALTER TABLE `tabelaclinica` DISABLE KEYS */;
INSERT INTO `tabelaclinica` VALUES ('000001','Saúde Plus','Av. Rosa e Silva, 406, Graças','(81) 4002-3633','saudeplus@mail.com'),('000002','Visão Recife','Av. Governador Agamenon Magalhães, 810','(81) 3042-1112','visaorecife@mail.com'),('000003','Clínica Bem Estar','R. do Sol, 120, Boa Viagem','(81) 3322-1100','bemestar@mail.com'),('000004','Centro Médico Esperança','Av. Rio Branco, 45, Centro','(81) 4005-7777','contato.esperanca@mail.com');
/*!40000 ALTER TABLE `tabelaclinica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabelaconsulta`
--

DROP TABLE IF EXISTS `tabelaconsulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabelaconsulta` (
  `CodCli` char(6) NOT NULL,
  `CodMed` char(7) NOT NULL,
  `CpfPaciente` char(11) NOT NULL,
  `Data_Hora` datetime NOT NULL,
  PRIMARY KEY (`CodCli`,`CodMed`,`CpfPaciente`,`Data_Hora`),
  KEY `CodMed` (`CodMed`),
  KEY `CpfPaciente` (`CpfPaciente`),
  CONSTRAINT `tabelaconsulta_ibfk_1` FOREIGN KEY (`CodCli`) REFERENCES `tabelaclinica` (`CodCli`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tabelaconsulta_ibfk_2` FOREIGN KEY (`CodMed`) REFERENCES `tabelamedico` (`CodMed`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tabelaconsulta_ibfk_3` FOREIGN KEY (`CpfPaciente`) REFERENCES `tabelapaciente` (`CpfPaciente`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelaconsulta`
--

LOCK TABLES `tabelaconsulta` WRITE;
/*!40000 ALTER TABLE `tabelaconsulta` DISABLE KEYS */;
INSERT INTO `tabelaconsulta` VALUES ('000003','1234567','58961234752','2025-12-05 14:30:00'),('000001','2819374','58961234752','2025-11-03 15:00:00'),('000003','2819374','34512389765','2026-02-01 08:30:00'),('000002','4567890','22233344455','2025-12-20 16:00:00'),('000001','5543210','12345678900','2025-11-28 09:00:00'),('000002','8532974','34512389765','2025-12-10 16:40:00'),('000004','8765432','98765432100','2026-01-15 11:00:00'),('000002','9183424','34512389765','2026-01-05 10:30:00');
/*!40000 ALTER TABLE `tabelaconsulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabelamedico`
--

DROP TABLE IF EXISTS `tabelamedico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabelamedico` (
  `CodMed` char(7) NOT NULL,
  `NomeMed` varchar(100) NOT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Telefone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Especialidade` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodMed`),
  CONSTRAINT `tabelamedico_chk_1` CHECK ((`Genero` in (_utf8mb4'F',_utf8mb4'M')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelamedico`
--

LOCK TABLES `tabelamedico` WRITE;
/*!40000 ALTER TABLE `tabelamedico` DISABLE KEYS */;
INSERT INTO `tabelamedico` VALUES ('1234567','Pedro Souza','M','(81) 99876-5432','pedro.souza@mail.com','Ortopedia'),('2819374','Marcela Gomes','F','(81) 98273-3245','marcelagomes@mail.com','Pediatria'),('4567890','Ricardo Melo','M','(81) 97777-1111','ricardo.melo@mail.com','Pediatria'),('5543210','Juliana Costa','F','(81) 98765-4321','juliana.costa@mail.com','Ginecologia'),('5793149','Amanda Vieira','F','(81) 99240-2571','fernandavieira@mail.com','Pediatria'),('8532974','Lucas Carvalho','M','(81) 98256-5703','lucascarvalho@mail.com','Oftalmologia'),('8765432','Fernanda Lima','F','(81) 98123-4567','fernanda.lima@mail.com','Cardiologia'),('9183424','Alexandre Alencar','M','(81) 99482-4758','fernandoalencar@mail.com','Oftalmologia');
/*!40000 ALTER TABLE `tabelamedico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabelapaciente`
--

DROP TABLE IF EXISTS `tabelapaciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabelapaciente` (
  `CpfPaciente` char(11) NOT NULL,
  `NomePac` varchar(100) NOT NULL,
  `DataNascimento` date DEFAULT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Telefone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CpfPaciente`),
  CONSTRAINT `tabelapaciente_chk_1` CHECK ((`Genero` in (_utf8mb4'F',_utf8mb4'M')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabelapaciente`
--

LOCK TABLES `tabelapaciente` WRITE;
/*!40000 ALTER TABLE `tabelapaciente` DISABLE KEYS */;
INSERT INTO `tabelapaciente` VALUES ('12345678900','Sofia Oliveira','1985-06-10','F','(81) 99911-2233','sofia.o@mail.com'),('22233344455','Carla Silva','1978-03-15','F','(81) 99777-0000','carla.s@mail.com'),('34512389765','Rebeca Lins','1993-04-15','F','(81) 99945-4177','rebeca@mail.com'),('58961234752','Paulo Martins','2020-08-21','M','(81) 99873-4312','paulo@mail.com'),('98765432100','André Gomes','2005-11-25','M','(81) 98844-5566','andre.g@mail.com');
/*!40000 ALTER TABLE `tabelapaciente` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28 21:46:14

--trigger para restrição de horário de consultas na clínica e médico disponível na clínica

DELIMITER $$

CREATE TRIGGER trg_clinica_horario
BEFORE INSERT ON tabelaconsulta
FOR EACH ROW
BEGIN
    -- Exemplo: não permite agendamento aos domingos
    IF DAYOFWEEK(NEW.Data_Hora) = 1 THEN  -- 1 = domingo no MySQL
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A clínica não funciona aos domingos.';
    END IF;

    -- Exemplo: horário comercial (8h às 18h)
    IF HOUR(NEW.Data_Hora) < 8 OR HOUR(NEW.Data_Hora) >= 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Fora do horário de funcionamento da clínica.';
    END IF;
END$$

DELIMITER ;


-- Tabela de vínculo (exemplo)
CREATE TABLE medico_clinica (
    CodMed CHAR(7),
    CodCli CHAR(6),
    PRIMARY KEY (CodMed, CodCli),
    FOREIGN KEY (CodMed) REFERENCES tabelamedico(CodMed),
    FOREIGN KEY (CodCli) REFERENCES tabelaclinica(CodCli)
);

-- Trigger de validação
DELIMITER $$

CREATE TRIGGER trg_medico_na_clinica
BEFORE INSERT ON tabelaconsulta
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM medico_clinica
        WHERE CodMed = NEW.CodMed AND CodCli = NEW.CodCli
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Médico não atende nesta clínica.';
    END IF;
END$$

DELIMITER ;
