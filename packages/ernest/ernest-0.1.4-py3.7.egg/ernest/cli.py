import click
from os.path import expanduser

from ernest import get_config, Directory


@click.group(invoke_without_command=True)
@click.option('--config', default='{0}/.config/ernest/ernest.json'.format(expanduser('~')))
@click.option('--name')
@click.argument('folder', default='.')
@click.pass_context
def cli(ctx, config, name, folder):
    try:
        conf = get_config(config, name)
    except FileNotFoundError:
        click.echo('That config file does not exist. Using the default.')
        conf = get_config()
    fol = Directory(folder, conf)
    ctx.obj = {
        'FOLDER': fol
        }
    if ctx.invoked_subcommand is None:
        click.echo('This is your config:')
        click.echo(conf)


@cli.command()
@click.confirmation_option(
    prompt='Make sure you have a backup of anything important! '
           'Do you want to continue formatting?')
@click.argument('ext')
@click.argument('methods', nargs=-1)
@click.pass_context
def fix(ctx, ext, methods):
    fol = ctx.obj['FOLDER']

    for i in fol.files[ext]:
        try:
            i.correct(*methods)
            click.echo('fixed {0}'.format(i.meta.filename))
        except Exception as e:
            click.echo('could not fix {0}'.format(i.meta.path))
            click.echo(e)


@cli.command()
@click.argument('exts', nargs=-1, required=False)
@click.pass_context
def stats(ctx, exts):
    fol = ctx.obj['FOLDER']
    if len(exts) > 0:
        click.echo(fol.filter(exts))
    else:
        click.echo(fol)
