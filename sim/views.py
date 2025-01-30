
# Create your views here.
from core.utils import hash_message # for hashing messages
from django.http import JsonResponse

from datetime import datetime
import asyncio

from typing import AsyncGenerator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse, JsonResponse
from . import models
import json
import random
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def chat(request: HttpRequest) -> HttpResponse:
    return render(request, 'chat.html')

@login_required
def create_message(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content", "").strip()
    client_hash = request.POST.get("hash")
    username = request.user.username

    # debug
    #print(f"Received content: {content}")
    #print(f"Received hash: {client_hash}")
    #print(f"Logged in user: {username}")

    if not username:
        return HttpResponse(status=403)
    author, _ = models.Author.objects.get_or_create(name=username)

    if content and client_hash:
        server_hash = hash_message(content)
        print(f"Server hash: {server_hash}")

        if server_hash != client_hash:
            return JsonResponse({"error": "Message integrity check failed."}, status=400)

        models.Message.objects.create(author=author, content=content)
        print("Message saved successfully.")
        return HttpResponse(
            json.dumps({"message": "Message saved successfully."}),
            status=201,
        )
    else:
        return JsonResponse({"error": "Content or hash is missing."}, status=400)


async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as we create messages.
    """
    async def event_stream():
        """
        We use this function to send a continuous stream of data 
        to the connected clients.
        """
        # Start with existing messages
        async for message in get_existing_messages():
            yield message

        last_id = await get_last_message_id()
        last_checked_time = datetime.now()  # Keep track of the last check time

        # Continuously check for both new and edited messages
        while True:
            # Fetch messages that are either new or modified
            new_and_edited_messages = models.Message.objects.filter(
                Q(id__gt=last_id) | Q(updated_at__gt=last_checked_time)
            ).order_by('created_at').values('id', 'author__name', 'content', 'updated_at')

            async for message in new_and_edited_messages:
                # Convert datetime to string before serializing to JSON
                message['updated_at'] = message['updated_at'].isoformat() if message['updated_at'] else None
                #print("Making message")
                if message.get('file'):
                    print("Found a file!!")
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
                last_checked_time = message['updated_at']
            await asyncio.sleep(0.1)

    async def get_existing_messages() -> AsyncGenerator:
        messages = models.Message.objects.all().order_by('created_at').values(
            'id', 'author__name', 'content', 'file'
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id() -> int:
        last_message = await models.Message.objects.all().alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

@login_required
def delete_message(request, message_id):
    try:
        # Get the message
        message = get_object_or_404(models.Message, id=message_id)
        
        # Check if the user is the author (by name), or has staff or superuser privileges
        if message.author.name != request.user.username and not (request.user.is_staff or request.user.is_superuser):
            return JsonResponse({"error": "You don't have permission to delete this message."}, status=403)
        
        # Delete the message
        message.delete()

        # Send a signal for deletion (this will be handled on the client-side)
        return JsonResponse({"success": True, "message_id": message_id, "deleted": True})
    except models.Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

@login_required
def edit_message(request, message_id):
    print("Editing message!")
    print(f"Message ID: {message_id}")
    print(f"User: {request.user.username}")
    
   # Get the message
    message = get_object_or_404(models.Message, id=message_id)
    print(f"Message before edit: {message.content}")
    
    # Check if the user is the author, a staff member, or a superuser
    if message.author.name != request.user.username and not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({"success": False, "error": "You do not have permission to edit this message"})
    
    if request.method == 'POST':
        try:
            new_content = json.loads(request.body).get('content', '').strip()
            print(f"Received new content: {new_content}")
            
            if new_content:
                # Update message content
                message.content = new_content
                message.save()

                # Update `updated_at` timestamp for SSE detection
                message.updated_at = datetime.now()
                message.save()
                print(f"Message after edit: {message.content}")

                return JsonResponse({"success": True, "content": new_content})
            else:
                return JsonResponse({"success": False, "error": "Content cannot be empty"})
        except Exception as e:
            print(f"Error parsing request body: {e}")
            return JsonResponse({"success": False, "error": "Invalid data"})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})@login_required

def upload_file(request: HttpRequest) -> JsonResponse:
    """
    Handles file uploads for chat messages.
    """
    if request.method == "POST":
        file = request.FILES.get('file')
        content = request.POST.get('content', '')  # Optional message content
        sender = request.user  # Assuming user authentication

        # Save the message with the file
        if file:
            #print(f"File uploaded: {file.url}")
            chat_message = models.Message.objects.create(
                author=models.Author.objects.get_or_create(name=sender.username)[0],
                file=file,  # Assuming the Message model has a FileField named `file`
                content=file.name
            )
            # Print the URL of the uploaded file for debugging purposes
            print(f"File URL: {chat_message.file.url}")

            # Return the full URL
            full_file_url = request.build_absolute_uri(chat_message.file.url)

            return JsonResponse({'message': 'File uploaded successfully!', 'file_url': full_file_url})
        
        return JsonResponse({'error': 'No file uploaded.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)