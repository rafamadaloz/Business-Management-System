from rest_framework import serializers
from SGEO.apps.customer.models import Client, Domain
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django_tenants.utils import tenant_context


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ('name', 'username', 'password', 'email', 'cpf_cnpj',
                  'schema_name')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """


        dias_teste = datetime.today().date() + timedelta(days=7)

        name = validated_data.pop('name')
        username = validated_data.pop('username')
        schema_name = validated_data.pop('schema_name')
        email = validated_data.pop('email')
        cpf_cnpj = validated_data.pop('cpf_cnpj')
        client, created = Client.objects.update_or_create(
            schema_name=schema_name,
            name=name,
            username=username,
            password=validated_data['password'],
            paid_until=dias_teste,
            email=email,
            cpf_cnpj=cpf_cnpj,
            on_trial=True,
        )

        domain = Domain()
        domain.domain = schema_name + ".SGEOerp.com.br"
        domain.tenant = client
        domain.is_primary = True
        domain.save()

        tenant1 = Client(schema_name=schema_name)

        with tenant_context(tenant1):
            User.objects.create_superuser(
                username=username,
                password=validated_data['password'],
                email=email
            )

        return client