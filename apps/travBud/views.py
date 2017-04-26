# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Users, Trips
from django.contrib import messages

def index(request):
	return render(request, 'travBud/index.html')

def register(request):
	context = {
		'name': request.POST['name'],
        'u_name': request.POST['username'],
		'pass': request.POST['password'],
		'c_pass': request.POST['confirm_pw'],
	}
	reg_results = Users.objects.reg(context)
	if reg_results['new'] != None:

		request.session['users_id'] = reg_results['new'].id
		request.session['users_name'] = reg_results['new'].n_ame
		return redirect('/travels')
	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def login(request):
    context = {
        'u_name': request.POST['username'],
        'pass': request.POST['password'],
    }
    results = Users.objects.log(context)
    if results['list_errors'] != None:
        for error in results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['users_id'] = results['logged_user'].id
        request.session['users_name'] = results['logged_user'].n_ame
        return redirect('/travels')

def travels(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')

    context ={
        'users': Users.objects.all(),
        'trips': Trips.objects.all(),
    }
    return render(request, 'travBud/travels.html', context)

def add(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')
    return render(request, 'travBud/addtrip.html')


def add_trip(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')

    context = {
    'users_id': request.session['users_id'],
    'destin': request.POST['destination'],
    'descr': request.POST['description'],
    'from': request.POST['date_from'],
    'to': request.POST['date_to'],
    }

    results = Trips.objects.add_trip(context)
    print context
    #
    # if results['new_errors'] != None:
    #     for error in results['new_errors']:
    #         messages.add_message(request, messages.ERROR, error)
    #         return redirect('/add_trip')
    #     else:
    #         return redirect('/travels')
    # return redirect('/')
    # return render(request, 'travBud/addtrip.html', context)
    return redirect('/travels')

def logout(request):
	request.session.clear()
	return redirect('/')
