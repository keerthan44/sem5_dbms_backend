from django.http import HttpResponse, JsonResponse
from authentication.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from pickle import FALSE
from django.forms.models import model_to_dict
from django.db import connection
from authentication.models import *


# Create your views here.
@csrf_exempt
def hello(request):
    return HttpResponse("Hello")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        try:
            data = json.loads(request.body)
            query = f'Select * from authentication_users where username = "{data["username"]}"'
            cursor.execute(query) 
            userObj = __dictfetchall(cursor)[0]      
            if userObj['password'] == data['password']:
                query = f'Select * from authentication_userprofiles where user_id = {userObj["id"]}'
                cursor.execute(query)
                data = __dictfetchall(cursor)[0] #userprofiles value
                data['user'] = userObj
                query = f'Select * from authentication_roles where id = {data["role_id"]}'
                cursor.execute(query)
                data['role'] = __dictfetchall(cursor)[0] #role values
                del data['role_id']
                del data['user_id']
                cursor.close()
                return JsonResponse(data, safe=False, status=200)
            else:
                cursor.close()
                return JsonResponse({"status": "Invalid Credentials"}, safe=False, status=401)
        except:
            cursor.close()
            return JsonResponse({"status": "Invalid Credentials"}, safe=False, status=401)


@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cursor = connection.cursor()
        query = f'Select * from authentication_users where username = "{data["username"]}"'
        cursor.execute(query) 
        
        if not __dictfetchall(cursor):
            try:
                query = "Start Transaction"
                cursor.execute(query)
                query = f'INSERT INTO authentication_users(username, password) values ("{data["username"]}", "{data["password"]}")'
                cursor.execute(query) 
                query = f'Select * from authentication_users where username = "{data["username"]}" && password = "{data["password"]}"'
                cursor.execute(query)
                user = __dictfetchall(cursor)[0]
                if cursor.rowcount < 1:
                    raise Exception("User not add")

                # userObj = Users.objects.create(
                #     username=data['username'], password=data['password'])
                query = "Select * from authentication_roles where role = 'user'"
                cursor.execute(query)
                role = __dictfetchall(cursor)[0]

                query = f'INSERT INTO authentication_userprofiles(user_id, role_id, contact_email, first_name, last_name) values ({user["id"]}, {role["id"]}, "{data["email"]}", "{data["first_name"]}", "{data["last_name"]}")'
                cursor.execute(query) 
                query = f'select * from authentication_userprofiles where user_id = {user["id"]}'
                cursor.execute(query)
                data = __dictfetchall(cursor)[0]
                # userProfileObj = UserProfiles.objects.create(
                #                             user=userObj,
                #                             role=Roles.objects.get(role="user"),
                #                             contact_email=data['email'],
                #                             first_name=data['first_name'],
                #                             last_name=data['last_name'],
                #                             )
                data['user'] = user
                data['role'] = role 
                query = "COMMIT"
                cursor.execute(query)
                cursor.close()
                return JsonResponse(data, status=201)
            except:
                query = "ROLLBACK"
                cursor.execute(query)
                cursor.close()
                return JsonResponse({"status" : "Invalid data"}, status=400)
        else: 
            cursor.close()
            return JsonResponse({"status" : "User Already Exists"}, status=303)


def authenticate_user(username, password):
    try:
        user = Users.objects.get(username=username, password=password)
        return user
    except:
        return 0 

def __dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]