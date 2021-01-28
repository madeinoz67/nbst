import click
from loguru import logger
from marshmallow import EXCLUDE

from nbst.cli import pass_info
from nbst.domain.netbox_schema import VirtualMachineSchema
from nbst.services.netbox import NetboxService


class Context:
    def __init__(self):
        self.netboxservice = None


@click.group()
@click.option("--host", type=str, help="Netbox Host")
@click.option("--apikey", type=str, help="Netbox API key")
@click.option(
    "--use-ssl", default=False, flag_value=True, show_default=True, help="Use SSL"
)
# @click.pass_context
@pass_info
def cli(ctx, host, apikey, use_ssl):
    """Netbox Utilities"""
    ctx.obj = Context()
    ctx.obj.netboxservice = NetboxService(host, apikey, use_ssl)


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
@click.option(
    "--prism",
    default=False,
    help="Prism Host name",
)
@click.argument("prism_hostname", type=str, metavar="<prism>")
@pass_info
def sync(ctx, netbox_hostname, prism_hostname, dryrun, prune=False):
    """Sync netbox with prism central server

    This will update Netbox with the objects on the remote Nutanix prism central server.

    Where:\n
    <prism> is the FQDN of the Nutanix Prism central server
    """
    click.echo("syncing....")
    logger.debug(
        f"Syncing Netbox host {netbox_hostname} from prism host {prism_hostname} prune={prune} dryrun={dryrun}"
    )


@cli.command()
@pass_info
def list_vms(ctx):
    """lists all virtual machines in netbox """
    logger.debug("command: list_vms")
    try:
        vm_schema = VirtualMachineSchema(many=True, unknown=EXCLUDE)

        vm_data = ctx.obj.netboxservice.get_vms()

        results = vm_schema.load(vm_data)
    except TypeError as e:
        logger.exception(f"{e.args}")
        exit(1)
    logger.debug(results)
