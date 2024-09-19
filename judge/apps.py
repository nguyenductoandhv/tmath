from django.apps import AppConfig
from django.db import DatabaseError
from django.utils.translation import gettext_lazy


class JudgeAppConfig(AppConfig):
    name = 'judge'
    verbose_name = gettext_lazy('Online Judge')

    def ready(self):
        # WARNING: AS THIS IS NOT A FUNCTIONAL PROGRAMMING LANGUAGE,
        #          OPERATIONS MAY HAVE SIDE EFFECTS.
        #          DO NOT REMOVE THINKING THE import IS UNUSED.
        # noinspection PyUnresolvedReferences
        from chat.models import ChatParticipation, ChatRoom
        from judge.models import Organization, Problem
        import pytz
        from datetime import datetime

        from . import jinja2, signals  # noqa: F401, imported for side effects

        try:
            tz = pytz.timezone('Asia/Bangkok')
            date = tz.localize(datetime(2024, 8, 1))
            Problem.objects.filter(approved=False, date__lt=date).update(approved=True)
            for org in Organization.objects.filter(chat_room=None):
                room = ChatRoom(organization=org, title=org.name)
                room.save()
                for user in org.members.all():
                    participation = ChatParticipation(user=user, room=room)
                    participation.save()
        except DatabaseError:
            pass
