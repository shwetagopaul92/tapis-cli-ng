import configparser
import os
from .config_file import load_config, config_path

__all__ = ['key_values', 'generate_template_ini', 'update_config']


def key_values(filename=None, as_dict=True):
    """Load project config file into a dict for template remdering

    Keyword Arguments:
        filename (str, optional): Path to a project config file. Defaults to $PWD/project.ini
    Returns:
        dict: Variables and names to support Jinja template rendering
    """
    file_path = config_path(filename)
    if os.path.exists(file_path):
        return load_config(file_path, as_dict=as_dict)
    else:
        return dict()


def update_config(config, values_dict=None, add_keys=False):
    """Recursively merge a dict onto a ConfigParser

    This is used to initialize the parser with passed values, like one
    might do when setting up a project for the first time.
    """
    if not isinstance(values_dict, dict):
        values_dict = dict()
    for k, v in values_dict.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                if not isinstance(v1, dict):
                    if add_keys:
                        if k not in config:
                            config[k] = {}
                        config[k][k1] = v1
                    elif k in config and k1 in config[k]:
                        config[k][k1] = v1
                    else:
                        raise KeyError(
                            'Unknown config section or option: {0}/{1}'.format(
                                k, k1))
        else:
            if add_keys:
                config[k] = v
            elif k in config:
                config[k] = v
            else:
                raise KeyError('Unknown config section: {0}'.format(k))


def generate_template_ini(passed_vals=None):
    # TODO - import ini stanzas from function-specific modules (apps, docker, etc)
    # TODO - set config.BOOLEAN_STATES to same as in settings module
    # TODO - add more top-level keys from app.json schema as apps options
    if not isinstance(passed_vals, dict):
        passed_vals = dict()
    config = configparser.ConfigParser()
    config['app'] = {
        'name': '',
        'version': '',
        'bundle': '',
        'deployment_path': '',
        'deployment_system': '',
        'execution_system': ''
    }
    config['actor'] = {
        'name': '',
        'description': '',
        'alias': '',
        'stateless': True,
        'hint': '',
        'privileged': False,
        'use_uid': True,
        'workers': ''
    }
    config['docker'] = {
        'dockerfile': 'Dockerfile',
        'namespace': '',
        'repo': '',
        'tag': '',
        'build_args': '',
        'use_commit_hash': False
    }
    config['env'] = {}
    config['git'] = {'branch': 'master', 'remote': ''}
    config['grants'] = {'read': '', 'execute': '', 'update': ''}
    config['job'] = {}
    config['system'] = {'ssh_private_key': '~/.ssh/id_rsa'}
    update_config(config, passed_vals)
    return config
