"""
Vipps Payment Integration for Norwegian Market
Complete mobile payment solution for Norway
"""
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from loguru import logger
from pydantic import BaseModel
import base64


# ============================================================================
# VIPPS CONFIGURATION
# ============================================================================

class VippsConfig(BaseModel):
    """Vipps API configuration"""
    merchant_serial_number: str
    client_id: str
    client_secret: str
    subscription_key: str
    environment: str = "test"  # test or production

    @property
    def base_url(self) -> str:
        """Get base URL based on environment"""
        if self.environment == "production":
            return "https://api.vipps.no"
        return "https://apitest.vipps.no"


# ============================================================================
# VIPPS PAYMENT MANAGER
# ============================================================================

class VippsPaymentManager:
    """
    Vipps Payment Integration

    Supports:
    - One-time payments (eCom)
    - Recurring payments (subscriptions)
    - QR code payments
    - Mobile app integration
    """

    def __init__(self, config: VippsConfig):
        self.config = config
        self.access_token = None
        self.token_expires = None

    async def get_access_token(self) -> str:
        """Get Vipps access token"""
        if self.access_token and self.token_expires and datetime.now() < self.token_expires:
            return self.access_token

        try:
            url = f"{self.config.base_url}/accesstoken/get"
            headers = {
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "Ocp-Apim-Subscription-Key": self.config.subscription_key
            }

            response = requests.post(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            self.access_token = data["access_token"]
            self.token_expires = datetime.now() + timedelta(seconds=data.get("expires_in", 3600) - 60)

            logger.info("Vipps access token obtained successfully")
            return self.access_token

        except Exception as e:
            logger.error(f"Failed to get Vipps access token: {str(e)}")
            raise

    def _get_headers(self, token: str, idempotency_key: Optional[str] = None) -> Dict:
        """Get standard Vipps API headers"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Ocp-Apim-Subscription-Key": self.config.subscription_key,
            "Merchant-Serial-Number": self.config.merchant_serial_number,
            "Content-Type": "application/json"
        }

        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        return headers

    # ========================================================================
    # ECOM PAYMENTS (One-time)
    # ========================================================================

    async def initiate_payment(
        self,
        amount: int,  # In øre (1 NOK = 100 øre)
        phone_number: str,  # Norwegian mobile number
        order_id: str,
        transaction_text: str,
        callback_url: Optional[str] = None,
        fallback_url: Optional[str] = None,
        shipping_details: Optional[Dict] = None,
        static_shipping: Optional[Dict] = None
    ) -> Dict:
        """
        Initiate Vipps payment

        Args:
            amount: Amount in øre (100 øre = 1 NOK)
            phone_number: Customer phone number (Norwegian format)
            order_id: Unique order ID
            transaction_text: Description shown to customer
            callback_url: URL for payment status callbacks
            fallback_url: URL to redirect after payment
            shipping_details: Optional shipping information
            static_shipping: Optional static shipping cost

        Returns:
            Payment initiation response with deeplink URL
        """
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/ecomm/v2/payments"
            headers = self._get_headers(token)

            payload = {
                "customerInfo": {
                    "mobileNumber": phone_number
                },
                "merchantInfo": {
                    "merchantSerialNumber": self.config.merchant_serial_number,
                    "callbackPrefix": callback_url or "",
                    "fallBack": fallback_url or f"https://mindframe.no/payment/status/{order_id}",
                    "paymentType": "eComm Express Payment"
                },
                "transaction": {
                    "orderId": order_id,
                    "amount": amount,
                    "transactionText": transaction_text,
                    "timeStamp": datetime.now().isoformat()
                }
            }

            if shipping_details:
                payload["merchantInfo"]["shippingDetails"] = shipping_details

            if static_shipping:
                payload["merchantInfo"]["staticShippingDetails"] = static_shipping

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Vipps payment initiated: {order_id} for {amount/100} NOK")

            return {
                "order_id": order_id,
                "url": data.get("url"),  # Deeplink URL for Vipps app
                "amount": amount / 100,  # Convert back to NOK
                "currency": "NOK",
                "status": "initiated"
            }

        except Exception as e:
            logger.error(f"Vipps payment initiation failed: {str(e)}")
            raise

    async def get_payment_details(self, order_id: str) -> Dict:
        """Get payment status and details"""
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/ecomm/v2/payments/{order_id}/details"
            headers = self._get_headers(token)

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            return {
                "order_id": order_id,
                "status": data.get("transactionInfo", {}).get("status"),
                "amount": data.get("transactionInfo", {}).get("amount", 0) / 100,
                "transaction_id": data.get("transactionInfo", {}).get("transactionId"),
                "timestamp": data.get("transactionInfo", {}).get("timeStamp")
            }

        except Exception as e:
            logger.error(f"Failed to get Vipps payment details: {str(e)}")
            raise

    async def capture_payment(
        self,
        order_id: str,
        amount: int,  # In øre
        transaction_text: str
    ) -> Dict:
        """
        Capture reserved payment

        Vipps uses reserve-capture flow
        """
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/ecomm/v2/payments/{order_id}/capture"
            headers = self._get_headers(token)

            payload = {
                "merchantInfo": {
                    "merchantSerialNumber": self.config.merchant_serial_number
                },
                "transaction": {
                    "amount": amount,
                    "transactionText": transaction_text
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Vipps payment captured: {order_id} for {amount/100} NOK")

            return {
                "order_id": order_id,
                "transaction_id": data.get("transactionInfo", {}).get("transactionId"),
                "status": data.get("transactionInfo", {}).get("status"),
                "amount": amount / 100
            }

        except Exception as e:
            logger.error(f"Vipps payment capture failed: {str(e)}")
            raise

    async def cancel_payment(self, order_id: str, transaction_text: str) -> Dict:
        """Cancel/void a reserved payment"""
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/ecomm/v2/payments/{order_id}/cancel"
            headers = self._get_headers(token)

            payload = {
                "merchantInfo": {
                    "merchantSerialNumber": self.config.merchant_serial_number
                },
                "transaction": {
                    "transactionText": transaction_text
                }
            }

            response = requests.put(url, json=payload, headers=headers)
            response.raise_for_status()

            logger.info(f"Vipps payment cancelled: {order_id}")

            return {
                "order_id": order_id,
                "status": "cancelled"
            }

        except Exception as e:
            logger.error(f"Vipps payment cancellation failed: {str(e)}")
            raise

    async def refund_payment(
        self,
        order_id: str,
        amount: int,  # In øre
        transaction_text: str
    ) -> Dict:
        """Refund a captured payment"""
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/ecomm/v2/payments/{order_id}/refund"
            headers = self._get_headers(token)

            payload = {
                "merchantInfo": {
                    "merchantSerialNumber": self.config.merchant_serial_number
                },
                "transaction": {
                    "amount": amount,
                    "transactionText": transaction_text
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Vipps refund processed: {order_id} for {amount/100} NOK")

            return {
                "order_id": order_id,
                "refund_id": data.get("transactionInfo", {}).get("transactionId"),
                "status": data.get("transactionInfo", {}).get("status"),
                "amount": amount / 100
            }

        except Exception as e:
            logger.error(f"Vipps refund failed: {str(e)}")
            raise

    # ========================================================================
    # RECURRING PAYMENTS (Subscriptions)
    # ========================================================================

    async def create_agreement(
        self,
        amount: int,  # Monthly price in øre
        interval: str,  # "MONTH", "WEEK", "DAY"
        product_name: str,
        product_description: str,
        phone_number: str,
        redirect_url: Optional[str] = None
    ) -> Dict:
        """
        Create recurring payment agreement (subscription)

        Args:
            amount: Subscription price in øre
            interval: Billing interval
            product_name: Subscription name
            product_description: Description
            phone_number: Customer phone
            redirect_url: URL to redirect after agreement

        Returns:
            Agreement creation response with confirmation URL
        """
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/recurring/v2/agreements"
            headers = self._get_headers(token)

            agreement_id = f"AGR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            payload = {
                "merchantAgreementUrl": redirect_url or f"https://mindframe.no/subscriptions/{agreement_id}",
                "phoneNumber": phone_number,
                "interval": interval,
                "merchantRedirectUrl": redirect_url or "https://mindframe.no/subscriptions",
                "price": amount,
                "productName": product_name,
                "productDescription": product_description
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Vipps recurring agreement created: {agreement_id}")

            return {
                "agreement_id": data.get("agreementId"),
                "vipps_confirm_url": data.get("vippsConfirmationUrl"),
                "amount": amount / 100,
                "interval": interval,
                "status": "pending"
            }

        except Exception as e:
            logger.error(f"Vipps recurring agreement creation failed: {str(e)}")
            raise

    async def get_agreement(self, agreement_id: str) -> Dict:
        """Get recurring agreement details"""
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/recurring/v2/agreements/{agreement_id}"
            headers = self._get_headers(token)

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            return {
                "agreement_id": agreement_id,
                "status": data.get("status"),
                "amount": data.get("price", 0) / 100,
                "interval": data.get("interval"),
                "start_date": data.get("start"),
                "stop_date": data.get("stop")
            }

        except Exception as e:
            logger.error(f"Failed to get Vipps agreement: {str(e)}")
            raise

    async def cancel_agreement(self, agreement_id: str) -> Dict:
        """Cancel recurring agreement"""
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/recurring/v2/agreements/{agreement_id}"
            headers = self._get_headers(token)

            payload = {
                "status": "STOPPED"
            }

            response = requests.patch(url, json=payload, headers=headers)
            response.raise_for_status()

            logger.info(f"Vipps agreement cancelled: {agreement_id}")

            return {
                "agreement_id": agreement_id,
                "status": "stopped"
            }

        except Exception as e:
            logger.error(f"Vipps agreement cancellation failed: {str(e)}")
            raise

    async def create_charge(
        self,
        agreement_id: str,
        amount: int,  # In øre
        description: str,
        due_date: Optional[datetime] = None
    ) -> Dict:
        """
        Create a charge under existing agreement

        Used for monthly subscription charges
        """
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/recurring/v2/agreements/{agreement_id}/charges"
            headers = self._get_headers(token)

            charge_id = f"CHG-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            payload = {
                "amount": amount,
                "currency": "NOK",
                "description": description,
                "due": (due_date or datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "retryDays": 5
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            logger.info(f"Vipps charge created: {charge_id} for agreement {agreement_id}")

            return {
                "charge_id": data.get("chargeId"),
                "agreement_id": agreement_id,
                "amount": amount / 100,
                "status": data.get("status"),
                "due_date": payload["due"]
            }

        except Exception as e:
            logger.error(f"Vipps charge creation failed: {str(e)}")
            raise

    # ========================================================================
    # QR CODE PAYMENTS
    # ========================================================================

    async def generate_qr_code(
        self,
        merchant_callback: str,
        amount: Optional[int] = None
    ) -> Dict:
        """
        Generate static or dynamic QR code for payments

        Args:
            merchant_callback: Callback URL for payment notification
            amount: Optional fixed amount (if None, customer can enter)

        Returns:
            QR code image and ID
        """
        try:
            token = await self.get_access_token()

            url = f"{self.config.base_url}/qr/v1/merchant/{self.config.merchant_serial_number}"
            headers = self._get_headers(token)

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            return {
                "qr_id": data.get("id"),
                "qr_image_url": data.get("url"),
                "status": "active"
            }

        except Exception as e:
            logger.error(f"Vipps QR code generation failed: {str(e)}")
            raise


# ============================================================================
# PRICING TIERS FOR VIPPS (Norwegian Market)
# ============================================================================

VIPPS_PRICING_NORWAY = {
    "free": {
        "name": "Gratis",
        "price_nok": 0,
        "price_ore": 0
    },
    "pro": {
        "name": "Pro",
        "price_nok": 990,  # 990 NOK ~ 99 USD
        "price_ore": 99000
    },
    "enterprise": {
        "name": "Enterprise",
        "price_nok": 4990,  # 4990 NOK ~ 499 USD
        "price_ore": 499000
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_norwegian_phone(phone: str) -> str:
    """
    Format phone number to Norwegian standard

    Accepts: +4712345678, 004712345678, 12345678
    Returns: 4712345678
    """
    # Remove spaces and special characters
    phone = phone.replace(" ", "").replace("-", "").replace("+", "")

    # Remove leading 00
    if phone.startswith("00"):
        phone = phone[2:]

    # Ensure country code
    if not phone.startswith("47"):
        phone = "47" + phone

    return phone


def nok_to_ore(nok: float) -> int:
    """Convert NOK to øre (100 øre = 1 NOK)"""
    return int(nok * 100)


def ore_to_nok(ore: int) -> float:
    """Convert øre to NOK"""
    return ore / 100


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'VippsConfig',
    'VippsPaymentManager',
    'VIPPS_PRICING_NORWAY',
    'format_norwegian_phone',
    'nok_to_ore',
    'ore_to_nok'
]
