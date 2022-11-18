from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_tenants.utils import schema_exists, schema_context
from apps.shared.clients.models import Client, Domain, Account
from apps.tenant.user.models import User


class SignupView(APIView):
    # serializer_class = 'serializer_class'

    def post(self, request):
        name = request.data['name']
        mobile = request.data['mobile']
        email = request.data['email']
        workspace = request.data['workspace']
        password = request.data['password']
        workspace = ''.join(workspace)
        schema = workspace.lower()
        if schema == '':
            return Response({'error': 'workspace cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        elif schema_exists(schema):
            return Response({'error': 'workspace name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            tenant = Client(schema_name=schema)
            tenant.save()
            domain = Domain(domain=schema + '.moonlightsenpai.ml', tenant=tenant)
            domain.save()
            account = Account(mobile=mobile, name=name, workspace=tenant, email=email)
            account.save()
            with schema_context(tenant.schema_name):
                User.objects.create_super_user(name=name, mobile=mobile, password=password)
            context = {
                'success': 'user signup successfully',
                'url': domain.domain
            }
            return Response(context, status=status.HTTP_200_OK)
