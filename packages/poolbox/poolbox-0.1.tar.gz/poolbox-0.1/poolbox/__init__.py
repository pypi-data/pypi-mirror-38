"""Main entry point.
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.include("cornice_swagger")
    config.scan("poolbox")
    return config.make_wsgi_app()
