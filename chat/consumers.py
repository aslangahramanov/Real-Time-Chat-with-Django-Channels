import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
import random
from .models import Person, Interest
import time

from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name = 'chat'
    person_id = None
    is_matched = False
    
    async def connect(self):
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.disconnect_person(self.person_id)
        
        if self.room_group_name != 'chat':
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        else:
            await self.set_on_chat_false(self.person_id)
        
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'person.offline',
                    'user_id': self.person_id,
                    'offline': True,
                    'find_person': True
                }
        )
        
        
    async def person_offline(self, event):
        user_id = event["user_id"]
        offline = event["offline"]
        find_person = event["find_person"]
        await self.send(text_data=json.dumps({
            'type': 'offline',
            'user_id': user_id,
            'offline': offline,
            'find_person': find_person
        }))
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json["action_type"]
        
        if action_type == 'match_persons':
            user_id = text_data_json["user_id"]
            person_interest = text_data_json["person_interest"]
            await self.update_interest(person_interest, user_id)
            person = await self.get_person(user_id)
            person_interests = await self.get_person_interests(user_id)
            count_down = 0
            
            if person:
                while True:
                    matched_users = await self.get_matched_users(person_interests, person.unique_id)
                    
                    if count_down == 10:
                        self.is_matched = False
                        break
                    
                                
                    if len(matched_users) == 2:
                        sorted_users = sorted(matched_users)
                        room_group_name = f"private_chat_{sorted_users[0]}_{sorted_users[1]}"
                        print(self.room_group_name)
                        self.room_group_name = room_group_name
                        if self.room_group_name not in self.groups:
                            print(self.room_group_name)
                            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                        for matched_user in matched_users:
                            await self.set_on_chat_true(matched_user)
                        
                        break
                    else:
                        time.sleep(1)
                        count_down += 1
                        continue


        elif action_type == 'rematch_persons':
            print("REMATCH")
            user_id = text_data_json["user_id"]
            person_interest = text_data_json["person_interest"]
            person = await self.get_person(user_id)
            person_interests = await self.get_person_interests(user_id)
            count_down = 0  
            print(user_id, person, person_interests)
            if person:
                while True:      
                    matched_users = await self.get_matched_users(person_interests, person.unique_id)
                    print(matched_users)
                    if count_down == 10:
                        print("BREAK")
                        self.is_matched = False
                        break
                    
                                
                    if len(matched_users) == 2:
                        print("LEN")
                        sorted_users = sorted(matched_users)
                        new_room_group_name = f"private_chat_{sorted_users[0]}_{sorted_users[1]}"
                        print(self.room_group_name)
                        print(new_room_group_name)
                        
                        if self.room_group_name not in self.groups:
                            if new_room_group_name != self.room_group_name:
                                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  # Mevcut odadan çık
                                self.room_group_name = new_room_group_name
                                await self.channel_layer.group_add(self.room_group_name, self.channel_name)      # Yeni odaya katıl

                        for matched_user in matched_users:
                            await self.set_on_chat_true(matched_user)
                        
                        
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'person.online',
                                'user_id': self.person_id,
                                'online': True,
                                'find_person': False
                            }
                        )
                        
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
            print(self.room_group_name)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'user_id': user_id
            }
        )
            
        elif action_type == 'writing_start':
            user_id = text_data_json["user_id"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.user_writing',
                    'user_id': user_id,
                    'writing': True,
                }
        )
            
            
        elif action_type == 'writing_end':
            user_id = text_data_json["user_id"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.user_writing',
                    'user_id': user_id,
                    'writing': False
                }
        )
        
        elif action_type == 'send_image':
            user_id = text_data_json["user_id"]
            image_url = text_data_json["image_url"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.send_image_message',
                    'user_id': user_id,
                    'image_url': image_url
                }
            )
            
            
        elif action_type == 'discard_room':
            print("DISCARD ROOM")
            user_id = text_data_json["user_id"]
            print(user_id)
            if self.room_group_name != 'chat':
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                await self.set_on_chat_false(user_id)
            
         
         
    async def person_online(self, event):
        user_id = event["user_id"]
        online = event["online"]
        find_person = event["find_person"]
        await self.send(text_data=json.dumps({
            'type': 'online',
            'user_id': user_id,
            'online': online,
            'find_person': find_person
        }))
            
            
    async def chat_user_writing(self, event):
        user_id = event["user_id"]
        writing = event["writing"]
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'writing': writing,
            'type': 'writing_status',
        }))
            
       

            
    async def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        await self.send(text_data=json.dumps({
                'message': message,
                'sender': user_id,
                'type': 'send_message'
            }))
    
    
    async def chat_send_image_message(self, event):
        user_id = event["user_id"]
        image_url = event["image_url"]
        await self.send(text_data=json.dumps({
            'sender': user_id,
            'image_url': image_url,
            'type': 'send_image'
        }))
  



    @database_sync_to_async
    def set_on_chat_true(self, id):
        Person.objects.filter(unique_id=id).update(on_chat=True)
        
        
    @database_sync_to_async
    def set_on_chat_false(self, id):
        Person.objects.filter(unique_id=id).update(on_chat=False)



    @database_sync_to_async
    def get_matched_users(self, interests_list, user_id):
        matched_list = []
        matched_users = Person.objects.filter(
            interests__title__in=interests_list,
            on_chat=False
            ).exclude(unique_id=user_id)
        if matched_users:
            random_user = random.choice(matched_users)
            matched_list.append(random_user.unique_id)
            matched_list.append(user_id)
            self.is_matched = True
        else:
            matched_list.append(user_id)
            self.is_matched = True
            
        
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
            valueList = value.split(",")
            for value in valueList:
                interest, created = Interest.objects.get_or_create(title=value)
                interest = Interest.objects.get(title=value)
                person.interests.add(interest)
        except Person.DoesNotExist:
            pass
        
    @database_sync_to_async
    def get_person(self, id):
        try:
            return Person.objects.get(unique_id=id)
        except Person.DoesNotExist:
            return None
        
        
        
    @database_sync_to_async
    def get_person_interests(self, id):
        try:
            return list(Person.objects.get(unique_id=id).interests.all())
        except Person.DoesNotExist:
            return None