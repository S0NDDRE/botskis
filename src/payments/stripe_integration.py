"""
Mindframe Stripe Payment Integration
Complete payment processing system
"""
import stripe
from typing import Dict, Optional, List
from datetime import datetime
from loguru import logger
from pydantic import BaseModel

# Initialize Stripe (set your key in env)
# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ============================================================================
# PRICING PLANS
# ============================================================================

PRICING_PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "currency": "usd",
        "interval": "month",
        "features": {
            "ai_agents": 2,
            "tasks_per_month": 100,
            "voice_calls_per_month": 0,
            "integrations": ["basic"],
            "support": "community",
            "academy_access": True,
            "certificates": False,
            "meta_ai_guardian": False
        }
    },
    "pro": {
        "name": "Pro",
        "price": 99,
        "currency": "usd",
        "interval": "month",
        "stripe_price_id": "price_pro_monthly",  # Set in Stripe dashboard
        "features": {
            "ai_agents": "unlimited",
            "tasks_per_month": 10000,
            "voice_calls_per_month": 100,
            "integrations": "all",
            "support": "email",
            "academy_access": True,
            "certificates": True,
            "meta_ai_guardian": False,
            "priority_support": False
        }
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 499,
        "currency": "usd",
        "interval": "month",
        "stripe_price_id": "price_enterprise_monthly",
        "features": {
            "ai_agents": "unlimited",
            "tasks_per_month": "unlimited",
            "voice_calls_per_month": "unlimited",
            "integrations": "all",
            "support": "priority",
            "academy_access": True,
            "certificates": True,
            "meta_ai_guardian": True,
            "white_label": True,
            "custom_integrations": True,
            "account_manager": True,
            "sla": "99.99%"
        }
    }
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class PaymentMethod(BaseModel):
    id: str
    type: str
    card_last4: Optional[str] = None
    card_brand: Optional[str] = None
    exp_month: Optional[int] = None
    exp_year: Optional[int] = None


class Subscription(BaseModel):
    id: str
    customer_id: str
    plan: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False


class Invoice(BaseModel):
    id: str
    customer_id: str
    amount_due: int
    amount_paid: int
    status: str
    created: datetime
    due_date: Optional[datetime] = None
    pdf_url: Optional[str] = None


# ============================================================================
# STRIPE MANAGER
# ============================================================================

class StripeManager:
    """
    Complete Stripe integration for Mindframe
    Handles subscriptions, payments, invoices, webhooks
    """
    
    def __init__(self, api_key: str):
        stripe.api_key = api_key
        logger.info("Stripe manager initialized")
    
    # ========================================================================
    # CUSTOMER MANAGEMENT
    # ========================================================================
    
    async def create_customer(
        self,
        email: str,
        name: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            logger.info(f"Created Stripe customer: {customer.id}")
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create customer: {e}")
            raise
    
    async def get_customer(self, customer_id: str) -> Dict:
        """Get customer details"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "created": datetime.fromtimestamp(customer.created)
            }
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get customer: {e}")
            raise
    
    async def update_customer(
        self,
        customer_id: str,
        **kwargs
    ) -> Dict:
        """Update customer information"""
        try:
            customer = stripe.Customer.modify(customer_id, **kwargs)
            logger.info(f"Updated customer: {customer_id}")
            return customer
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update customer: {e}")
            raise
    
    # ========================================================================
    # SUBSCRIPTION MANAGEMENT
    # ========================================================================
    
    async def create_subscription(
        self,
        customer_id: str,
        plan: str,
        payment_method_id: Optional[str] = None,
        trial_days: int = 0
    ) -> Subscription:
        """Create a subscription"""
        try:
            plan_info = PRICING_PLANS.get(plan)
            if not plan_info:
                raise ValueError(f"Invalid plan: {plan}")
            
            # Skip payment for free plan
            if plan == "free":
                return Subscription(
                    id="free_subscription",
                    customer_id=customer_id,
                    plan="free",
                    status="active",
                    current_period_start=datetime.now(),
                    current_period_end=datetime.now(),
                    cancel_at_period_end=False
                )
            
            # Attach payment method if provided
            if payment_method_id:
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer_id
                )
                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={
                        'default_payment_method': payment_method_id
                    }
                )
            
            # Create subscription
            subscription_params = {
                "customer": customer_id,
                "items": [{"price": plan_info["stripe_price_id"]}],
                "expand": ["latest_invoice.payment_intent"]
            }
            
            if trial_days > 0:
                subscription_params["trial_period_days"] = trial_days
            
            subscription = stripe.Subscription.create(**subscription_params)
            
            logger.info(f"Created subscription: {subscription.id} for {customer_id}")
            
            return Subscription(
                id=subscription.id,
                customer_id=customer_id,
                plan=plan,
                status=subscription.status,
                current_period_start=datetime.fromtimestamp(subscription.current_period_start),
                current_period_end=datetime.fromtimestamp(subscription.current_period_end),
                cancel_at_period_end=subscription.cancel_at_period_end
            )
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create subscription: {e}")
            raise
    
    async def get_subscription(self, subscription_id: str) -> Subscription:
        """Get subscription details"""
        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            
            # Get plan name from price ID
            plan_name = "unknown"
            for name, info in PRICING_PLANS.items():
                if info.get("stripe_price_id") == sub.items.data[0].price.id:
                    plan_name = name
                    break
            
            return Subscription(
                id=sub.id,
                customer_id=sub.customer,
                plan=plan_name,
                status=sub.status,
                current_period_start=datetime.fromtimestamp(sub.current_period_start),
                current_period_end=datetime.fromtimestamp(sub.current_period_end),
                cancel_at_period_end=sub.cancel_at_period_end
            )
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get subscription: {e}")
            raise
    
    async def update_subscription(
        self,
        subscription_id: str,
        new_plan: str
    ) -> Subscription:
        """Update subscription to new plan"""
        try:
            plan_info = PRICING_PLANS.get(new_plan)
            if not plan_info:
                raise ValueError(f"Invalid plan: {new_plan}")
            
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': plan_info["stripe_price_id"]
                }],
                proration_behavior='always_invoice'
            )
            
            logger.info(f"Updated subscription {subscription_id} to {new_plan}")
            
            return await self.get_subscription(subscription_id)
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update subscription: {e}")
            raise
    
    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> Subscription:
        """Cancel a subscription"""
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
                logger.info(f"Subscription {subscription_id} will cancel at period end")
            else:
                subscription = stripe.Subscription.delete(subscription_id)
                logger.info(f"Subscription {subscription_id} cancelled immediately")
            
            return await self.get_subscription(subscription_id)
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise
    
    async def reactivate_subscription(self, subscription_id: str) -> Subscription:
        """Reactivate a cancelled subscription"""
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False
            )
            logger.info(f"Reactivated subscription: {subscription_id}")
            return await self.get_subscription(subscription_id)
        except stripe.error.StripeError as e:
            logger.error(f"Failed to reactivate subscription: {e}")
            raise
    
    # ========================================================================
    # PAYMENT METHODS
    # ========================================================================
    
    async def add_payment_method(
        self,
        customer_id: str,
        payment_method_id: str,
        set_default: bool = True
    ) -> PaymentMethod:
        """Add payment method to customer"""
        try:
            # Attach to customer
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )
            
            # Set as default if requested
            if set_default:
                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={
                        'default_payment_method': payment_method_id
                    }
                )
            
            logger.info(f"Added payment method {payment_method_id} to {customer_id}")
            
            return PaymentMethod(
                id=payment_method.id,
                type=payment_method.type,
                card_last4=payment_method.card.last4 if payment_method.card else None,
                card_brand=payment_method.card.brand if payment_method.card else None,
                exp_month=payment_method.card.exp_month if payment_method.card else None,
                exp_year=payment_method.card.exp_year if payment_method.card else None
            )
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to add payment method: {e}")
            raise
    
    async def list_payment_methods(self, customer_id: str) -> List[PaymentMethod]:
        """List all payment methods for customer"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            
            return [
                PaymentMethod(
                    id=pm.id,
                    type=pm.type,
                    card_last4=pm.card.last4 if pm.card else None,
                    card_brand=pm.card.brand if pm.card else None,
                    exp_month=pm.card.exp_month if pm.card else None,
                    exp_year=pm.card.exp_year if pm.card else None
                )
                for pm in payment_methods.data
            ]
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to list payment methods: {e}")
            raise
    
    async def remove_payment_method(self, payment_method_id: str) -> bool:
        """Remove a payment method"""
        try:
            stripe.PaymentMethod.detach(payment_method_id)
            logger.info(f"Removed payment method: {payment_method_id}")
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to remove payment method: {e}")
            raise
    
    # ========================================================================
    # INVOICES
    # ========================================================================
    
    async def get_invoice(self, invoice_id: str) -> Invoice:
        """Get invoice details"""
        try:
            invoice = stripe.Invoice.retrieve(invoice_id)
            
            return Invoice(
                id=invoice.id,
                customer_id=invoice.customer,
                amount_due=invoice.amount_due,
                amount_paid=invoice.amount_paid,
                status=invoice.status,
                created=datetime.fromtimestamp(invoice.created),
                due_date=datetime.fromtimestamp(invoice.due_date) if invoice.due_date else None,
                pdf_url=invoice.invoice_pdf
            )
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get invoice: {e}")
            raise
    
    async def list_invoices(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[Invoice]:
        """List invoices for customer"""
        try:
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit
            )
            
            return [
                Invoice(
                    id=inv.id,
                    customer_id=inv.customer,
                    amount_due=inv.amount_due,
                    amount_paid=inv.amount_paid,
                    status=inv.status,
                    created=datetime.fromtimestamp(inv.created),
                    due_date=datetime.fromtimestamp(inv.due_date) if inv.due_date else None,
                    pdf_url=inv.invoice_pdf
                )
                for inv in invoices.data
            ]
        except stripe.error.StripeError as e:
            logger.error(f"Failed to list invoices: {e}")
            raise
    
    # ========================================================================
    # CHECKOUT SESSION (For initial subscription)
    # ========================================================================
    
    async def create_checkout_session(
        self,
        customer_id: str,
        plan: str,
        success_url: str,
        cancel_url: str,
        trial_days: int = 0
    ) -> str:
        """Create Stripe Checkout session for subscription"""
        try:
            plan_info = PRICING_PLANS.get(plan)
            if not plan_info or plan == "free":
                raise ValueError(f"Invalid plan for checkout: {plan}")
            
            session_params = {
                "customer": customer_id,
                "payment_method_types": ["card"],
                "line_items": [{
                    "price": plan_info["stripe_price_id"],
                    "quantity": 1
                }],
                "mode": "subscription",
                "success_url": success_url,
                "cancel_url": cancel_url
            }
            
            if trial_days > 0:
                session_params["subscription_data"] = {
                    "trial_period_days": trial_days
                }
            
            session = stripe.checkout.Session.create(**session_params)
            
            logger.info(f"Created checkout session: {session.id}")
            return session.url
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise
    
    # ========================================================================
    # CUSTOMER PORTAL
    # ========================================================================
    
    async def create_portal_session(
        self,
        customer_id: str,
        return_url: str
    ) -> str:
        """Create customer portal session for managing subscription"""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            
            logger.info(f"Created portal session for customer: {customer_id}")
            return session.url
        
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create portal session: {e}")
            raise
    
    # ========================================================================
    # WEBHOOKS
    # ========================================================================
    
    async def handle_webhook(
        self,
        payload: bytes,
        signature: str,
        webhook_secret: str
    ) -> Dict:
        """
        Handle Stripe webhook events
        
        Important events:
        - customer.subscription.created
        - customer.subscription.updated
        - customer.subscription.deleted
        - invoice.payment_succeeded
        - invoice.payment_failed
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            event_type = event['type']
            data = event['data']['object']
            
            logger.info(f"Received webhook: {event_type}")
            
            # Handle different event types
            if event_type == 'customer.subscription.created':
                return await self._handle_subscription_created(data)
            
            elif event_type == 'customer.subscription.updated':
                return await self._handle_subscription_updated(data)
            
            elif event_type == 'customer.subscription.deleted':
                return await self._handle_subscription_deleted(data)
            
            elif event_type == 'invoice.payment_succeeded':
                return await self._handle_payment_succeeded(data)
            
            elif event_type == 'invoice.payment_failed':
                return await self._handle_payment_failed(data)
            
            else:
                logger.info(f"Unhandled event type: {event_type}")
                return {"status": "ignored"}
        
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            raise
    
    async def _handle_subscription_created(self, subscription) -> Dict:
        """Handle new subscription"""
        logger.info(f"New subscription created: {subscription['id']}")
        # Update user in database
        return {"status": "subscription_created", "id": subscription['id']}
    
    async def _handle_subscription_updated(self, subscription) -> Dict:
        """Handle subscription update"""
        logger.info(f"Subscription updated: {subscription['id']}")
        # Update user in database
        return {"status": "subscription_updated", "id": subscription['id']}
    
    async def _handle_subscription_deleted(self, subscription) -> Dict:
        """Handle subscription cancellation"""
        logger.info(f"Subscription deleted: {subscription['id']}")
        # Downgrade user to free plan
        return {"status": "subscription_deleted", "id": subscription['id']}
    
    async def _handle_payment_succeeded(self, invoice) -> Dict:
        """Handle successful payment"""
        logger.info(f"Payment succeeded for invoice: {invoice['id']}")
        # Send receipt email
        return {"status": "payment_succeeded", "invoice_id": invoice['id']}
    
    async def _handle_payment_failed(self, invoice) -> Dict:
        """Handle failed payment"""
        logger.error(f"Payment failed for invoice: {invoice['id']}")
        # Send payment failure email
        # Maybe suspend account after X failed attempts
        return {"status": "payment_failed", "invoice_id": invoice['id']}


# ============================================================================
# USAGE TRACKING (for billing)
# ============================================================================

class UsageTracker:
    """
    Track usage for billing purposes
    - AI agents created
    - Tasks executed
    - Voice calls made
    - API calls
    """
    
    def __init__(self):
        self.usage_data = {}
    
    async def record_usage(
        self,
        customer_id: str,
        usage_type: str,
        quantity: int = 1
    ):
        """Record usage event"""
        if customer_id not in self.usage_data:
            self.usage_data[customer_id] = {}
        
        if usage_type not in self.usage_data[customer_id]:
            self.usage_data[customer_id][usage_type] = 0
        
        self.usage_data[customer_id][usage_type] += quantity
        
        logger.debug(f"Recorded {quantity} {usage_type} for {customer_id}")
    
    async def get_usage(self, customer_id: str) -> Dict:
        """Get usage for customer"""
        return self.usage_data.get(customer_id, {})
    
    async def reset_usage(self, customer_id: str):
        """Reset usage (call at end of billing period)"""
        if customer_id in self.usage_data:
            self.usage_data[customer_id] = {}
        logger.info(f"Reset usage for {customer_id}")
    
    async def check_limit(
        self,
        customer_id: str,
        plan: str,
        usage_type: str
    ) -> bool:
        """Check if customer is within limits"""
        plan_info = PRICING_PLANS.get(plan)
        if not plan_info:
            return False
        
        limit = plan_info["features"].get(usage_type)
        
        # Unlimited
        if limit == "unlimited":
            return True
        
        # Get current usage
        current_usage = self.usage_data.get(customer_id, {}).get(usage_type, 0)
        
        # Check limit
        return current_usage < limit


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_plan_features(plan: str) -> Dict:
    """Get features for a plan"""
    return PRICING_PLANS.get(plan, {}).get("features", {})


def calculate_proration(
    current_plan: str,
    new_plan: str,
    days_remaining: int
) -> int:
    """Calculate proration amount when upgrading/downgrading"""
    current_price = PRICING_PLANS[current_plan]["price"]
    new_price = PRICING_PLANS[new_plan]["price"]
    
    daily_rate_current = current_price / 30
    daily_rate_new = new_price / 30
    
    refund = daily_rate_current * days_remaining
    charge = daily_rate_new * days_remaining
    
    return int((charge - refund) * 100)  # In cents
