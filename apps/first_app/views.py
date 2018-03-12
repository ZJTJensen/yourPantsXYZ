from django.contrib import messages
from django.shortcuts import redirect, render

from models import *
def noname(req):
    return 'id' not in req.session

def index(req):
    return render(req, "regis/index.html")

def login(req):
    result = User.manager.login(req.POST)
    if result[0]:
        req.session['id'] = result[1].id
        user = User.manager.get(id=req.session['id'])
        Messages.objects.create(message = "" + user.user_name + " has just logged in.", user = None)
        return redirect('/success')
    for key, message in result[1].iteritems():
        messages.error(req,message)
    return redirect('/')

def register(req):
    result = User.manager.createUser(req.POST)
    if result[0]:
        req.session['id'] = result[1].id
        user = User.manager.get(id=req.session['id'])
        Messages.objects.create(message = "" + user.user_name + " has just made a account, welcome them.", user = None)
        return redirect('/success')
    for key, message in result[1]:
        messages.error(req, message)
    return redirect('/')

def message(req):
    msgsLen = Messages.objects.all().count()
    user = User.manager.get(id=req.session['id'])
    for users in BanList.objects.all():
        if users.user == user:
            message = Messages.objects.all()
            user = User.manager.get(id=req.session['id'])
            banlist = BanList.objects.all()
            context = {
                'self': user,
                'messages': message,
                "banList":  banlist,
                'banmessage': 'you have been banneed'
            }
            return render(req, 'regis/all.html', context)
    #if there are more than 100 messages, deletes the first four hundred messages
    if msgsLen > 30:
       for message in Messages.objects.all()[:20]:
           message.delete()
    result = Messages.manager.createMessages(req.POST)
    if len(result):
        for tag, error in result.iteritems():
            messages.error(req, error, extra_tags=tag)
        message = Messages.objects.all()
        banlist = BanList.objects.all()
        user = User.manager.get(id=req.session['id'])
        context = {
            'self': user,
            "banList":  banlist,
            'messages': message
        }
        return render(req, 'regis/all.html', context)
    else:
        user = User.manager.get(id=req.session['id'])
        newmessage = profanity.censor(req.POST['message'])
        Messages.objects.create(message = newmessage, user = user)
        message = Messages.objects.all()
        banlist = BanList.objects.all()
        user = User.manager.get(id=req.session['id'])
        context = {
            'self': user,
            "banList":  banlist,
            'messages': message
        }
        return render(req, 'regis/all.html', context)

def success(req):
    if noname(req):
        return redirect('/')
    message = Messages.objects.all()
    banlist = BanList.objects.all()
    user = User.manager.get(id=req.session['id'])
    context = {
        'self': user,
        "banList":  banlist,
        'messages': message
    }
    return render(req, "regis/success.html", context)

def logout(req):
    user = User.manager.get(id=req.session['id'])
    Messages.objects.create(message = "" + user.user_name + " Has logged out", user = None)
    req.session.clear()
    return redirect('/')

def load(req):
    message = Messages.objects.all()
    user = User.manager.get(id=req.session['id'])
    banlist = BanList.objects.all()
    context = {
        'self': user,
        "banList":  banlist,
        'messages': message
    }
    return render(req, 'regis/all.html', context)

def removeMessage(req, id):
    m = Messages.objects.get(id=id)
    m.message = "This message has been deleted"
    m.save()
    return redirect('/success')

def banUser(req, id):
    cuser = User.manager.get(id=req.session['id'])
    if cuser.admin != True:
        return redirect ('/success')
    message = Messages.objects.get(id=id)
    banned = BanList.objects.all()
    for ban in banned:
        if ban.user == message.user:
            ban.delete()
            Messages.objects.create(message = "" + message.user.user_name + " Has been unbanned", user = None)
            return redirect('/success')
    message.message = "This user has been banned for this message"
    message.save()
    user = message.user
    BanList.objects.create(user=user)
    return redirect('/success')

def unbanUser(req, id):
    cuser = User.manager.get(id=req.session['id'])
    if cuser.admin != True:
        return redirect ('/success')
    banned = BanList.objects.get(id=id)
    Messages.objects.create(message = "" + banned.user.user_name + " Has been unbanned", user = None)
    banned.delete()
    return redirect('/success')

def adminUser(req,id):
    cuser = User.manager.get(id=req.session['id'])
    if cuser.admin != True:
        return redirect ('/success')
    message = Messages.objects.get(id=id)
    user = message.user
    user.admin = True
    user.save()
    Messages.objects.create(message = "" + user.user_name + " Has been made a admin", user = None)
    return redirect('/success')
    
def noAdminUser(req,id):
    cuser = User.manager.get(id=req.session['id'])
    if cuser.admin != True:
        return redirect ('/success')
    message = Messages.objects.get(id=id)
    user = message.user
    user.admin = False
    user.save()
    Messages.objects.create(message = "" + user.user_name + " Has been removed as a admin", user = None)
    return redirect('/success')

def find(request):
    users = User.manager.filter(user_name__contains=request.POST['first_name_starts_with'])
    banlist = BanList.objects.all()
    context ={
        "users": users,
         "banList": banlist
    }
    return render(request, 'regis/users.html', context)