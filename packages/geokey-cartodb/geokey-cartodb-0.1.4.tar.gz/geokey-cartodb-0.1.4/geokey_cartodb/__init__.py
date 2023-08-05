from geokey.extensions.base import register


VERSION = (0, 1, 4)
__version__ = '.'.join(map(str, VERSION))

register(
    'geokey_cartodb',
    'CartoDB',
    display_admin=True,
    superuser=False,
    version=__version__
)
