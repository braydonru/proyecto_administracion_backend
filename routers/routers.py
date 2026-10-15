from routers.user_router import users_router
from routers.store_router import store_router
from routers.product_router import product_router
from routers.sales_router import sales_router
from config.security import security
from routers.test_router import test_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(security)
router.include_router(users_router)
router.include_router(store_router)
router.include_router(product_router)
router.include_router(sales_router)
router.include_router(test_router)