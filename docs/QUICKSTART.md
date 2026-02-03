# 🚀 Guia de Início Rápido - MusicMetrics

## Parabéns! Você está quase pronto para começar! 🎉

Este guia vai te ajudar a dar os primeiros passos após configurar suas credenciais do Spotify.

---

## ✅ Checklist Pré-Execução

Antes de executar os scripts, certifique-se de que:

- [ ] Python 3.13+ está instalado (`python --version`)
- [ ] Todas as bibliotecas foram instaladas (`pip install -r requirements.txt`)
- [ ] MySQL está rodando
- [ ] Você criou a aplicação no Spotify Developer Dashboard
- [ ] Você tem o Client ID e Client Secret
- [ ] Você configurou o arquivo `.env` com suas credenciais

---

## 📝 Passo a Passo

### 1️⃣ Configure o arquivo .env

Copie o arquivo `.env.example` para `.env` e preencha com suas informações:

```bash
cp .env.example .env
```

Edite o `.env`:
```env
SPOTIFY_CLIENT_ID=cole_seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=cole_seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha_mysql
MYSQL_DATABASE=musicmetrics_db
MYSQL_PORT=3306
```

### 2️⃣ Crie o banco de dados MySQL

**Opção A: Usando MySQL Workbench**
1. Abra o MySQL Workbench
2. Conecte ao seu servidor MySQL
3. File > Open SQL Script
4. Selecione `sql/01_create_schema.sql`
5. Execute o script (⚡ lightning icon ou Ctrl+Shift+Enter)

**Opção B: Via linha de comando**
```bash
mysql -u root -p < sql/01_create_schema.sql
```

### 3️⃣ Teste a conexão com o Spotify

Navegue até a pasta scripts:
```bash
cd scripts
```

Execute o teste de conexão:
```bash
python 01_test_spotify_connection.py
```

**O que vai acontecer:**
- Seu navegador abrirá automaticamente
- Você fará login no Spotify (se necessário)
- O Spotify pedirá permissão para o app acessar seus dados
- Clique em "Aceitar"
- Você será redirecionado (pode dar erro no navegador, mas está OK!)
- Volte ao terminal e veja seus dados!

**Resultado esperado:**
```
==================================================
🎵 MUSICMETRICS - Teste de Conexão Spotify API
==================================================

✅ Conectado com sucesso!
👤 Usuário: Seu Nome
📧 Email: seu.email@example.com
🎵 Conta: premium (ou free)

==================================================

🎤 Seus Top 5 Artistas (short_term):
--------------------------------------------------
1. Artista 1
   Gêneros: pop, rock
   Popularidade: 85/100
...
```

### 4️⃣ Extraia seus dados do Spotify

```bash
python 02_extract_spotify_data.py
```

Isso vai criar arquivos CSV na pasta `data/raw/` com:
- Seus top artistas
- Suas top músicas
- Audio features das músicas
- Histórico recente de reprodução

### 5️⃣ Próximos scripts (em desenvolvimento)

Os scripts seguintes serão criados em breve:
- `03_clean_and_transform.py` - Limpeza e transformação
- `04_load_to_mysql.py` - Carregar no banco de dados

---

## 🎯 Dicas Importantes

### Primeira Execução
- Na primeira vez, o Spotify pedirá autorização - isso é normal!
- Após autorizar, um arquivo `.cache` será criado localmente
- Nas próximas execuções, você não precisará autorizar novamente

### Limites da API
- A API do Spotify tem limites de requisições
- Os scripts incluem delays para evitar bloqueios
- Seja paciente nas primeiras extrações!

### Dados Disponíveis
A API tem algumas limitações:
- **Recently Played**: Apenas últimas 50 músicas
- **Top Artists/Tracks**: Calculado em 3 períodos:
  - `short_term`: Últimas 4 semanas
  - `medium_term`: Últimos 6 meses
  - `long_term`: Vários anos

### Histórico Completo
Se você quiser seu histórico completo de audição:
1. Vá em Spotify.com > Conta
2. Privacidade > Baixar seus dados
3. Aguarde alguns dias
4. Você receberá um arquivo JSON completo

---

## ❓ Troubleshooting

### Erro: "No module named 'spotipy'"
```bash
pip install -r requirements.txt
```

### Erro: "Can't connect to MySQL server"
- Certifique-se que o MySQL está rodando
- Verifique usuário e senha no `.env`
- Teste conexão: `mysql -u root -p`

### Erro: "Invalid client credentials"
- Verifique se o Client ID e Secret estão corretos no `.env`
- Certifique-se de não ter espaços extras

### Navegador não abre automaticamente
- Copie a URL que aparece no terminal
- Cole no navegador manualmente
- Complete a autorização

### Erro: "Redirect URI mismatch"
- No Spotify Dashboard, verifique se o Redirect URI está exatamente:
  `http://localhost:8888/callback`
- Sem espaços, com http (não https), com porta 8888

---

## 📚 Documentação Útil

- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/)
- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🎉 Próximos Passos

Após extrair seus dados com sucesso:

1. Explore os arquivos CSV gerados em `data/raw/`
2. Analise os dados no Excel/Google Sheets
3. Aguarde os próximos scripts para análises mais profundas
4. Prepare-se para criar dashboards incríveis no Power BI!

---

**Dúvidas?** Abra uma issue no GitHub ou consulte a documentação completa no README.md

Bom projeto! 🎵✨
