# 🏥 Sistema de Consultório Médico - Dashboard Profissional

Sistema completo de gerenciamento para consultórios médicos com dashboard moderno e analytics avançados.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.14.2-brightgreen.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)

> 📋 **GUIA DE INSTALAÇÃO COMPLETO**: [INSTALACAO.md](INSTALACAO.md)

## ✨ Novidades da Versão Profissional

### 🎨 Design Completamente Reformulado
- **Interface moderna** com gradientes e animações suaves
- **Cards KPI** com ícones e bordas coloridas
- **Navbar aprimorada** com ícones Bootstrap
- **Tema profissional** com sombras e efeitos hover
- **CSS responsivo** para todos os dispositivos

### 📊 Nova Página de Analytics
- Gráficos interativos avançados separados em aba dedicada
- Série temporal de consultas
- Análise por médico, clínica e especialidade
- Heatmap de horários mais movimentados
- Distribuição de idades dos pacientes
- Boxplot e scatter plots
- **Filtros dinâmicos** por clínica, médico e período

### 🏠 Dashboard Principal Redesenhado
- **4 KPIs principais** com design moderno
- **Botões de ação rápida** para navegação
- **Gráfico de tendência** dos últimos 30 dias
- **Top 5 médicos** mais ativos
- **Próximas consultas** em lista elegante
- **Distribuição por especialidade**

### 🗄️ Banco de Dados Populado
- **Script automático** para gerar dados artificiais
- **200 pacientes**, **80 médicos**, **12 clínicas**
- **1500+ consultas** distribuídas em 120 dias
- Dados realistas usando biblioteca Faker
- Diversidade de especialidades médicas

## 🚀 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

As novas dependências incluem:
- `Faker==22.0.0` - Geração de dados artificiais

### 2. Popular o Banco de Dados

Execute o script de população para criar dados de demonstração:

```bash
python populate_database.py
```

Este script irá:
- ✅ Limpar dados existentes (opcional)
- ✅ Criar 200 pacientes realistas
- ✅ Criar 80 médicos com especialidades variadas
- ✅ Criar 12 clínicas
- ✅ Gerar 1500 consultas distribuídas ao longo de 120 dias

**⚠️ Atenção:** O script limpa os dados existentes por padrão. Comente as linhas de DELETE no código se quiser manter dados anteriores.

### 3. Executar a Aplicação

```bash
python app.py
```

Acesse: `http://127.0.0.1:8050`

## 📱 Navegação

### 🏠 Início (Dashboard)
- Visão geral com KPIs principais
- Ações rápidas para cadastro
- Próximas consultas
- Gráfico de tendência mensal
- Top 5 médicos

### 👥 Pacientes
- Listagem com filtro de busca
- Cadastro e edição inline
- DataTable interativa com ordenação

### ⚕️ Médicos
- Gerenciamento completo de médicos
- Especialidades
- Média de consultas por médico

### 🏥 Clínicas
- Cadastro de clínicas
- Informações de contato
- Endereços

### 📅 Consultas
- Agendamento de consultas
- Filtros por data e médico
- Visualização detalhada

### 📊 Analytics (NOVO!)
- **Página dedicada para análises avançadas**
- Filtros interativos (clínica, médico, período)
- 8+ tipos de visualizações:
  - Série temporal
  - Consultas por médico/clínica
  - Distribuição de gênero
  - Histograma de idades
  - Heatmap de horários
  - Boxplot
  - Scatter plot

## 🎨 Melhorias Visuais

### Cores e Gradientes
- **Roxo/Azul**: Primário (cabeçalhos, botões principais)
- **Verde**: Sucesso (médicos, confirmações)
- **Azul Claro**: Informação (clínicas)
- **Rosa/Amarelo**: Avisos (consultas)
- **Vermelho**: Perigos (exclusões)

### Animações
- Hover effects em cards e botões
- Transições suaves (0.3s)
- SlideIn para alerts
- FadeIn para páginas
- Lift effect em tabelas

### Componentes
- Scrollbar customizada com gradiente
- Badges arredondados
- Shadows em múltiplos níveis
- Border-radius consistente (0.5rem)
- Typography profissional com Inter font

## 🔧 Configurações

### Banco de Dados
O sistema suporta MySQL e SQLite (fallback automático).

Arquivo `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=consultoriomedico
DEMO=false
DB_USE_SQLITE_FALLBACK=true
```

### Personalização
- **CSS**: `assets/styles.css` - Todas as variáveis CSS customizáveis
- **Cores**: Modifique as variáveis CSS no `:root`
- **Logo**: Substitua `assets/icons/logo.svg`

## 📦 Estrutura do Projeto

```
consultoriomedico/
├── app.py                    # Aplicação principal
├── db.py                     # Conexão com banco
├── config.py                 # Configurações
├── populate_database.py      # Script de população (NOVO!)
├── requirements.txt          # Dependências
├── assets/
│   └── styles.css           # CSS profissional (ATUALIZADO!)
├── pages/
│   ├── home.py              # Dashboard principal (REDESENHADO!)
│   ├── analytics.py         # Página de analytics (NOVO!)
│   ├── pacientes.py         # Gestão de pacientes
│   ├── medicos.py           # Gestão de médicos
│   ├── clinicas.py          # Gestão de clínicas
│   └── consultas.py         # Gestão de consultas
```

## 🛠️ Tecnologias

- **Dash** 2.14.2 - Framework web Python
- **Plotly** 5.18.0 - Gráficos interativos
- **Dash Bootstrap Components** 1.5.0 - Componentes UI
- **Pandas** 2.1.4 - Manipulação de dados
- **MySQL Connector** 8.2.0 - Conexão com banco
- **Faker** 22.0.0 - Geração de dados fake (NOVO!)

## 📈 Recursos de Analytics

### Consultas Suportadas
1. Total de consultas por especialidade
2. Série temporal de consultas
3. Distribuição por médico (com top rankings)
4. Distribuição por clínica
5. Análise de gênero dos pacientes
6. Distribuição de idades
7. Padrões de horário (heatmap)
8. Correlações entre variáveis

### Filtros Disponíveis
- **Clínica**: Filtra consultas por clínica específica
- **Médico**: Filtra consultas por médico específico
- **Período**: Define range de datas customizado

## 🎯 Próximos Passos Sugeridos

- [ ] Adicionar exportação de relatórios (PDF/Excel)
- [ ] Implementar sistema de autenticação
- [ ] Criar dashboard para pacientes
- [ ] Adicionar notificações/lembretes
- [ ] Integrar com calendário (Google Calendar, Outlook)
- [ ] Implementar telemedicina
- [ ] Adicionar prontuário eletrônico

## 📝 Licença

Este projeto é de uso educacional e demonstrativo.

## 👨‍💻 Suporte

Para dúvidas ou sugestões, consulte a documentação do Dash:
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)

---

**Desenvolvido com ❤️ usando Dash e Plotly**
