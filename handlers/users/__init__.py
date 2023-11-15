from aiogram import Router

from .start import router as start_router
from .shop import router as shop_router
from .admin import router as admin_router


__all__ = ["router"]

router = Router()
router.include_router(router=start_router)
router.include_router(router=shop_router)
router.include_router(router=admin_router)
