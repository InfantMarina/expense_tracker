from rest_framework import serializers
from application import models

class User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserManager
        fields = "__all__"

class Transaction_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transaction
        fields = "__all__"