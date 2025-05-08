from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Distributor, PaymentRecord
from .serializers import DistributorSerializer, PaymentRecordSerializer, UserSerializer
from .sap_integration import sync_distributor, sync_payment
from . import sap_integration


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def distributor_list_create(request):
    if request.method == 'GET':
        distributors = Distributor.objects.all()
        serializer = DistributorSerializer(distributors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            distributor = serializer.save()
            sync_distributor(distributor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def distributor_retrieve_update(request, pk):
    try:
        distributor = Distributor.objects.get(pk=pk)
    except Distributor.DoesNotExist:
        return Response({'detail': 'Distributor not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DistributorSerializer(distributor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DistributorSerializer(distributor, data=request.data)
        if serializer.is_valid():
            distributor = serializer.save()
            sync_distributor(distributor)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_list_create(request):
    if request.method == 'GET':
        payments = PaymentRecord.objects.all()
        serializer = PaymentRecordSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PaymentRecordSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            sync_payment(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def payment_retrieve(request, pk):
    try:
        payment = PaymentRecord.objects.get(pk=pk)
    except PaymentRecord.DoesNotExist:
        return Response({'detail': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentRecordSerializer(payment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PaymentRecordSerializer(payment, data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            sync_payment(payment)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .cashfree_integration import confirm_payment_cashfree

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_confirm(request, pk):
    try:
        payment = PaymentRecord.objects.get(pk=pk)
    except PaymentRecord.DoesNotExist:
        return Response({'detail': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

    if payment.status == 'CONFIRMED':
        return Response({'detail': 'Payment already confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

    # Confirm payment with Cashfree
    payment_id = request.data.get('payment_id')
    if not payment_id:
        return Response({'detail': 'Payment ID is required for confirmation.'}, status=status.HTTP_400_BAD_REQUEST)

    confirmed = confirm_payment_cashfree(payment_id, request.data)
    if not confirmed:
        return Response({'detail': 'Payment confirmation failed with Cashfree.'}, status=status.HTTP_400_BAD_REQUEST)

    payment.status = 'CONFIRMED'
    payment.save()
    return Response({'detail': 'Payment confirmed successfully.'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([])
def register_user(request):
    if request.method == 'GET':
        return Response({'detail': 'Method GET not allowed on this endpoint.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'detail': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    }, status=status.HTTP_200_OK)

# Removed login_page and register_page views as per removal of HTML templates

# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             request.session['access_token'] = str(refresh.access_token)
#             request.session['refresh_token'] = str(refresh)
#             return redirect('/api/distributors/')  # Redirect to API page after login
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Automatically log in the user after registration
#             from django.contrib.auth import login as auth_login
#             auth_login(request, user)
#             from rest_framework_simplejwt.tokens import RefreshToken
#             refresh = RefreshToken.for_user(user)
#             request.session['access_token'] = str(refresh.access_token)
#             request.session['refresh_token'] = str(refresh)
#             return redirect('/api/distributors/')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})

# Removed login_page and register_page views as per removal of HTML templates
@api_view(['POST'])
@permission_classes([])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

