from .models import Store
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        # fields = [
        #     "id",
        #     "store_name",
        #     "branch",
        #     "tel",
        #     "address",
        #     "latitude",
        #     "longitude",
        # ]
