from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'POST': 'api/users/token/'},
        {'POST': 'api/users/token/refresh/'},
        {'POST': 'api/users/register/'},
        {'POST': 'api/users/login/'},
    ]
    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    # Validate the user input.
    if not data['first_name']:
        return Response({'detail': 'First name is required.'}, status=400)
    if not data['last_name']:
        return Response({'detail': 'Last name is required.'}, status=400)
    if not data['username']:
        return Response({'detail': 'Username is required.'}, status=400)
    if not validate_email(data['email']):
        return Response({'detail': 'Invalid email address.'}, status=400)
    if User.objects.filter(email=data['email']).exists():
        return Response({'detail': 'User with this email already exists.'}, status=400)
    if not data['password']:
        return Response({'detail': 'Password is required.'}, status=400)
    if not data['password_confirmation']:
        return Response({'detail': 'Please confirm your password.'}, status=400)
    if data['password'] != data['password_confirmation']:
        return Response({'detail': 'Passwords do not match.'}, status=400)

    # Hash the user password.
    password = data['password']
    user = User.objects.create_user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        password=password
    )
    user.set_password(password)
    user.save()

    return Response('User was created')


@api_view(['POST'])
def loginUser(request):
    data = request.data
    username_or_email = data['identifier']
    password = data['password']

    # Validate the user input.
    if not username_or_email:
        return Response({'detail': 'Username or email is required.'}, status=400)
    if not password:
        return Response({'detail': 'Password is required.'}, status=400)

    # if the username_or_email is an email, get the user by email.
    try:
        validate_email(username_or_email)
        user = User.objects.get(email=username_or_email)
    except:
        user = User.objects.get(username=username_or_email)
    if not user:
        return Response({'detail': 'User with this username or email does not exist.'}, status=400)

    # Check if the password is correct.
    is_valid_password = authenticate(username=user.username, password=password)
    if not is_valid_password:
        return Response({'detail': 'Invalid password.'}, status=401)

    # Login the user.
    auth_token = user.auth_token
    return Response({'detail': 'User was logged in', 'auth_token': auth_token})
