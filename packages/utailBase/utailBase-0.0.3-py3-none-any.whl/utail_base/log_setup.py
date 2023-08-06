# import os
# import logging
# import logging.config
# import yaml

# def setup_logging(
#     default_path='logging.yaml',
#     default_level=logging.INFO,
#     env_key='LOG_CFG'
# ):
#     """Setup logging configuration

#     """
#     path = default_path
#     value = os.getenv(env_key, None)

#     print(path)

#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, 'rt') as f:
#             config = yaml.safe_load(f.read())
#         logging.config.dictConfig(config)
#         print('loaded yaml. path:{}'.format(path))
#     else:
#         logging.basicConfig(level=default_level)
#         print('not found configFile.')


import os
import yaml
import logging.config
import logging
import coloredlogs

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    | Logging Setup
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
        print('loaded yaml. path:{}'.format(path))
        print( config )
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')