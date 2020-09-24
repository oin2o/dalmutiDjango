from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


#웹소켓 class instance를 만듦
class dalmuti_consumer(WebsocketConsumer):

    # websocket이 연결 되었을 때
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['gamename']
        self.game_group_name = 'game_dalmuti_%s' % self.game_name

        # 그룹에 Join 하는 메서드이다.
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    # 연결이 끊어졌을 때
    def disconnect(self, close_code):
        # 그룹을 leave 하는 메서드이다.
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지를 받아 처리하는 부분이다.
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 그룹으로 메세지를 돌려보내주는 부분이다.
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    # 위의 receive 메서드에서 그룹으로 메세지를 보내면 그 메세지를 받아 처리하는 부분이다.
    def game_message(self, event):
        message = event['message']

        # 클라이언트로 웹소켓을 통해 받은 메세지를 다시 보내주는 부분이다.
        self.send(text_data=json.dumps({
            'message': message
        }))
