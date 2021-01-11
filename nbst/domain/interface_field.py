import ipaddress
import typing

from loguru import logger
from marshmallow import fields
from marshmallow import utils


class IPInterface(fields.Field):
    """A IP Interface field

    :param bool exploded: If `True`, serialize ipv6 network address in long form,
     ie. with groups
        consisting entirely of zeros included.
    """

    default_error_messages = {"invalid_ip_interface": "Not a valid IP interface."}

    DESERIALIZATION_CLASS = None  # type: typing.Optional[typing.Type]

    def __init__(self, *args, exploded=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.exploded = exploded

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        if value is None:
            return None
        if self.exploded:
            return value.exploded
        return value.compressed

    def _deserialize(
        self, value, attr, data, **kwargs
    ) -> typing.Optional[
        typing.Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]
    ]:
        if value is None:
            return None
        try:
            logger.info(f"deserialize : {value}")
            return (self.DESERIALIZATION_CLASS or ipaddress.ip_interface)(
                utils.ensure_text_type(value)
            )
        except (ValueError, TypeError) as error:
            raise self.make_error("invalid_ip_interface") from error


class IPv4Interface(IPInterface):
    """A IPv4 Interface field"""

    default_error_messages = {"invalid_ip_interface": "Not a valid IPv4 interface."}

    DESERIALIZATION_CLASS = ipaddress.IPv4Interface


class IPv6Network(IPInterface):
    """A IPv6 Interface field."""

    default_error_messages = {"invalid_ip_interface": "Not a valid IPv6 interface."}

    DESERIALIZATION_CLASS = ipaddress.IPv6Interface
