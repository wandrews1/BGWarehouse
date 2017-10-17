# Ron Mitsugo Zacharski
#
#   BP1   keep configuration data in separate file
#
## Postgresql configuration
POSTGRES_USER="bgtemp"
# BP9: use real passwords for postgres users
POSTGRES_PASSWORD="bgprod"
POSTGRES_DATABASE="bg"
POSTGRES_HOST="localhost"

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY ="ThisisaSecret"