from jinja2 import (
    FileSystemLoader, Environment, select_autoescape)

from pydoc import locate


DEFAULT_AUTOESCAPING = {
    'enabled_extensions': ('html', 'htm', 'xml'),
    'disabled_extensions': [],
    'default_for_string': True,
    'default': False
}


def load_extensions_from_config(**config):
    """
    Loads extensions
    """
    extensions = []
    if 'EXTENSIONS' in config:
        for ext in config['EXTENSIONS']:
            try:
                extensions.append(locate(ext))
            except Exception as e:
                print(e)
    return extensions


def get_autoescaping_params(**config):
    if 'AUTOESCAPING' in config:
        autoescaping_params = config['AUTOESCAPING']
    else:
        autoescaping_params = DEFAULT_AUTOESCAPING
    return autoescaping_params


def create_environment(**config):
    params = {}
    template_location = config['path']
    params['encoding'] = config.get('encoding', 'utf-8')
    params['followlinks'] = config.get('followlinks', False)
    env = Environment(
        loader=FileSystemLoader(template_location, **params),
        autoescape=select_autoescape(**get_autoescaping_params(**config)),
        extensions=load_extensions_from_config(**config)
    )
    return env
