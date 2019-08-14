# Configuração da base de dados
# Exemplo: DEFAULT_DATABASE_URL = 'postgres://user:pass@localhost/dbname'
# Caso seja deixado vazio o default será: 'sqlite:////...SGEO/db.sqlite3'
DEFAULT_DATABASE_URL = 'postgres://postgres:postgres@localhost/SGEO'


#
# Configurações do servidor de email
# Obs: Por enquanto o endereço de email é utilizado apenas para a troca de senha do usuário.
# Endereço de email padrão utilizado
#
DEFAULT_FROM_EMAIL = 'contato@SGEOerp.com.br'

# EMAIL_HOST = 'smtp.gmail.com'  # Gmail
# EMAIL_HOST = 'smtp.live.com' #Hotmail

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'contato@SGEOerp.com.br'
EMAIL_HOST_PASSWORD = 'SGEO@@2019'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
