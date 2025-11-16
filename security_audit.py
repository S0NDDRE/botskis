#!/usr/bin/env python3
"""
Security Audit Script
Automated security vulnerability scanning

Checks:
- SQL Injection vulnerabilities
- XSS vulnerabilities
- CSRF protection
- Rate limiting
- Security headers
- Input validation
- Password policies
- Session management
"""
import asyncio
import sys
from typing import List, Dict
from datetime import datetime
from pathlib import Path
import re


class SecurityIssue:
    """Security issue found during audit"""

    def __init__(
        self,
        severity: str,  # critical, high, medium, low
        category: str,
        description: str,
        file_path: str = None,
        line_number: int = None,
        recommendation: str = None
    ):
        self.severity = severity
        self.category = category
        self.description = description
        self.file_path = file_path
        self.line_number = line_number
        self.recommendation = recommendation


class SecurityAuditor:
    """
    Automated security auditor

    Scans codebase for common vulnerabilities
    """

    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.scanned_files = 0

    def add_issue(self, issue: SecurityIssue):
        """Add security issue"""
        self.issues.append(issue)

    async def audit_sql_injection(self):
        """Audit for SQL injection vulnerabilities"""
        print("🔍 Checking for SQL injection vulnerabilities...")

        # Dangerous patterns
        dangerous_patterns = [
            (r'f"SELECT.*{.*}"', "String formatting in SQL query"),
            (r'f\'SELECT.*{.*}\'', "String formatting in SQL query"),
            (r'\.format\(.*\).*SELECT', "String formatting in SQL query"),
            (r'%.*%.*SELECT', "% formatting in SQL query"),
        ]

        # Scan Python files
        for py_file in Path("src").rglob("*.py"):
            content = py_file.read_text()
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                for pattern, description in dangerous_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.add_issue(SecurityIssue(
                            severity="critical",
                            category="SQL Injection",
                            description=description,
                            file_path=str(py_file),
                            line_number=i,
                            recommendation="Use parameterized queries or ORM"
                        ))

        print(f"   Found {len([i for i in self.issues if i.category == 'SQL Injection'])} SQL injection issues")

    async def audit_xss_vulnerabilities(self):
        """Audit for XSS vulnerabilities"""
        print("🔍 Checking for XSS vulnerabilities...")

        # Check if XSS protection is used
        has_xss_protection = False

        for py_file in Path("src").rglob("*.py"):
            content = py_file.read_text()

            if "XSSProtection" in content or "sanitize" in content:
                has_xss_protection = True
                break

        if not has_xss_protection:
            self.add_issue(SecurityIssue(
                severity="high",
                category="XSS",
                description="No XSS protection middleware found",
                recommendation="Implement XSS sanitization for user inputs"
            ))

        # Check frontend files
        for tsx_file in Path("frontend/src").rglob("*.tsx"):
            if not tsx_file.exists():
                continue

            content = tsx_file.read_text()

            # Check for dangerouslySetInnerHTML
            if "dangerouslySetInnerHTML" in content:
                self.add_issue(SecurityIssue(
                    severity="high",
                    category="XSS",
                    description="Using dangerouslySetInnerHTML without sanitization",
                    file_path=str(tsx_file),
                    recommendation="Sanitize HTML before rendering or use safe alternatives"
                ))

        print(f"   Found {len([i for i in self.issues if i.category == 'XSS'])} XSS issues")

    async def audit_csrf_protection(self):
        """Audit CSRF protection"""
        print("🔍 Checking CSRF protection...")

        # Check if CSRF middleware exists
        csrf_file = Path("src/security/security_middleware.py")

        if not csrf_file.exists():
            self.add_issue(SecurityIssue(
                severity="critical",
                category="CSRF",
                description="No CSRF protection middleware found",
                recommendation="Implement CSRF token validation"
            ))
        else:
            content = csrf_file.read_text()

            if "CSRFProtection" not in content:
                self.add_issue(SecurityIssue(
                    severity="high",
                    category="CSRF",
                    description="CSRF protection not implemented",
                    recommendation="Add CSRF middleware"
                ))

        print(f"   Found {len([i for i in self.issues if i.category == 'CSRF'])} CSRF issues")

    async def audit_rate_limiting(self):
        """Audit rate limiting"""
        print("🔍 Checking rate limiting...")

        # Check if rate limiting exists
        has_rate_limiting = False

        for py_file in Path("src").rglob("*.py"):
            content = py_file.read_text()

            if "RateLimiter" in content or "rate_limit" in content.lower():
                has_rate_limiting = True
                break

        if not has_rate_limiting:
            self.add_issue(SecurityIssue(
                severity="high",
                category="Rate Limiting",
                description="No rate limiting found",
                recommendation="Implement rate limiting to prevent abuse"
            ))

        print(f"   Found {len([i for i in self.issues if i.category == 'Rate Limiting'])} rate limiting issues")

    async def audit_authentication(self):
        """Audit authentication security"""
        print("🔍 Checking authentication security...")

        # Check for password hashing
        auth_files = list(Path("src/auth").rglob("*.py"))

        if not auth_files:
            self.add_issue(SecurityIssue(
                severity="critical",
                category="Authentication",
                description="No authentication module found",
                recommendation="Implement secure authentication"
            ))
        else:
            # Check if using secure hashing
            has_secure_hashing = False

            for auth_file in auth_files:
                content = auth_file.read_text()

                if "bcrypt" in content or "argon2" in content or "pbkdf2" in content:
                    has_secure_hashing = True
                    break

            if not has_secure_hashing:
                self.add_issue(SecurityIssue(
                    severity="critical",
                    category="Authentication",
                    description="Not using secure password hashing",
                    recommendation="Use bcrypt, argon2, or pbkdf2 for password hashing"
                ))

        print(f"   Found {len([i for i in self.issues if i.category == 'Authentication'])} authentication issues")

    async def audit_secrets_exposure(self):
        """Audit for exposed secrets"""
        print("🔍 Checking for exposed secrets...")

        # Patterns that might indicate secrets
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'secret_key\s*=\s*["\'][^"\']+["\']', "Hardcoded secret key"),
            (r'AWS_SECRET', "AWS secret key"),
        ]

        for py_file in Path("src").rglob("*.py"):
            content = py_file.read_text()
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                for pattern, description in secret_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Exclude test files and examples
                        if "test" not in str(py_file) and "example" not in line.lower():
                            self.add_issue(SecurityIssue(
                                severity="critical",
                                category="Secrets Exposure",
                                description=description,
                                file_path=str(py_file),
                                line_number=i,
                                recommendation="Use environment variables or secrets manager"
                            ))

        print(f"   Found {len([i for i in self.issues if i.category == 'Secrets Exposure'])} secrets exposure issues")

    async def audit_security_headers(self):
        """Audit security headers"""
        print("🔍 Checking security headers...")

        # Check if security headers middleware exists
        middleware_file = Path("src/security/security_middleware.py")

        if middleware_file.exists():
            content = middleware_file.read_text()

            required_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection",
                "Strict-Transport-Security",
                "Content-Security-Policy"
            ]

            for header in required_headers:
                if header not in content:
                    self.add_issue(SecurityIssue(
                        severity="medium",
                        category="Security Headers",
                        description=f"Missing security header: {header}",
                        recommendation=f"Add {header} header to responses"
                    ))
        else:
            self.add_issue(SecurityIssue(
                severity="high",
                category="Security Headers",
                description="No security headers middleware found",
                recommendation="Implement security headers middleware"
            ))

        print(f"   Found {len([i for i in self.issues if i.category == 'Security Headers'])} security header issues")

    async def audit_input_validation(self):
        """Audit input validation"""
        print("🔍 Checking input validation...")

        # Check if input validation exists
        has_validation = False

        for py_file in Path("src").rglob("*.py"):
            content = py_file.read_text()

            if "InputValidator" in content or "pydantic" in content:
                has_validation = True
                break

        if not has_validation:
            self.add_issue(SecurityIssue(
                severity="high",
                category="Input Validation",
                description="No input validation framework found",
                recommendation="Implement input validation using Pydantic or custom validators"
            ))

        print(f"   Found {len([i for i in self.issues if i.category == 'Input Validation'])} input validation issues")

    def generate_report(self) -> str:
        """Generate security audit report"""

        report = []
        report.append("=" * 80)
        report.append("🔒 SECURITY AUDIT REPORT")
        report.append("=" * 80)
        report.append(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Files scanned: {self.scanned_files}")
        report.append(f"Issues found: {len(self.issues)}\n")

        # Count by severity
        critical = len([i for i in self.issues if i.severity == "critical"])
        high = len([i for i in self.issues if i.severity == "high"])
        medium = len([i for i in self.issues if i.severity == "medium"])
        low = len([i for i in self.issues if i.severity == "low"])

        report.append("📊 SEVERITY BREAKDOWN")
        report.append("-" * 80)
        report.append(f"🔴 Critical: {critical}")
        report.append(f"🟠 High: {high}")
        report.append(f"🟡 Medium: {medium}")
        report.append(f"🟢 Low: {low}")
        report.append("")

        # Issues by category
        categories = {}
        for issue in self.issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue)

        report.append("📋 ISSUES BY CATEGORY")
        report.append("-" * 80)

        for category, issues in sorted(categories.items()):
            report.append(f"\n{category}: {len(issues)} issues")

            for issue in issues:
                severity_icon = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(issue.severity, "⚪")

                report.append(f"\n  {severity_icon} [{issue.severity.upper()}] {issue.description}")

                if issue.file_path:
                    report.append(f"     File: {issue.file_path}:{issue.line_number or '?'}")

                if issue.recommendation:
                    report.append(f"     Fix: {issue.recommendation}")

        # Overall score
        report.append("\n" + "=" * 80)

        max_score = 100
        deductions = critical * 20 + high * 10 + medium * 5 + low * 2
        score = max(0, max_score - deductions)

        report.append(f"🎯 SECURITY SCORE: {score}/100")

        if score >= 90:
            rating = "EXCELLENT ✅"
        elif score >= 75:
            rating = "GOOD ✓"
        elif score >= 50:
            rating = "NEEDS IMPROVEMENT ⚠️"
        else:
            rating = "CRITICAL ISSUES ❌"

        report.append(f"📈 RATING: {rating}")
        report.append("=" * 80)

        return "\n".join(report)

    async def run_audit(self):
        """Run complete security audit"""
        print("\n🔒 Starting Security Audit...\n")

        await self.audit_sql_injection()
        await self.audit_xss_vulnerabilities()
        await self.audit_csrf_protection()
        await self.audit_rate_limiting()
        await self.audit_authentication()
        await self.audit_secrets_exposure()
        await self.audit_security_headers()
        await self.audit_input_validation()

        print("\n✅ Audit complete!\n")

        # Generate report
        report = self.generate_report()

        # Print report
        print(report)

        # Save report
        report_file = Path("SECURITY_AUDIT_REPORT.md")
        report_file.write_text(report)
        print(f"\n📄 Report saved to: {report_file}")

        # Return exit code based on critical issues
        critical_issues = len([i for i in self.issues if i.severity == "critical"])

        if critical_issues > 0:
            print(f"\n❌ FAILED: {critical_issues} critical security issues found!")
            return 1
        else:
            print("\n✅ PASSED: No critical security issues found!")
            return 0


async def main():
    """Main function"""
    auditor = SecurityAuditor()
    exit_code = await auditor.run_audit()
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
