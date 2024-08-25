# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Determine the type of message
        message_type = text_data_json.get('type')

        if message_type == 'chat_message':
            message = text_data_json['message']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        elif message_type == 'webrtc_offer':
            offer = text_data_json['offer']
            # Send WebRTC offer to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': offer
                }
            )
        elif message_type == 'webrtc_answer':
            answer = text_data_json['answer']
            # Send WebRTC answer to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': answer
                }
            )
        elif message_type == 'ice_candidate':
            candidate = text_data_json['candidate']
            # Send ICE candidate to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice_candidate',
                    'candidate': candidate
                }
            )

    async def chat_message(self, event):
        message = event['message']
        # Send chat message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    async def webrtc_offer(self, event):
        offer = event['offer']
        # Send WebRTC offer to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'webrtc_offer',
            'offer': offer
        }))

    async def webrtc_answer(self, event):
        answer = event['answer']
        # Send WebRTC answer to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'webrtc_answer',
            'answer': answer
        }))

    async def ice_candidate(self, event):
        candidate = event['candidate']
        # Send ICE candidate to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'ice_candidate',
            'candidate': candidate
        }))
