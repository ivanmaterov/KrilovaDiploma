from .installed_apps import LOCAL_APPS

SHELL_PLUS = 'ipython'

# loading of factories in shell_plus
SHELL_PLUS_PRE_IMPORTS = [
    f'from {app}.factories import *' for app in LOCAL_APPS
]

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
