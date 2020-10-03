import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", "Gaia ACES API")
API_V1_STR = "/v1"

SERVER_HOST  = os.getenv("SERVER_HOST", "http://localhost:8000")

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
EMAILS_FROM_NAME     = os.getenv("EMAILS_FROM_NAME")
EMAIL_RESET_TOKEN_EXPIRE_HOURS = int(os.getenv("EMAIL_RESET_TOKEN_EXPIRE_HOURS", 48))
EMAIL_TEMPLATES_DIR  = "./email-templates/build"
EMAIL_TEST_USER      = "test@example.com"

SMTP_TLS  = True
SMTP_PORT = 587
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

# Token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", (7 * 24 * 60)))  # 7 days

#
NEW_LICENSE_PASSWORD = os.getenv("NEW_LICENSE_PASSWORD", "kal10soL0")
LICENSE_CODE_MIN_LENGTH=3
LICENSE_CODE_MAX_LENGTH=10
LICENSE_CODE_ERROR_MESSAGE="LicenseSlug harus alfanumerik dengan panjang %s-%s karakter." % (LICENSE_CODE_MIN_LENGTH, LICENSE_CODE_MAX_LENGTH)

CLIENT_CODE_MIN_LENGTH=3
CLIENT_CODE_MAX_LENGTH=10
CLIENT_CODE_ERROR_MESSAGE="Client code must be alphanumeric, %s-%s characters length" % (CLIENT_CODE_MIN_LENGTH, CLIENT_CODE_MAX_LENGTH)

USERNAME_MIN_LENGTH=4
USERNAME_MAX_LENGTH=12
USERNAME_ERROR_MESSAGE=f"Username must be {USERNAME_MIN_LENGTH} - {USERNAME_MAX_LENGTH} characters length"

PASSWORD_MIN_LENGTH=6
PASSWORD_MAX_LENGTH=12
PASSWORD_ERROR_MESSAGE=f"Password must be {PASSWORD_MIN_LENGTH} - {PASSWORD_MAX_LENGTH} characters length"

DEFAULT_DOCUMENTS_LIMIT=20

ERROR_MONGODB_INSERT = "Database insert error"
ERROR_MONGODB_UPDATE = "Database update error"
ERROR_MONGODB_DELETE = "Database delete error"

DOCTYPE_ADMIN    = "admin"
DOCTYPE_LICENSE  = "licenses"
DOCTYPE_MODULE   = "modules"
DOCTYPE_PROJECT_MODULE = "project_modules"
DOCTYPE_PROJECT_MEMBER = "project_members"
DOCTYPE_USER     = "users"
DOCTYPE_CLIENT   = "clients"
DOCTYPE_CONTRACT = "contracts"
DOCTYPE_PROJECT  = "projects"
DOCTYPE_PERSONA  = "personas"
DOCTYPE_BATCH    = "batches"

DOCTYPE_EV_GPQ  = "ev_GPQ"

ORG_SYMBOL_LENGTH = 6

LICENSE_TYPES = "personal corporate"

PROJECT_MIN_YEAR = 2020
PROJECT_MAX_YEAR = 2030

PROJECT_MEMBER_ROLES = "client expert guest"
PROJECT_MEMBER_TYPES = "internal external"

BEHAVIORAL_MODULE_TYPES = "aime csi gpq gmate prol psi sjt interview discussion presentation"
# BEHAVIORAL_SIMULATION_TYPES = "interview discussion presentation"
BEHAVIORAL_MODULE_METHODS = "selftest simulation"

ADMIN_ROLES = "license-admin project-creator project-admin"
USER_CAPABILITIES = "creator admin client expert"

