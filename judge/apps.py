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
        from judge.models import Organization

        from . import jinja2, signals  # noqa: F401, imported for side effects

        # try:
        #     lang = Language.get_default_language()
        #     for user in User.objects.filter(profile=None):
        #         # These poor profileless users
        #         profile = Profile(user=user, language=lang)
        #         profile.save()
        #     for user in User.objects.filter(logged_in_user=None):
        #         # These poor profileless users
        #         logged_in_user = LoggedInUser(user=user)
        #         logged_in_user.save()
        # except DatabaseError:
        #     pass
        # problems = Problem.objects.all()
        # for problem in problems:
        #     description: str = problem.description
        #     description = description.replace('~', '$')
        #     problem.description = description
        #     problem.save()

        try:
            for org in Organization.objects.filter(chat_room=None):
                room = ChatRoom(organization=org, title=org.name)
                room.save()
                for user in org.members.all():
                    participation = ChatParticipation(user=user, room=room)
                    participation.save()
        except DatabaseError:
            pass
