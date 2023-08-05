from stac.models.base import STACObject
from marshmallow import (
    Schema,
    fields
)


class Properties(STACObject):
    def __init__(
        self, datetime,
        provider, asset_license,
        ext_properties
    ):
        """Container for providing the core metatdata fields plus extensions

        Args:
            datetime (str):
            provider (str):
            asset_license (str):
            ext_properties (dict):
        """
        self.ext_properties = ext_properties
        self.license = asset_license
        self.provider = provider
        self.datetime = datetime

    @property
    def dict(self):
        base_properties = dict(
            license=self.license,
            provider=self.provider,
            datetime=self.datetime
        )
        if self.ext_properties:
            base_properties.update(self.ext_properties)
        return base_properties

    @property
    def json(self):
        return PropertiesSchema().dumps(
            self
        )


class PropertiesSchema(Schema):

    license = fields.Str()
    provider = fields.Str()
    ext_properties = fields.Dict()
    datetime = fields.Str()
