from fastapi import APIRouter

from api.v1.login import router as login
from api.v1.admin_license import router as admin_license
from api.v1.admin_user import router as admin_user
from api.v1.admin_module import router as admin_module

from api.v1.license import router as license_routes
from api.v1.user import router as user_routes
from api.v1.client import router as client_routes
from api.v1.contract import router as contract_routes
from api.v1.project import router as project_routes
from api.v1.public import router as public_routes

router = APIRouter()

# router.include_router(public_routes, prefix="/licenses/{license}", tags=["✅ Public"])
router.include_router(login, tags=["✅ Login"])
# router.include_router(admin_license, prefix="/admin/licenses", tags=["🅰️ Licenses"])
# router.include_router(admin_module, prefix="/admin/modules", tags=["🅰️ Modules"])
# router.include_router(admin_user, prefix="/admin/users", tags=["🅰️ Users"])

router.include_router(license_routes, prefix="/licenses/{slug}", tags=["✅ Tenant"])
router.include_router(user_routes, prefix="/licenses/{slug}/users", tags=["✅ Tenant Users"])
router.include_router(client_routes, prefix="/licenses/{slug}/clients", tags=["✅ Tenant Clients"])
router.include_router(contract_routes, prefix="/licenses/{slug}/contracts", tags=["✅ Tenant Contracts"])
router.include_router(project_routes, prefix="/licenses/{slug}/projects", tags=["✅ Tenant Projects"])
