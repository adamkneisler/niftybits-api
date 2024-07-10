from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from simple_history.models import HistoricalRecords

# from nft.models import Asset


class NiftyUser(models.Model):
    """ Extension of Django user model for Nifty """
    USER_TYPE = (
       ('creator', ('Content Creator')),
       ('admin', ('Admin')),
    )
    user_type = models.CharField(
        max_length=32,
        choices=USER_TYPE,
        default='creator',
    )
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    profile_name = models.CharField(max_length=512, blank=True, null=True)
    handle = models.CharField(max_length=128, blank=True, null=True, unique=True)
    verified = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    avatar = models.CharField(max_length=1024, blank=True, null=True)
    twitter_user_id = models.CharField(max_length=64, blank=True, null=True)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    @property
    # Tie this to returned value from Twitter auth
    # Build out Followers model to create 'users' and not just a count?
    def followers(self):
        return Follow.objects.filter(from_user=self).count()

    @property
    # Tie this to returned value from Twitter auth
    # Build out Followers model to create 'users' and not just a count?
    def following(self):
        return Follow.objects.filter(to_user=self).count()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(NiftyUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

class Deposit(models.Model):
    """ Model to store deposits by a NiftyUser """

    amount = models.FloatField(default=0.0)
    
    user = models.ForeignKey(NiftyUser, null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Deposit, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} + {self.amount}"

class Withdrawl(models.Model):
    """ Model to store withdrawls by a NiftyUser """

    amount = models.FloatField(default=0.0)
    fee = models.FloatField(default=0.0)
    
    user = models.ForeignKey(NiftyUser, null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Withdrawl, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} + {self.amount} + {self.fee}"

class Ledger(models.Model):
    """ Model to store ledgers by a NiftyUser """

    LEDGER_TYPE = (
       ('credit', ('Credit')),
       ('debit', ('Debit')),
    )
    ledger_type = models.CharField(
        max_length=32,
        choices=LEDGER_TYPE,
        default=None,
    )

    # Make this calculate based on based on reconciliation from withdrawl / deposit and transfers
    amount = models.FloatField(default=0.0)
    
    user = models.ForeignKey(NiftyUser, null=True, on_delete=models.SET_NULL)
    withdrawl = models.ForeignKey(Withdrawl, null=True, on_delete=models.SET_NULL)
    deposit = models.ForeignKey(Deposit, null=True, on_delete=models.SET_NULL)

    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Ledger, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} + {self.amount} + {self.fee}"