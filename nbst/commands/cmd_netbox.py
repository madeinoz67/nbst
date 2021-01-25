import click
from loguru import logger

from nbst.cli import pass_info


class Context:
    def __init__(self):
        self.netbox = None


@click.group()
@click.pass_context
def cli(ctx):
    """Netbox Utilities"""
    ctx.obj = Context()


@cli.command()
@click.option(
    "-d",
    "--dryrun",
    flag_value=True,
    help="Enable dry run (will not update NetBox)",
    default=False,
    show_default=True,
)
@click.option(
    "-p",
    "--prune",
    default=False,
    show_default=True,
    flag_value=True,
    help="Removes orphaned NetBox objects",
)
@click.argument("netbox_hostname", type=str, metavar="<netbox>")
@click.argument("prism_hostname", type=str, metavar="<prism>")
# @click.pass_context
@pass_info
def sync(ctx, netbox_hostname, prism_hostname, dryrun, prune=False):
    """Sync netbox with prism central server

    This will update Netbox with the objects on the remote nutanix prism central server.

    Where:\n
    <netbox> is the FQDN of the netbox server \n
    <prism> is the FQDN of the Nutanix Prism central server
    """
    click.echo("syncing....")
    logger.debug(
        f"Syncing Netbox host {netbox_hostname} from prism host {prism_hostname} prune={prune} dryrun={dryrun}"
    )
