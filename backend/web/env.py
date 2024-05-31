from pypharmaco.env_parser import \
    EnvParser, \
    create_entry, \
    replace_newline

def strip_newline(x : str): return x.strip()

ENV_VARS = EnvParser([
    create_entry(
        'PRODUCTION',
        default_value = 'false',
        parser = lambda x : False if x == 'false' else True
    ),
    create_entry('SECRET_KEY', True, parser = strip_newline),
    create_entry('PRIVATE_KEY', True, parser = strip_newline),
    create_entry('PUBLIC_KEY', True, parser = strip_newline) ,
    create_entry('DB_USER', True, parser = strip_newline),
    create_entry('DB_PASSWORD', True, parser = strip_newline),
    create_entry('DB_NAME', True, parser = strip_newline),
    create_entry('DB_PORT', default_value = '5432'),
    create_entry('DB_HOST', default_value = 'db'),
    create_entry('ALLOWED_HOSTS', parser = lambda x: x.split(',')),
    create_entry('CORS_ALLOWED_ORIGINS', parser = lambda x: x.split(',')),
    create_entry(
        'KSSO_SECRET_KEY',
        is_secret = True, 
        default_value = "ucT83TdDq/kUERb+mV9t3viFpD5KcVWshN+XKsiVEk+9VcOK3g6zgWM1erc9h2r0hd6pZmsO2XuKZO3JGyrZdguc",
    ),
    create_entry(
        'SMTP_USERNAME',
        is_secret = True,
        default_value = 'kisa@example.com',
    ),
    create_entry(
        'SMTP_PASSWORD',
        is_secret = True,
        default_value = 'password123'
    ),
    create_entry(
        'SMTP_SERVER',
        default_value = 'example.com'
    ),
])