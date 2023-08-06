import os

# your site id
SITE_ID = 0

CONFIG = {
    # key: (username, secret, apiserver)
}

def get_config(env_key):
    username = secret = apiserver = None

    if env_key in CONFIG:
        username, secret, apiserver = CONFIG[env_key]

    else:
        # Locate and autoload configuration from ~/.cxrc
        rc = os.path.join(os.path.expanduser('~'), '.cxrc')
        if os.path.exists(rc):
            for line in open(rc):
                fields = line.split()
                if fields[0] == 'authentication' and len(fields) == 3:
                    username = fields[1]
                    secret = fields[2]
                elif fields[0] == 'apiserver' and len(fields) == 2:
                    apiserver = fields[1]

    return username, secret, apiserver
