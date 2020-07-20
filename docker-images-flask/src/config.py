class SystemConfig:

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': 'user',
        'password': 'password',
        'host': 'mysql-db',
        'db_name': 'database'
    })


Config = SystemConfig
