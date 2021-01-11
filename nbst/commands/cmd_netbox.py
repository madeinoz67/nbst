import click
from loguru import logger
from marshmallow import EXCLUDE
from rich.table import Table

from nbst.cli import AppContext
from nbst.cli import pass_info
from nbst.domain.netbox_schema import VirtualMachine
from nbst.domain.netbox_schema import VirtualMachineSchema
from nbst.services.netbox import NetboxService


@click.group()
@click.option("--host", type=str, help="Netbox Host")
@click.option("--apikey", type=str, help="Netbox API key")
@click.option(
    "--use-ssl", default=False, flag_value=True, show_default=True, help="Use SSL"
)
@pass_info
def cli(app_ctx: AppContext, host, apikey, use_ssl):
    """Netbox Utilities Command

    Performs NetBox related commands

    """
    pass
    app_ctx.netboxservice = NetboxService(host, apikey, use_ssl)


# @cli.command()
# @click.option(
#     "-d",
#     "--dryrun",
#     flag_value=True,
#     help="Enable dry run (will not update NetBox)",
#     default=False,
#     show_default=True,
# )
# @click.option(
#     "-p",
#     "--prune",
#     default=False,
#     show_default=True,
#     flag_value=True,
#     help="Removes orphaned NetBox objects",
# )
# @click.option("--prism", default=False, help="Prism Host name")
# @click.argument("prism_hostname", type=str, metavar="<prismhost>")
# @pass_info
# def sync(app_ctx: AppContext, prism_hostname, dryrun, prune=False):
#     """Sync netbox with prism central server

#     This will update Netbox with the objects on the remote Nutanix prism
#     central server.

#     Parameters:
#     -----------
#     app_ctx: AppContext
#         Object with application settings shared between commands
#     prism_hostname: str
#         FQDN of the Nutanix Prism central server
#     dryrun: bool
#         when enabled will not do any updates on the NetBoxServer
#           (default is False)
#     prune: bool
#         when enabled entities on Netbox marked for pruning will be removed
#     """
#     click.echo("syncing....")
#     logger.debug(
#         f"Syncing Netbox host {netbox_hostname} from prism host {prism_hostname}
#       prune={prune} dryrun={dryrun}"
#     )


@cli.command()
@pass_info
def list_vms(app_ctx: AppContext):
    """lists all virtual machines in netbox

    Displays all Virtual Machine entities on the NetboxAPI in a table
    """
    logger.info("command: list_vms")

    console = app_ctx.console

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", width=14)
    table.add_column("Status", width=8, justify="center")
    table.add_column("vcpus", width=6, justify="right")
    table.add_column("Memory(MB)", justify="right")
    table.add_column("Disk(GB)", justify="right")
    table.add_column("Cluster", width=14, justify="center")
    table.add_column("IP", width=15)

    try:
        with console.status(
            "[bold green] Retrieving Virtual Machines from Netbox API..."
        ) as _:
            vm_schema = VirtualMachineSchema(many=True, unknown=EXCLUDE)
            vm_data = app_ctx.netboxservice.get_vms()
            results = vm_schema.load(vm_data)

        logger.debug(results)

        stats = {"vcpu_total": 0, "mem_total": 0, "disk_total": 0}

        for vm in results:
            vm is VirtualMachine
            stats["vcpu_total"] += vm.vcpus
            stats["mem_total"] += vm.memory
            stats["disk_total"] += vm.disk

            if vm.status.label == "Active":
                vm_status = f"[green]{vm.status.label}[/green]"
            else:
                vm_status = f"[yellow]{vm.status.label:^8}[/yellow]"

            table.add_row(
                vm.name,
                vm_status,
                str(vm.vcpus),
                str(vm.memory),
                str(vm.disk),
                vm.cluster.name,
                str(vm.primary_ip.address),
            )

        # Totals
        table.add_row(end_section=True)
        table.add_row(
            "Total:",
            "",
            str(stats["vcpu_total"]),
            str(stats["mem_total"]),
            str(stats["disk_total"]),
        )
        table.add_row(
            None,
            None,
            None,
            f"({str(round(stats['mem_total'] / 1000, 2))} GB)",
            f"({str(round(stats['disk_total'] / 1000, 2))} TB)",
        )
        console.print(table)

    except TypeError as e:
        logger.exception(f"{e.args}")
        exit(1)
