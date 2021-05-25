from django.shortcuts import render
from rest_framework import viewsets, mixins, status

from platforms.authentication import PlatformsAuthentication
from . import models
from . import serializers
from rest_framework.response import Response
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny,IsAuthenticated

import coreapi, coreschema
from rest_framework.schemas import ManualSchema

from rest_framework_simplejwt.views import TokenRefreshView

# Create your views here.


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class ClientViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

    authentication_classes = [PlatformsAuthentication]
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsAuthenticated: ['update', 'retrieve', 'destroy'],
        AllowAny: ['create']
    }

    def create(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            if models.Client.objects.filter(username=self.request.data['username']).exists():
                result['code'] = '04'
                result['data'] = 'Account with username :' + self.request.data['username'] + ' exists'
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            client = serializers.ClientSerializer(data=self.request.data)
            if client.is_valid():
                client = client.create(validated_data=client.validated_data)
                refresh = RefreshToken.for_user(client)
                result['token'] = {'refresh': str(refresh), 'access': str(refresh.access_token)}
                result['data'] = serializers.ClientSerializer(client).data
                # result['data']['user']['username'] = result['data']['user']['username'][2:]
                result['error'] = False
                creation_status = status.HTTP_200_OK
            else:
                result['code'] = '01'
                result['data'] = 'invalid client'
                creation_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(result, status=creation_status)
        except Exception as e:
            print(e)
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            client = self.get_object()
            client_serializer = self.get_serializer(client)
            result['data'] = client_serializer.data
            # result['data']['user']['username'] = result['data']['user']['username'][2:]
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except models.Client.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            client1 = self.get_object() # models.Client.objects.get(pk = self.request.data['id'])
            client = serializers.ClientSerializer(instance=client1, data=self.request.data)
            if client.is_valid():
                client = client.update(instance=client1, validated_data=client.validated_data)
                result['error'] = False
                result['data'] = serializers.ClientSerializer(client).data
            else:
                result['code'] = '01'
                print('client invalid')
            return Response(result, status=status.HTTP_200_OK)
        except models.Client.DoesNotExist:
            result['code'] = '03'
            result['data'] = 'client does not exist'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            client = self.get_object()
            result['data'] = client.pk
            client.delete()
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkerViewset(viewsets.ModelViewSet):
    queryset = models.Worker.objects.all()
    serializer_class = serializers.WorkerSerializer

    sep = '*~*'

    authentication_classes = [PlatformsAuthentication]
    permission_classes = (ActionBasedPermission, )
    action_permissions = {
        IsAuthenticated: ['update', 'retrieve', 'destroy', 'list'],
        AllowAny: ['create']
    }

    def create(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            enterprise_name = models.Enterprise.objects.get(pk=self.request.data['enterprise']).title
            data = self.request.data

            data['username'] = enterprise_name + WorkerViewset.sep + data['username']
            if models.Worker.objects.filter(username=data['username']).exists():
                result['code'] = '04'
                result['data'] = 'Account with username :' + self.request.data['username'] + ' exists'
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            worker = serializers.WorkerSerializer(data=data)
            if worker.is_valid():
                worker = worker.create(validated_data=worker.validated_data)
                refresh = RefreshToken.for_user(worker)
                result['token'] = {'refresh': str(refresh), 'access': str(refresh.access_token)}
                result['data'] = serializers.ClientSerializer(worker).data
                result['data']['username'] = self.__get_username_w(result['data']['username'])
                result['error'] = False
                creation_status = status.HTTP_200_OK
            else:
                result['code'] = '01'
                result['data'] = 'invalid worker data'
                creation_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(result, status=creation_status)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            worker = self.get_object()
            worker_serializer = self.get_serializer(worker)
            result['data'] = worker_serializer.data
            result['data']['username'] = self.__get_username_w(result['data']['user']['username'])
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except models.Worker.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        result = {"error": False}

        try:
            workers = self.get_queryset()
            worker_serializer = serializers.WorkerSerializer(workers, many=True)
            result['data'] = worker_serializer.data
            for i in range(len(result['data'])):
                result['data'][i]['username'] = self.__get_username_w(result['data']['user']['username'])
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            result['error'] = False
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            worker1 = self.get_object()  # models.Client.objects.get(pk = self.request.data['id'])
            enterprise_name = models.Enterprise.objects.get(pk=self.request.data['enterprise']).title
            data = self.request.data

            data['username'] = enterprise_name + WorkerViewset.sep + data['username']
            worker = serializers.ClientSerializer(instance=worker1, data=data)
            if worker.is_valid():
                worker = worker.update(instance=worker1, validated_data=worker.validated_data)
                result['error'] = False
                result['data'] = serializers.ClientSerializer(worker).data
            else:
                result['code'] = '01'
                print('worker invalid')
            return Response(result, status=status.HTTP_200_OK)
        except models.Worker.DoesNotExist:
            result['code'] = '03'
            result['data'] = 'worker does not exist'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            worker = self.get_object()
            result['data'] = worker.pk
            worker.delete()
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __get_username_w(self, username):
        i = username.find(WorkerViewset.sep)
        return username[i+len(WorkerViewset.sep):]


class SubscriptionViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer

    authentication_classes = [PlatformsAuthentication]
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        result = {'error': True}
        try:
            serializer = serializers.SubscriptionSerializer(data=self.request.data)
            if serializer.is_valid():
                object = serializer.create(validated_data=serializer.validated_data)
                result['data'] = serializers.SubscriptionSerializer(object).data
                result['error'] = False
                s_status = status.HTTP_200_OK
            else:
                print(serializer.validated_data)
                result['code'] = '02'
                s_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(result, status=s_status)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            object = self.get_object()
            serializer = self.get_serializer(object)
            result['data'] = serializer.data
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            objects = self.get_queryset()
            serializer = self.get_serializer(objects, many=True)
            result['data'] = serializer.data
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def update(self, request, *args, **kwargs):
    #     result = {"error": True}
    #
    #     try:
    #         instance = models.Subscription.objects.get(pk=kwargs['pk'])
    #         serializer = serializers.SubscriptionSerializer(instance=instance, data=self.request.data)
    #         if serializer.is_valid():
    #             object = serializer.update(instance=instance, validated_data=serializer.validated_data)
    #             result['error'] = False
    #             result['data'] = serializers.SubscriptionSerializer(object).data
    #             return Response(result, status=status.HTTP_200_OK)
    #         else:
    #             result['code'] = '01'
    #             print('client invalid')
    #
    #         return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     except models.Subscription.DoesNotExist:
    #         result['code'] = '03'
    #         return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     except Exception:
    #         result['code'] = '05'
    #         return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            object = self.get_object()
            result['data'] = object.pk
            object.delete()
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TOPViewset(TokenObtainPairView):
    authentication_classes = [PlatformsAuthentication]
    permission_classes =  [AllowAny]
    serializer_class = serializers.TOPSerializer


class TokenRefreshViewM(TokenRefreshView):
    authentication_classes = [PlatformsAuthentication]

### Code: description

## 01: invalid data from user
## 02: invalid field
## 03: user does not exist
## 04: account with given username exists
## 05: unknown server error
