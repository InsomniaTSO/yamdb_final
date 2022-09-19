from rest_framework import mixins, viewsets


class CustomGenreCategoryViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    """Кастомный вьюсет для создания, вывода списка и удаления."""
    pass


class CustomTitleViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """Кастомный вьюсет для создания, вывода, возврата, обновление,
       сохранение списка и удаления."""
    pass
