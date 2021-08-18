import click

from nbst.cli import AppContext
from nbst.cli import pass_info


@click.group()
# @click.option("--host", type=str, help="Netbox Host")
# @click.option("--apikey", type=str, help="Netbox API key")
# @click.option(
#    "--use-ssl", default=False, flag_value=True, show_default=True, help="Use SSL"
# )
@pass_info
def cli(app_ctx: AppContext):
    pass
