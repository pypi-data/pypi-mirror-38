import os
import click
import yaml
import typing as t
from clint.textui import colored
from pyfiglet import figlet_format


class Config:
    configuration: t.Optional[t.Dict] = None
    CONFIG_FILE = '.ml-cli.yml'
    sudo_prefix = ''


def configuration_exists():
    return os.path.isfile(Config.CONFIG_FILE)


def require_configuration():
    if not configuration_exists():
        click.echo('New Project :: Please, call init command before calling other commands!')
        exit()


def load_configuration():
    global configuration
    if configuration_exists():
        with open(Config.CONFIG_FILE, 'r') as f:
            Config.configuration = yaml.load(f).get('configuration')


def command_factory(cmd):
    return "{}{}".format(Config.sudo_prefix, cmd)


@click.group()
@click.option('--root/--no-root', default=False)
def cli(root):
    click.echo(figlet_format("ML-CLI", font='slant'))

    if root:
        Config.sudo_prefix = 'sudo '

    load_configuration()


@cli.command()
@click.option('--repository', required=True)
def init(repository):
    click.echo('Creating YAML configuration file ...')
    default_configuration = {
        'configuration': {
            'repository': repository.lower()
        }
    }
    with open(Config.CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(default_configuration, default_flow_style=False))


@cli.command()
def docker_build():
    require_configuration()

    cmd = command_factory("docker build -t {} .".format(Config.configuration['repository']))
    click.echo(colored.green('$ {}'.format(cmd)))
    os.system(cmd)


@cli.command()
@click.option('--gpu/--no-gpu', default=False)
def docker_bash(gpu):
    require_configuration()

    cmd = command_factory("docker run -v `pwd`:/usr/local/src/code {}--rm -it {} bash".format('--runtime=nvidia ' if gpu else '', Config.configuration['repository']))
    click.echo(colored.green('$ {}'.format(cmd)))
    os.system(cmd)


if __name__ == '__main__':
    cli()
