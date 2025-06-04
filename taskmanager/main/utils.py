class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        # Добавьте сюда общие данные для контекста, если необходимо
        return context