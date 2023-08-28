import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
import random
from .models import Person
import time

from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name = 'chat'
    person_id = None
    
    async def connect(self):
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.disconnect_person(self.person_id)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json["action_type"]
        
        if action_type == 'match_persons':
            user_id = text_data_json["user_id"]
            person_interest = text_data_json["person_interest"]

            await self.update_interest(person_interest, user_id)
            person = await self.get_person(user_id)
            count_down = 0
            
            if person:
                while True:        
                    matched_users = await self.get_matched_users(person.interests, person.unique_id)
                    
                    if count_down == 10:
                        break
                    
                                
                    if len(matched_users) == 2:
                        sorted_users = sorted(matched_users)
                        self.room_group_name = f"private_chat_{sorted_users[0]}_{sorted_users[1]}"
                        if self.room_group_name not in self.groups:
                            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                        for matched_user in matched_users:
                            await self.set_on_chat_true(matched_user)
                        
                        break
                    else:
                        time.sleep(1)
                        count_down += 1
                        continue


        elif action_type == 'insert_app':
            user_id = text_data_json["user_id"]
            self.person_id = user_id
            await self.connect_person(user_id)
            
            
        elif action_type == 'on_chat':
            message = text_data_json['message']
            user_id = text_data_json["user_id"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'user_id': user_id
            }
    )

            
    async def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        await self.send(text_data=json.dumps({
                'message': message,
                'sender': user_id
            }))



    @database_sync_to_async
    def set_on_chat_true(self, id):
        Person.objects.filter(unique_id=id).update(on_chat=True)



    @database_sync_to_async
    def get_matched_users(self, interests, user_id):
        matched_list = []
        matched_users = list(Person.objects.filter(
            interests=interests,
            on_chat=False
        ).exclude(unique_id=user_id))
        if matched_users:
            random_user = random.choice(matched_users)
            matched_list.append(random_user.unique_id)
            matched_list.append(user_id)
        else:
            matched_list.append(user_id)
        
        return matched_list
        


    @database_sync_to_async
    def connect_person(self, id):
        if not Person.objects.filter(unique_id=id).exists():
            person = Person.objects.create(unique_id=id) 
            person.save()
        
    @database_sync_to_async
    def disconnect_person(self, id):
        try:
            person = Person.objects.get(unique_id=id)
            person.delete()
        except Person.DoesNotExist:
            pass



    @database_sync_to_async
    def update_interest(self, value, id):
        try:
            person = Person.objects.get(unique_id=id)
            person.interests = value
            person.save()
        except Person.DoesNotExist:
            pass
        
    @database_sync_to_async
    def get_person(self, id):
        try:
            return Person.objects.get(unique_id=id)
        except Person.DoesNotExist:
            return None