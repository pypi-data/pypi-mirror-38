"""
Main entrance to commandline actions
"""
import click
import time
import logging
from watchdog.observers import Observer

from pylaroid import __version__
from pylaroid.file_handler import PhotoEventHandler


@click.command()
@click.option('-p', '--path', default='.', help="Path to scan")
@click.option('-V', '--version', is_flag=True,
              help="Print out version information.")
def cli_frontend(path, version):
    if version:
        click.echo("Pylaroid {}".format(__version__,))
        return

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = PhotoEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
