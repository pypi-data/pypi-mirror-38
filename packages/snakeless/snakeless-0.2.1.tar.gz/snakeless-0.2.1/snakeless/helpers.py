from functools import lru_cache
from pkg_resources import iter_entry_points
from contextlib import contextmanager

from halo import Halo
from yaml import load
from schema import Schema, And, Use, Optional

from .exceptions import CommandFailure

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

@contextmanager
def snakeless_spinner(*args, **kwargs):
    spinner = Halo(*args, **kwargs)
    spinner.start()
    try:
        yield spinner
    except CommandFailure as exc:
        spinner.fail(str(exc))
        raise
    except Exception as exc:
        spinner.fail(
            spinner.text
            + "\n"
            + "Unexpected exception."
        )
        raise
    finally:
        spinner.stop()

def check_config_existence(root_fs, file_name="snakeless.yml"):
    return root_fs.exists(file_name)

@lru_cache()
def get_providers():
    providers = {}
    for entry_point in iter_entry_points("snakeless.providers"):
        providers[entry_point.name] = entry_point.load()
    return providers

@lru_cache()
def get_schemas():
    schemas = {}
    for entry_point in iter_entry_points("snakeless.schemas"):
        schemas[entry_point.name] = entry_point.load()
    return schemas

def get_provider(provider_name, config):
    providers = get_providers() 
    for entry_point in iter_entry_points("snakeless.providers"):
        providers[entry_point.name] = entry_point.load()
    return providers[provider_name](config)

@lru_cache(maxsize=None)
def get_schema(provider_name):
    PROVIDERS = get_providers()
    SUPPORTED_PROVIDERS = PROVIDERS.keys()
    BASE_SCHEMA = {
        "project": {
            "name": str,
            "provider": And(
                Use(str),
                lambda provider: provider in SUPPORTED_PROVIDERS,
                error="Unsupported provider",
            ),
        },
    }
    schemas = get_schemas()
    provider_schema = schemas[provider_name]
    return merge(BASE_SCHEMA, provider_schema)

def parse_config(
    root_fs, file_name="snakeless.yml"
):
    config_file_data = root_fs.gettext("snakeless.yml")
    raw_parsed_config = load(config_file_data, Loader=Loader)
    try:
        provider_name = raw_parsed_config["project"]["provider"]
    except KeyError:
       raise
    else:
        provider_schema = get_schema(provider_name)
    validator = Schema(provider_schema, ignore_extra_keys=True)
    parse_config = validator.validate(raw_parsed_config)
    # TODO: validate a few more fields mannualy
    return parse_config

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value
    return destination
