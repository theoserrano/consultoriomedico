-- ============================================================
-- Triggers do Sistema de Consultório Médico
-- Regras de Negócio do Consultório
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
    SET dia_semana = DAYOFWEEK(NEW.Data_Hora); -- 1=Domingo, 7=Sábado
    
    -- Verifica se é final de semana
    IF dia_semana IN (1, 7) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Regra de Negócio: Consultório não atende aos finais de semana';
    END IF;
    
    -- Verifica horário de funcionamento (8h às 18h)
    IF hora_consulta < 8 OR hora_consulta >= 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Regra de Negócio: Horário de atendimento: 8h às 18h';
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
    
    -- Consulta deve ser agendada com pelo menos 2h de antecedência
    IF diferenca_horas < 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Regra de Negócio: Consultas devem ser agendadas com pelo menos 2 horas de antecedência';
    END IF;
    
    -- Não permite agendar com mais de 6 meses de antecedência
    IF diferenca_horas > (24 * 180) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Regra de Negócio: Não é possível agendar com mais de 6 meses de antecedência';
    END IF;
END$$

DELIMITER ;

-- ============================================================
-- Como aplicar os triggers:
-- mysql -u root -p consultoriomedico < triggers.sql
-- ============================================================
