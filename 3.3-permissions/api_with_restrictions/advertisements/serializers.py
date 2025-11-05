from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # Получаем текущего пользователя из контекста
        user = self.context["request"].user
        
        # Получаем статус из данных (если он передан)
        # При создании по умолчанию будет OPEN
        status = data.get('status', AdvertisementStatusChoices.OPEN)
        
        # Проверяем только если статус OPEN
        if status == AdvertisementStatusChoices.OPEN:
            # При обновлении нужно исключить текущее объявление из подсчета
            if self.instance:
                # Это обновление существующего объявления
                open_ads_count = Advertisement.objects.filter(
                    creator=user,
                    status=AdvertisementStatusChoices.OPEN
                ).exclude(id=self.instance.id).count()
            else:
                # Это создание нового объявления
                open_ads_count = Advertisement.objects.filter(
                    creator=user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()
            
            # Проверяем лимит
            if open_ads_count >= 10:
                raise serializers.ValidationError(
                    "Превышен лимит открытых объявлений (максимум 10)."
                )

        return data
