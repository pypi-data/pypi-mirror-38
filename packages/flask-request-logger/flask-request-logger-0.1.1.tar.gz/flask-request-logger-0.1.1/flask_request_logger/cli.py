import os
import sys
import click


def import_application(app_package, req_logger):
    sys.path.append(os.getcwd())
    try:
        _app = __import__(app_package)
    except Exception as e:
        click.echo(
            click.style('Was unable to import {} Error: {}'.format(app_package, e), fg='red'))
        exit(3)
    if hasattr(_app, 'req_logger'):
        return getattr(_app, req_logger)
    else:
        click.echo(click.style('There in no req_logger var on your package,\
                                you can use req_logger parameter to config', fg='red'))
        exit(3)


@click.group('logger')
def logger_cli():
    """
    Flask-Request-Logger commands group
    """
    pass


@logger_cli.command('init_db')
@click.option('--app', default='app', help='Your application init directory (package)')
@click.option('--req_logger', default='req_logger', help='your AppBuilder object')
def init_db(app, req_logger):
    from sqlalchemy import create_engine
    from flask_request_logger.database import Base
    from flask_request_logger.models import RequestLog, ResponseLog

    _req_logger = import_application(app, req_logger)
    print(_req_logger.db_info, type(_req_logger.db_info))
    engine = create_engine(_req_logger.db_info, convert_unicode=True)
    Base.metadata.create_all(bind=engine)
