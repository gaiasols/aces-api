import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME        = os.getenv("PROJECT_NAME", "FastAPI Config")

# MongoDB Atlas
MONGODB_URI  = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")
ADMIN_DBNAME = os.getenv("ADMIN_DBNAME")
MONGODB_MAX_POOL_SIZE=100
MONGODB_MIN_POOL_SIZE=10

# Sentry
SENTRY_DSN           = os.getenv("SENTRY_DSN")

# AWS
SMTP_HOST            = os.getenv("SMTP_HOST")
SMTP_USER            = os.getenv("SMTP_USER")
SMTP_PASSWORD        = os.getenv("SMTP_PASSWORD")
EMAILS_FROM_EMAIL    = os.getenv("EMAILS_FROM_EMAIL")

#
LICENSE_CODE_MIN_LENGTH=3
LICENSE_CODE_MAX_LENGTH=10
LICENSE_CODE_ERROR_MESSAGE="LicenseSlug harus alfanumerik dengan panjang %s-%s karakter." % (LICENSE_CODE_MIN_LENGTH, LICENSE_CODE_MAX_LENGTH)

CLIENT_CODE_MIN_LENGTH=3
CLIENT_CODE_MAX_LENGTH=10
CLIENT_CODE_ERROR_MESSAGE="Client code must be alphanumeric, %s-%s characters length" % (CLIENT_CODE_MIN_LENGTH, CLIENT_CODE_MAX_LENGTH)

USERNAME_MIN_LENGTH=5
USERNAME_MAX_LENGTH=12
USERNAME_ERROR_MESSAGE="Username must be 5 - 12 characters length"

PASSWORD_MIN_LENGTH=5
PASSWORD_MAX_LENGTH=12
PASSWORD_ERROR_MESSAGE="Password must be 6 - 15 characters length"

DEFAULT_DOCUMENTS_LIMIT=20

ERROR_MONGODB_INSERT = "Database insert error"
ERROR_MONGODB_UPDATE = "Database update error"
ERROR_MONGODB_DELETE = "Database delete error"

DOCTYPE_ADMIN    = "admin"
DOCTYPE_LICENSE  = "licenses"
DOCTYPE_MODULE   = "modules"
DOCTYPE_USER     = "users"
DOCTYPE_PROJECT  = "projects"
DOCTYPE_CLIENT   = "clients"
DOCTYPE_PERSONA  = "personas"
DOCTYPE_BATCH    = "batches"

ORG_SYMBOL_LENGTH = 6

LICENSE_TYPES = "personal corporate"

PROJECT_MIN_YEAR = 2020
PROJECT_MAX_YEAR = 2030

PROJECT_MEMBER_ROLES = "admin client expert visitor"
PROJECT_MEMBER_TYPES = "internal external"

BEHAVIORAL_MODULE_TYPES = "AIME CSI GPQ GMATE PROL PSI SJT INTERVIEW DISCUSSION PRESENTATION"
BEHAVIORAL_MODULE_METHODS = "selftest facetime"

ADMIN_ROLES = ""
USER_CAPABILITIES = "creator admin client expert"
