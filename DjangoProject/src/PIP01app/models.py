from django.db import models
from django.utils import timezone

#++++++++++++++++ RIDERS

class Triders(models.Model):
    code_rider = models.CharField (max_length=20, primary_key=True,)
    name = models.CharField (max_length=50)
    surnames = models.CharField (max_length=50)
    email = models.CharField (max_length=50,unique=True)
    password = models.CharField (max_length=200)
    code_address = models.OneToOneField ('Taddress', on_delete=models.SET_NULL, null=True)
    #telephone = models.IntegerField
    telephone = models.IntegerField(default=555555555)
    token_ph = models.CharField (max_length=200, blank=True)
    connect = models.BooleanField(default=False)

    def to_json (self):
        return {
            "code_rider":self.code_rider,
            "name": self.name,
            "email":self.email,
            "code_address":self.code_address.code_address, # en la serializacion solo obtengo el valor del code_address del to_json de Taddress
            "telephone": self.telephone,
            "token_ph":self.token_ph
        }
    class Meta:
        managed = True
        db_table = 'Triders'



#++++++++++++++++ SENDERS
class Tsenders(models.Model):
    code_sender = models.CharField (max_length=20,primary_key=True,)
    name = models.CharField (max_length=50)
    email = models.CharField (max_length=50,unique=True)
    password = models.CharField (max_length=200)
    code_address = models.OneToOneField ('Taddress', on_delete=models.SET_NULL, null=True)
    telephone = models.IntegerField (default=555555555)
    #telephone = models.CharField (max_length=50, blank=True)
    token_ph = models.CharField(max_length=200, blank=True)
    qualification = models.IntegerField(default=0)

    ##En tu modelo Tsenders, estás incluyendo el campo code_address
    # que es un ForeignKey a Taddress. Cuando intentas serializar un
    # objeto Tsenders a JSON, el campo code_address contiene una instancia
    # de Taddress, y Python no sabe cómo convertir esta instancia en un formato JSON.

    def to_json(self):
        return {
            "code_sender":self.code_sender,
            "name":self.name,
            "email":self.email,
            "code_address":self.code_address.code_address, # en la serializacion solo obtengo el valor del code_address del to_json de Taddress
            "telephone": self.telephone,
            "token_ph":self.token_ph

        }

    class Meta:
        managed = True
        db_table = 'Tsenders'




#++++++++++++++++ ORDERS

class Torders (models.Model):
    code_order = models.CharField (max_length=20, primary_key=True,)
    code_sender = models.ForeignKey(Tsenders, on_delete=models.SET_NULL, null=True)
    code_address = models.OneToOneField ('Taddress', on_delete=models.CASCADE, null=True)
    code_rider=models.ForeignKey(Triders, on_delete=models.SET_NULL, null=True)
    pay = models.FloatField (default=3.8)
    #pay_r = models.FloatField(default=3.0)
    application = models.DateTimeField(default=timezone.now)
    #application= models.DateTimeField(auto_now_add=True)  # Campo para almacenar la fecha de hoy  default=timezone.now
    pickup= models.DateTimeField(default=timezone.now)
    delivery=models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'Torders'

    def to_json (self):
        return {
            "date_deliver":self.delivery,
            "date_create":self.application,
            "order":self.code_order,
            "gain":self.pay,
            #"gain_r": self.pay_r,
            "sender": self.code_sender.code_sender,
            #"rider":self.code_rider.code_rider,
            "rider": self.code_rider,
            "address": self.code_address.code_address

        }

    def to_json1 (self):
        rider_code = self.code_rider.code_rider if self.code_rider else None
        return {
            "date_deliver":self.delivery,
            "date_create":self.application,
            "order":self.code_order,
            "gain":self.pay,
            #"gain_r": self.pay_r,
            "sender": self.code_sender.code_sender,
            #"rider":self.code_rider.code_rider,
            #"rider": self.code_rider,
            "rider":rider_code,
            "address": self.code_address.code_address

        }

#++++++++++++++++ ADDRESS
class Taddress(models.Model):
    code_address= models.CharField (max_length=20, primary_key=True,)
    street= models.CharField (max_length=50)
    gate = models.CharField (max_length=50)
    floor = models.CharField (max_length=10, blank=True)
    door = models.CharField (max_length=10, blank=True)
    local = models.CharField (max_length=10, blank=True)
    #urbanization=models.CharField(max_length=50)
    cpostal = models.CharField (max_length=10, blank=True)

    wo_lift=models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'Taddress'


    def to_json(self):
        return {
            'code_address':self.code_address,
            'street':self.street,
            'gate':self.gate,
            'floor':self.floor,
            'door':self.door,
            'local':self.local,
            "cpostal": self.cpostal,
            #"urb": self.urbanizacion,
            "wo_lift" : self.wo_lift
        }




#--------------------------------- Tsession -----------------------------

class Tsession(models.Model):
    username = models.CharField (max_length=50)
    email = models.CharField (max_length=50, default=None)
    token_access = models.CharField (max_length=200)
    def to_json(self):
        return {
            "code": self.username,
            "token": self.token_access
        }
    class Meta:
        managed = True
        db_table = 'Tsessions'



#--------------------------------- Tconnect -----------------------------

class Tconnect(models.Model):
    username = models.CharField (max_length=50)
    token_ph = models.CharField (max_length=200)
    connect = models.BooleanField(default=False)
    position=models.IntegerField(default=999999)

    class Meta:
        managed = True
        db_table = 'Tconnect'

    def to_json(self):
        return {
            "username": self.username,
            "token_ph": self.token_ph,
            "connect":self.connect,
            "position": self.position
        }

#--------------------------------- Twolift -----------------------------

class Twolifts(models.Model):
    gate = models.CharField (max_length=50)
    street = models.CharField (max_length=200)
    lift = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'Twolifts'

    def to_json(self):
        return {
            "lift":self.lift,
        }

    def to_json2(self):
        return {
            "weather":self.lift,
        }

