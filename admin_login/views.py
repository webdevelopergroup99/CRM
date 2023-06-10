import json
import random

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import auth
from django.views.decorators.cache import cache_control

from admin_login.models import CustomUser


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def welcome_page(request):
    return render(request, 'adminLogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method == 'POST':
        username = str(request.POST['username'])
        password = str(request.POST['password'])

        # user = auth.authenticate(username=username, password=password)
        userdata = CustomUser.objects.filter(is_admin='True', username=username).values()
        # if user is not None and user.is_admin:
        if userdata.exists() and userdata[0]["password"] == password:
            print('OKKKKKKKKKK')
            print(userdata[0]["username"])
            # auth.login(request, user)
            # request.session['user_id'] = user.username
            request.session['user_id'] = userdata[0]["username"]
            user_details = CustomUser.objects.filter(is_admin='False', is_superuser='False').order_by(
                '-date_joined').values()
            context = {
                'all_users': user_details,
            }
            return render(request, 'addAndViewUser.html', context)
        else:
            print('wrong cred')
            messages.error(request, 'username or password not correct')
    return render(request, 'adminLogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    del request.session['user_id']
    # auth.logout(request)
    return render(request, 'adminLogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_user(request):
    print("create_user")
    if request.method == 'POST':
        user_json_data = json.loads(request.body.decode("utf-8"))
        print(user_json_data)
        print("create_user")
        print(user_json_data["first_name"])
        firstname = user_json_data["first_name"]
        lastname = user_json_data["last_name"]
        email = user_json_data["email"]
        mobile = user_json_data["phone_number"]
        birthday = user_json_data["birthday"]
        username = firstname + '_' + lastname
        initialpass = firstname + str(random.randint(1000, 9999))
        password = make_password(initialpass)
        print(username)
        print(initialpass)
        createuser = CustomUser.objects.create(username=username,
                                               first_name=firstname, last_name=lastname,
                                               email=email, password=password, phone_number=mobile,
                                               birthday=birthday)
        createuser.save()
        context = {
            'user_name': username,
            'user_password': initialpass,
            'success': 'The user was added successfully'
        }
    return JsonResponse(context, status=200)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fetch_user(request):
    if request.method == 'GET':
        all_users = CustomUser.objects.filter(is_admin='False', is_superuser='False').order_by(
            '-date_joined').values()
        print(list(all_users))
        return JsonResponse({"response": list(all_users)}, safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_password(request, main_user_type):
    context = {
        'user_id': main_user_type,
    }
    return render(request, 'forgotPassword.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validate_forgot_password(request):
    if request.method == 'POST':
        userid = str(request.POST['userid'])
        old_password = str(request.POST['oldPassword'])
        userdata = CustomUser.objects.filter(is_admin='True', username=userid).values()
        # if userdata.exists() and check_password(old_password, userdata[0]["password"]):
        if userdata.exists() and userdata[0]["password"] == old_password:
            username = userdata[0]["username"]
            context = {
                'user_name': username,
            }
            return render(request, 'forgotPwdInput.html', context)
        else:
            context = {
                'user_id': userid,
            }
            messages.error(request, 'Password is incorrect. Please try again')
            return render(request, 'forgotPassword.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    if request.method == 'POST':
        username = str(request.POST['username'])
        new_password = str(request.POST['new-password'])
        confirm_password = str(request.POST['confirm-password'])
        record = CustomUser.objects.get(username=username)
        record.password = str(new_password)
        record.is_verified = True
        record.save(update_fields=["password", "is_verified"])
        messages.success(request, 'Your password has been changed successfully')
        return render(request, 'adminLogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def is_admin_verified(request):
    if request.method == 'GET':
        record = CustomUser.objects.get(username='admin')
        print(record.is_verified)
        return JsonResponse({"response": record.is_verified}, safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validate_admin_before_show(request):
    if request.method == 'GET':
        context = {
            'user_id': 'ADMIN',
        }
        return render(request, 'validateAdminBeforeShowDetails.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_admin_details(request):
    if request.method == 'POST':
        username = str(request.POST['userid'])
        mobile = str(request.POST['mobile'])
        record = CustomUser.objects.get(username='admin')
        print("hellooooo")
        print(record.phone_number)
        if record.phone_number == mobile:
            context = {
                'admin_data': record,
            }
            return render(request, 'viewAdminDetails.html', context)
        else:
            context = {
                'user_id': username,
            }
            messages.error(request, 'Contact is incorrect. Please try again')
            return render(request, 'validateAdminBeforeShowDetails.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def redirect_admin_login(request):
    if request.method == 'GET':
        return render(request, 'adminLogin.html')

