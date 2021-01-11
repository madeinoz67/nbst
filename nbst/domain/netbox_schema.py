import attr
from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from marshmallow import validate

from nbst.domain.interface_field import IPInterface
from nbst.domain.interface_field import IPv4Interface


@attr.s
class Status:
    """represents Status DTO"""

    id = attr.ib()
    value = attr.ib()
    label = attr.ib()


class StatusSchema(Schema):
    id = fields.Int(required=True)
    value = fields.Str(required=True)
    label = fields.Str(required=True)

    @post_load
    def make_status(self, data, **kwargs):
        return Status(**data)


@attr.s
class Site:
    id = attr.ib()
    name = attr.ib()
    slug = attr.ib()
    url = attr.ib()


class SiteSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    slug = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    url = fields.URL()

    @post_load
    def make_site(self, data, **kwargs):
        return Site(**data)


@attr.s
class Cluster:
    id = attr.ib()
    name = attr.ib()
    url = attr.ib()


class ClusterSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    url = fields.URL()

    @post_load
    def make_cluster(self, data, **kwargs):
        return Cluster(**data)


@attr.s
class PrimaryIPInterface:
    id = attr.ib()
    family = attr.ib()
    address = attr.ib()
    url = attr.ib()


class PrimaryIPSchema(Schema):
    id = fields.Int()
    family = fields.Int()
    url = fields.URL()
    address = IPInterface(required=True)

    @post_load
    def make_ip(self, data, **kwargs):
        return PrimaryIPInterface(**data)


@attr.s
class PrimaryIPv4Interface:
    id = attr.ib()
    family = attr.ib()
    address = attr.ib()
    url = attr.ib()


class PrimaryIPv4InterfaceSchema(Schema):
    id = fields.Int()
    family = fields.Int()
    url = fields.URL()
    address = IPv4Interface(required=True)

    @post_load
    def make_ipv4(self, data, **kwargs):
        return IPv4Interface(**data)


@attr.s
class Tenant:
    id = attr.ib()
    name = attr.ib()
    slug = attr.ib()
    url = attr.ib()


class TenantSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    slug = fields.Str(
        required=True,
        validate=[validate.Regexp("^[-a-zA-Z0-9_]+$"), validate.Length(min=1, max=50)],
    )
    url = fields.URL()

    @post_load
    def make_tenant(self, data, **kwargs):
        return Tenant(**data)


@attr.s
class Role:
    id = attr.ib()
    name = attr.ib()
    slug = attr.ib()
    url = attr.ib()


class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    slug = fields.Str(
        required=True,
        validate=[validate.Regexp("^[-a-zA-Z0-9_]+$"), validate.Length(min=1, max=50)],
    )
    url = fields.URL()

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)


@attr.s
class Platform:
    id = attr.ib()
    name = attr.ib()
    slug = attr.ib()
    url = attr.ib()


class PlatformSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    slug = fields.Str(
        validate=[validate.Regexp("^[-a-zA-Z0-9_]+$"), validate.Length(min=1, max=50)]
    )
    url = fields.URL()

    @post_load
    def make_Platform(self, data, **kwargs):
        return Platform(**data)


@attr.s
class VmCustomFields:
    cf_itsop = attr.ib()
    cf_itsop_url = attr.ib()
    cf_sync_key = attr.ib()


class VmCustomFieldsSchema(Schema):
    cf_itsop = fields.Str(allow_none=True)
    cf_itsop_url = fields.URL(allow_none=True)
    cf_sync_key = fields.UUID(allow_none=True)

    @post_load
    def make_custom_fields(self, data, **kwargs):
        return VmCustomFields(**data)


@attr.s
class VirtualMachine:
    id = attr.ib()
    name = attr.ib()
    vcpus = attr.ib()
    memory = attr.ib()
    disk = attr.ib()
    tags = attr.ib()
    comments = attr.ib()
    created = attr.ib()
    last_updated = attr.ib()
    status = attr.ib()
    cluster = attr.ib()
    role = attr.ib()
    platform = attr.ib()
    primary_ip = attr.ib()
    primary_ip4 = attr.ib()
    custom_fields = attr.ib()
    site = attr.ib()
    # config_context = attr.ib()
    tenant = attr.ib()


class VirtualMachineSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=64))
    status = fields.Nested(StatusSchema)
    cluster = fields.Nested(ClusterSchema, required=True)
    role = fields.Nested(RoleSchema, allow_none=True)
    platform = fields.Nested(PlatformSchema, allow_none=True)
    site = fields.Nested(SiteSchema)
    tenant = fields.Nested(TenantSchema, allow_none=True)
    vcpus = fields.Int(validate=validate.Range(min=0, max=32767))
    memory = fields.Int(validate=validate.Range(min=0, max=2147483647))
    disk = fields.Int(validate=validate.Range(min=0, max=2147483647))
    primary_ip = fields.Nested(PrimaryIPSchema, allow_none=True)
    primary_ip4 = fields.Nested(PrimaryIPv4InterfaceSchema, allow_none=True)
    custom_fields = fields.Nested(VmCustomFieldsSchema)
    tags = fields.List(fields.Str())
    # config_context = fields.Str() #TODO: not being seeing as string
    comments = fields.String()
    created = fields.Date()
    last_updated = fields.DateTime()

    @post_load
    def make_vm(self, data, **kwargs):
        return VirtualMachine(**data)
