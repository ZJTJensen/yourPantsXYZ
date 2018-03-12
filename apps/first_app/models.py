from __future__ import unicode_literals

from django.db import models
from profanity import profanity 
import collections
import re
import bcrypt

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^a-zA-Z0-9._-]+$')

def uni_str_dict(mydict):
    data={}
    for key, value in mydict.iteritems():
        data[key] = str(value)
    return data

class MessageManager(models.Model):
    def createMessages(self, form):
        errors= {}
        data = uni_str_dict(form)
        if len (data['message'])< 1:

            errors['message']="The Message must be greater than 10 letters"
        return (errors)

class UserManager(models.Manager):
    def createUser(self, form):
        flag = False
        errors = []
        data = uni_str_dict(form)
        if User.manager.filter(email = data['email']):
            flag = True
            errors.append(("used_email", "This email is already in use"))
            return (False, errors)
        if len(data['user_name'])<2:
            flag = True
            errors.append(('user_name_length', "Your first name must be at lest three characters long"))
        
        if User.manager.filter(user_name = data['user_name']):
            flag = True
            errors.append(("user_name_found", "This name is already in use"))
            return (False, errors)
        if not EMAIL_REGEX.match(data['email']):
            errors.append(('email', "we are going to need a valid email address."))
            flag = True
        if not data['password']== data['confirm_password']:
            errors.append(('password', "password does not match"))
            flag= True
        if flag:
            return (False, collections.OrderedDict(errors))
        if len(User.manager.all()) >= 1:
            admin = False
        else:
            admin = True
        new_user = self.create(admin = admin, user_name = data['user_name'], email = data['email'],  password = bcrypt.hashpw(data['password'], bcrypt.gensalt()))
        return(True, new_user)
    
    def login(self, form):
        flag = False
        errors = {}
        data = uni_str_dict(form)
        try:
            called_user = User.manager.get(email=data['email'])
        except Exception:
            flag=True  
            errors["death"] = "not found in record"
            return (False, errors)
        if not bcrypt.checkpw(data['password'].encode(), called_user.password.encode()):
            flag= True
            errors["password"]="wrong password"

        if flag:
            return (False, errors)
        return(True, called_user)

class User(models.Model):
    user_name = models.CharField(max_length= 20)
    email = models.CharField(max_length= 50)
    password = models.CharField(max_length= 255)
    admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager= UserManager()

class Messages(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messager", null = True)
    manager = MessageManager()

class BanList(models.Model):
    # created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="banned", null = True)
    


