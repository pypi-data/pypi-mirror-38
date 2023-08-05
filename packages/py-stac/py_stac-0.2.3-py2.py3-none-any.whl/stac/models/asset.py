from stac.models.base import STACObject
from marshmallow import Schema, fields


class Asset(STACObject):
    def __init__(self, href, name=None, key=None):
        """Asset referenced by item

        Args:
            href (str): location (full or relative) of the asset
            name (str): human readable name of asset (optional)
            key (str): key for the asset object value (optional)
        """

        if not key:
            key = "self"
            if name:
                key = name

        if not name:
            self.asset = {"{0}".format(key): {"href": href}}
        else:
            self.asset = {
                "{0}".format(key): {"name": name, "href": href}
            }

    def __repr__(self):
        return '<Asset(asset={self.asset!r})>'.format(self=self)

    @property
    def dict(self):
        return dict(asset=self.asset)

    @property
    def json(self):
        return AssetSchema().dumps(
            self
        )


class AssetValueSchema(Schema):

    name = fields.Str()
    href = fields.URL(required=True)


class AssetSchema(Schema):

    asset = fields.Dict(
        values=fields.Nested(AssetValueSchema),
        key=fields.Str()
    )
