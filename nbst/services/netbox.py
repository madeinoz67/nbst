import urllib3
from loguru import logger
from netbox import NetBox

urllib3.disable_warnings()  # prevents warnings when not validating SSL certs


class NetboxService:
    """Class representing the external Netbox host"""

    def __init__(self, host, api_key, use_ssl):
        logger.info(
            f"Initialising NetBox service, host={host}, api_key={api_key}, use_ssl={use_ssl}"  # noqa: E501
        )
        self.netboxapi = NetBox(
            host=host, auth_token=api_key, use_ssl=use_ssl, ssl_verify=False
        )
        self.api_key = api_key
        self.host = host

    def get_vms(self):
        """Gets the list of all virtual machines from NetBox"""
        logger.info("Getting list of VMs from NetBox API")
        try:
            result = self.netboxapi.virtualization.get_virtual_machines()
            logger.info(f"Retrieved {len(result)} virtual machines")
            return result
        except ConnectionError as e:
            logger.exception(f"{e.args}")
            exit(1)
