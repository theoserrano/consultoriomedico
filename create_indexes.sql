-- Índices para otimizar performance das queries
-- Executar após criar as tabelas

-- Índices para tabela de consultas (queries mais comuns)
CREATE INDEX idx_consulta_data ON tabelaconsulta(Data_Hora);
CREATE INDEX idx_consulta_clinica ON tabelaconsulta(CodCli);
CREATE INDEX idx_consulta_medico ON tabelaconsulta(CodMed);
CREATE INDEX idx_consulta_paciente ON tabelaconsulta(CpfPaciente);

-- Índice composto para queries com múltiplos filtros
CREATE INDEX idx_consulta_cli_med ON tabelaconsulta(CodCli, CodMed);
CREATE INDEX idx_consulta_data_cli ON tabelaconsulta(Data_Hora, CodCli);
CREATE INDEX idx_consulta_data_med ON tabelaconsulta(Data_Hora, CodMed);

-- Índices para joins frequentes
CREATE INDEX idx_medico_nome ON tabelamedico(NomeMed);
CREATE INDEX idx_clinica_nome ON tabelaclinica(NomeCli);
CREATE INDEX idx_paciente_nome ON tabelapaciente(NomePac);
CREATE INDEX idx_paciente_data_nasc ON tabelapaciente(DataNascimento);
CREATE INDEX idx_paciente_genero ON tabelapaciente(Genero);
CREATE INDEX idx_medico_especialidade ON tabelamedico(Especialidade);
