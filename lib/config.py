# Billy Andrews
## Postgresql configuration
POSTGRES_USER="bgtemp"
# BP9: use real passwords for postgres users
POSTGRES_PASSWORD="bgprod"
POSTGRES_DATABASE="bg"
POSTGRES_HOST="localhost"

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY ="ThisisaSecret"


# Flask Mail
confDEBUG = True
confMAIL_SERVER = 'smtp.gmail.com'
confMAIL_PORT = 587
confMAIL_USE_TLS = True
confMAIL_USE_SSL = False
confMAIL_USERNAME = 'bgsalestest@gmail.com'
confMAIL_PASSWORD = 'bgprodtest'