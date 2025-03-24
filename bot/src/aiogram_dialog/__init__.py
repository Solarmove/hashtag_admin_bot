from .admin_dialogs import dialogs as admin_dialogs
from .user_dialogs import dialogs as user_dialogs

dialog_routers = [
    *admin_dialogs,
    *user_dialogs,
]
