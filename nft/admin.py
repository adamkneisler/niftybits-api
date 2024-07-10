from django.contrib import admin

from .models import *


admin.site.register(NiftyFile)
admin.site.register(Attribute)
admin.site.register(Unlockable)
admin.site.register(Collection)
admin.site.register(CollectionAuth)
admin.site.register(CollectionAttribute)
admin.site.register(CollectionStats)
admin.site.register(CollectionRoyalty)
admin.site.register(Schema)
admin.site.register(SchemaAttribute)
admin.site.register(Template)
admin.site.register(TemplateAttribute)
admin.site.register(TemplateRoyalty)
admin.site.register(TemplateUnlockable)
admin.site.register(Asset)
admin.site.register(AssetAttribute)
admin.site.register(AssetUnlockable)
admin.site.register(AssetTransfer)
admin.site.register(Order)
