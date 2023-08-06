from setuptools import setup

setup(
    name='sedldata',
    version='0.0.2',
    license='BSD',
    packages=['sedldata', 'sedldata.migrate', 'sedldata.migrate.versions'],
    package_data={'sedldata': ['alembic.ini'], 'sedldata.migrate': 'script.py.mako'},
    install_requires=[
        'Click',
        'SQLAlchemy',
        'alembic',
        'psycopg2',
        'configparser',
        'jinja2',
        'requests',
        'flattentool'
    ],
    entry_points='''
        [console_scripts]
        sedldata=sedldata.cli:cli
    ''',
)
