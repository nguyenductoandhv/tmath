import datetime

from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

__all__ = ['TypoData', 'TypoContest', 'TypoResult', 'TypoProfile', 'TypoRoom']

# Create your models here.

DIFFICULT = (
    ('newbie', _('Newbie')),
    ('amateur', _('Amateur')),
    ('expert', _('Expert')),
    ('master', _('Master')),
    ('gmaster', _('Grand Master')),
)


class TypoData(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    data = models.TextField(blank=False)
    difficult = models.CharField(_('difficult'), max_length=10, choices=DIFFICULT, default='newbie')

    def __str__(self) -> str:
        return self.name


class TypoContest(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True, null=True)
    data = models.ForeignKey(TypoData, related_name='contest', null=True, on_delete=models.SET_NULL)
    time_start = models.DateTimeField(_('time start'), help_text=_('time to start racing'))
    time_join = models.DateTimeField(_('time join'), help_text=_('time to participation join'))
    limit = models.IntegerField(_('time limit'), help_text=_('time limit'), default=0)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return 'typo %s' % self.id

    @cached_property
    def _now(self):
        return now()

    @cached_property
    def start_time(self):
        return self.time_start.total_seconds()

    @property
    def time_until_start(self):
        if self._now >= self.time_start:
            return 0
        return (self.time_start - self._now).total_seconds()

    @property
    def time_until_end(self):
        if self._now >= self.time_start:
            return 0
        return (self.time_end - self._now).total_seconds()

    @property
    def time_end(self):
        return self.time_start + datetime.timedelta(seconds=self.limit)

    @property
    def ended(self):
        return self._now > self.time_start + datetime.timedelta(seconds=self.limit)

    @property
    def time_before_join(self):
        if self.time_join > self._now:
            return self.time_join - self._now
        else:
            return None

    @property
    def can_join(self):
        return self._now < self.time_start and self._now >= self.time_join

    @property
    def is_opened(self):
        return self._now >= self.time_join


class TypoResult(models.Model):
    user = models.ForeignKey('judge.Profile', verbose_name=_('user'), related_name='typos', on_delete=models.CASCADE)
    time = models.FloatField(_('time'), default=0)
    speed = models.FloatField(_('speed'), default=0)
    ranked = models.BooleanField(_('is ranking'), default=False)
    order = models.PositiveIntegerField(_('order'), default=1)
    progress = models.IntegerField(_("progress"), default=0)
    is_finish = models.BooleanField(_("is finished"), default=False)
    contest = models.ForeignKey("typeracer.TypoContest", verbose_name=_("contest"), related_name='participations',
                                null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "%s - %s" % (self.user, self.contest)

    class Meta:
        unique_together = ('user', 'contest')
        verbose_name = _('typo result')
        verbose_name_plural = _('typo results')


class TypoProfile(models.Model):
    max_speed = models.FloatField(_('max speed'), default=0)
    date = models.DateTimeField(_('date created'))
    level = models.CharField(_('level'), max_length=10, choices=DIFFICULT, default='newbie')


class TypoRoom(models.Model):
    MODE = (
        ('solo', _('Solo')),
        ('multi', _('Multi')),
    )

    name = models.CharField(_("name"), max_length=255, default='')
    contest = models.ForeignKey(TypoContest, related_name='room', null=True, blank=True, on_delete=models.SET_NULL)
    is_random = models.BooleanField(_("is random contest"), default=True)
    max_user = models.IntegerField(_("max number user can participation"), default=-1)
    practice = models.BooleanField(_("practice room"), default=False)
    is_private = models.BooleanField(_("is private"), default=False)
    access_code = models.CharField(_('access code'), max_length=100, blank=True, default='')
    mode = models.CharField(_('mode'), max_length=10, choices=MODE, default='multi')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("typeracer:room_detail", kwargs={"pk": self.pk})
    
    @property
    def user_count(self):
        return TypoResult.objects.filter(contest=self.contest).count()


class TypoRoomUser(models.Model):
    ACTION = (
        ('0', _('Participant')),
        ('1', _('Spectator')),
        ('2', _('Waiting')),
    )

    room = models.ForeignKey(TypoRoom, related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey('judge.Profile', related_name='rooms', on_delete=models.CASCADE)
    action = models.CharField(_('action'), max_length=1, choices=ACTION, default='2')

    def __str__(self) -> str:
        return "%s - %s" % (self.room, self.user)

    class Meta:
        unique_together = ('room', 'user')
        verbose_name = _('room user')
        verbose_name_plural = _('room users')
