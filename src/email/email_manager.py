"""
Mindframe Email System
Complete email management with SendGrid
"""
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from pydantic import BaseModel, EmailStr
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment
import base64

# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

class EmailTemplate:
    """Email templates for different use cases"""
    
    # Welcome Email
    WELCOME = {
        "subject": "Welcome to Mindframe! 🚀",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9fafb; padding: 30px; }
        .button { display: inline-block; background: #8B5CF6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { background: #f3f4f6; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Mindframe!</h1>
        </div>
        <div class="content">
            <p>Hi {{name}},</p>
            
            <p>Welcome to Mindframe - the AI Agent Automation Platform! 🎉</p>
            
            <p>We're excited to have you on board. Here's what you can do next:</p>
            
            <ul>
                <li><strong>Create your first AI agent</strong> in natural language</li>
                <li><strong>Explore Mindframe Academy</strong> - 24 free courses</li>
                <li><strong>Browse the Marketplace</strong> - 20+ pre-built agents</li>
                <li><strong>Connect your tools</strong> - 40+ integrations</li>
            </ul>
            
            <a href="{{dashboard_url}}" class="button">Go to Dashboard</a>
            
            <p>Need help? Check out our <a href="{{academy_url}}">Academy</a> or <a href="{{support_url}}">contact support</a>.</p>
            
            <p>Best regards,<br>The Mindframe Team</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 Mindframe. All rights reserved.</p>
            <p><a href="{{unsubscribe_url}}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
        """
    }
    
    # Email Verification
    EMAIL_VERIFICATION = {
        "subject": "Verify your Mindframe email",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #8B5CF6; color: white; padding: 20px; text-align: center; }
        .content { background: #fff; padding: 30px; border: 1px solid #e5e7eb; }
        .button { display: inline-block; background: #10B981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .code { background: #f3f4f6; padding: 15px; font-size: 24px; letter-spacing: 5px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Verify Your Email</h2>
        </div>
        <div class="content">
            <p>Hi {{name}},</p>
            
            <p>Please verify your email address to activate your Mindframe account.</p>
            
            <p>Click the button below or use the verification code:</p>
            
            <div class="code">{{verification_code}}</div>
            
            <a href="{{verification_url}}" class="button">Verify Email</a>
            
            <p><small>This link expires in 7 days.</small></p>
            
            <p>If you didn't create this account, you can safely ignore this email.</p>
        </div>
    </div>
</body>
</html>
        """
    }
    
    # Password Reset
    PASSWORD_RESET = {
        "subject": "Reset your Mindframe password",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .content { padding: 30px; background: #fff; border: 1px solid #e5e7eb; }
        .button { display: inline-block; background: #EF4444; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .warning { background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <h2>Reset Your Password</h2>
            
            <p>Hi {{name}},</p>
            
            <p>We received a request to reset your password. Click the button below to create a new password:</p>
            
            <a href="{{reset_url}}" class="button">Reset Password</a>
            
            <p><small>This link expires in 1 hour.</small></p>
            
            <div class="warning">
                <strong>⚠️ Security Notice:</strong> If you didn't request this, someone may be trying to access your account. Please secure your account immediately.
            </div>
            
            <p>Best regards,<br>The Mindframe Team</p>
        </div>
    </div>
</body>
</html>
        """
    }
    
    # Subscription Success
    SUBSCRIPTION_SUCCESS = {
        "subject": "Welcome to Mindframe {{plan}}! 🎉",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #fff; }
        .plan-details { background: #f3f4f6; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .feature { padding: 10px 0; border-bottom: 1px solid #e5e7eb; }
        .button { display: inline-block; background: #8B5CF6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to {{plan}}!</h1>
        </div>
        <div class="content">
            <p>Hi {{name}},</p>
            
            <p>Your subscription to Mindframe {{plan}} is now active! Thank you for upgrading.</p>
            
            <div class="plan-details">
                <h3>Your Plan Details:</h3>
                <div class="feature">✓ {{plan}} Plan</div>
                <div class="feature">✓ ${{price}}/month</div>
                <div class="feature">✓ Next billing: {{next_billing_date}}</div>
            </div>
            
            <h3>What's Included:</h3>
            <ul>
                {{features_list}}
            </ul>
            
            <a href="{{dashboard_url}}" class="button">Start Building</a>
            
            <p>Have questions? <a href="{{support_url}}">Contact our support team</a>.</p>
            
            <p>Best regards,<br>The Mindframe Team</p>
        </div>
    </div>
</body>
</html>
        """
    }
    
    # Payment Failed
    PAYMENT_FAILED = {
        "subject": "Payment failed for your Mindframe subscription",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .alert { background: #FEE2E2; border-left: 4px solid #EF4444; padding: 20px; margin: 20px 0; }
        .button { display: inline-block; background: #EF4444; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Payment Issue</h2>
        
        <div class="alert">
            <p><strong>⚠️ Payment Failed</strong></p>
            <p>We were unable to process your payment for Mindframe {{plan}}.</p>
        </div>
        
        <p>Hi {{name}},</p>
        
        <p>We attempted to charge your payment method on file but the payment failed.</p>
        
        <p><strong>Why this might happen:</strong></p>
        <ul>
            <li>Insufficient funds</li>
            <li>Expired card</li>
            <li>Card declined by bank</li>
        </ul>
        
        <p>Please update your payment method to continue using Mindframe {{plan}}.</p>
        
        <a href="{{billing_url}}" class="button">Update Payment Method</a>
        
        <p><small>Your account will be downgraded to Free if payment is not received within 7 days.</small></p>
        
        <p>Need help? <a href="{{support_url}}">Contact support</a>.</p>
        
        <p>Best regards,<br>The Mindframe Team</p>
    </div>
</body>
</html>
        """
    }
    
    # Invoice Receipt
    INVOICE_RECEIPT = {
        "subject": "Invoice for Mindframe {{plan}} - {{invoice_number}}",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .invoice { background: #fff; border: 1px solid #e5e7eb; padding: 30px; }
        .invoice-header { border-bottom: 2px solid #8B5CF6; padding-bottom: 20px; margin-bottom: 20px; }
        .invoice-details { margin: 20px 0; }
        .total { background: #f3f4f6; padding: 15px; font-size: 20px; font-weight: bold; margin-top: 20px; }
        .button { display: inline-block; background: #8B5CF6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="invoice">
            <div class="invoice-header">
                <h1>INVOICE</h1>
                <p>Invoice #{{invoice_number}}</p>
                <p>Date: {{invoice_date}}</p>
            </div>
            
            <div class="invoice-details">
                <p><strong>Bill To:</strong><br>
                {{customer_name}}<br>
                {{customer_email}}<br>
                {{customer_company}}</p>
                
                <p><strong>Description:</strong><br>
                Mindframe {{plan}} Subscription<br>
                Period: {{billing_period}}</p>
                
                <div class="total">
                    Total: ${{amount}}
                </div>
            </div>
            
            <p>Payment Status: <strong style="color: #10B981;">PAID</strong></p>
            
            <a href="{{invoice_pdf_url}}" class="button">Download PDF</a>
            
            <p>Thank you for your business!</p>
            
            <p>Questions? <a href="{{support_url}}">Contact support</a></p>
        </div>
    </div>
</body>
</html>
        """
    }
    
    # New Agent Created
    AGENT_CREATED = {
        "subject": "Your AI agent '{{agent_name}}' is ready! 🤖",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .success { background: #D1FAE5; border-left: 4px solid #10B981; padding: 20px; margin: 20px 0; }
        .button { display: inline-block; background: #8B5CF6; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">
            <h2>🤖 Your AI Agent is Live!</h2>
        </div>
        
        <p>Hi {{name}},</p>
        
        <p>Great news! Your AI agent <strong>{{agent_name}}</strong> has been created and deployed successfully.</p>
        
        <p><strong>Agent Details:</strong></p>
        <ul>
            <li>Name: {{agent_name}}</li>
            <li>Type: {{agent_type}}</li>
            <li>Status: Active ✅</li>
            <li>Created: {{created_date}}</li>
        </ul>
        
        <a href="{{agent_url}}" class="button">View Agent Dashboard</a>
        
        <p>Your agent is now working 24/7 to help automate your workflows!</p>
        
        <p>Best regards,<br>The Mindframe Team</p>
    </div>
</body>
</html>
        """
    }
    
    # Course Certificate
    CERTIFICATE_EARNED = {
        "subject": "Congratulations! You earned: {{certificate_name}} 🎓",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .certificate { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; padding: 40px; text-align: center; border-radius: 10px; }
        .button { display: inline-block; background: #10B981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="certificate">
            <h1>🎓 Congratulations!</h1>
            <h2>{{certificate_name}}</h2>
            <p>Earned by {{name}}</p>
            <p>{{completion_date}}</p>
        </div>
        
        <div style="padding: 30px;">
            <p>Well done! You've successfully completed <strong>{{course_name}}</strong> and earned your certificate.</p>
            
            <p><strong>What's next?</strong></p>
            <ul>
                <li>Download and share your certificate</li>
                <li>Add it to your LinkedIn profile</li>
                <li>Continue learning with our other courses</li>
            </ul>
            
            <a href="{{certificate_url}}" class="button">Download Certificate</a>
            
            <p>Keep learning and automating!</p>
            
            <p>Best regards,<br>The Mindframe Academy Team</p>
        </div>
    </div>
</body>
</html>
        """
    }


# ============================================================================
# EMAIL MANAGER
# ============================================================================

class EmailManager:
    """
    Complete email management system using SendGrid
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        logger.info("Email manager initialized")
    
    def _replace_template_vars(self, template: str, variables: Dict) -> str:
        """Replace template variables with actual values"""
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: str = "hello@mindframe.ai",
        from_name: str = "Mindframe",
        attachments: Optional[List[Dict]] = None
    ) -> bool:
        """Send email via SendGrid"""
        try:
            message = Mail(
                from_email=Email(from_email, from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    message.add_attachment(Attachment(
                        file_content=attachment.get("content"),
                        file_name=attachment.get("filename"),
                        file_type=attachment.get("type", "application/pdf")
                    ))
            
            response = self.sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent to {to_email}: {subject}")
                return True
            else:
                logger.error(f"Email failed: {response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"Email error: {e}")
            return False
    
    # ========================================================================
    # TEMPLATE EMAILS
    # ========================================================================
    
    async def send_welcome_email(
        self,
        to_email: str,
        name: str,
        dashboard_url: str
    ) -> bool:
        """Send welcome email to new user"""
        template = EmailTemplate.WELCOME
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                "dashboard_url": dashboard_url,
                "academy_url": f"{dashboard_url}/academy",
                "support_url": "https://mindframe.ai/support",
                "unsubscribe_url": f"{dashboard_url}/settings/notifications"
            }
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=template["subject"],
            html_content=html_content
        )
    
    async def send_verification_email(
        self,
        to_email: str,
        name: str,
        verification_url: str,
        verification_code: str
    ) -> bool:
        """Send email verification"""
        template = EmailTemplate.EMAIL_VERIFICATION
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                "verification_url": verification_url,
                "verification_code": verification_code
            }
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=template["subject"],
            html_content=html_content
        )
    
    async def send_password_reset_email(
        self,
        to_email: str,
        name: str,
        reset_url: str
    ) -> bool:
        """Send password reset email"""
        template = EmailTemplate.PASSWORD_RESET
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                "reset_url": reset_url
            }
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=template["subject"],
            html_content=html_content
        )
    
    async def send_subscription_success_email(
        self,
        to_email: str,
        name: str,
        plan: str,
        price: float,
        next_billing_date: str,
        features: List[str],
        dashboard_url: str
    ) -> bool:
        """Send subscription success email"""
        template = EmailTemplate.SUBSCRIPTION_SUCCESS
        
        features_html = "".join([f"<li>{feature}</li>" for feature in features])
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                "plan": plan.capitalize(),
                "price": price,
                "next_billing_date": next_billing_date,
                "features_list": features_html,
                "dashboard_url": dashboard_url,
                "support_url": "https://mindframe.ai/support"
            }
        )
        
        subject = self._replace_template_vars(
            template["subject"],
            {"plan": plan.capitalize()}
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
    
    async def send_payment_failed_email(
        self,
        to_email: str,
        name: str,
        plan: str,
        billing_url: str
    ) -> bool:
        """Send payment failed notification"""
        template = EmailTemplate.PAYMENT_FAILED
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                "plan": plan.capitalize(),
                "billing_url": billing_url,
                "support_url": "https://mindframe.ai/support"
            }
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=template["subject"],
            html_content=html_content
        )
    
    async def send_invoice_receipt(
        self,
        to_email: str,
        invoice_data: Dict
    ) -> bool:
        """Send invoice receipt"""
        template = EmailTemplate.INVOICE_RECEIPT
        
        html_content = self._replace_template_vars(
            template["html"],
            invoice_data
        )
        
        subject = self._replace_template_vars(
            template["subject"],
            invoice_data
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
    
    async def send_agent_created_email(
        self,
        to_email: str,
        name: str,
        agent_data: Dict
    ) -> bool:
        """Send agent created notification"""
        template = EmailTemplate.AGENT_CREATED
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                **agent_data
            }
        )
        
        subject = self._replace_template_vars(
            template["subject"],
            agent_data
        )
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
    
    async def send_certificate_email(
        self,
        to_email: str,
        name: str,
        certificate_data: Dict,
        certificate_pdf: Optional[bytes] = None
    ) -> bool:
        """Send certificate earned email"""
        template = EmailTemplate.CERTIFICATE_EARNED
        
        html_content = self._replace_template_vars(
            template["html"],
            {
                "name": name,
                **certificate_data
            }
        )
        
        subject = self._replace_template_vars(
            template["subject"],
            certificate_data
        )
        
        # Attach PDF if provided
        attachments = None
        if certificate_pdf:
            attachments = [{
                "content": base64.b64encode(certificate_pdf).decode(),
                "filename": f"certificate_{certificate_data.get('certificate_name', 'mindframe')}.pdf",
                "type": "application/pdf"
            }]
        
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            attachments=attachments
        )
