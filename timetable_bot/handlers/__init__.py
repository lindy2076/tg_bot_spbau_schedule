from .commands import (
    main_router,
)
from .callback import (
    callback_router
)


# list_of_commands = [
#     (send_hello, ['start', 'help']),
#     (send_week_schedule, ['week']),
#     (get_day_schedule, ['day']),
#     (get_today_schedule, ['today']),
#     (get_current_class, ['now']),
#     (get_next_class, ['next']),
#     (set_user_group, ['setgr']),
#     (get_user_group, ['me']),
#     (del_me_from_db, ['del']),
#     (send_echo, None)
# ]

# callback_handlers = [
#     (handle_user_group, lambda c: c.data and c.data.startswith("setgr")),
#     (handle_day_select, lambda c: c.data and c.data.startswith("day")),
#     (handle_day_switch, lambda c: c.data and c.data.startswith("wd"))
# ]

__all__ = [
    "main_router", "callback_router"
]
