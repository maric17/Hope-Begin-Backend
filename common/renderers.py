from rest_framework.renderers import JSONRenderer

class BaseJSONRenderer(JSONRenderer):
    """
    Standardizes all API responses to:
    {
        "status": bool,
        "message": str,
        "data": any
    }
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        
        # Determine status
        status = True if response.status_code < 400 else False
        
        # Determine message
        # You can customize this if you want specific messages for certain status codes
        message = "success" if status else "error"
        
        # If the view set a custom message on the response object, use it
        if hasattr(response, 'message'):
            message = response.message
        elif not status:
            # For errors, we can use the status text as a fallback message
            message = response.status_text

        # Create the standard response envelope
        envelope = {
            'status': status,
            'message': message,
            'data': data
        }

        return super().render(envelope, accepted_media_type, renderer_context)
