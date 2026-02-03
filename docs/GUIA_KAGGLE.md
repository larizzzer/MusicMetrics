# 🎯 GUIA DE USO - Scripts Atualizados para Dataset do Kaggle

## 📋 O Que Mudou?

Os scripts foram **atualizados** para trabalhar com os arquivos CSV do Kaggle:
- ✅ `tracks.csv` (600k músicas com audio features)
- ✅ `artists.csv` (informações dos artistas)

Os scripts da API do Spotify (01 e 02) foram **mantidos** caso você queira usar no futuro.

---

## 🗂️ Estrutura dos Novos Scripts

### Script 03: `03_explore_kaggle_data.py`
**O que faz:** Explora e analisa os arquivos CSV do Kaggle

### Script 04: `04_clean_and_transform.py`  
**O que faz:** Limpa, transforma e prepara os dados para o MySQL

### Script 05: `05_load_to_mysql.py`
**O que faz:** Carrega os dados processados no banco MySQL

---

## 🚀 Passo a Passo para Usar

### ✅ Pré-requisitos

1. Você já tem os CSVs do Kaggle baixados:
   - `tracks.csv`
   - `artists.csv`
   
2. MySQL instalado e rodando

3. Bibliotecas Python instaladas (você já fez isso!)

---

### 📍 PASSO 1: Colocar os CSVs no Lugar Certo

**Copie os arquivos CSV do Kaggle para:**
```
Documentos/Projeto - MusicMetrics/data/raw/
```

Deve ficar assim:
```
Projeto - MusicMetrics/
├── data/
│   └── raw/
│       ├── tracks.csv          ← Cole aqui
│       └── artists.csv         ← Cole aqui
```

---

### 📍 PASSO 2: Configurar Caminhos (SE NECESSÁRIO)

Os scripts já vêm com os caminhos configurados. Mas **SE** sua estrutura for diferente:

#### Abra cada script e veja a seção de CONFIGURAÇÃO no topo:

**No `03_explore_kaggle_data.py`:**
```python
# ============================================
# CONFIGURAÇÃO - ALTERE AQUI OS CAMINHOS
# ============================================

# Caminho para a pasta onde estão os CSVs do Kaggle
DATA_PATH = '../data/raw/'

# Nomes dos arquivos
TRACKS_FILE = 'tracks.csv'
ARTISTS_FILE = 'artists.csv'
```

**Se seus arquivos tiverem nomes diferentes**, altere aqui!

---

### 📍 PASSO 3: Executar Script de Exploração

Abra o terminal na pasta `scripts/`:
```bash
cd "Documentos/Projeto - MusicMetrics/scripts"
```

Execute:
```bash
python 03_explore_kaggle_data.py
```

**O que vai acontecer:**
- ✅ Mostra quantas músicas e artistas você tem
- ✅ Identifica valores nulos e duplicatas
- ✅ Mostra estatísticas gerais
- ✅ Lista as colunas de cada arquivo

**IMPORTANTE:** Revise os resultados! Veja se está tudo OK.

---

### 📍 PASSO 4: Limpar e Transformar os Dados

Execute:
```bash
python 04_clean_and_transform.py
```

**O que vai acontecer:**
- 🧹 Remove duplicatas
- 🧹 Preenche valores nulos
- 🧹 Padroniza formatos
- 🧹 Extrai audio features em arquivo separado
- 💾 Salva arquivos limpos em `data/processed/`

**Arquivos gerados:**
```
data/processed/
├── tracks_clean.csv
├── artists_clean.csv
└── audio_features_clean.csv
```

---

### 📍 PASSO 5: Configurar Arquivo .env

**ANTES de carregar no MySQL**, configure suas credenciais!

1. Copie o arquivo `.env.example` para `.env`:
```bash
copy .env.example .env
```

2. Edite o `.env` com suas credenciais do MySQL:
```env
# MySQL Database Credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=SUA_SENHA_AQUI
MYSQL_DATABASE=musicmetrics_db
MYSQL_PORT=3306
```

---

### 📍 PASSO 6: Criar o Banco de Dados

**Opção A - MySQL Workbench:**
1. Abra MySQL Workbench
2. Conecte ao servidor
3. File > Open SQL Script
4. Selecione: `sql/01_create_schema.sql`
5. Execute (⚡ lightning icon)

**Opção B - Linha de comando:**
```bash
mysql -u root -p < sql/01_create_schema.sql
```

---

### 📍 PASSO 7: Carregar Dados no MySQL

Execute:
```bash
python 05_load_to_mysql.py
```

**O que vai acontecer:**
- 📊 Carrega artistas primeiro
- 📊 Depois carrega músicas
- 📊 Por último, carrega audio features
- ✅ Mostra progresso em tempo real
- ✅ Verifica se tudo foi carregado

**Tempo estimado:** 5-15 minutos (dependendo do tamanho do dataset)

---

## ⚠️ Possíveis Problemas e Soluções

### Problema: "Pasta não encontrada"
**Solução:** Verifique se você está executando o script da pasta correta:
```bash
cd scripts
python 03_explore_kaggle_data.py
```

### Problema: "Can't connect to MySQL"
**Solução:** 
1. MySQL está rodando? Verifique no Task Manager (Windows)
2. Senha correta no `.env`?
3. Tente conectar manualmente: `mysql -u root -p`

### Problema: "Foreign key constraint fails"
**Solução:** 
- Execute os scripts na ORDEM correta (artistas → músicas → features)
- Se der erro, delete tudo e rode de novo:
```sql
DROP DATABASE musicmetrics_db;
CREATE DATABASE musicmetrics_db;
```

### Problema: "Module not found"
**Solução:**
```bash
pip install -r requirements.txt
```

---

## 📊 Após Carregar os Dados

### O que fazer agora:

1. **Verificar no MySQL Workbench:**
   - Abra o banco `musicmetrics_db`
   - Veja as tabelas criadas
   - Execute queries de teste:
   ```sql
   SELECT COUNT(*) FROM dim_tracks;
   SELECT COUNT(*) FROM dim_artists;
   SELECT COUNT(*) FROM dim_audio_features;
   ```

2. **Executar Queries Analíticas:**
   - Abra: `sql/02_analytical_queries.sql` (será criado em breve)
   - Execute as queries para ver insights

3. **Conectar o Power BI:**
   - Abra Power BI Desktop
   - Get Data > MySQL
   - Conecte ao `localhost`, banco `musicmetrics_db`
   - Importe as views (vw_*)

---

## 🎯 Checklist Final

Antes de ir para o Power BI, confirme:

- [ ] CSVs do Kaggle na pasta `data/raw/`
- [ ] Script 03 executado com sucesso
- [ ] Script 04 executado - arquivos em `data/processed/`
- [ ] Arquivo `.env` configurado
- [ ] Schema MySQL criado (`01_create_schema.sql`)
- [ ] Script 05 executado - dados no MySQL
- [ ] Verificação no MySQL Workbench - tabelas populadas

---

## 💡 Dicas

- **Sempre execute os scripts na ordem:** 03 → 04 → 05
- **Não pule o script 04** - ele limpa os dados!
- **Revise os relatórios** que cada script gera
- **Documente problemas** que encontrar

---

## 📞 Precisa de Ajuda?

Se encontrar algum erro:
1. Leia a mensagem de erro com atenção
2. Verifique se seguiu todos os passos
3. Consulte a seção "Possíveis Problemas"
4. Me avise o erro específico que apareceu!

---

**Boa sorte com o projeto! 🎵✨**
