# -*- coding: utf-8 -*-

""" Helper functions to deal with configuration files
"""

from __future__ import print_function, division, unicode_literals

from collections import OrderedDict

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import time
import json
import os


def load_config_ini(full_path, default=True):
    """ Load configuration file with the option of
        ignoring the DEFAULT section.

        Parameters
        ----------
        full_path : str

            File path to the configuration file.

        default : bool, optional

            Whether to allow the python ConfigParser to expand the
            contents of the DEFAULT section into the other sections.
            (the default is True, which expands copies all the
            attributes inside the DEFAULT section into the other
            sections inside which they don't exist already.)

        Returns
        -------
        config : collections.OrderedDict

            The configuration dictionary resulting from parsing the
            configuration file. It is a collections.OrderedDict
            dictionary so that the order of the sections and attributes
            is preserved in the resulting dictionary.
    """
    if default:
        default_section = 'DEFAULT'
    else:
        default_section = 'DEFAULT' + os.urandom(16).hex()
    config_ini = configparser.ConfigParser(dict_type=OrderedDict,
                                           default_section=default_section,
                                           interpolation=None)
    config_ini.read(full_path)
    config = OrderedDict()
    for section in config_ini.sections():
        config[section] = OrderedDict()
        for option in config_ini.options(section):
            config[section][option] = config_ini.get(section, option)
    return config


def merge_default(config):
    """ Merge the values of the DEFAULT item into the other items.
    
        Merge a dictionary that has an item with a "DEFAULT" key,
        if that item is itself a dictionary, then merge that
        item's subitems with all the other items in the dictionary
        that are also themselves dictionaries.

        The purpose is to mimic the behaviour of the [DEFAULT]
        sections of .ini or .conf files when using .json or .yaml
        files, or when using OrderedDict or dict data structures.

        Parameters
        ----------
        config : dict or OrderedDict

            The dictionary that is to have its "DEFAULT" key merged
            with the other keys.

        Returns
        -------
        OrderedDict or dict

            The merged version of the dictionary as an OrderedDict,
            or the original config (be it a dict or an OrderedDict)
            if it had no "DEFAULT" key to begin with, or it was not
            a dict or an OrderedDict.
    """
    if isinstance(config, dict) and "DEFAULT" in config:
        default = config["DEFAULT"]
        merged_config = OrderedDict()
        for item in config:
            if item != "DEFAULT":
                if isinstance(config[item], dict):
                    merged_item = default.copy()
                    merged_item.update(config[item])
                    merged_config[item] = merged_item
                else:
                    merged_config[item] = config[item]
        return merged_config
    else:
        return config


def load_config_json(full_path, default=True):
    try:
        with open(full_path) as config_json:
            config = json.load(config_json, object_pairs_hook=OrderedDict)
            if default:
                config = merge_default(config)
    except IOError:
        time.sleep(1.0)
        with open(full_path) as config_json:
            config = json.load(config_json, object_pairs_hook=OrderedDict)
            if default:
                config = merge_default(config)

    return config


try:
    import yaml
    import sys

    if sys.version_info[0] < 3:
        def my_unicode_repr(self, data):
            return self.represent_str(data.encode('utf-8'))

        yaml.representer.Representer.add_representer(unicode, my_unicode_repr)

    YAML_AVAILABLE = True

except ImportError:
    YAML_AVAILABLE = False


if YAML_AVAILABLE:

    class OrderedDictYAMLLoader(yaml.Loader):
        """ A YAML loader that loads mappings into ordered dictionaries.
        """

        def __init__(self, *args, **kwargs):
            yaml.Loader.__init__(self, *args, **kwargs)

            self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
            self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

        def construct_yaml_map(self, node):
            data = OrderedDict()
            yield data
            value = self.construct_mapping(node)
            data.update(value)

        def construct_mapping(self, node, deep=False):
            if isinstance(node, yaml.MappingNode):
                self.flatten_mapping(node)
            else:
                raise yaml.constructor.ConstructorError(None, None,
                                                        'expected a mapping node, but found %s' % node.id,
                                                        node.start_mark)
            mapping = OrderedDict()
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                try:
                    hash(key)
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError('while constructing a mapping',
                                                            node.start_mark, 'found unacceptable key (%s)' % exc,
                                                            key_node.start_mark)
                value = self.construct_object(value_node, deep=deep)
                mapping[key] = value
            return mapping


def load_config_yaml(full_path, default=True):
    if YAML_AVAILABLE:
        try:
            with open(full_path) as config_yaml:
                config = yaml.load(config_yaml, Loader=OrderedDictYAMLLoader)
                if default:
                    config = merge_default(config)
        except IOError:
            time.sleep(1.0)
            with open(full_path) as config_yaml:
                config = yaml.load(config_yaml, Loader=OrderedDictYAMLLoader)
                if default:
                    config = merge_default(config)
        return config
    else:
        return dict()


def write_yaml(f, data):
    if YAML_AVAILABLE:
        final_yaml = ''
        for heading in data:
            if final_yaml:
                final_yaml += "\n{}:\n".format(heading)
            else:
                final_yaml = "{}:\n".format(heading)
            for item in data[heading]:
                yaml_item = yaml.dump({ item: data[heading][item] },
                                        default_flow_style=False)
                final_yaml += '  {}'.format(yaml_item)
        f.write(final_yaml)
    else:
        print('''
To use YAML files the pyyaml package must be installed.
To install it try using one of the following commands:

  conda install pyyaml
    or
  pip install pyyaml
''')


def get_file_type_and_mtime(path_with_name):
    latest_mtime = -1.0
    latest_type = ''
    tokens = path_with_name.split('.')
    explicit_type = ''
    if len(tokens) > 0:
        explicit_type = '.' + tokens[-1]
        if explicit_type in {'.json', '.conf', '.ini', '.yaml', '.yml'}:
            path_with_name = '.'.join(tokens[:-1])
        else:
            explicit_type = ''
    if explicit_type:
        try:
            mtime = os.path.getmtime(path_with_name + explicit_type)
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_type = explicit_type
        except OSError:
            pass
    else:
        for file_type in {'.json', '.conf', '.ini', '.yaml', '.yml'}:
            try:
                mtime = os.path.getmtime(path_with_name + file_type)
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    latest_type = file_type
            except OSError:
                pass
    return path_with_name, latest_type, latest_mtime


def get_config(path_with_name, file_type, default=True):
    if file_type == '.json':
        return load_config_json(path_with_name + file_type,
                                default=default)
    elif file_type in ('.conf', '.ini'):
        return load_config_ini(path_with_name + file_type,
                               default=default)
    elif YAML_AVAILABLE and file_type in ('.yaml', '.yml'):
        return load_config_yaml(path_with_name + file_type,
                                default=default)
    return OrderedDict()  # No config file found
