from random import randint

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)
from django.views.generic.detail import SingleObjectMixin

# from judge import event_poster as event
from judge.models import Profile
from judge.utils.views import TitleMixin, generic_message
from typeracer.forms import CreateRoomForm
from typeracer.models import (TypoContest, TypoData, TypoResult, TypoRoom,
                              TypoRoomUser)

# Create your views here.

channel_layer = get_channel_layer()


def get_random_contest(limit=12):
    data = TypoData.objects.all()
    i = randint(0, data.count() - 1)
    contest = TypoContest.objects.create(
        data=data[i],
        time_start=timezone.now() + timezone.timedelta(seconds=limit),
        time_join=timezone.now(),
        limit=300,
    )
    return contest


def updateProgress(request):
    # if request.method == 'POST':
    #     user = request.POST.get('user')
    #     progress = request.POST.get('progress')
    #     contest = request.POST.get('contest')
    #     event.post('typocontest_%s' % contest, {
    #       'user': user,
    #       'progress': progress,
    #     })
    return JsonResponse({
        'result': 'success',
        'status': 200,
    })


def get_rank(index):
    if index == 0:
        return '1st'
    if index == 1:
        return '2nd'
    if index == 2:
        return '3rd'
    return str(index + 1) + 'th'


def finishTypoContest(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        contest = request.POST.get('contest')
        progress = request.POST.get('progress')
        speed = request.POST.get('speed')
        time = request.POST.get('time')
        is_finish = request.POST.get('finish')
        contest_object = TypoContest.objects.get(pk=contest)
        # rank = TypoResult.objects.filter(contest=contest_object)
        profile = Profile.objects.get(user__pk=user)
        result = TypoResult.objects.get(
            user=profile,
            contest=contest_object,
        )
        result.speed = int(speed)
        result.time = int(time) / 1000
        result.progress = int(progress)
        # result.order = rank + 1
        result.is_finish = is_finish == 'true'
        result.save()
        async_to_sync(channel_layer.group_send)(
            'contest_%s' % contest,
            {
                'type': 'change.progress.participation',
                'message': {
                    'user': profile.pk,
                    'progress': progress,
                },
            },
        )
    return JsonResponse({
        'result': 'success',
        'status': 200,
    })


def getQuote(request, pk):
    room: TypoRoom = TypoRoom.objects.get(pk=pk)
    contest: TypoContest = room.contest
    if contest._now >= contest.time_start:
        return JsonResponse({
            'content': room.contest.data.data,
        })
    else:
        return JsonResponse({
            'content': '',
        })


class Racer(TemplateView):
    template_name: str = 'typeracer/racer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user.user
        return context

    def dispatch(self, request, *args, **kwargs):
        index = request.GET.get('user')
        self.object = TypoResult.objects.get(pk=index)
        return super().dispatch(request, *args, **kwargs)


class TypoRoomList(TitleMixin, ListView):
    model = TypoRoom
    context_object_name = 'rooms'
    template_name: str = 'typeracer/listroom.html'
    title = _('Rooms')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.profile.typo_contest is not None:
            context['current_room'] = self.request.user.profile.typo_contest.room
        return context


class RoomMixin(object):
    slug_url_kwarg: str = 'pk'
    slug_field: str = 'pk'
    model = TypoRoom
    context_object_name = 'room'


@method_decorator(never_cache, name='dispatch')
class RoomDetail(TitleMixin, RoomMixin, DetailView):
    template_name: str = 'typeracer/room.html'

    def get_title(self):
        return f'{self.object.pk} - {self.object.name}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participations = TypoRoomUser.objects.filter(room=self.object)
        context['participants'] = list(participations.filter(action='0'))
        context['spectators'] = list(participations.filter(action='1'))
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class Ranking(TitleMixin, DetailView):
    slug_url_kwarg: str = 'pk'
    slug_field: str = 'pk'
    model = TypoContest
    context_object_name = 'contest'
    template_name: str = 'typeracer/rank.html'
    title: str = 'Typo Contest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranks'] = TypoResult.objects.filter(contest=self.object) \
                                             .order_by('-progress', '-speed', 'time')
        return context


class CreateRoom(LoginRequiredMixin, TitleMixin, CreateView):
    model = TypoRoom
    template_name: str = 'typeracer/create_room.html'
    title = _('Create Room')
    form_class = CreateRoomForm

    def get_success_url(self):
        return reverse('typeracer:room_detail', args=(self.object.id, ))


class JoinRoom(LoginRequiredMixin, RoomMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile: Profile = request.profile
        rooms = profile.rooms.all()
        if profile.rooms.all().count() > 0 and (self.object != rooms.first().room):
            return generic_message(request, 'Can\'t join room', 'You are in %s' % profile.rooms.room.pk, 403)
        if profile.rooms.all().count() > 0 and self.object == rooms.first().room:
            return HttpResponseRedirect(reverse('typeracer:room_detail', args=(self.object.id, )))
        room: TypoRoom = self.object
        if room.is_private and room.access_code != request.POST.get('access_code'):
            return generic_message(request, 'Can\'t join room', 'Access code is wrong', 403)

        # Create new Room user
        participant = TypoRoomUser(room=room, user=profile)
        participant.save()
        return HttpResponseRedirect(reverse('typeracer:room_detail', args=(room.id, )))


@method_decorator(never_cache, name='dispatch')
class SoloRoomList(ListView):
    model = TypoRoom
    context_object_name = 'rooms'
    template_name: str = 'typeracer/rooms.html'

    def get_queryset(self):
        return TypoRoom.objects.filter(mode='solo')


@method_decorator(never_cache, name='dispatch')
class MultiRoomList(ListView):
    model = TypoRoom
    context_object_name = 'rooms'
    template_name: str = 'typeracer/rooms.html'

    def get_queryset(self):
        # print(TypoRoom.objects.filter(mode='solo').count())
        return TypoRoom.objects.filter(mode='multi')


def participate(request, pk):
    room = TypoRoom.objects.get(pk=pk)
    profile = request.profile
    if room != profile.rooms.all().first().room:
        return JsonResponse({
            'result': 'You are not in this room',
            'status': 403,
        })

    user = profile.rooms.get(room=room)
    user.action = '0'
    user.save()

    async_to_sync(channel_layer.group_send)(
        'room_%s' % pk,
        {
            'type': 'change.user',
            'message': 'participant'
        },
    )

    return JsonResponse({
        'result': 'Change to participant success',
        'status': 200,
    })


def spectate(request, pk):
    room = TypoRoom.objects.get(pk=pk)
    profile = request.profile
    if room != profile.rooms.all().first().room:
        return JsonResponse({
            'result': 'You are not in this room',
            'status': 403,
        })

    user = profile.rooms.get(room=room)
    user.action = '1'
    user.save()

    async_to_sync(channel_layer.group_send)(
        'room_%s' % pk,
        {
            'type': 'change.user',
            'message': 'spectator'
        },
    )

    return JsonResponse({
        'result': 'Change to spectator success',
        'status': 200,
    })


@method_decorator(never_cache, name='dispatch')
class RoomInfo(RoomMixin, DetailView):
    template_name: str = 'typeracer/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participations = TypoRoomUser.objects.filter(room=self.object)
        context['participants'] = list(participations.filter(action='0'))
        context['spectators'] = list(participations.filter(action='1'))
        return context


class CreateContest(LoginRequiredMixin, RoomMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not request.user.is_superuser:
            raise Http404()
        
        contest = get_random_contest()
        self.object.contest = contest
        self.object.save()
    
        async_to_sync(channel_layer.group_send)(
            'room_%s' % self.object.pk,
            {
                'type': 'start.typo',
                'message': 'Typo contest start',
            },
        )
        return HttpResponseRedirect(reverse('typeracer:room_detail', args=(self.object.pk, )))


@method_decorator(never_cache, name='dispatch')
class Contest(LoginRequiredMixin, TitleMixin, RoomMixin, DetailView):
    template_name: str = 'typeracer/contest.html'
    title = _('Typo Contest')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contest'] = self.object.contest
        context['participant'] = self.user
        context['contestants'] = TypoResult.objects.filter(contest=self.object.contest)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = request.profile

        self.user = get_object_or_404(TypoRoomUser, room=self.object, user=profile)
        if self.user.action == '2':
            return HttpResponseRedirect(reverse('typeracer:room_detail', args=(self.object.id, )))
        
        TypoResult.objects.get_or_create(
            user=self.user.user,
            contest=self.object.contest,
        )

        return super().get(request, *args, **kwargs)


class LeaveRoom(LoginRequiredMixin, RoomMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile: Profile = request.profile
        room = TypoRoomUser.objects.filter(room=self.object, user=profile)
        if room.count() == 0:
            return generic_message(request, 'You isn\'t in this room')
        # Create new Room user
        participant = room.first()
        participant.delete()
        return HttpResponseRedirect(reverse('typeracer:list_room'))
