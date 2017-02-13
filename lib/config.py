# Ron Mitsugo Zacharski
#
#   BP1   keep configuration data in separate file
#
## Postgresql configuration
POSTGRES_USER="faceboardtemp"
# BP9: use real passwords for postgres users
POSTGRES_PASSWORD="pass"
POSTGRES_DATABASE="faceboard"
POSTGRES_HOST="localhost"

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY ="ThisisaSecret"