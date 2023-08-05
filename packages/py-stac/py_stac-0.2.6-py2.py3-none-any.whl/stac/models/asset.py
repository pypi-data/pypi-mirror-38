from stac.models.base import STACObject
from marshmallow import Schema, fields


class Asset(STACObject):
    def __init__(self, href, name=""):
        """Asset referenced by item

        Args:
            href (str): location (full or relative) of asset
            name (str): human readable name of asset
        """

        self.name = name
        self.href = href

    @property
    def dict(self):
        base_properties = dict(
            href=self.href
        )
        if self.name:
            base_properties['name'] = self.name

        return base_properties

    @property
    def json(self):
        return AssetSchema().dumps(
            self
        )


class AssetSchema(Schema):

    name = fields.Str()
    href = fields.Str()  # TBD fields.URL()
