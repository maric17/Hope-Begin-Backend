from rest_framework.throttling import AnonRateThrottle

class StrictPublicFormThrottle(AnonRateThrottle):
    """
    Stricter throttle for public form submissions.
    """
    scope = 'public_form'
