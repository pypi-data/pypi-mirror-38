import geojson
from stac.models.geojson_type import GeojsonType
from stac.models.asset import AssetValueSchema
from stac.models.base import STACObject
from stac.models.link import LinkValueSchema
from stac.models.properties import PropertiesSchema
from marshmallow import (
    Schema,
    fields
)


class Item(STACObject):
    def __init__(
        self, item_id,
        geometry, properties,
        links, assets
    ):
        """STAC Catalog item

        Args:
            item_id (str):
            geometry (Polygon):
            properties (Properties):
            links (Dict[Link.link]):
            assets (Dict[Asset.asset]):
        """
        self.links = links
        self.properties = properties
        self.geometry = geometry
        self.id = item_id
        self.assets = assets

    @property
    def bbox(self):
        lats, lngs = zip(*geojson.utils.coords(self.geometry))
        return [min(lats), min(lngs), max(lats), max(lngs)]

    @property
    def type(self):
        return GeojsonType.Feature.value

    @property
    def dict(self):
        return dict(
            type=self.type,
            id=self.id,
            properties=self.properties.dict,
            geometry=self.geometry,
            bbox=self.bbox,
            links={k_link: v_link for (k_link, v_link) in self.links.items()},
            assets={k_asset: v_asset for (k_asset, v_asset) in self.assets.items()}
        )

    @property
    def json(self):
        return ItemSchema().dumps(
            self
        )


class ItemSchema(Schema):

    type = fields.Str()
    links = fields.Dict(
        key=fields.Str(),
        values=fields.Nested(LinkValueSchema),
        many=True
    )
    properties = fields.Nested(PropertiesSchema)
    bbox = fields.List(fields.Float())
    geometry = fields.Dict()
    id = fields.Str()
    assets = fields.Dict(
        key=fields.Str(),
        values=fields.Nested(AssetValueSchema),
        many=True
    )
