from stac.models.base import STACObject
from marshmallow import (
    Schema,
    fields
)


class Link(STACObject):
    def __init__(self, rel, href, key=None):
        """Link to related objects, use the rel argument as key

        Args:
            rel (str): self
            href (str): uri location
            key (str): key for the link object value (optional)
        """

        if not key:
            key = rel
        self.link = {
            "{0}".format(key): {"rel": rel, "href": href}
        }

    def __repr__(self):
        return '<Link(link={self.link!r})>'.format(self=self)

    @property
    def dict(self):
        return dict(link=self.link)

    @property
    def json(self):
        return LinkSchema().dumps(
            self
        )


class LinkValueSchema(Schema):

    rel = fields.Str(required=True)
    href = fields.URL(required=True)


class LinkSchema(Schema):

    link = fields.Dict(
        values=fields.Nested(LinkValueSchema),
        key=fields.Str()
    )
