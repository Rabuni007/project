import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def get_basic_auth():
    return (settings.SAP_USERNAME, settings.SAP_PASSWORD)

def sync_distributor(distributor):
    """
    Sync distributor data with SAP OData service using Basic Auth.
    """
    try:
        url = f"{settings.SAP_API_URL}/Distributors"
        distributor_data = {
            "ID": distributor.id,
            "Name": distributor.name,
            "Address": distributor.address,
            # Add other fields as needed
        }
        response = requests.post(url, json=distributor_data, auth=get_basic_auth())
        response.raise_for_status()
        logger.info(f"Distributor synced to SAP: {distributor.id}")
    except Exception as e:
        logger.error(f"Failed to sync distributor {distributor.id} to SAP: {e}")

def sync_payment(payment):
    """
    Sync payment data with SAP OData service using Basic Auth.
    """
    try:
        url = f"{settings.SAP_API_URL}/Payments"
        payment_data = {
            "ID": payment.id,
            "DistributorID": payment.distributor.id if payment.distributor else None,
            "Amount": payment.amount,
            "Status": payment.status,
            # Add other fields as needed
        }
        response = requests.post(url, json=payment_data, auth=get_basic_auth())
        response.raise_for_status()
        logger.info(f"Payment synced to SAP: {payment.id}")
    except Exception as e:
        logger.error(f"Failed to sync payment {payment.id} to SAP: {e}")
