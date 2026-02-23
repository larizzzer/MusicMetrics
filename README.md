# 🎵 MusicMetrics

**Projeto de Análise de Dados Musicais com Python, SQL e Power BI**

Análise completa de dados do Spotify utilizando API, ETL com Python, armazenamento em MySQL e visualização em Power BI para gerar insights sobre padrões musicais e comportamento de escuta.

---

## 📊 Sobre o Projeto

O **MusicMetrics** é um projeto end-to-end de análise de dados que demonstra habilidades em:

- **Extração de dados** via Dataset do Kaggle
- **Transformação e limpeza** de dados com Python (Pandas)
- **Modelagem dimensional** e armazenamento em MySQL
- **Análises SQL** para responder perguntas de negócio
- **Visualização** de insights em dashboards do Power BI

### Objetivos

- Analisar padrões de consumo musical ao longo do tempo
- Identificar características de músicas populares
- Compreender evolução do gosto musical pessoal
- Gerar insights acionáveis sobre preferências musicais

---

## 🛠 Tecnologias Utilizadas

### Linguagens e Frameworks
- **Python** - Extração e transformação de dados
- **SQL (MySQL)** - Armazenamento e análises relacionais
- **Power BI** - Visualização de dados

### Bibliotecas Python
- `pandas` - Manipulação de dados
- `numpy` - Operações numéricas
- `mysql-connector-python` - Conexão com MySQL
- `sqlalchemy` - ORM para banco de dados
- `python-dotenv` - Gerenciamento de variáveis de ambiente

### Ferramentas
- **VS Code** - Editor de código
- **MySQL Workbench** - Gerenciamento de banco de dados
- **Git** - Controle de versão

---

## 📁 Estrutura do Projeto

```
MusicMetrics/
│
├── scripts/
│   ├── 01_Exploracao_Inicial.py           # Extrai dados do Spotify
│   ├── 02_Limpeza_e_Transformacao.py      # Limpa e transforma dados
│   ├── 03_Carregamento_dos_Dados.py       # Carrega dados no MySQL
│
├── sql/
│   ├── 01_Criacao_Banco_de_Dados.sql      # Cria estrutura do banco
│   ├── 02_Queries_Analiticas.sql          # Queries analíticas
│   └── 03_Views_e_Procedures.sql          # Views e procedures úteis
│
├── dashboards/
│   └── Imagens_Dashboard/                 # Imagens do Dashboard no Power BI
│       ├── Visual_1.png
│       ├── Visual_2.png
│       ├── Visual_3.png
│       ├── Visual_4.png
│       └── Visual_5.png
│
├── docs/
│   └── projeto.pdf                        # Projeto documentado
│
├── .gitignore                             # Arquivos ignorados pelo Git
└── README.md                              # Este arquivo
```

---

## 📈 Análises Disponíveis

### Análises de Perfil Musical

- **Top Artistas e Músicas**: Rankings por período (4 semanas, 6 meses, histórico)
- **Evolução do Gosto Musical**: Como suas preferências mudaram ao longo do tempo
- **Diversidade Musical**: Quantidade de gêneros e artistas únicos

### Análises de Características de Áudio

- **Perfil Sonoro**: Distribuição de danceability, energy, valence
- **Correlações**: Relação entre características (ex: músicas felizes são mais dançantes?)
- **Comparação Temporal**: Evolução das características das músicas que você escuta

### Análises de Comportamento

- **Padrões de Escuta**: Horários e dias com mais reproduções
- **Músicas Recorrentes**: Faixas mais repetidas
- **Descoberta Musical**: Taxa de músicas novas vs conhecidas

---

## 📊 Dashboard Power BI

O dashboard interativo irá incluir:

### Página 1: Visão Geral
- KPIs principais (total de artistas, músicas, gêneros)
- Top 10 artistas e músicas
- Timeline de descoberta musical

### Página 2: Audio Features
- Radar chart com perfil sonoro médio
- Distribuição de características de áudio
- Análise comparativa por gênero

### Página 3: Tendências Temporais
- Evolução de preferências ao longo do tempo
- Padrões de escuta por dia/hora
- Sazonalidade musical

### Página 4: Descoberta e Diversidade
- Matriz de gêneros musicais
- Análise de popularidade
- Taxa de descoberta de novos artistas

---

## 🎯 Próximos Passos

- [ ] Adicionar análise de letras das músicas
- [ ] Implementar sistema de recomendação básico
- [ ] Automação de extração diária/semanal

---

## 👤 Autora

**Larissa Gomes Gaspar**
- GitHub: [larizzzer](https://github.com/larizzzer)
- LinkedIn: [Larissa Gomes Gaspar](https://linkedin.com/in/larissa-gomes-gaspar)
