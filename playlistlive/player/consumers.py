from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room
import json
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.channel_name)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'DJRoom_%s' % self.room_name

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await(self.accept())

        print("Joining a room... send a message to DJ...")
        print("socket id: ", self.channel_name)
        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "init_player",
                'new_socket': self.channel_name
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("recived!")
        print("text_data received: ", text_data)
        if(text_data is None):
            return
        
        text_data_json = json.loads(text_data)
        
        if(text_data_json["msg_type"]=="chatting"):
            message = text_data_json['message']
            print(message)
            await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatting',
                'message': message
            }
            )
            return
        
        if (text_data_json["msg_type"]=="pause"):
            print("recieved pause mesage")
            # await self.send(text_data=text_data)
            # await(self.channel_layer.group_send)(self.room_group_name, text_data)
            await(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': "play_pause",
                    'state': text_data
                }
            )
            return

        elif (text_data_json["msg_type"]=="resume"):
            # await self.send(text_data=text_data)
            # await(self.channel_layer.group_send)(self.room_group_name, text_data)
            await(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': "play_pause",
                    'state': text_data
                }
            )
            return


        else:

            text_data_json = json.loads(text_data)

            # new socket current state message
            if (text_data_json['msg_type'] == 'new_socket'):
                print("new socket got current song info")
                
                uri = text_data_json['uris']
                pos = text_data_json['position_ms']
                queue = text_data_json['queue']                

                # Send message to room group
                await(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': "new_socket",
                        'uris': uri,
                        'queue': queue,
                        'position_ms': pos,
                        'socket_id': text_data_json['socket_id']
                    }
                )
                return


            if (text_data_json['msg_type']=='queue'):
                print("new socket got current queue info")
                queue = text_data_json['queue']
                await(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': "queue",
                        'queue': queue
                    }
                )
                return 

            # normal current state message
            # else:

            uri = text_data_json['uris']
            pos = text_data_json['position_ms']
            # queue = text_data_json['queue']

            # Send message to room group
            await(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': "chat_message",
                    'uris': uri,
                    # 'queue': queue,
                    'position_ms': pos,
                    'socket_id': None,
                }
            )

    async def chatting(self, event):
        
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type': 'chatting',
            'message': message
        }))

    # Receive state message from room group
    async def chat_message(self, event):
        print("recieved message from room group")

        print("chat_message received...", event)
        uri = event['uris']
        pos = event['position_ms']
        socket_id = event['socket_id']

        if (socket_id == None):
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'uris': uri,
                'position_ms' : pos
            }))
        
        elif (socket_id == self.channel_name):
            print("sending song info to itself", uri, pos)
            await self.send(text_data=json.dumps({
                'uris': uri,
                'position_ms' : pos,
            }))
    
        # Receive state message from room group
    async def new_socket(self, event):

        uri = event['uris']
        pos = event['position_ms']
        socket_id = event['socket_id']
        queue = event['queue']

        if (socket_id == None):
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'uris': uri,
                'position_ms' : pos
            }))
        
        elif (socket_id == self.channel_name):
            print("sending song info to itself", uri, pos)
            await self.send(text_data=json.dumps({
                'uris': uri,
                'position_ms' : pos,
                'queue': queue
            }))


    async def queue(self, event):
        print("queue event recieve: ", event)
        queue = event['queue']
        await self.send(text_data=json.dumps({
            'msg_type': 'queue',
            'queue': queue
        }))

    
    async def play_pause(self, event):
        print("event received: ", event)
        data = json.loads(event['state'])
        print(data['msg_type'])
        await self.send(text_data=data['msg_type'])

    async def init_player(self, event):

        print("init_player received...", event)
        
        new_socket = event['new_socket']
        print("prompted init_player", new_socket)
        await self.send(text_data=json.dumps({
            'msg_type': 'new_socket',
            'socket_id': new_socket
        }))

"""
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chatRoom = ChatRoom.objects.get(name=self.room_name.lower())
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        Message.objects.create(chatRoom=self.chatRoom,message=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

"""