from django.db import models
from bitfield import BitField
from django.utils.functional import cached_property


# Create your models here.
class ListingModel(models.Model):
    realtor = models.ForeignKey("RealtorModel", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RealtorModel(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TestModel(models.Model):
    flags = BitField(
        flags=(
            ('is_ram', 'ram is the user'),
            ('is_kane', 'kane is the user')
        )
    )    
    name = models.CharField(max_length=100)


class AuthorModel(models.Model):
    name = models.CharField(max_length=100)


class BooksModel(models.Model):
    authors = models.ManyToManyField(AuthorModel)
    name = models.CharField(max_length=100)


class LedModel(models.Model):
    name = models.CharField(max_length=100)


class HoldModel(models.Model):
    holding_name = models.CharField(max_length=100)
    ledger = models.ForeignKey(LedModel, on_delete=models
                               .SET_NULL, null=True)

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SalesModel(models.Model):
    product_name = models.CharField(max_length=100)
    sale = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    cus_man = CustomManager()


class CustomerModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

class OrderModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()



class Post(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    test = models.CharField(max_length=100, blank=True, null=True)


class UserModel(models.Model):
    name = models.CharField(max_length=100, default='')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='belonged_to')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True, blank=True)


class UserInfo(models.Model):
    place = models.CharField(max_length=100, blank=True)
    mf = models.OneToOneField(UserModel, related_name='metadata', on_delete=models.CASCADE)


def sample():
    print('abcdefhgi')
def sample1():
    print('abcdefhgi')
def sample2():
    print('231123123')




class UserM(models.Model):
    name = models.CharField(max_length=100)

class UserDetails(models.Model):
    age = models.IntegerField()
    user = models.ForeignKey(UserM, on_delete=models.CASCADE)


class ModelA(models.Model):
    name = models.CharField(max_length=100)

class ModelB(models.Model):
    name = models.CharField(max_length=100)
    mo = models.ForeignKey(ModelA, on_delete=models.CASCADE, related_name='linked_model')



class TimeZoneModel(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now_add=True)


class Person(models.Model):
    MAN = 2
    WOMAN = 10
    TYPE_CHOICES = [
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
    ]
    name = models.CharField(max_length=100)
    ty = models.IntegerField(choices=TYPE_CHOICES)

    @cached_property
    def is_human(self):
        if self.ty == self.MAN:
            return True
        return False
    
    @property
    def is_something(self):
        if self.ty == self.WOMAN:
            return True
        return False


class ManageFalseModel(models.Model):
    name = models.CharField(max_length=100)
    temp = models.CharField(max_length=100)

    class Meta:
        managed=False



class A(models.Model):
    name = models.CharField(max_length=100)

class B(models.Model):
    text = models.CharField(max_length=100)
    fk = models.ForeignKey(A, on_delete=models.CASCADE)



class FileUploadModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='files')


class file1model(models.Model):
    name = models.CharField(max_length=100)

class file2model(models.Model):
    fname = models.CharField(max_length=100)     
    file = models.ForeignKey(file1model, on_delete=models.CASCADE)


class ChoiceModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

