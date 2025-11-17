from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ContactMessage


def home(request):
    return render(request, 'login.html')


@csrf_exempt
@require_http_methods(["POST"])
def submit_message(request):
    """POST /api/submit - Submit new message"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({
                'message': 'All fields are required.'
            }, status=400)

        # Save to database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return JsonResponse({
            'message': f'Thank you, {name.title()}! Your message has been received.',
            'id': contact_message.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'message': f'Error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_messages(request):
    """GET /api/messages - Retrieve all messages"""
    try:
        messages = ContactMessage.objects.all()
        messages_list = [{
            'id': msg.id,
            'name': msg.name,
            'email': msg.email,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]

        return JsonResponse({
            'messages': messages_list,
            'count': len(messages_list)
        })
    except Exception as e:
        return JsonResponse({
            'message': f'Error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_message(request, message_id):
    """DELETE /api/delete/<id> - Remove a message"""
    try:
        message = ContactMessage.objects.get(id=message_id)
        message.delete()

        return JsonResponse({
            'message': 'Message deleted successfully.',
            'id': message_id
        })
    except ContactMessage.DoesNotExist:
        return JsonResponse({
            'message': 'Message not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'message': f'Error: {str(e)}'
        }, status=500)