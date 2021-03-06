from setuptools import setup
import sys
from version import VERSION

setup(
    name = "BootManager",
    version = VERSION,
    maintainer = "Konstantin Andrusenko",
    maintainer_email = "blikproject@gmail.com",
    description = "Blik cloud boot manager",
    packages = ['blik.bootManager'],  # include all packages under src
    scripts = ['bin/configureBootManager.py',
                'bin/node-type-installer',
                'bin/node-image-updater',
                'bin/change-node',
                'blik/bootManager/bootEventListener.py',
                'blik/db/syslog_writer.py'],
    license = 'GPLv3',
    data_files = [('/opt/blik/db', ['blik/db/cloud_db_schema.sql']),
                    ('/opt/blik/db', ['blik/db/logs_schema.sql']),
                    ('/opt/blik/conf',['config/default_node.yaml'])],
    zip_safe = True
)

