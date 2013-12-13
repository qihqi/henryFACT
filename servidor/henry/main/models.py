import hashlib
from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from productos.models import Bodega
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

#solo para descuentos
class Descuento(models.Model):
    param = models.CharField(max_length=50, primary_key=True)
    value = models.IntegerField(null=True)
    def __unicode__(self):
        return self.param

    class Meta:
        db_table = 'descuentos'


class UserJava(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=200)
    #nivel de permisos
    CHOICES = [ (0 , 'vendedor/cajero'),
                (1 , 'supervisor'),
                (2 , 'administrador'),
                (3 , 'super')]
    nivel = models.IntegerField(choices=CHOICES)
    is_staff = models.BooleanField() #si es staff => tiene una cuenta de
                                     #django
    last_factura = models.IntegerField()
    bodega_factura = models.ForeignKey(Bodega)
    def __unicode__(self):
        return self.username
    class Meta:
        db_table = 'usuarios'

@transaction.commit_on_success
def createUser(username, password, nivel, bodega):
#createUser given the username, password, nivel
    is_staff = nivel > 0
    #Create user for java client
    usuario = UserJava()
    usuario.username = username
    usuario.password = generatePass(password)
    usuario.nivel = nivel
    usuario.last_factura = 0
    usuario.is_staff = is_staff
    usuario.bodega_factura = Bodega(bodega)
    usuario.save()
    user = User.objects.create_user(username,
                            'test@test.test',
                            password)

    #UserJava es como un profile de user
def hasNivel(nivel):
    def func(user):
        try:
            return getUserJava(user.username).nivel >= nivel
        except ObjectDoesNotExist:
            return False
    return func

def generatePass(password):
    m = hashlib.sha1()
    m.update(password)
    return m.hexdigest()

def getUserJava(username):
    return UserJava.objects.get(username=username)


