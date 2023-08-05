from stac.models.base import STACObject
from marshmallow import (
    Schema,
    fields
)


class Link(STACObject):
    def __init__(self, link_type, rel, href, hreflang):
        """Link to related objects, must have an href optionally type

        Args:
            type (str): only one type (self)
            rel (str): self
            href (str): uri location
            hreflang (str): uri language
        """
        self.type = link_type
        self.rel = rel
        self.href = href
        self.hreflang = hreflang

    @property
    def dict(self):
        return dict(
            type=self.type,
            rel=self.rel,
            href=self.href,
            hreflang=self.hreflang
        )

    @property
    def json(self):
        return LinkSchema().dumps(
            self
        )


class LinkSchema(Schema):

    link_type = fields.Str()
    rel = fields.Str()
    href = fields.Str()   # TBD with fields.URL()
    hreflang = fields.Str()
