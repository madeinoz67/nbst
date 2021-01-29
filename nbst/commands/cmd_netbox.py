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
@click.option("--prism", default=False, help="Prism Host name")
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
        logger.debug(results)

        stats = {"vcpu_total": 0, "mem_total": 0, "disk_total": 0}

        click.echo(" ".center(int(14 * 5.5), "="))

        click.echo(
            f'{"Name":14} {"Status":8} {"vcpus":6} {"Memory-MB":6} {"disk-GB":6} {"cluster":20}'
        )
        click.echo(" ".center(int(14 * 5.5), "-"))
        for vm in results:
            stats["vcpu_total"] += vm.vcpus
            stats["mem_total"] += vm.memory
            stats["disk_total"] += vm.disk
            click.echo(f"{vm.name:15}", nl=False)
            if vm.status.label == "Active":
                click.secho(f"{vm.status.label:8}", fg="green", nl=False)
            else:
                click.secho(f"{vm.status.label:8}", fg="yellow", nl=False)
            click.echo(f"{vm.vcpus:6} {vm.memory:8} {vm.disk:8} {vm.cluster.name:20} ")
        click.echo("\n")
        click.echo(
            f"Totals: CPUs:{stats['vcpu_total']:3} Memory-GB: {round(stats['mem_total']/1024,2):6} Disk-TB: {round(stats['disk_total']/1024,2):6} \n"
        )
    except TypeError as e:
        logger.exception(f"{e.args}")
        exit(1)
