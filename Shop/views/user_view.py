
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from cart.models import Cart
from wishlist.models import Wishlist
from users.models import MyUser, ProfileUser

User = get_user_model()

@csrf_exempt
def register(request):
  if request.method == 'GET':
    return render(request, 'register.html')
  if request.method == 'POST':
    username = request.POST.get('username', None)
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    phone = request.POST.get('phone', None)
    avatar = request.FILES.get('avatar', None)
    email = request.POST.get('email', None)
    birth = request.POST.get('birth', None)
    gender = request.POST.get('gender', None)
    city = request.POST.get('city', None)
    address = request.POST.get('address', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)

    if not first_name or not last_name or not email or not birth or not password or password != re_password:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Register account failded, please enter all value fields!'
      }
      return JsonResponse(data)

    if User.objects.filter(email=email).count() == 1:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Email is already existing'
      }
      return JsonResponse(data)

    user = User.objects.create_user(
      username=username,
      password=password,
      email=email
    )
    if user.id:
      profile_user = ProfileUser.objects.create_profileuser(
        user=user,
        first_name=first_name,
        last_name=last_name,
        avatar=avatar,
        phone=phone,
        gender=gender,
        city=city,
        address=address
      )
      if profile_user.id:
        # subject = 'Active account'
        # message = 'Thank for your register account, please click to below link in this email to active your account!'
        # recipent_list = [profile_user.email]
        # result = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipent_list)
        # if not result:
        #   data = {
        #     'code': 400,
        #     'status': 'error',
        #     'message': 'Register account failed, We can not send email to your email to active account'
        #   }
        #   return JsonResponse(data)

        data = {
          'code': 200,
          'status': 'success',
          'message': 'Register account successful'
        }
        return JsonResponse(data)

    data = {
      'code': 400,
      'status': 'error',
      'message': 'Register account failed'
    }
    return JsonResponse(data)

def login_user(request, *args, **kwargs):
  if request.method == 'GET':
    next = request.GET.get('next', '')
    return render(request, 'login.html', {'next': next})
  if request.method == 'POST':
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    next = request.POST.get('next', '')
    if email is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Can not login, email incorrect'
      }
      return JsonResponse(data)

    if password is None:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Can not login, password incorrect'
      }
      return JsonResponse(data)


    user = authenticate(request, username=email, password=password)
    if user is not None:
      login(request, user)
      cart, created = Cart.objects.get_existing_or_new(request)
      wish, craeted = Wishlist.objects.get_wishlist_or_create(request)
      data = {
        'code': 200,
        'status': 'success',
        'message': 'login success',
        'next': next,
        'username': user.get_username(),
        'num_cart': cart.num_item,
        'num_wish': wish.count_items
      }
      return JsonResponse(data)

    user = User.objects.filter(email=email).first()
    if user and not user.is_active:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'This user had not active'
      }
      return JsonResponse(data)
    else:
      data = {
        'code': 400,
        'status': 'error',
        'message': 'Login failed, you should check email and password again'
      }
      return JsonResponse(data)

def logout_user(request):
  logout(request)
  if request.user.is_authenticated is False:
    data = {
      'code': 200,
      'status': 'success',
      'message': 'logout success'
    }
    return JsonResponse(data)

  data = {
    'code': 400,
    'status': 'error',
    'message': 'logout failed'
  }
  return JsonResponse(data)

