import json
import secrets
import bcrypt
import calendar
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt  # No nos olvidemos del import
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, datetime, date

from requests import Response
from starlette import status

#from .models import Torders

from .models import Taddress,Torders,Triders,Tsession,Tsenders, Tconnect, Twolifts

def health_check (request):
    http_response={'is_living':True}
    return JsonResponse(http_response)

#++++++++++++++++ Riders
@csrf_exempt
def riders(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

    # Aquí procesamos un POST
    body_json = json.loads(request.body)
    json_code_rider = body_json.get('code_rider', None)
    json_name = body_json.get ('name',None)
    json_surnames = body_json.get('surnames', None)
    json_email = body_json.get('email', None)
    json_password = body_json.get('password', None)
    json_code_address = body_json.get('code_address', None)
    json_telephone = int(body_json.get('telephone', None))
    json_street = body_json.get('street', None)
    json_gate = body_json.get('gate', None)
    json_floor = body_json.get ('floor', None)
    json_door = body_json.get('door', None)
    json_cpostal = body_json.get('cpostal', None)

    if json_code_address is None or json_street is None or json_gate is None or json_floor is None or json_door is None or json_cpostal is None:
        return JsonResponse({"error": "Missing parameter in body request"}, status=400)

    #address_r(json_code_address, json_street, json_gate, json_floor, json_door, json_cpostal)

    address_object_r = Taddress(code_address=json_code_address, street=json_street, gate=json_gate,
                           floor=json_floor, door=json_door, cpostal=json_cpostal)
    address_object_r.save()



    if json_code_rider is None or json_name is None or json_surnames is None or json_email is None or json_password is None or json_code_address is None or json_telephone is None:
        return JsonResponse({"error": "Missing parameter in body request"}, status=400)

    # verifica que el email es valido
    if '@' not in json_email or len(json_email) < 6:
        return JsonResponse({"error": "Invalid email"}, status=400)

    # verificar el email si existe enviar 409
    users = Triders.objects.filter(email=json_email)
    if len(users) > 0:  # is not None:
        return JsonResponse({"error": "Already registered"}, status=409)

    # se crea el hash de email con salt
    salted_and_hashed_pass = bcrypt.hashpw(json_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    address_instance = Taddress.objects.get(code_address=json_code_address)

    # Creamos la entrada
    user_object = Triders(code_rider=json_code_rider, name=json_name, surnames=json_surnames, email=json_email,
                          password=salted_and_hashed_pass, code_address=address_instance, telephone=json_telephone)
    user_object.save()
    return JsonResponse({"is_created": True}, status=201)

def rider_get(request, email):
    if request.method == 'GET':

        authenticated_user = __get_request_user(request)
        if authenticated_user is None:
            return JsonResponse({"error": "Not valid token or missing header"}, status=401)
        else:
            user = Triders.objects.filter(email=email).first()

            response_data = user.to_json()

            return JsonResponse(response_data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

def rider_get_session(request, email):
        if request.method == 'GET':

            user = Triders.objects.filter(email=email).first()

            response_data = user.to_json()

            return JsonResponse(response_data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'HTTP method unsupported'}, status=405)


@csrf_exempt
@require_http_methods(["PATCH"])
def rider_token_ph_patch(request):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    body_json = json.loads(request.body)
    json_username = body_json.get('username', None)

    try:
        tupla = Triders.objects.get(code_rider=json_username)
    except Tconnect.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        try:
            patch_data = body_json
            for key, value in patch_data.items():
                # if hasattr(tupla, key):
                #     setattr(tupla, key, value)
                if key == 'token_ph':  # Verifica si el campo es 'connect'
                    tupla.token_ph = value

            tupla.save()

            return JsonResponse({"message": "Item updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


#++++++++++++++++ Senders
@csrf_exempt
def senders(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

    # Aquí procesamos un POST
    body_json = json.loads(request.body)
    json_code_sender = body_json.get('code_sender', None)
    json_name = body_json.get('name', None)
    json_email = body_json.get('email', None)
    json_password = body_json.get('password', None)
    json_code_address = body_json.get('code_address', None)
    json_telephone = int(body_json.get('telephone', None))
    json_street = body_json.get('street', None)
    json_gate = body_json.get('gate', None)
    json_local = body_json.get('local', None)
    json_cpostal = body_json.get('cpostal', None)
    json_token_ph=body_json.get("token_ph",None)
    json_qualification=body_json.get("qualification", 0)

    if json_telephone is not None:
        print("aqui voy bien" + str(json_telephone))
    else:
        print("json_telephone es None")

    # if json_code_address is None or json_street is None or json_gate is None or json_local is None or json_cpostal is None:
    #     return JsonResponse({"error": "Missing parameter in body request"}, status=400)

    #address_s(json_code_address, json_street, json_gate, json_local, json_cpostal)

    address_object_s = Taddress(code_address=json_code_address, street=json_street, gate=json_gate,
                           local=json_local, cpostal=json_cpostal)
    address_object_s.save()

    # if json_code_sender is None or json_name is None or json_email is None or json_password is None or json_code_address is None or json_telephone is None:
    #     return JsonResponse({"error": "Missing parameter in body request"}, status=400)

    #verifica que el email es valido
    if '@' not in json_email or len(json_email) < 6:
        return JsonResponse({"error": "Invalid email"}, status=400)

    # verificar el email si existe enviar 409
    users = Tsenders.objects.filter(email=json_email)
    if len(users) > 0:  # is not None:
        return JsonResponse({"error": "Already registered"}, status=409)

    # se crea el hash de email con salt
    salted_and_hashed_pass = bcrypt.hashpw(json_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
    address_instance = Taddress.objects.get(code_address=json_code_address)

    # Creamos la entrada
    user_object = Tsenders(code_sender=json_code_sender, name=json_name,email=json_email,
                          password=salted_and_hashed_pass, code_address=address_instance,
                           telephone=json_telephone, token_ph=json_token_ph, qualification=json_qualification)
    user_object.save()
    return JsonResponse({"is_created": True}, status=201)

def sender_get(request, email):
    if request.method == 'GET':

        authenticated_user = __get_request_user(request)
        if authenticated_user is None:
            return JsonResponse({"error": "Not valid token or missing header"}, status=401)
        else:

            user = Tsenders.objects.filter(email=email).first()

            response_data = user.to_json()


            return JsonResponse(response_data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

def sender_session_get(request, email):
        if request.method == 'GET':

            user = Tsenders.objects.get(email=email)

            response_data = user.to_json()

            return JsonResponse(response_data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

#------------------------Sessions

@csrf_exempt
def sessions(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)
    body_json = json.loads(request.body)
    try:
        json_type=body_json['type']
        json_email = body_json['email']
        print (json_email)
        json_password = body_json['password']
        print (json_password)
    except:
        return JsonResponse({"error": "Missing parameter in JSON body"}, status=400)
    if json_type=='sender':
        try:
            db_user = Tsenders.objects.get(email=json_email)
            db_user_email=db_user.email
            print(db_user.email)
            db_user_c=db_user.code_sender
            print(db_user.code_sender)
            # db_user_a = Taddress.objects.get(code_address=db_user.code_address)
            # db_user_postal = db_user_a.cpostal
        except Tsenders.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        try:
            db_user = Triders.objects.filter(email=json_email).first()
            db_user_email = db_user.email
            print(db_user.email)
            db_user_c = db_user.code_rider
            print(db_user.code_rider)
            # db_user_a = Taddress.objects.get(code_address=db_user.code_address)
            # db_user_postal=db_user_a.cpostal
        except Triders.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)



    if bcrypt.checkpw(json_password.encode('utf8'), db_user.password.encode('utf8')):
        # json_password y db_user.encrypted_password coinciden

        # json_password y db_user.encrypted_password coinciden
        random_token = secrets.token_hex(10)
        session = Tsession(username=db_user_c, email=db_user.email, token_access=random_token)
        session.save()

        response_data = {
            "token":random_token,
            "username":db_user_c,
            "email":db_user_email
        }
        #return JsonResponse({"user_session_token": random_token }, status=201)
        return JsonResponse(response_data, status=201)

    else:
        return JsonResponse({'error': 'Invalid password'}, status=401)
        pass


#/////////////////// Verificacion de la sessions
def __get_request_user(request):
    header_token = request.headers.get('Session-Token', None)
    print(header_token)
    if header_token is None:
        return None
    try:
        db_session = Tsession.objects.get(token_access=header_token)
        print(db_session.username)
        return db_session.username
    except Tsession.DoesNotExist:
        return None
    pass

#////////////////////////////////

#---------------------Address ---------------------++

def address_get(request, code_address):
    if request.method == 'GET':
        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
        # else:
            try:
                address = Taddress.objects.filter(code_address=code_address).first()
                #address = Taddress.objects.get(code_address=code_address)
                print(address)

                print("222222222222222222++++++++++++")
                response_data = address.to_json()
                return JsonResponse(response_data, safe=False, status=200)
            except Taddress.DoesNotExist:
                return None
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

def address_get_wol (request):

    if request.method == 'GET':
        street = request.GET.get('street')
        gate = request.GET.get('gate')
        wo_lift = request.GET.get('wo_lift')
        authenticated_user = __get_request_user(request)
        if authenticated_user is None:
            return JsonResponse({"error": "Not valid token or missing header"}, status=401)
        else:
            if street and gate and wo_lift:
                try:
                    address = Taddress.objects.get(street=street, gate=gate, wo_lift=wo_lift)
                    return JsonResponse({'result': True})
                except Taddress.DoesNotExist:
                    return JsonResponse({'result': False})
            else:
                return JsonResponse({'error': 'Missing parameters'}, status=400)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)


#++++++++++++++++++++++++ Order
@csrf_exempt
def orders_p(request):
    if request.method == 'POST':
        body_json = json.loads(request.body)
        json_code_order=body_json.get('code_order',None)
        json_code_sender = body_json.get('code_sender', None)
        json_code_address = body_json.get('code_address', None)
        json_street = body_json.get('street', None)
        json_gate = body_json.get('gate', None)
        json_floor = body_json.get('floor', None)
        json_door = body_json.get('door', None)
        json_cpostal = body_json.get('cpostal', None)
        json_pay=body_json.get("pay",None )

        authenticated_user = __get_request_user(request)
        if authenticated_user is None:
            return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        if json_code_address is None or json_street is None or json_gate is None or json_floor is None or json_door is None or json_cpostal is None:
            return JsonResponse({"error": "Missing parameter in body request"}, status=400)

        order_object_address = Taddress(code_address=json_code_address, street=json_street, gate=json_gate,
                                floor=json_floor, door=json_door, cpostal=json_cpostal)
        order_object_address.save()

        address_instance = Taddress.objects.get(code_address=json_code_address)
        sender_instance = Tsenders.objects.get(code_sender=json_code_sender)

        order_object = Torders(code_order=json_code_order, code_sender=sender_instance,
                               code_address=address_instance, pay=float(json_pay), application=timezone.now())
        # fixed_date = date(2023, 7, 22)
        # order_object = Torders(code_order=json_code_order, code_sender=sender_instance,
        #                        code_address=address_instance, pay=float(json_pay), application=fixed_date)
        order_object.save()
        return JsonResponse({"created": True}, status=201)

    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

def order_g (request):
    if request.method == 'GET':
        #orders = Torder.objects.filter(code_order=)
        orders = Torders.objects.all()

        json_response = []

        for row in orders:
            # Iteramos sobre cada fila SQL de la tabla Entry
            # Podemos acceder a row.id, row.title, row.content y row.publication_date
            json_response.append(row.to_json())
        return JsonResponse(json_response, safe=False, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_tupla(self, request, code_order, format=None):
        try:
            #tupla = Torders.objects.get(code_order=code_order)
            tupla=Torders.objects.get(code_order=code_order)
            tupla.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # Respuesta exitosa sin contenido
        except tupla.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # No encontrado

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_order (request, code_order):
    authenticated_user = __get_request_user(request)
    if authenticated_user is None:
        return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    #print(code_order)
    order = get_object_or_404(Torders, code_order=code_order)

    if request.method == 'DELETE':
        order.delete()
        return JsonResponse({'message': f'Order with code_order {code_order} has been deleted.'}, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

    # if request.method == 'GET':
    #     order = Torders.objects.get(code_order=code_order)
    #     order_data = order.to_json()
    #     return JsonResponse(order_data, status=200)
    # elif request.method == 'DELETE':
    #     #orders = Torder.objects.filter(code_order=)
    #     orders = Torders.objects.get(code_order=code_order)
    #     orders.delete()
    #     return JsonResponse({"message": "Order deleted successfully"}, status=200)

    # else:
    #     return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

@csrf_exempt
@require_http_methods(["PATCH"])
def patch_tupla(request, code_order):
        authenticated_user = __get_request_user(request)
        if authenticated_user is None:
            return JsonResponse({"error": "Not valid token or missing header"}, status=401)
        try:
            tupla = Torders.objects.get(code_order=code_order)
        except Torders.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        if request.method == "PATCH":
            try:
                patch_data = json.loads(request.body)
                for key, value in patch_data.items():
                    # if hasattr(tupla, key):
                    #     setattr(tupla, key, value)
                    if key == 'pay':  # Verifica si el campo es 'pay'
                        tupla.pay = value
                    # if key == 'pay_r':  # Verifica si el campo es 'pay'
                    #     tupla.pay_r = value
                tupla.save()

                return JsonResponse({"message": "Item updated successfully"})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

        return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
@require_http_methods(["PATCH"])
def patch_deliver_time(request):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    body_json = json.loads(request.body)
    json_code_order = body_json.get('code_order', None)
    json_date=body_json.get('date',None)
    # json_code_rider=body_json.get('code_rider', None)
    # print(json_code_rider)
    print(json_code_order)
    print(json_date)

    try:
        tupla = Torders.objects.get(code_order=json_code_order)
    except Torders.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        try:
            #patch_data = body_json
            if (json_date=="pickup"):
                tupla.pickup=timezone.now()
            elif (json_date=="delivery"):
                tupla.delivery=timezone.now()
            # elif(json_code_rider is not None):
            #     tupla.code_rider=json_code_rider
            tupla.save()

            return JsonResponse({"message": "Item updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
@require_http_methods(["PATCH"])
def patch_deliver_rider(request, code_order):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    body_json = json.loads(request.body)
    #json_code_order = body_json.get('code_order', None)
    #json_code_rider = body_json.get('code_rider', None)

    try:
        tupla = Torders.objects.get(code_order=code_order)
    except Torders.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        try:
            #patch_data = body_json
            for key, value in body_json.items():
                # if hasattr(tupla, key):
                #     setattr(tupla, key, value)
                if key == 'code_rider':  # Verifica si el campo es 'connect'
                    try:
                        triders_instance = Triders.objects.get(code_rider=value)
                        tupla.code_rider = triders_instance
                    except Triders.DoesNotExist:
                        # Aquí puedes manejar el caso en el que la instancia de Triders no existe
                        return JsonResponse({"error": "Triders instance not found"}, status=400)
            tupla.save()

            return JsonResponse({"message": "Item updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)



#++++++++++++++++++++++++ Connect

@csrf_exempt
def connect_post(request):
    if request.method == 'POST':
        body_json = json.loads(request.body)
        json_username = body_json.get('username', None)
        json_token_ph = body_json.get('token_ph', None)
        json_connect = body_json.get('connect', None)

        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        if json_username is None or json_token_ph is None:
            return JsonResponse({"error": "Missing parameter in body request"}, status=400)

        #conns = Tconnect.objects.filter(username=json_username).order_by( '-position').first()
        conns=Tconnect.objects.filter(position__lt=999999).order_by('position').first()

        if conns is None:
            json_position=1
        else:
            json_position= conns.position+1
        # elif conns.position<999998:
        #     json_position=conns.position+1

        conn_object = Tconnect(username=json_username, token_ph=json_token_ph, connect=json_connect, position=json_position)
        conn_object.save()
        return JsonResponse({"created": True}, status=201)

    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

@csrf_exempt
@require_http_methods(["PATCH"])
def connect_patch(request):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    body_json = json.loads(request.body)
    json_username = body_json.get('username', None)

    try:
        tupla = Tconnect.objects.get(username=json_username)
    except Tconnect.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        try:
            patch_data = body_json
            for key, value in patch_data.items():
                # if hasattr(tupla, key):
                #     setattr(tupla, key, value)
                if key == 'connect':  # Verifica si el campo es 'connect'
                    tupla.connect = value
                if key =='position':
                    tupla.position = value
                if key == 'username':
                    tupla.username = "borrado"
            tupla.save()

            return JsonResponse({"message": "Item updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)

def connect_get(request):
    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':
        #conns = Tconnect.objects.order_by('numero_entero').first()
        conns=Tconnect.objects.order_by('position').first()
        print (conns)
        if conns is None:
            return JsonResponse({"message": "No items available"}, status=404)

        # Serializa el objeto para devolverlo como JSON
        # response_data = {
        #     "username": conns.username,
        #     "position": conns.position,
        #     # Agrega otros atributos si es necesario
        # }
        response_data = conns.to_json()
        print (response_data)
        conns.position += 10
        conns.save()
        return JsonResponse(response_data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)
@csrf_exempt
@require_http_methods(["DELETE"])
def remove_connect(request):
    authenticated_user = __get_request_user(request)
    if authenticated_user is None:
        return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    if request.method == 'DELETE':
        Tconnect.objects.all().delete()
        return JsonResponse({'message': 'The Tconnect has been deleted.'}, status=200)
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)


 #------------------------- Profits o Debits +++++++++++++++++++++++++++

def get_orders_last_12_biweeklys(request, code_sender):

    if request.method == 'GET':
        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        twelve_biweeklys = []

        today = timezone.now().date()
        six_months_ago = today - timedelta(days=180)

        if (today - six_months_ago).days >= 16:
            six_months_ago.replace(day=16)
        else:
            six_months_ago.replace(day=1)
        start_date = six_months_ago
        # Iterating through the last 12 biweeklys
        for _ in range(13):

            if start_date.day>=16:
                start_date = start_date.replace(day=16)
            else:
                start_date = start_date.replace(day=1)

            # Calculate end_date for the first biweekly period
            end_date = start_date + timedelta(days=14)  # 14 days after the start

            if end_date.day>20:
                if end_date.month==1 or end_date.month==3 or end_date.month==5 or end_date.month==7 or end_date.month==8 or end_date.month==10 or end_date.month==12:
                    end_date =end_date.replace(day=31)
                    end_date = end_date + timedelta(days=1)
                elif end_date.month==4 or end_date.month==6 or end_date.month==9 or end_date.month==11:
                    end_date =end_date.replace(day=30)
                    end_date = end_date + timedelta(days=1)
                elif end_date.month==2:
                    if end_date.year==2028 or end_date.year==2032 or end_date.year==2036 or end_date.year==2040 or end_date.year==2044 or end_date.year==2048:
                        end_date =end_date.replace(day=29)
                        end_date = end_date + timedelta(days=1)
                    else:
                        end_date =end_date.replace(day=28)
                        end_date=end_date+ timedelta(days=1)

            if end_date > today:
                end_date = today + timedelta(days=1)

            orders = Torders.objects.filter(
                code_sender=code_sender,
                application__range=(start_date, end_date)
            ).order_by('-application')

            # if end_date > today:
            #     end_date = today

            end_date=end_date-timedelta(days=1)

            total_pay = sum(order.pay for order in orders)
            orders_data = [order.to_json() for order in orders]

            twelve_biweeklys.insert(0, {
                "start_date": start_date,
                "end_date": end_date,
                "total_pay": total_pay,
                #"orders": orders_data
            })

            start_date += timedelta(days=17)


        # response_data = {
        #     "biweeklys": twelve_biweeklys
        # }
        response_data = twelve_biweeklys

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_orders_all(request, code_sender):

    if request.method == 'GET':

        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        today = timezone.now().date()
        six_months_ago = timezone.now() - timedelta(days=180)

        print(six_months_ago)

        # orders = Torders.objects.filter(
        #     code_sender=code_sender,
        #     application__gte=six_months_ago
        # ).order_by('-application')

        orders = Torders.objects.filter(
            code_sender=code_sender,
            application__gte=six_months_ago
        ).order_by('-application')

        biweeklys_data = {}

        print (orders)

        for order in orders:
            order_data = order.to_json()

            order_date = order.application.date()
            year = order_date.year
            month = order_date.month

            # Determinar el día límite para el final de la quincena
            if order_date.day <= 15:
                last_day = 15
            else:
                last_day = calendar.monthrange(year, month)[1]

            if last_day > timezone.now().day:
                last_day = timezone.now().day

            # Construir el rango de fechas de la quincena
            start_date = timezone.datetime(year, month, 1).date()
            end_date = timezone.datetime(year, month, last_day).date()

            biweekly = (start_date, end_date)

            if biweekly not in biweeklys_data:
                biweeklys_data[biweekly] = {
                    "total_pay": order.pay,
                    "orders": [order_data]
                }
            else:
                biweeklys_data[biweekly]["total_pay"] += order.pay
                biweeklys_data[biweekly]["orders"].append(order_data)

        response_data = {
            "biweeklys": [
                {
                    "start_date": start_date,
                    "end_date": end_date,
                    "total_pay": data["total_pay"],
                    "orders": data["orders"]
                }
                for (start_date, end_date), data in biweeklys_data.items()
            ]
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_orders_bw(request,  code_sender,*args, **kwargs):
#def get_orders_bw(request, code_sender, start_date, end_date):
    if request.method == 'GET':

        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        start_date_str = request.GET.get('startDate')
        end_date_str = request.GET.get('endDate')

        print(start_date_str)
        print(end_date_str)
        # start_date_str='2023-08-16'
        # end_date_str='2023-08-28'
        #
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        #date_difference = (end_date - start_date).days  # Obtén la diferencia en días

        date_difference = (end_date - start_date).days  # Obtiene la diferencia en días

        delta = timedelta(days=1)
        current_date = start_date

        orders_data = []

        for _ in range (date_difference+1):

            orders = Torders.objects.filter(
                code_sender=code_sender,
                application__date=current_date
            ).order_by('-application')

            total_pay = sum(order.pay for order in orders)
            #orders_data = [order.to_json() for order in orders]

            orders_data.insert(0, {
            'date': current_date.strftime('%Y-%m-%d'),
            'total_pay': str(total_pay)
            })

            current_date += delta

        response_data = orders_data

        return JsonResponse(response_data, safe=False)

        #
        # orders = Torders.objects.filter(
        #     code_sender=code_sender,
        #     application__date__gte=start_date,
        #     application__date__lte=end_date
        # ).order_by('-application')
        #
        # total_pay = sum(order.pay for order in orders)
        #
        # orders_data = []
        # for order in orders:
        #     orders_data.append({
        #         'date': order.application.strftime('%Y-%m-%d'),
        #         'pay': str(order.pay)
        #     })
        #
        # response_data = {
        #     'orders': orders_data,
        #     'total_pay': str(total_pay)
        # }
        #
        # return JsonResponse(response_data, safe=False)
        #
        # # total_pay_by_date = []
        # #
        # # for order in orders:
        # #     order_date = order.application.date()
        # #
        # #     if order_date not in total_pay_by_date:
        # #         total_pay_by_date[order_date] = 0
        # #     total_pay_by_date[order_date] += order.pay
        # #
        # # response_data = {
        # #     "total_pay_by_date": [
        # #         {
        # #             "date": date.strftime('%Y-%m-%d'),  # Convertir datetime.date a string,
        # #             "total_pay": total_pay
        # #         }
        # #         for date, total_pay in total_pay_by_date.items()
        # #     ]
        # # }
        # #
        # # return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_orders_by_day(request, code_sender,*args, **kwargs):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':

        date_str = request.GET.get('date')

        print(date_str)

        # date_str='2023-08-22'
        try:
            #date=datetime.strptime(date_str, '%Y-%m-%d').date
            date=date_str
            print(date)

            # Convierte la cadena de fecha en un objeto consciente de la zona horaria
            date = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d'))

            orders_data=[]


            orders = Torders.objects.filter(code_sender=code_sender, application__date=date).order_by('-application')
            #total_pay = orders.aggregate(total_pay=Sum('pay'))['total_pay']

            orders_data = [order.to_json1() for order in orders]

            response_data=orders_data

            print (response_data)

            # response_data = {
            #     # "total_pay": total_pay,
            #     # "orders": orders_data
            #     orders_data
            #
            # }

            return JsonResponse(response_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def gains_get(request, code_rider):
    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':
        today = timezone.now().date()

        # date_str = '2023-08-22'
        #
        # today = datetime.strptime(date_str, '%Y-%m-%d')

        try:
            orders = Torders.objects.filter(code_rider=code_rider, application__date=today).order_by('-application')
            total_pay = orders.aggregate(total_pay=Sum('pay'))['total_pay']

            response_data = {
                "gain": total_pay
            }
            return JsonResponse(response_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_profit_last_12_biweeklys(request, code_rider):

    print ('123123123')

    if request.method == 'GET':
        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        twelve_biweeklys = []

        today = timezone.now().date()
        six_months_ago = today - timedelta(days=180)

        if (today - six_months_ago).days >= 16:
            six_months_ago.replace(day=16)
        else:
            six_months_ago.replace(day=1)
        start_date = six_months_ago
        # Iterating through the last 12 biweeklys
        for _ in range(13):

            if start_date.day>=16:
                start_date = start_date.replace(day=16)
            else:
                start_date = start_date.replace(day=1)

            # Calculate end_date for the first biweekly period
            end_date = start_date + timedelta(days=14)  # 14 days after the start

            if end_date.day > 20:
                if end_date.month == 1 or end_date.month == 3 or end_date.month == 5 or end_date.month == 7 or end_date.month == 8 or end_date.month == 10 or end_date.month == 12:
                    end_date = end_date.replace(day=31)
                    end_date = end_date + timedelta(days=1)
                elif end_date.month == 4 or end_date.month == 6 or end_date.month == 9 or end_date.month == 11:
                    end_date = end_date.replace(day=30)
                    end_date = end_date + timedelta(days=1)
                elif end_date.month == 2:
                    if end_date.year == 2028 or end_date.year == 2032 or end_date.year == 2036 or end_date.year == 2040 or end_date.year == 2044 or end_date.year == 2048:
                        end_date = end_date.replace(day=29)
                        end_date = end_date + timedelta(days=1)
                    else:
                        end_date = end_date.replace(day=28)
                        end_date = end_date + timedelta(days=1)

            if end_date > today:
                end_date = today + timedelta(days=1)

            print(code_rider)

            orders = Torders.objects.filter(
                code_rider=code_rider,
                #application__range=(start_date, end_date)
                pickup__range=(start_date, end_date)
            ).order_by('-application')

            # if end_date > today:
            #     end_date = today

            end_date = end_date - timedelta(days=1)

            total_pay = sum(order.pay for order in orders)
            orders_data = [order.to_json() for order in orders]

            twelve_biweeklys.insert(0, {
                "start_date": start_date,
                "end_date": end_date,
                "total_pay": total_pay,
                #"orders": orders_data
            })

            start_date += timedelta(days=17)


        # response_data = {
        #     "biweeklys": twelve_biweeklys
        # }
        response_data =  twelve_biweeklys

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_profit_bw(request,  code_rider,*args, **kwargs):
    if request.method == 'GET':

        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        start_date_str = request.GET.get('startDate')
        end_date_str = request.GET.get('endDate')

        print(start_date_str)
        print(end_date_str)
        # start_date_str='2023-08-16'
        # end_date_str='2023-08-28'
        #
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        #date_difference = (end_date - start_date).days  # Obtén la diferencia en días

        date_difference = (end_date - start_date).days  # Obtiene la diferencia en días

        delta = timedelta(days=1)
        current_date = start_date

        orders_data = []

        for _ in range (date_difference+1):

            orders = Torders.objects.filter(
                code_rider=code_rider,
                #application__date=current_date
                pickup__date=current_date
            ).order_by('-application')

            total_pay = sum(order.pay for order in orders)
            #orders_data = [order.to_json() for order in orders]

            orders_data.insert(0, {
            'date': current_date.strftime('%Y-%m-%d'),
            'total_pay': str(total_pay)
            })

            current_date += delta

        response_data = orders_data

        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_profit_by_day(request, code_rider,*args, **kwargs):
    print('123123123')

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':

        date_str = request.GET.get('date')

        print(date_str+"hola")

        # date_str='2023-08-22'

        if date_str=='today':
            date = timezone.now().date()
        else:
            #date=datetime.strptime(date_str, '%Y-%m-%d').date()
            date = date_str

        orders_data=[]

        print((date))

        try:
            #orders = Torders.objects.filter(code_rider=code_rider, application__date=date).order_by('-application')
            orders = Torders.objects.filter(code_rider=code_rider, pickup__date=date).order_by('-application')
            # total_pay = orders.aggregate(total_pay=Sum('pay'))['total_pay']

            print (orders)

            orders_data = [order.to_json1() for order in orders]

            response_data = orders_data

            return JsonResponse(response_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


#++++++++++++++++++++++++ Wolift

@csrf_exempt
def wolift_post(request):
    if request.method == 'POST':
        body_json = json.loads(request.body)
        json_gate = body_json.get('gate', None)
        json_street = body_json.get('street', None)
        json_lift = body_json.get('lift', None)

        # authenticated_user = __get_request_user(request)
        # if authenticated_user is None:
        #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

        if json_gate is None or json_street is None:
            return JsonResponse({"error": "Missing parameter in body request"}, status=400)

        #conns = Tconnect.objects.filter(username=json_username).order_by( '-position').first()
        wolift=Twolifts.objects.filter(street=json_street, gate=json_gate).first()

        if wolift is None:
            wolift_object = Tconnect(gate=json_gate, street=json_street, lift=json_lift)
            wolift_object.save()
            return JsonResponse({"created": True}, status=201)
        else:
            return JsonResponse({"message": "The record already exists"}, status=409)

    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

@csrf_exempt
@require_http_methods(["PATCH"])
def weather_patch(request):

    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)
    body_json = json.loads(request.body)
    #json_street = body_json.get('street', None)

    try:
        #tupla = Twolifts.objects.get(street=json_street)
        tupla = Twolifts.objects.get(street='heaven')
    except Tconnect.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        try:
            patch_data = body_json
            for key, value in patch_data.items():
                if key == 'lift':  # Verifica si el campo es 'lift'
                    tupla.lift = value
            tupla.save()

            return JsonResponse({"message": "Item updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

def wolift_get(request, street, gate):
    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':

        try:
            # address = Taddress.objects.filter(code_address=code_address).first()
            #lift = Twolifts.objects.get(street=street, gate=gate)
            lift = Twolifts.objects.filter(street=street, gate=gate).first()
            print(lift)

            print("Estoy leyendo al WOLIFT")
            response_data = lift.to_json()
            return JsonResponse(response_data, safe=False, status=200)
        except Taddress.DoesNotExist:
            return None
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)

def weather_get(request):
    # authenticated_user = __get_request_user(request)
    # if authenticated_user is None:
    #     return JsonResponse({"error": "Not valid token or missing header"}, status=401)

    if request.method == 'GET':

        try:
            weather = Twolifts.objects.filter(street='heaven').first()
            #weather = Twolifts.objects.get(street='heaven')
            print(weather.lift)

            print("Estoy leyendo de WEathers")
            response_data = weather.to_json2()
            return JsonResponse(response_data, safe=False, status=200)
        except Taddress.DoesNotExist:
            return None
    else:
        return JsonResponse({'error': 'HTTP method unsupported'}, status=405)


