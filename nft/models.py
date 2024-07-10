from django.db import models
from django.contrib.postgres.fields import JSONField

from simple_history.models import HistoricalRecords

from user.models import NiftyUser


class NiftyFile(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    uri = models.CharField(max_length=2048, blank=True, null=True)
    thumb_uri = models.CharField(max_length=2048, blank=True, null=True)
    ipfs_hash = models.CharField(max_length=1024, blank=True, null=True)
    thumb_ipfs_hash = models.CharField(max_length=1024, blank=True, null=True)

    uploader = models.ForeignKey(NiftyUser, related_name='nifty_file_uploader', null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(NiftyFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    ATTRIBUTE_TYPE = (
       ('number', ('Number')),
       ('string', ('String')),
       ('boolean', ('Boolean')),
    )
    attribute_type = models.CharField(
        max_length=32,
        choices=ATTRIBUTE_TYPE,
        default='string',
    )

    name = models.CharField(max_length=512, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Attribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Unlockable(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    uri = models.CharField(max_length=2048, blank=True, null=True)

    uploader = models.ForeignKey(NiftyUser, related_name='unlockable_uploader', null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Unlockable, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


#############################
### Collection Models ###
#############################
class Collection(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)

    banner_image = models.ForeignKey(NiftyFile, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(NiftyUser, null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CollectionAuth(models.Model):
    user = models.ForeignKey(NiftyUser, related_name='collectionauth_user', null=True, on_delete=models.SET_NULL)
    collection = models.ForeignKey(Collection, related_name='collectionauth_collection', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user + " " + self.collection

class CollectionAttribute(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    count = models.FloatField()

    collection = models.ForeignKey(Collection, related_name='collectionattribute_collection', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.collection + " " + self.name

class CollectionStats(models.Model):
    value = models.CharField(max_length=512, blank=True, null=True)
    count = models.FloatField()

    attribute = models.ForeignKey(CollectionAttribute, related_name='collectionstats_attribute', null=True, on_delete=models.SET_NULL)
    collection = models.ForeignKey(Collection, related_name='collectionstats_collection', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.collection + " " + self.value

class CollectionRoyalty(models.Model):
    bp = models.FloatField()

    collection = models.ForeignKey(Collection, related_name='collectionroyaltty_collection', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.collection + " " + str(self.bp)


#############################
### Schema Models ###
#############################
class Schema(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    
    collection = models.ForeignKey(Collection, related_name='schema_collection', null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Schema, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class SchemaAttribute(models.Model):
    schema = models.ForeignKey(Schema, related_name='schemaattribute_schema', null=True, on_delete=models.SET_NULL)
    attribute = models.ForeignKey(Attribute, related_name='schemaattribute_attribue', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.schema + " " + self.attribute


#############################
### Template Models ###
#############################
class Template(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    max_supply = models.IntegerField(blank=True, null=True)
    burnable = models.BooleanField(default=False)
    transferrable = models.BooleanField(default=False)
    
    image = models.ForeignKey(NiftyFile, related_name='template_image', null=True, on_delete=models.SET_NULL)
    schema = models.ForeignKey(Schema, null=True, related_name='template_schema', on_delete=models.SET_NULL)
    creator = models.ForeignKey(NiftyUser, related_name='template_creator', null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Template, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class TemplateAttribute(models.Model):
    template = models.ForeignKey(Template, related_name='templateattribute_template', null=True, on_delete=models.SET_NULL)
    attribute = models.ForeignKey(Attribute, related_name='templateattribute_attribute', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.template + " " + self.attribute

class TemplateRoyalty(models.Model):
    bp = models.FloatField()

    template = models.ForeignKey(Template, related_name='templateroyalty_template', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.template + " " + str(self.bp)

class TemplateUnlockable(models.Model):
    template = models.ForeignKey(Template, related_name='templateunlockable_template', null=True, on_delete=models.SET_NULL)
    unlockable = models.ForeignKey(Unlockable, related_name='templateunlockable_unlockable', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.template + " " + self.unlockable


#############################
### Asset Models ###
#############################
class Asset(models.Model):
    mint_number = models.IntegerField()
    ipfs_hash = models.CharField(max_length=1024, blank=True, null=True)

    image = models.ForeignKey(NiftyFile, related_name='asset_image', null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(NiftyUser, related_name='asset_owner', null=True, on_delete=models.SET_NULL)
    template = models.ForeignKey(Template, related_name='asset_template', null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Asset, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class AssetAttribute(models.Model):
    asset = models.ForeignKey(Asset, related_name='assetattribute_asset', null=True, on_delete=models.SET_NULL)
    attribute = models.ForeignKey(Attribute, related_name='assetattribute_attribute', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.asset + " " + self.attribute

class AssetUnlockable(models.Model):
    asset = models.ForeignKey(Asset, related_name='assetunlockable_asset', null=True, on_delete=models.SET_NULL)
    unlockable = models.ForeignKey(Unlockable, related_name='assetunlockable_unlockable', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.asset + " " + self.unlockable

class AssetTransfer(models.Model):
    STATUS = (
       ('pending', ('Pending')),
       ('assigned', ('Assigned')),
       ('submitted', ('Submitted')),
       ('confirmed', ('Confirmed')),
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=None,
    )

    asset = models.ForeignKey(Asset, related_name='assettransfer_asset', null=True, on_delete=models.SET_NULL)
    from_user = models.ForeignKey(NiftyUser, related_name='assettransfer_from_user', null=True, on_delete=models.SET_NULL)
    to_user = models.ForeignKey(NiftyUser, related_name='assettransfer_to_user', null=True, on_delete=models.SET_NULL)

    history = HistoricalRecords()

    def __str__(self):
        return self.asset + " " + self.status

class Order(models.Model):
    ORDER_TYPE = (
       ('bid', ('Bid')),
       ('ask', ('Ask')),
    )
    order_type = models.CharField(
        max_length=32,
        choices=ORDER_TYPE,
        default=None,
    )
    STATUS = (
       ('pending', ('Pending')),
       ('fulfilled', ('Fulfilled')),
       ('rejected', ('Rejected')),
       ('expired', ('Expired')),
       ('cancelled', ('Cancelled')),
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=None,
    )

    price = models.FloatField()
    expiry = models.DateTimeField()

    asset = models.ForeignKey(Asset, related_name='order_asset', null=True, on_delete=models.SET_NULL)
    maker = models.ForeignKey(NiftyUser, related_name='order_maker', null=True, on_delete=models.SET_NULL)
    taker = models.ForeignKey(NiftyUser, related_name='order_taker', null=True, on_delete=models.SET_NULL)

    history = HistoricalRecords()

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.asset + " " + self.status
