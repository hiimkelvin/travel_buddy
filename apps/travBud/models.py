# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, datetime

class UsersManager(models.Manager):
    def reg(self, data):
    	errors = []

    	if len(data['name']) < 3:
    		errors.append("Name must be at least three characters long.")
    	if len(data['u_name']) < 3:
    		errors.append("Username must be at least three characters long.")
    	try:
    		Users.objects.get(user_name=data['u_name'])
    		errors.append("Username is already registered")
    	except:
    		pass
    	if len(data['pass']) < 8:
    		errors.append("Password must be at least eight characters long.")
    	if data['pass'] != data['c_pass']:
    		errors.append("Password does not match Confirm Password.")

    	if len(errors) == 0:
    		data['pass'] = bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt())
    		new_user = Users.objects.create(n_ame=data['name'], user_name=data['u_name'], pass_word=data['pass'])
    		return {
    			'new': new_user,
    			'error_list': None
    		}
    	else:
    		print(errors)
    		return {
    			'new': None,
    			'error_list': errors
    		}
    def log(self, data):
        errors = []
        try:
        	user = Users.objects.get(user_name=data['u_name'])
        	if bcrypt.hashpw(data['pass'].encode('utf-8'), user.pass_word.encode('utf-8')) != user.pass_word.encode('utf-8'):
        		errors.append("Incorrect password.")
        except:
        	errors.append("Username not registered.")
        if len(errors) == 0:
        	return {
        		'logged_user': user,
        		'list_errors': None
        	}
        else:
            return {
                'logged_user': None,
                'list_errors': errors
                }
    def add_trip(self, data):
        try:
            users_id = data['users_id']
            current_user = Users.objects.get(id = users_id)
            Trips.objects.create(id=current_user, user=current_user, destination=data['destin'], description=data['descr'], start_date=data['from'], end_date=data['to'])
        except:
            pass

    # def add_trip(self, data):
    #     errors = []
    #
    #     if data['destin'] == '':
    #         errors.append("Destination may not be blank.")
    #     if data['descr'] == '':
    #         errors.append("Description may not be blank.")
    #     if data['from'] == '':
    #         errors.append("Travel From Date is required.")
    #     elif datetime.datetime.strptime(data['from'], '%Y-%m-%d') <= datetime.datetime.now():
    #         errors.append("Cannot travel to the past!")
    #     if data['to'] == '':
    #         errors.append("Travel To Date is required.")
    #     elif datetime.datetime.strptime(data['to'], '%Y-%m-%d') <= datetime.datetime.now():
    #         errors.append("Cannot travel to the past!")
    #
    #     if len(errors) == 0:
    #         users_id = data['users_id']
    #         current_user = Users.objects.get(id = users_id)
    #         Trips.objects.create(id=current_user, user=current_user, destination=data['destin'], description=data['descr'], start_date=data['from'], end_date=data['to'])
    #         return {
    #         'new_errors': None
    #         }
    #     else:
    #         return {
    #         'new_errors': errors
    #         }

class Users(models.Model):
    n_ame = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    pass_word = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)
    user = models.ManyToManyField(Users, related_name='user_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
