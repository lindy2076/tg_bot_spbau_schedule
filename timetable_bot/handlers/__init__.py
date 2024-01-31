from .commands import (
    main_router
)
from .callback import (
    callback_router
)

from .admin import (
    admin_router
)


__all__ = [
    "main_router", "callback_router", "admin_router"
]
