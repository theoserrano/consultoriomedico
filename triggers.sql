-- ============================================================
-- Triggers do Sistema de Consultório Médico
-- Regras de Negócio do Consultório
-- ============================================================
-- IMPORTANTE: No MySQL Workbench, execute todo este arquivo de uma vez
-- ou selecione todo o conteúdo e clique em "Execute"
-- ============================================================

DELIMITER $$

-- ============================================================
-- TRIGGER 1: Horário comercial do consultório
-- Regra: Consultas só podem ser agendadas entre 8h e 18h em dias úteis
-- ============================================================
DROP TRIGGER IF EXISTS horario_comercial$$

CREATE TRIGGER horario_comercial
BEFORE INSERT ON tabelaconsulta
FOR EACH ROW
BEGIN
    DECLARE hora_consulta INT;
    DECLARE dia_semana INT;
    
    SET hora_consulta = HOUR(NEW.Data_Hora);
    SET dia_semana = DAYOFWEEK(NEW.Data_Hora);
    
    IF dia_semana IN (1, 7) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'TRIGGER_AVISO: Consultório não atende aos finais de semana';
    END IF;
    
    IF hora_consulta < 8 OR hora_consulta >= 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'TRIGGER_AVISO: Horário de atendimento é de 8h às 18h';
    END IF;
END$$

-- ============================================================
-- TRIGGER 2: Antecedência mínima para agendamento
-- Regra: Consultas devem ser agendadas com pelo menos 2 horas de antecedência
-- ============================================================
DROP TRIGGER IF EXISTS antecedencia_minima$$

CREATE TRIGGER antecedencia_minima
BEFORE INSERT ON tabelaconsulta
FOR EACH ROW
BEGIN
    DECLARE diferenca_horas INT;
    
    SET diferenca_horas = TIMESTAMPDIFF(HOUR, NOW(), NEW.Data_Hora);
    
    IF diferenca_horas < 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'TRIGGER_AVISO: Consultas devem ser agendadas com pelo menos 2 horas de antecedência';
    END IF;
    
    IF diferenca_horas > (24 * 180) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'TRIGGER_AVISO: Não é possível agendar com mais de 6 meses de antecedência';
    END IF;
END$$

DELIMITER ;

-- ============================================================
-- Como aplicar:
-- 1. No MySQL Workbench: Selecione TUDO (Ctrl+A) e execute (Ctrl+Shift+Enter)
-- 2. Por terminal: mysql -u root -p consultoriomedico < triggers.sql
-- 3. Por Python: python apply_triggers.py
-- ============================================================
