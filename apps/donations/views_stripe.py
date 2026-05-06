import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import Donation

logger = logging.getLogger(__name__)

# Set Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(views.APIView):
    """
    Creates a Stripe Checkout Session for a donation.
    Supports One-time and Monthly donations.
    Calculates fees if the donor opts to cover them.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            amount = request.data.get('amount')
            donation_type = request.data.get('donation_type', 'ONE_TIME') # ONE_TIME or MONTHLY
            covers_fee = request.data.get('covers_fee', False)
            donor_name = request.data.get('name', 'Anonymous')
            donor_email = request.data.get('email')

            if not amount:
                return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                base_amount = float(amount)
                if base_amount <= 0:
                    raise ValueError
            except ValueError:
                return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

            # Stripe Fee Calculation (Approx 2.9% + 15 PHP - using a simplified formula for PH)
            # Standard Stripe PH fee is 3.5% + 15 PHP for international, 
            # but let's use the standard 2.9% + 15 PHP or similar logic.
            # Formula: (base_amount + fixed_fee) / (1 - percentage_fee)
            fee = 0
            total_amount = base_amount
            
            if covers_fee:
                # PH standard for international cards is often higher, 
                # but for simplicity we use 3.5% + 15 PHP as a safe margin for PH Stripe users
                percentage = 0.035
                fixed = 15.0
                total_amount = (base_amount + fixed) / (1 - percentage)
                fee = total_amount - base_amount

            # Create a pending donation record to track the intent
            donation = Donation.objects.create(
                name=donor_name,
                email=donor_email,
                amount=base_amount,
                covered_fee=fee,
                donation_type=donation_type,
                status='PENDING'
            )

            # Prepare Stripe Session Data
            session_data = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price_data': {
                        'currency': 'php',
                        'product_data': {
                            'name': f'Hope Seed Donation - {donation_type.replace("_", " ").title()}',
                            'description': 'Your support helps us reach more people with hope.',
                        },
                        'unit_amount': int(round(total_amount * 100)), # Cents
                    },
                    'quantity': 1,
                }],
                'mode': 'payment' if donation_type == 'ONE_TIME' else 'subscription',
                'success_url': settings.FRONTEND_URL + '/give-hope/success?session_id={CHECKOUT_SESSION_ID}',
                'cancel_url': settings.FRONTEND_URL + '/give-hope?cancelled=true',
                'metadata': {
                    'donation_id': str(donation.id)
                }
            }

            # Handle Recurring (Monthly)
            if donation_type == 'MONTHLY':
                session_data['line_items'][0]['price_data']['recurring'] = {'interval': 'month'}
            
            if donor_email:
                session_data['customer_email'] = donor_email

            checkout_session = stripe.checkout.Session.create(**session_data)

            # Update donation with session ID
            donation.stripe_session_id = checkout_session.id
            donation.save()

            return Response({'checkout_url': checkout_session.url})

        except stripe.error.StripeError as e:
            logger.error(f"Stripe Error: {str(e)}")
            return Response({'error': 'Stripe processing error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected Donation Error: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def stripe_webhook(request):
    """
    Webhook handler for Stripe events.
    Verifies signature and updates donation status on success.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not sig_header or not endpoint_secret:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle completion events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        donation_id = session.get('metadata', {}).get('donation_id')
        
        if donation_id:
            try:
                donation = Donation.objects.get(id=donation_id)
                donation.status = 'COMPLETED'
                donation.stripe_payment_intent_id = session.get('payment_intent')
                # If subscription, payment_intent is null, session has 'subscription' id
                if not donation.stripe_payment_intent_id:
                    donation.stripe_payment_intent_id = session.get('subscription')
                donation.save()
                logger.info(f"Donation {donation_id} successfully marked as COMPLETED via webhook.")
            except Donation.DoesNotExist:
                logger.error(f"Donation ID {donation_id} not found during webhook processing.")

    return HttpResponse(status=200)
