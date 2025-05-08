import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def confirm_payment_cashfree(payment_id, payment_details):
    """
    Confirm payment with Cashfree payment gateway.

    Integration Approach:
    - Use Cashfree's Payment Verification API to confirm payment status.
    - Send payment_id and other required details to Cashfree API.
    - Verify the response to ensure payment is successful.
    - Return True if payment confirmed, False otherwise.

    Args:
        payment_id (str): The payment identifier from Cashfree.
        payment_details (dict): Additional payment details if needed.

    Returns:
        bool: True if payment is confirmed, False otherwise.
    """
    try:
        url = settings.CASHFREE_PAYMENT_VERIFY_URL
        headers = {
            'Content-Type': 'application/json',
            'x-api-version': '2022-01-01',
            'x-client-id': settings.CASHFREE_CLIENT_ID,
            'x-client-secret': settings.CASHFREE_CLIENT_SECRET,
        }
        payload = {
            'paymentId': payment_id,
            # Add other required fields from payment_details if needed
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'SUCCESS':
            logger.info(f"Payment {payment_id} confirmed by Cashfree.")
            return True
        else:
            logger.warning(f"Payment {payment_id} not confirmed by Cashfree: {data}")
            return False
    except Exception as e:
        logger.error(f"Error confirming payment {payment_id} with Cashfree: {e}")
        return False
