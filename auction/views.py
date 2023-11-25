from django.http import HttpResponse, JsonResponse
from auction.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from pickle import FALSE
from django.forms.models import model_to_dict
from authentication.views import authenticate_user
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from datetime import datetime


# Create your views here.
@csrf_exempt
def hello(request):
    return HttpResponse("Hello")

@csrf_exempt
def create_auction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            try:
                Auction.objects.get(
                    user = user, 
                    title = data['title'],
                    startDate = data['startDate'],
                    endDate = data['endDate'],
                )
                return JsonResponse({"status" : "Auction Already Exists"}, status=303)
            except:
                pass

            try:
                data = model_to_dict(Auction.objects.create(
                    user = user, 
                    title = data['title'],
                    startDate = data['startDate'],
                    endDate = data['endDate'],
                ))
                data['user'] = model_to_dict(Users.objects.get(id=data['user']))
                return JsonResponse(data, safe=False, status=201)
            except Exception as e:
                print(e)
                return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)
        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)

@csrf_exempt
def update_auction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            try:
                auction = Auction.objects.get(
                    user = user, 
                    title = data['title'],
                )
            except:
                return JsonResponse({"status" : "Auction Does Not Exists"}, status=303)

            try:
                auction.title = data['title']
                auction.startDate = data['startDate']
                auction.endDate = data['endDate']
                auction.save(update_fields=['title', 'startDate', 'endDate'])
                auction = model_to_dict(auction)
                print(auction)
                auction['user'] = model_to_dict(user)
                return JsonResponse(data, safe=False, status=201)
            except Exception as e:
                print(e)
                return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)
        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)

@csrf_exempt
def get_auctions(request):
    if request.method == 'GET':
        data = Auction.objects.all().values()
        return JsonResponse(list(data), safe=False, status=201)

@csrf_exempt
def create_items(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            cursor = connection.cursor()
            cursor.callproc('update_auction_status')
            cursor.close()
            try:
                auction = Auction.objects.get(
                    id=data['auction_id'],
                )
                print(auction.status)
            except:
                return JsonResponse({"status" : "Auction Does Not Exists"}, status=404)
            if auction.status == 'not begun':

                try:
                    data = Item.objects.get(
                        user = user, 
                        auction = auction,
                        name = data['item']['name'], 
                        # image = 
                        description = data['item']['description'],
                        basePrice = data['item']['basePrice']
                    )
                    return JsonResponse({"status": "Item Already Exists"}, status=303)
                except:
                    pass

                try:
                    data = model_to_dict(
                        Item.objects.create(
                            user = user, 
                            auction = auction,
                            name = data['item']['name'], 
                            # image = 
                            description = data['item']['description'],
                            basePrice = data['item']['basePrice']
                        )
                    )
                    if data['image']:
                        data['image'] = data['image']['url']
                    else:
                        data['image'] = None
                    data['user'] = model_to_dict(user)
                    data['auction'] = model_to_dict(auction)
                    return JsonResponse(data, safe=False, status=201)
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)
            else:
                return JsonResponse({"status": "Auction has already started"}, safe=False, status=400)
        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)

@csrf_exempt
def update_items(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            try:
                auction = Auction.objects.get(
                    id=data['auction_id'],
                )
            except:
                return JsonResponse({"status" : "Auction Does Not Exists"}, status=404)
            cursor = connection.cursor()
            cursor.callproc('update_auction_status')
            cursor.close()
            if auction.status == 'not_begun':
                try:
                    item = Item.objects.get(
                        user = user, 
                        auction = auction,
                        name = data['item']['name'], 
                    )
                except:
                    return JsonResponse({"status": "Item Does Not Exists"}, status=303)

                try:
                    item.user = user
                    item.auction = auction
                    item.name = data['item']['name'] 
                    item.description = data['item']['description'] 
                    item.basePrice = data['item']['basePrice']
                    # item.basePrice = 500 
                    item.save()
                    item = model_to_dict(item)
                    print(item)
                    if item['image']:
                        item['image'] = item['image']['url']
                    else:
                        item['image'] = None
                    item['user'] = model_to_dict(user)
                    item['auction'] = model_to_dict(auction)
                    return JsonResponse(item, safe=False, status=200)
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)
            else:
                return JsonResponse({"status": "Auction has already started"}, safe=False, status=400)

        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)

@csrf_exempt
def get_all_items_auction(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data = Item.objects.filter(auction_id=data['auction_id']).values()
        return JsonResponse(list(data), safe=False, status=201)

@csrf_exempt
def create_bid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            cursor = connection.cursor()
            cursor.callproc('update_auction_status')
            cursor.close()
            try:
                auction = Auction.objects.get(
                    id=data['auction_id'],
                )
            except:
                return JsonResponse({"status" : "Auction Does Not Exists"}, status=404)
            if auction.status == "started":
                try:
                    item = Item.objects.get(
                        user = user, 
                        auction = auction,
                        name = data['item']['name'], 
                    )
                except:
                    return JsonResponse({"status": "Item Does Not Exists"}, status=303)

                try:
                    bid = Bids.objects.create(
                        user = user,
                        item = item,
                        amount = data['amount'],
                        time = str(datetime.now())
                    )
                    bid = model_to_dict(bid)
                    bid['user'] = model_to_dict(user)
                    bid['auction'] = model_to_dict(auction)
                    return JsonResponse(bid, safe=False, status=200)
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)
            else:
                return JsonResponse({"status": "Auction hasnt started or is over"}, safe=False, status=404)
        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)
@csrf_exempt
def get_auction_summary(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate_user(data['user']['username'], data['user']['password'])
        if user:
            cursor = connection.cursor()
            query = f'''
                WITH MaxBids AS (
                    SELECT
                        i.id AS item_id,
                        MAX(b.amount) AS max_bid_amount
                    FROM auction_item i
                    LEFT JOIN auction_bids b ON i.id = b.item_id
                    GROUP BY i.id
                )

                SELECT
                    i.id AS item_id,
                    i.name AS item_name,
                    i.basePrice AS item_base_price,
                    i.bidCount AS item_bid_count,
                    mb.max_bid_amount,
                    u.username AS bidder_username
                FROM auction_item i
                LEFT JOIN MaxBids mb ON i.id = mb.item_id
                LEFT JOIN auction_bids b ON i.id = b.item_id AND mb.max_bid_amount = b.amount
                LEFT JOIN authentication_users u ON b.user_id = u.id
                Where i.auction_id = {data['auction_id']}     
                ORDER BY i.id;
            '''
            cursor.execute(query)
            all_bids = __dictfetchall(cursor)
            query = f"select calculate_total_bid_amount({data['auction_id']});"
            cursor.execute(query)
            context = {
                'final_bids': all_bids,
                'total_bid_amount': cursor.fetchone()[0]
            }
            return JsonResponse(context, safe=False, status=200)
        else:
            return JsonResponse({"status": "Invalid User"}, safe=False, status=401)

def __dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]