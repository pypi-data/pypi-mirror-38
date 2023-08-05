from marshmallow import fields, Schema
from stac.models.geojson_type import GeojsonType
from stac.models.item import ItemSchema
from stac.models.base import STACObject


class Collection(STACObject):
    def __init__(
        self, features, collection_id
    ):
        """STAC Catalog item collection

        Args:
            features (List[Item]):
        """
        self.features = features
        self.id = collection_id

    @property
    def type(self):
        return GeojsonType.FeatureCollection.value

    @property
    def dict(self):
        return dict(
            type=self.type,
            id=self.id,
            features=[feature.dict for feature in self.features]
        )

    @property
    def json(self):
        return CollectionSchema().dumps(
            self
        )


class CollectionSchema(Schema):

    type = fields.Str()
    id = fields.Str()
    features = fields.Nested(ItemSchema, many=True)
