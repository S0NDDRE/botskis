"""
Mindframe Authentication System
Complete JWT-based authentication with security best practices
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, validator
from loguru import logger
import secrets
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # Change in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UserCreate(BaseModel):
    """User registration model"""
    name: str
    email: EmailStr
    password: str
    company: Optional[str] = None
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        """Enforce password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: str
    email: str
    role: str
    exp: datetime


class User(BaseModel):
    """User model"""
    id: str
    email: EmailStr
    name: str
    role: str = "user"  # user, admin, superadmin
    subscription_tier: str = "free"  # free, pro, enterprise
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    company: Optional[str] = None


class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str
    
    @validator('new_password')
    def password_strength(cls, v):
        """Enforce password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


# ============================================================================
# AUTHENTICATION MANAGER
# ============================================================================

class AuthenticationManager:
    """
    Complete authentication system
    Handles registration, login, JWT tokens, password reset
    """
    
    def __init__(self, secret_key: str = SECRET_KEY):
        self.secret_key = secret_key
        self.pwd_context = pwd_context
        logger.info("Authentication manager initialized")
    
    # ========================================================================
    # PASSWORD HASHING
    # ========================================================================
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    # ========================================================================
    # JWT TOKEN GENERATION
    # ========================================================================
    
    def create_access_token(
        self,
        user_id: str,
        email: str,
        role: str = "user",
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": expire,
            "type": "access"
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
        logger.debug(f"Created access token for user: {user_id}")
        return encoded_jwt
    
    def create_refresh_token(
        self,
        user_id: str,
        email: str
    ) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
        logger.debug(f"Created refresh token for user: {user_id}")
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            
            user_id: str = payload.get("user_id")
            email: str = payload.get("email")
            role: str = payload.get("role", "user")
            exp: datetime = datetime.fromtimestamp(payload.get("exp"))
            
            if user_id is None or email is None:
                raise JWTError("Invalid token payload")
            
            return TokenData(
                user_id=user_id,
                email=email,
                role=role,
                exp=exp
            )
        
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            raise ValueError("Invalid or expired token")
    
    # ========================================================================
    # USER REGISTRATION
    # ========================================================================
    
    async def register_user(self, user_data: UserCreate) -> Dict:
        """
        Register a new user
        
        Returns user data and tokens
        In production, this should:
        1. Check if email exists
        2. Create user in database
        3. Send verification email
        4. Create Stripe customer
        """
        # Hash password
        hashed_password = self.hash_password(user_data.password)
        
        # Generate user ID
        user_id = f"user_{secrets.token_urlsafe(16)}"
        
        # Create user object (in production, save to database)
        user = User(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            role="user",
            subscription_tier="free",
            is_active=True,
            is_verified=False,  # Should verify email first
            created_at=datetime.utcnow(),
            company=user_data.company
        )
        
        # Generate tokens
        access_token = self.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role
        )
        
        refresh_token = self.create_refresh_token(
            user_id=user.id,
            email=user.email
        )
        
        logger.info(f"New user registered: {user.email}")
        
        return {
            "user": user.dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "hashed_password": hashed_password  # Save this to database
        }
    
    # ========================================================================
    # USER LOGIN
    # ========================================================================
    
    async def login_user(
        self,
        email: str,
        password: str,
        stored_password_hash: str,
        user_data: Dict
    ) -> Token:
        """
        Authenticate user and return tokens
        
        Args:
            email: User email
            password: Plain password
            stored_password_hash: Hashed password from database
            user_data: User data from database
        """
        # Verify password
        if not self.verify_password(password, stored_password_hash):
            logger.warning(f"Failed login attempt for: {email}")
            raise ValueError("Incorrect email or password")
        
        # Check if user is active
        if not user_data.get("is_active", True):
            raise ValueError("Account is disabled")
        
        # Generate tokens
        access_token = self.create_access_token(
            user_id=user_data["id"],
            email=email,
            role=user_data.get("role", "user")
        )
        
        refresh_token = self.create_refresh_token(
            user_id=user_data["id"],
            email=email
        )
        
        logger.info(f"User logged in: {email}")
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    # ========================================================================
    # TOKEN REFRESH
    # ========================================================================
    
    async def refresh_access_token(self, refresh_token: str) -> str:
        """Generate new access token from refresh token"""
        try:
            # Verify refresh token
            token_data = self.verify_token(refresh_token)
            
            # Create new access token
            access_token = self.create_access_token(
                user_id=token_data.user_id,
                email=token_data.email,
                role=token_data.role
            )
            
            logger.debug(f"Refreshed access token for: {token_data.email}")
            return access_token
        
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise ValueError("Invalid refresh token")
    
    # ========================================================================
    # PASSWORD RESET
    # ========================================================================
    
    def generate_reset_token(self, email: str) -> str:
        """Generate password reset token"""
        expire = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "password_reset"
        }
        
        token = jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
        logger.info(f"Generated password reset token for: {email}")
        return token
    
    async def verify_reset_token(self, token: str) -> str:
        """Verify password reset token and return email"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            
            email = payload.get("email")
            token_type = payload.get("type")
            
            if not email or token_type != "password_reset":
                raise ValueError("Invalid reset token")
            
            return email
        
        except JWTError as e:
            logger.error(f"Reset token verification failed: {e}")
            raise ValueError("Invalid or expired reset token")
    
    async def reset_password(
        self,
        reset_token: str,
        new_password: str
    ) -> str:
        """Reset password using reset token"""
        # Verify token and get email
        email = await self.verify_reset_token(reset_token)
        
        # Hash new password
        hashed_password = self.hash_password(new_password)
        
        logger.info(f"Password reset for: {email}")
        
        # In production: update password in database
        return hashed_password
    
    # ========================================================================
    # EMAIL VERIFICATION
    # ========================================================================
    
    def generate_verification_token(self, email: str) -> str:
        """Generate email verification token"""
        expire = datetime.utcnow() + timedelta(days=7)  # 7 days
        
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "email_verification"
        }
        
        token = jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
        logger.info(f"Generated verification token for: {email}")
        return token
    
    async def verify_email_token(self, token: str) -> str:
        """Verify email verification token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            
            email = payload.get("email")
            token_type = payload.get("type")
            
            if not email or token_type != "email_verification":
                raise ValueError("Invalid verification token")
            
            logger.info(f"Email verified: {email}")
            return email
        
        except JWTError as e:
            logger.error(f"Email verification failed: {e}")
            raise ValueError("Invalid or expired verification token")
    
    # ========================================================================
    # ROLE-BASED ACCESS CONTROL
    # ========================================================================
    
    def check_permission(
        self,
        user_role: str,
        required_role: str
    ) -> bool:
        """Check if user has required role"""
        role_hierarchy = {
            "user": 0,
            "admin": 1,
            "superadmin": 2
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        has_permission = user_level >= required_level
        
        if not has_permission:
            logger.warning(f"Permission denied: {user_role} < {required_role}")
        
        return has_permission
    
    # ========================================================================
    # SESSION MANAGEMENT
    # ========================================================================
    
    async def logout_user(self, user_id: str, token: str):
        """
        Logout user
        In production, this should:
        1. Blacklist the token
        2. Clear session from Redis/cache
        """
        logger.info(f"User logged out: {user_id}")
        # In production: add token to blacklist in Redis
        return True
    
    async def logout_all_sessions(self, user_id: str):
        """Logout user from all devices"""
        logger.info(f"All sessions terminated for user: {user_id}")
        # In production: blacklist all tokens for user
        return True


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

class SecurityUtils:
    """Additional security utilities"""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate API key for external integrations"""
        return f"mf_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate session ID"""
        return secrets.token_urlsafe(24)
    
    @staticmethod
    def check_password_pwned(password: str) -> bool:
        """
        Check if password has been pwned (leaked)
        Uses haveibeenpwned API (implement in production)
        """
        # In production: check against haveibeenpwned API
        # For now, just return False
        return False
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize and normalize email"""
        return email.lower().strip()
    
    @staticmethod
    def generate_invite_token() -> str:
        """Generate team invite token"""
        return secrets.token_urlsafe(16)


# ============================================================================
# RATE LIMITING (In-memory, use Redis in production)
# ============================================================================

class RateLimiter:
    """Simple rate limiter for login attempts"""
    
    def __init__(self):
        self.attempts = {}  # In production: use Redis
    
    async def check_rate_limit(
        self,
        identifier: str,  # email or IP
        max_attempts: int = 5,
        window_minutes: int = 15
    ) -> bool:
        """Check if identifier has exceeded rate limit"""
        now = datetime.utcnow()
        
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Remove old attempts
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if (now - attempt).seconds < window_minutes * 60
        ]
        
        # Check limit
        if len(self.attempts[identifier]) >= max_attempts:
            logger.warning(f"Rate limit exceeded for: {identifier}")
            return False
        
        # Record attempt
        self.attempts[identifier].append(now)
        return True
    
    async def reset_rate_limit(self, identifier: str):
        """Reset rate limit for identifier"""
        if identifier in self.attempts:
            del self.attempts[identifier]


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Register user
    auth = AuthenticationManager()
    
    # Create user
    user_data = UserCreate(
        name="John Doe",
        email="john@example.com",
        password="SecurePass123",
        company="Acme Inc"
    )
    
    # This would be async in production
    # result = await auth.register_user(user_data)
    # print(result)
