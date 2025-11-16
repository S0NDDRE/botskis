"""
Extended Payment API Endpoints
Additional payment features for production
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from src.payments.stripe_extended import (
    RefundManager,
    RefundReason,
    DiscountManager,
    PaymentIntentManager,
    TrialManager,
    SubscriptionPreview,
    FailedPaymentRecovery,
    CustomerBalanceManager,
    TaxManager
)
from src.core.auth import get_current_user, get_current_active_user
from src.database.models import User


router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class RefundRequest(BaseModel):
    payment_intent_id: str
    amount: Optional[int] = None  # None for full refund
    reason: RefundReason
    notes: Optional[str] = None


class CouponCreateRequest(BaseModel):
    code: str
    percent_off: Optional[float] = None
    amount_off: Optional[int] = None
    duration: str = "once"
    duration_in_months: Optional[int] = None
    max_redemptions: Optional[int] = None
    expires_at: Optional[datetime] = None


class ApplyCouponRequest(BaseModel):
    coupon_code: str


class PaymentIntentRequest(BaseModel):
    amount: int  # In cents
    currency: str = "usd"
    description: Optional[str] = None
    payment_method_id: Optional[str] = None


class ExtendTrialRequest(BaseModel):
    days: int


class AddCreditRequest(BaseModel):
    amount: int  # In cents
    description: str


# ============================================================================
# REFUND ENDPOINTS
# ============================================================================

@router.post("/refunds")
async def create_refund(
    request: RefundRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a refund for a payment

    **Requires:** Admin role

    **Use cases:**
    - Customer requests refund
    - Duplicate charge
    - Fraudulent transaction
    - Product not delivered
    """
    # TODO: Check if user is admin
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=403, detail="Admin access required")

    metadata = {
        "requested_by": current_user.email,
        "notes": request.notes
    }

    refund = await RefundManager.create_refund(
        payment_intent_id=request.payment_intent_id,
        amount=request.amount,
        reason=request.reason,
        metadata=metadata
    )

    return {
        "success": True,
        "refund_id": refund.id,
        "amount": refund.amount / 100,
        "status": refund.status,
        "message": "Refund processed successfully"
    }


@router.get("/refunds/{refund_id}")
async def get_refund(
    refund_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get refund details"""
    refund = await RefundManager.get_refund(refund_id)

    return {
        "success": True,
        "refund": {
            "id": refund.id,
            "amount": refund.amount / 100,
            "currency": refund.currency,
            "status": refund.status,
            "reason": refund.reason,
            "created": datetime.fromtimestamp(refund.created).isoformat()
        }
    }


@router.get("/refunds")
async def list_refunds(
    payment_intent_id: Optional[str] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """List refunds"""
    refunds = await RefundManager.list_refunds(
        payment_intent_id=payment_intent_id,
        limit=limit
    )

    return {
        "success": True,
        "refunds": [
            {
                "id": r.id,
                "amount": r.amount / 100,
                "status": r.status,
                "created": datetime.fromtimestamp(r.created).isoformat()
            }
            for r in refunds
        ]
    }


# ============================================================================
# COUPON/DISCOUNT ENDPOINTS
# ============================================================================

@router.post("/coupons")
async def create_coupon(
    request: CouponCreateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a discount coupon

    **Requires:** Admin role

    **Examples:**
    - LAUNCH50: 50% off first month
    - YEARLY20: 20% off yearly plans
    - FREEMONTH: Free month credit
    """
    # TODO: Check admin role

    coupon = await DiscountManager.create_coupon(
        code=request.code,
        percent_off=request.percent_off,
        amount_off=request.amount_off,
        duration=request.duration,
        duration_in_months=request.duration_in_months,
        max_redemptions=request.max_redemptions,
        expires_at=request.expires_at
    )

    return {
        "success": True,
        "coupon_id": coupon.id,
        "code": request.code,
        "discount": f"{request.percent_off}%" if request.percent_off else f"${request.amount_off/100}",
        "message": f"Coupon '{request.code}' created successfully"
    }


@router.post("/coupons/apply")
async def apply_coupon(
    request: ApplyCouponRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Apply coupon to current user

    **Use case:** User enters promo code at checkout
    """
    # Get user's Stripe customer ID from database
    # customer_id = current_user.stripe_customer_id

    # For demo purposes
    customer_id = "cus_demo"

    customer = await DiscountManager.apply_coupon_to_customer(
        customer_id=customer_id,
        coupon_code=request.coupon_code
    )

    return {
        "success": True,
        "message": f"Coupon '{request.coupon_code}' applied successfully",
        "discount": customer.discount
    }


@router.get("/coupons/{code}")
async def get_coupon(code: str):
    """
    Get coupon details

    **Public endpoint** - allows users to check if code is valid
    """
    try:
        coupon = await DiscountManager.get_coupon(code)

        if not coupon.valid:
            raise HTTPException(status_code=404, detail="Coupon is not valid or has expired")

        return {
            "success": True,
            "coupon": {
                "code": coupon.id,
                "percent_off": coupon.percent_off,
                "amount_off": coupon.amount_off,
                "duration": coupon.duration,
                "valid": coupon.valid,
                "max_redemptions": coupon.max_redemptions,
                "times_redeemed": coupon.times_redeemed
            }
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Coupon not found: {str(e)}")


@router.delete("/coupons/{code}")
async def delete_coupon(
    code: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete/deactivate coupon"""
    # TODO: Check admin role

    coupon = await DiscountManager.delete_coupon(code)

    return {
        "success": True,
        "message": f"Coupon '{code}' deleted successfully"
    }


# ============================================================================
# PAYMENT INTENT ENDPOINTS (for one-time payments)
# ============================================================================

@router.post("/payment-intents")
async def create_payment_intent(
    request: PaymentIntentRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create payment intent for one-time payment

    **Use cases:**
    - Buy credits
    - One-time add-ons
    - Pay invoice manually
    """
    # Get customer ID from user
    # customer_id = current_user.stripe_customer_id

    intent = await PaymentIntentManager.create_payment_intent(
        amount=request.amount,
        currency=request.currency,
        customer_id=None,  # Replace with actual customer_id
        payment_method_id=request.payment_method_id,
        description=request.description,
        metadata={"user_id": current_user.id}
    )

    return {
        "success": True,
        "client_secret": intent.client_secret,
        "payment_intent_id": intent.id,
        "amount": intent.amount / 100,
        "currency": intent.currency,
        "status": intent.status
    }


@router.post("/payment-intents/{intent_id}/confirm")
async def confirm_payment_intent(
    intent_id: str,
    payment_method_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Confirm a payment intent"""
    intent = await PaymentIntentManager.confirm_payment_intent(
        intent_id=intent_id,
        payment_method_id=payment_method_id
    )

    return {
        "success": True,
        "status": intent.status,
        "message": "Payment confirmed" if intent.status == "succeeded" else f"Payment {intent.status}"
    }


# ============================================================================
# TRIAL MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/subscriptions/{subscription_id}/trial/extend")
async def extend_trial(
    subscription_id: str,
    request: ExtendTrialRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Extend trial period

    **Use cases:**
    - Customer needs more time to evaluate
    - Promotion/goodwill gesture
    - Technical issues during trial
    """
    # TODO: Verify user owns this subscription

    subscription = await TrialManager.extend_trial(
        subscription_id=subscription_id,
        days=request.days
    )

    return {
        "success": True,
        "subscription_id": subscription.id,
        "trial_end": datetime.fromtimestamp(subscription.trial_end).isoformat(),
        "message": f"Trial extended by {request.days} days"
    }


# ============================================================================
# SUBSCRIPTION PREVIEW ENDPOINTS
# ============================================================================

@router.get("/subscriptions/{subscription_id}/preview")
async def preview_subscription_change(
    subscription_id: str,
    new_price_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Preview subscription upgrade/downgrade before applying

    **Shows:**
    - Immediate charge (proration)
    - New recurring amount
    - Next billing date

    **Use case:** User can see exactly what they'll pay before confirming upgrade
    """
    # TODO: Verify user owns this subscription

    preview = await SubscriptionPreview.preview_upgrade(
        subscription_id=subscription_id,
        new_price_id=new_price_id
    )

    return {
        "success": True,
        "preview": preview,
        "message": "Preview generated. Use /upgrade endpoint to confirm changes."
    }


# ============================================================================
# FAILED PAYMENT RECOVERY ENDPOINTS
# ============================================================================

@router.post("/invoices/{invoice_id}/retry")
async def retry_failed_payment(
    invoice_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retry a failed invoice payment

    **Use case:** User updates payment method and wants to retry immediately
    """
    # TODO: Verify user owns this invoice

    invoice = await FailedPaymentRecovery.retry_failed_payment(invoice_id)

    return {
        "success": True,
        "invoice_id": invoice.id,
        "status": invoice.status,
        "amount_due": invoice.amount_due / 100,
        "message": "Payment retry initiated" if invoice.status == "paid" else "Payment failed"
    }


@router.post("/invoices/{invoice_id}/update-payment-method")
async def update_payment_method_and_retry(
    invoice_id: str,
    payment_method_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update payment method and retry failed invoice

    **Use case:** User's card declined, they add new card and want to pay immediately
    """
    # TODO: Verify user owns this invoice

    invoice = await FailedPaymentRecovery.update_payment_method_for_failed_invoice(
        invoice_id=invoice_id,
        payment_method_id=payment_method_id
    )

    return {
        "success": True,
        "invoice_id": invoice.id,
        "status": invoice.status,
        "message": "Payment method updated and payment successful" if invoice.status == "paid" else "Payment failed"
    }


# ============================================================================
# CUSTOMER BALANCE/CREDITS ENDPOINTS
# ============================================================================

@router.post("/credits/add")
async def add_customer_credit(
    request: AddCreditRequest,
    customer_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Add credit to customer account

    **Requires:** Admin role

    **Use cases:**
    - Compensation for service issues
    - Promotional credits
    - Refund as credit
    """
    # TODO: Check admin role

    transaction = await CustomerBalanceManager.add_credit(
        customer_id=customer_id,
        amount=request.amount,
        description=request.description
    )

    return {
        "success": True,
        "transaction_id": transaction.id,
        "amount": abs(transaction.amount) / 100,
        "description": request.description,
        "message": f"${abs(request.amount)/100} credit added to customer"
    }


@router.get("/credits/balance")
async def get_customer_balance(
    current_user: User = Depends(get_current_active_user)
):
    """Get current customer balance (credits)"""
    # Get customer ID from user
    # customer_id = current_user.stripe_customer_id
    customer_id = "cus_demo"

    balance = await CustomerBalanceManager.get_balance(customer_id)

    return {
        "success": True,
        "balance": balance / 100,  # Negative = credit
        "available_credit": abs(balance) / 100 if balance < 0 else 0,
        "message": f"You have ${abs(balance)/100} in account credit" if balance < 0 else "No credits available"
    }


@router.get("/credits/transactions")
async def list_balance_transactions(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """List customer balance transactions"""
    # Get customer ID from user
    customer_id = "cus_demo"

    transactions = await CustomerBalanceManager.list_balance_transactions(
        customer_id=customer_id,
        limit=limit
    )

    return {
        "success": True,
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount / 100,
                "description": t.description,
                "created": datetime.fromtimestamp(t.created).isoformat()
            }
            for t in transactions
        ]
    }


# ============================================================================
# TAX CALCULATION ENDPOINTS
# ============================================================================

@router.post("/tax/calculate")
async def calculate_tax(
    amount: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Calculate tax for a transaction

    **Use case:** Show tax amount before checkout
    """
    # Get customer ID from user
    customer_id = "cus_demo"

    tax_data = await TaxManager.calculate_tax(
        amount=amount,
        customer_id=customer_id,
        currency="usd"
    )

    return {
        "success": True,
        "amount": amount / 100,
        "tax": tax_data["tax_amount"] / 100,
        "total": tax_data["total_amount"] / 100,
        "tax_breakdown": tax_data["tax_breakdown"]
    }
