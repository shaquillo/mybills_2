from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from django.contrib.auth.models import User
from . import models
from . import serializers
from rest_framework.response import Response

# Create your views here.


class ClientViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer()

    def create(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            user = serializers.UserClientSerializer(data=self.request.data['user'])
            if user.is_valid():
                if User.objects.filter(username=user.validated_data['username']).exists():
                    result['code'] = '04'
                    result['data'] = 'Account with username :' + user.validated_data['username'] + 'exists'
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                user = user.create(validated_data=user.validated_data)
                client = serializers.ClientSerializer(data={'tel': self.request.data['tel'], 'user': user.id})
                if client.is_valid():
                    client = client.create(validated_data=client.validated_data)
                    result['data'] = serializers.ClientSerializer(client).data
                    result['error'] = False
                    creation_status = status.HTTP_200_OK
                else:
                    result['code'] = '01'
                    user.delete()
                    creation_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                return Response(result, status=creation_status)
            else:
                result['code'] = '01'
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            client = self.get_object()
            client_serializer = self.get_serializer(client)
            result['data'] = client_serializer.data
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            user1 = User.objects.get_by_natural_key(username=self.request.data['user']['username'])
            user = serializers.UserClientSerializer(instance=user1, data=self.request.data['user'])
            if user.is_valid():
                client1 = models.Client.objects.get(pk = self.request.data['id'])
                client = serializers.ClientSerializer(instance=client1, data={'tel': self.request.data['tel'], 'user': self.request.data['user']['id']})
                if client.is_valid():
                    user.update(instance=user1, validated_data=user.validated_data)
                    client = client.update(instance=client1, validated_data=client.validated_data)
                    result['error'] = False
                    result['data'] = serializers.ClientSerializer(client).data
                    return Response(result, status=status.HTTP_200_OK)

                else:
                    result['code'] = '01'
                    print('client invalid')
            else:
                result['code'] = '01'
                print('user invalid')
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except models.User.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except models.Client.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            client = self.get_object()
            client = client.delete()
            result['error'] = False
            result['data'] = client.pk
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkerViewset(viewsets.ModelViewSet):
    queryset = models.Worker.objects.all()
    serializer_class = serializers.WorkerSerializer()

    def create(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            user = serializers.UserClientSerializer(data=self.request.data['user'])
            if user.is_valid():
                user = user.create(validated_data=user.validated_data)
                worker = serializers.WorkerSerializer(data={'tel': self.request.data['tel'], 'user': user.id, 'enterprise': self.request.data['enterprise']})
                if worker.is_valid():
                    worker = worker.create(validated_data=worker.validated_data)
                    result['data'] = serializers.ClientSerializer(worker).data
                    result['error'] = False
                    creation_status = status.HTTP_200_OK
                else:
                    result['code'] = '01'
                    user.delete()
                    creation_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                return Response(result, status=creation_status)
            else:
                result['code'] = '01'
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'

    def retrieve(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            worker = self.get_object()
            worker_serializer = self.get_serializer(worker)
            result['data'] = worker_serializer.data
            result['error'] = False
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            user1 = User.objects.get_by_natural_key(username=self.request.data['user']['username'])
            user = serializers.UserClientSerializer(instance=user1, data=self.request.data['user'])
            if user.is_valid():
                worker1 = models.Worker.objects.get(pk=self.request.data['id'])
                worker = serializers.WorkerSerializer(instance=worker1, data={'tel': self.request.data['tel'], 'user': self.request.data['user']['id'], 'enterprise': self.request.data['enterprise']})
                if worker.is_valid():
                    user.update(instance=user1, validated_data=user.validated_data)
                    worker = worker.update(instance=worker1, validated_data=worker.validated_data)
                    result['error'] = False
                    result['data'] = serializers.WorkerSerializer(worker).data
                    return Response(result, status=status.HTTP_200_OK)

                else:
                    result['code'] = '01'
                    print('client invalid')
            else:
                result['code'] = '01'
                print('user invalid')
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except models.User.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except models.Worker.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            worker = self.get_object()
            worker = worker.delete()
            result['error'] = False
            result['data'] = worker.pk
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubscriptionViewset(viewsets.ModelViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer

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

    def update(self, request, *args, **kwargs):
        result = {"error": True}

        try:
            instance = models.Subscription.objects.get(pk=kwargs['pk'])
            serializer = serializers.SubscriptionSerializer(instance=instance, data=self.request.data)
            if serializer.is_valid():
                serializer.update(instance=instance, validated_data=serializer.validated_data)
                object = serializer.update(instance=instance, validated_data=serializer.validated_data)
                result['error'] = False
                result['data'] = serializers.SubscriptionSerializer(object).data
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['code'] = '01'
                print('client invalid')

            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except models.Subscription.DoesNotExist:
            result['code'] = '03'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        result = {"error": True}
        try:
            object = self.get_object()
            object = object.delete()
            result['error'] = False
            result['data'] = object.pk
            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            result['code'] = '05'
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### Code: description

## 01: invalid data from user
## 02: invalid field
## 03: user does not exist
## 04: account with given username exists
## 05: unknown server error
