# -*- encoding: utf-8 -*-



from . import brand, equipment
from ... import decorators, module

_all = module.All(globals())


class Camera(equipment.Equipement):

    brand_class = brand.Brand

    @property
    def brand(self):
        return self.brand_class(self.metadata['Exif.Image.Make'].data)

    @property
    def _model(self):
        return self.metadata['Exif.Image.Model'].data

    @decorators.cached_property
    def tags(self):
        return {k: t for k, t in self.metadata.tags.items() if 'camera' in t.label.lower()}


__all__ = _all.diff(globals())
