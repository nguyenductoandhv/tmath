from django.urls import include, path

from typeracer.views import (Contest, CreateContest, CreateRoom, JoinRoom,
                             LeaveRoom, MultiRoomList, Racer, Ranking,
                             RoomDetail, RoomInfo, SoloRoomList, TypoRoomList,
                             finishTypoContest, getQuote, participate,
                             spectate, updateProgress)

app_name = 'typeracer'

urlpatterns = [
    path('rooms/', TypoRoomList.as_view(), name='list_room'),
    path('asdawdadsa/', updateProgress, name='update_progress'),
    path('new_user/', Racer.as_view(), name="new_user"),
    path('finish/', finishTypoContest, name='finish_contest'),
    path('room/<int:pk>', include([
        path('/', RoomDetail.as_view(), name='room_detail'),
        path('/join', JoinRoom.as_view(), name='join_room'),
        path('/leave', LeaveRoom.as_view(), name='leave_room'),
        path('/getquote', getQuote, name="get_quote"),
        path('/participate', participate, name="participate"),
        path('/spectate', spectate, name="spectate"),
        path('/info', RoomInfo.as_view(), name="get_info"),
        path('/contest', Contest.as_view(), name="contest"),
        path('/create,', CreateContest.as_view(), name="create_contest"),
        # url(r'^/ranking$', ),
    ])),
    path('contest/<int:pk>', include([
        path('/rank', Ranking.as_view(), name="typo_ranking"),
    ])),
    path('solorooms/', SoloRoomList.as_view(), name='list_solo_room'),
    path('multirooms/', MultiRoomList.as_view(), name='list_multi_room'),
    path('create/', CreateRoom.as_view(), name='create_room'),
]
