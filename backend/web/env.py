from pypharmaco.env_parser import \
    EnvParser, \
    create_entry, \
    replace_newline

ENV_VARS = EnvParser([
    create_entry(
        'PRODUCTION',
        default_value = 'false',
        parser = lambda x : False if x == 'false' else True
    ),
    create_entry('SECRET_KEY', True),
    create_entry('PRIVATE_KEY', True),
    create_entry('PUBLIC_KEY', True) ,
    create_entry('DB_USER', True),
    create_entry('DB_PASSWORD', True),
    create_entry('DB_NAME', True),
    create_entry('DB_PORT', default_value = '5432'),
    create_entry('DB_HOST', default_value = 'db'),
    create_entry('ALLOWED_HOSTS', parser = lambda x: x.split(',')),
    create_entry('CORS_ALLOWED_ORIGINS', parser = lambda x: x.split(',')),
    create_entry('KSSO_SECRET_KEY', is_secret = True),
    create_entry('KSSO_CLIENT_ID')
])
