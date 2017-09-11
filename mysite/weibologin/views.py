from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
from pymongo import MongoClient
import weibologin.weibo as weibo


def weibo_login(request):
    return render(request, 'weibo_login.html')

def auth(request):
    API_KEY = '1627111321'
    API_SECRET = '2151b8e598084507b71671cb12e9db19'
    REDIRECT_URI = 'http://47.93.240.22/auth'
    client = weibo.Client(API_KEY, API_SECRET, REDIRECT_URI)
    code = request.GET.get('code', 0)
    # if authorized
    if code != 0:
        client.set_code(code)
        token = client.token
        uid = token.get('uid', 0)
        client = pymongo.MongoClient('localhost', 27017)
        db = client.weibo_login
        collection = db.user_info
        # if user is the first time come here
        if collection.find({'uid': uid}).count() == 0:
            client.close()
            return HttpResponseRedirect('/phone?uid=%s'%(uid))
        # the user has logined before
        else:
            client.close()
            return HttpResponseRedirect('/login_success')
    # authorization
    else:
        a_url = client.authorize_url
        return HttpResponseRedirect(a_url)

def phone(request):
    # POST
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        uid = request.GET.get('uid')
        client = pymongo.MongoClient('localhost', 27017)
        db = client.weibo_login
        collection = db.user_info
        collection.insert_one({'uid': uid, 'phone_num': phone_num})
        client.close()
        return HttpResponseRedirect('/login_success')
    #GET
    elif request.method == 'GET':
        return render(request, 'phone.html')

def login_success(request):
    return render(request, 'login_success.html')


