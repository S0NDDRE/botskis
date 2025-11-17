"""
Extended Stripe Payment Features
Additional production-ready payment functionalities
"""
import stripe
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from loguru import logger
from pydantic import BaseModel, EmailStr
from enum import Enum


# ============================================================================
# REFUND MANAGEMENT
# ============================================================================

class RefundReason(str, Enum):
    """Refund reasons"""
    DUPLICATE = "duplicate"
    FRAUDULENT = "fraudulent"
    REQUESTED_BY_CUSTOMER = "requested_by_customer"
    PRODUCT_NOT_RECEIVED = "product_not_received"
    PRODUCT_UNACCEPTABLE = "product_unacceptable"
    SUBSCRIPTION_CANCELED = "subscription_canceled"


class RefundManager:
    """Handle refunds and chargebacks"""

    @staticmethod
    async def create_refund(
        payment_intent_id: str,
        amount: Optional[int] = None,  # In cents, None = full refund
        reason: RefundReason = RefundReason.REQUESTED_BY_CUSTOMER,
        metadata: Optional[Dict] = None
    ) -> stripe.Refund:
        """
        Create a refund for a payment

        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund in cents (None for full refund)
            reason: Reason for refund
            metadata: Additional metadata

        Returns:
            Stripe Refund object
        """
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount,
                reason=reason.value,
                metadata=metadata or {}
            )

            logger.info(
                f"Refund created: {refund.id} | "
                f"Amount: {amount or 'full'} | "
                f"Reason: {reason.value}"
            )

            return refund

        except stripe.error.StripeError as e:
            logger.error(f"Refund failed: {str(e)}")
            raise

    @staticmethod
    async def get_refund(refund_id: str) -> stripe.Refund:
        """Get refund by ID"""
        return stripe.Refund.retrieve(refund_id)

    @staticmethod
    async def list_refunds(
        payment_intent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[stripe.Refund]:
        """List refunds"""
        params = {"limit": limit}
        if payment_intent_id:
            params["payment_intent"] = payment_intent_id

        refunds = stripe.Refund.list(**params)
        return refunds.data


# ============================================================================
# DISCOUNT & COUPON CODES
# ============================================================================

class DiscountManager:
    """Handle discount codes and promotions"""

    @staticmethod
    async def create_coupon(
        code: str,
        percent_off: Optional[float] = None,
        amount_off: Optional[int] = None,  # In cents
        duration: str = "once",  # once, repeating, forever
        duration_in_months: Optional[int] = None,
        max_redemptions: Optional[int] = None,
        expires_at: Optional[datetime] = None
    ) -> stripe.Coupon:
        """
        Create a discount coupon

        Args:
            code: Coupon code (e.g., "LAUNCH50")
            percent_off: Percentage discount (0-100)
            amount_off: Fixed amount discount in cents
            duration: How long discount applies
            duration_in_months: For "repeating" duration
            max_redemptions: Maximum number of times code can be used
            expires_at: Expiration date

        Returns:
            Stripe Coupon object
        """
        try:
            coupon_data = {
                "id": code,
                "duration": duration,
                "max_redemptions": max_redemptions
            }

            if percent_off:
                coupon_data["percent_off"] = percent_off
            elif amount_off:
                coupon_data["amount_off"] = amount_off
                coupon_data["currency"] = "usd"

            if duration == "repeating" and duration_in_months:
                coupon_data["duration_in_months"] = duration_in_months

            if expires_at:
                coupon_data["redeem_by"] = int(expires_at.timestamp())

            coupon = stripe.Coupon.create(**coupon_data)

            logger.info(f"Coupon created: {code} | Discount: {percent_off or amount_off}")

            return coupon

        except stripe.error.StripeError as e:
            logger.error(f"Coupon creation failed: {str(e)}")
            raise

    @staticmethod
    async def apply_coupon_to_customer(
        customer_id: str,
        coupon_code: str
    ) -> stripe.Customer:
        """Apply coupon to customer"""
        try:
            customer = stripe.Customer.modify(
                customer_id,
                coupon=coupon_code
            )

            logger.info(f"Coupon {coupon_code} applied to customer {customer_id}")

            return customer

        except stripe.error.StripeError as e:
            logger.error(f"Coupon application failed: {str(e)}")
            raise

    @staticmethod
    async def apply_coupon_to_subscription(
        subscription_id: str,
        coupon_code: str
    ) -> stripe.Subscription:
        """Apply coupon to subscription"""
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                coupon=coupon_code
            )

            logger.info(f"Coupon {coupon_code} applied to subscription {subscription_id}")

            return subscription

        except stripe.error.StripeError as e:
            logger.error(f"Coupon application failed: {str(e)}")
            raise

    @staticmethod
    async def get_coupon(code: str) -> stripe.Coupon:
        """Get coupon details"""
        return stripe.Coupon.retrieve(code)

    @staticmethod
    async def delete_coupon(code: str) -> stripe.Coupon:
        """Delete/deactivate coupon"""
        return stripe.Coupon.delete(code)


# ============================================================================
# PAYMENT INTENTS (for SCA - Strong Customer Authentication)
# ============================================================================

class PaymentIntentManager:
    """Handle payment intents for one-time payments and SCA"""

    @staticmethod
    async def create_payment_intent(
        amount: int,  # In cents
        currency: str = "usd",
        customer_id: Optional[str] = None,
        payment_method_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> stripe.PaymentIntent:
        """
        Create a payment intent

        Used for one-time payments or when SCA is required

        Args:
            amount: Amount in cents
            currency: Currency code
            customer_id: Stripe customer ID
            payment_method_id: Payment method to use
            description: Payment description
            metadata: Additional metadata

        Returns:
            Stripe PaymentIntent object
        """
        try:
            intent_data = {
                "amount": amount,
                "currency": currency,
                "description": description,
                "metadata": metadata or {},
                "automatic_payment_methods": {"enabled": True}
            }

            if customer_id:
                intent_data["customer"] = customer_id

            if payment_method_id:
                intent_data["payment_method"] = payment_method_id
                intent_data["confirm"] = True

            intent = stripe.PaymentIntent.create(**intent_data)

            logger.info(
                f"Payment intent created: {intent.id} | "
                f"Amount: ${amount/100} {currency}"
            )

            return intent

        except stripe.error.StripeError as e:
            logger.error(f"Payment intent creation failed: {str(e)}")
            raise

    @staticmethod
    async def confirm_payment_intent(
        intent_id: str,
        payment_method_id: str
    ) -> stripe.PaymentIntent:
        """Confirm a payment intent"""
        try:
            intent = stripe.PaymentIntent.confirm(
                intent_id,
                payment_method=payment_method_id
            )

            logger.info(f"Payment intent confirmed: {intent_id}")

            return intent

        except stripe.error.StripeError as e:
            logger.error(f"Payment intent confirmation failed: {str(e)}")
            raise

    @staticmethod
    async def cancel_payment_intent(intent_id: str) -> stripe.PaymentIntent:
        """Cancel a payment intent"""
        try:
            intent = stripe.PaymentIntent.cancel(intent_id)

            logger.info(f"Payment intent canceled: {intent_id}")

            return intent

        except stripe.error.StripeError as e:
            logger.error(f"Payment intent cancellation failed: {str(e)}")
            raise


# ============================================================================
# TRIAL MANAGEMENT
# ============================================================================

class TrialManager:
    """Handle trial periods and extensions"""

    @staticmethod
    async def extend_trial(
        subscription_id: str,
        days: int
    ) -> stripe.Subscription:
        """
        Extend trial period

        Args:
            subscription_id: Stripe subscription ID
            days: Number of days to extend

        Returns:
            Updated subscription
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            if subscription.trial_end:
                # Extend existing trial
                current_trial_end = datetime.fromtimestamp(subscription.trial_end)
                new_trial_end = current_trial_end + timedelta(days=days)
            else:
                # Start new trial
                new_trial_end = datetime.now() + timedelta(days=days)

            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                trial_end=int(new_trial_end.timestamp())
            )

            logger.info(
                f"Trial extended for subscription {subscription_id} | "
                f"New end date: {new_trial_end}"
            )

            return updated_subscription

        except stripe.error.StripeError as e:
            logger.error(f"Trial extension failed: {str(e)}")
            raise

    @staticmethod
    async def start_trial(
        customer_id: str,
        price_id: str,
        trial_days: int
    ) -> stripe.Subscription:
        """Start subscription with trial period"""
        try:
            trial_end = datetime.now() + timedelta(days=trial_days)

            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                trial_end=int(trial_end.timestamp())
            )

            logger.info(
                f"Trial started for customer {customer_id} | "
                f"Duration: {trial_days} days"
            )

            return subscription

        except stripe.error.StripeError as e:
            logger.error(f"Trial start failed: {str(e)}")
            raise


# ============================================================================
# SUBSCRIPTION PREVIEW
# ============================================================================

class SubscriptionPreview:
    """Preview subscription changes before applying"""

    @staticmethod
    async def preview_upgrade(
        subscription_id: str,
        new_price_id: str
    ) -> Dict:
        """
        Preview subscription upgrade/downgrade

        Args:
            subscription_id: Current subscription ID
            new_price_id: New price to switch to

        Returns:
            Preview data with proration amount
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            # Get upcoming invoice with the proposed changes
            upcoming_invoice = stripe.Invoice.upcoming(
                customer=subscription.customer,
                subscription=subscription_id,
                subscription_items=[{
                    "id": subscription["items"]["data"][0].id,
                    "price": new_price_id
                }]
            )

            preview = {
                "current_plan": subscription.plan.id,
                "new_plan": new_price_id,
                "immediate_charge": upcoming_invoice.amount_due,
                "proration_amount": sum(
                    line.amount for line in upcoming_invoice.lines
                    if line.proration
                ),
                "next_billing_date": datetime.fromtimestamp(
                    upcoming_invoice.period_end
                ).isoformat(),
                "amount_due_now": upcoming_invoice.amount_due / 100,  # Convert to dollars
                "currency": upcoming_invoice.currency
            }

            logger.info(f"Subscription preview generated for {subscription_id}")

            return preview

        except stripe.error.StripeError as e:
            logger.error(f"Subscription preview failed: {str(e)}")
            raise


# ============================================================================
# FAILED PAYMENT RECOVERY
# ============================================================================

class FailedPaymentRecovery:
    """Handle failed payments and dunning"""

    @staticmethod
    async def retry_failed_payment(
        invoice_id: str
    ) -> stripe.Invoice:
        """
        Retry a failed invoice payment

        Args:
            invoice_id: Stripe invoice ID

        Returns:
            Updated invoice
        """
        try:
            invoice = stripe.Invoice.pay(invoice_id)

            logger.info(f"Payment retry initiated for invoice {invoice_id}")

            return invoice

        except stripe.error.StripeError as e:
            logger.error(f"Payment retry failed: {str(e)}")
            raise

    @staticmethod
    async def update_payment_method_for_failed_invoice(
        invoice_id: str,
        payment_method_id: str
    ) -> stripe.Invoice:
        """Update payment method and retry"""
        try:
            invoice = stripe.Invoice.retrieve(invoice_id)

            # Update customer's default payment method
            stripe.Customer.modify(
                invoice.customer,
                invoice_settings={
                    "default_payment_method": payment_method_id
                }
            )

            # Retry payment
            paid_invoice = stripe.Invoice.pay(invoice_id)

            logger.info(
                f"Payment method updated and payment retried for invoice {invoice_id}"
            )

            return paid_invoice

        except stripe.error.StripeError as e:
            logger.error(f"Payment method update failed: {str(e)}")
            raise


# ============================================================================
# CUSTOMER BALANCE & CREDITS
# ============================================================================

class CustomerBalanceManager:
    """Handle customer credits and balance"""

    @staticmethod
    async def add_credit(
        customer_id: str,
        amount: int,  # In cents (negative for credit)
        description: str
    ) -> stripe.CustomerBalanceTransaction:
        """
        Add credit to customer balance

        Args:
            customer_id: Stripe customer ID
            amount: Amount in cents (use negative for credit)
            description: Description of credit

        Returns:
            Balance transaction
        """
        try:
            transaction = stripe.Customer.create_balance_transaction(
                customer_id,
                amount=-abs(amount),  # Negative for credit
                currency="usd",
                description=description
            )

            logger.info(
                f"Credit added to customer {customer_id} | "
                f"Amount: ${abs(amount)/100}"
            )

            return transaction

        except stripe.error.StripeError as e:
            logger.error(f"Credit addition failed: {str(e)}")
            raise

    @staticmethod
    async def get_balance(customer_id: str) -> int:
        """Get customer balance"""
        customer = stripe.Customer.retrieve(customer_id)
        return customer.balance

    @staticmethod
    async def list_balance_transactions(
        customer_id: str,
        limit: int = 10
    ) -> List[stripe.CustomerBalanceTransaction]:
        """List customer balance transactions"""
        transactions = stripe.Customer.list_balance_transactions(
            customer_id,
            limit=limit
        )
        return transactions.data


# ============================================================================
# TAX HANDLING
# ============================================================================

class TaxManager:
    """Handle tax calculations and compliance"""

    @staticmethod
    async def calculate_tax(
        amount: int,
        customer_id: str,
        currency: str = "usd"
    ) -> Dict:
        """
        Calculate tax for a transaction

        Uses Stripe Tax for automatic calculation

        Args:
            amount: Amount in cents
            customer_id: Stripe customer ID
            currency: Currency code

        Returns:
            Tax calculation details
        """
        try:
            # This requires Stripe Tax to be enabled
            calculation = stripe.tax.Calculation.create(
                currency=currency,
                line_items=[{
                    "amount": amount,
                    "reference": "subscription"
                }],
                customer_details={
                    "address": {
                        # Get from customer object
                    },
                    "address_source": "billing"
                }
            )

            return {
                "tax_amount": calculation.tax_amount_exclusive,
                "total_amount": calculation.amount_total,
                "tax_breakdown": calculation.tax_breakdown
            }

        except stripe.error.StripeError as e:
            logger.error(f"Tax calculation failed: {str(e)}")
            # Return without tax if calculation fails
            return {
                "tax_amount": 0,
                "total_amount": amount,
                "tax_breakdown": []
            }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'RefundManager',
    'RefundReason',
    'DiscountManager',
    'PaymentIntentManager',
    'TrialManager',
    'SubscriptionPreview',
    'FailedPaymentRecovery',
    'CustomerBalanceManager',
    'TaxManager',
]
