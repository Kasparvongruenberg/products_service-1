from django.db import models
import uuid


# Create your models here.
class Product(models.Model):
    workflowlevel2_uuid = models.CharField(max_length=255, editable=False, verbose_name='WorkflowLevel2 UUID', default=uuid.uuid4, unique=True, blank=True, help_text="Unique ID to relate back to Bifrost workflow")
    name = models.CharField(max_length=255, help_text="Product name")
    make = models.CharField(max_length=255, help_text="Who made the product",blank=True, null=True)
    model = models.CharField(max_length=255, help_text="What is the model from the manufacturer",blank=True, null=True)
    style = models.CharField(max_length=255, help_text="Distinguishing look or color of product", blank=True,null=True)
    description = models.CharField(max_length=255, help_text="Detailed info",blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True, help_text="Type of product")
    status = models.CharField(max_length=255, blank=True, null=True, help_text="Status of Product (in-stock, on back order etc.) ")
    reference_id = models.CharField("Product identifier", max_length=255, blank=True, null=True, help_text="Unique ID for external tracking or thrid part data system")
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} <{}>'.format(self.name, self.type)


class Property(models.Model):
    product = models.ManyToManyField(Product, blank=True, null=True)
    name = models.CharField(max_length=255, help_text="Dynamic Field name for additional meta definition of a product")
    type = models.CharField(max_length=255, blank=True, null=True, help_text="Type of field")
    value = models.CharField(max_length=255, help_text="Dynamic Field value for additional meta definition of a product")
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} <{}>'.format(self.product, self.name)