from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение: только автор может обновлять и удалять объявление.
    """
    
    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь является создателем объявления
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
