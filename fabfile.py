from fabric.api import local
from fabric.context_managers import lcd
from os.path import join, dirname
import datetime

here = dirname(__file__)


def upload():
    with lcd(here):
        local('epio upload -a pygraz')


def extract_messages():
    with lcd(here):
        local('pybabel extract -F babel.cfg -o pygraz_website/translations/messages.pot pygraz_website')
        local('pybabel update -i pygraz_website/translations/messages.pot -d pygraz_website/translations')


def build():
    with lcd(here):
        local('pybabel compile -d pygraz_website/translations')
    with lcd(join(here, 'pygraz_website/static/s')):
        local('compass compile -s compressed')


def backup():
    with(lcd(here)):
        suffix = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        backup_file = 'backup-{0}.sql'.format(suffix)
        local('epio run -- pg_dump > {0}'.format(backup_file))
        local('bzip2 {0}'.format(backup_file))
        local('s3cmd put {0}.bz2 s3://pygraz-backups/'.format(backup_file))
        local('rm {0}.bz2'.format(backup_file))
