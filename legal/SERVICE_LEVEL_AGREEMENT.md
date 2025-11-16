# SERVICE LEVEL AGREEMENT (SLA)

**Last Updated:** November 16, 2025
**Effective Date:** November 16, 2025

---

## AGREEMENT OVERVIEW

This Service Level Agreement ("SLA") is between Mindframe AI and all users of the Mindframe AI platform ("Services"). This SLA defines the service levels, uptime commitments, support response times, and remedies available to customers.

**Service Provider:**
- **Company:** Mindframe AI
- **Founder:** Sondre Kjær
- **Email:** hello@mframe.io
- **Website:** https://mindframe.ai / https://mframe.io

---

## 1. DEFINITIONS

**"Availability"** means the percentage of time the Services are operational and accessible during a calendar month.

**"Downtime"** means any period when the Services are unavailable, excluding Scheduled Maintenance and Exceptions.

**"Scheduled Maintenance"** means planned maintenance notified at least 48 hours in advance.

**"Monthly Uptime Percentage"** means total minutes in month minus Downtime minutes, divided by total minutes in month, expressed as a percentage.

**"Service Credit"** means the compensation provided for failure to meet SLA commitments.

**"Critical Failure"** means complete unavailability of core platform functionality.

**"Degraded Performance"** means reduced performance but continued availability.

---

## 2. SERVICE AVAILABILITY COMMITMENT

### 2.1 Uptime Guarantee

| Service Tier | Uptime Commitment | Maximum Downtime/Month |
|--------------|-------------------|------------------------|
| **Free Tier** | 95.0% | ~36 hours |
| **Starter** | 99.0% | ~7.2 hours |
| **Professional** | 99.5% | ~3.6 hours |
| **Enterprise** | 99.9% | ~43 minutes |

### 2.2 Service Components

**Core Platform:**
- API endpoints
- Web application
- Authentication system
- Database access
- File storage

**Income Bots:**
- Freelance Bot operations
- Testing Bot operations
- Survey Bot operations
- Writing Bot operations
- Income tracking and dashboard

**Marketplace:**
- Agent browsing and search
- Agent installation
- Agent management

**Learning Platform:**
- Course access
- Video streaming
- Quiz functionality
- Certificate generation

### 2.3 Excluded from Uptime Calculation

- Scheduled Maintenance (notified 48h+ in advance)
- Force majeure events
- Customer's internet connectivity issues
- Third-party service failures (if beyond our control)
- Customer's misuse or unauthorized modifications
- Beta or experimental features
- Suspension due to Terms of Service violations

---

## 3. SCHEDULED MAINTENANCE

### 3.1 Maintenance Windows

**Standard Maintenance:**
- **Frequency:** Monthly
- **Duration:** Maximum 2 hours
- **Timing:** Typically Sundays 02:00-04:00 CET (lowest traffic period)
- **Notice:** Minimum 48 hours advance notice

**Emergency Maintenance:**
- **Timing:** As needed for critical security or stability issues
- **Notice:** Best effort notification, minimum 2 hours when possible

### 3.2 Notification Methods

- Email to account holders
- Status page: https://status.mindframe.ai
- In-app notification banner
- Twitter: @mindframeai

---

## 4. PERFORMANCE STANDARDS

### 4.1 API Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| **API Response Time (p95)** | <500ms | 95th percentile |
| **API Response Time (p99)** | <1000ms | 99th percentile |
| **API Error Rate** | <0.5% | Errors per total requests |
| **Throughput** | 1000 req/sec/instance | Sustained load |

### 4.2 Web Application Performance

| Metric | Target |
|--------|--------|
| **Page Load Time (p95)** | <3 seconds |
| **Time to Interactive (p95)** | <5 seconds |
| **First Contentful Paint** | <1.5 seconds |

### 4.3 Income Bot Performance

| Bot Type | Expected Performance |
|----------|---------------------|
| **Freelance Bot** | Process 50+ jobs/hour |
| **Testing Bot** | Complete 15+ tests/day |
| **Survey Bot** | Complete 30+ surveys/day |
| **Writing Bot** | Generate 10+ articles/day |

*Note: Actual performance depends on platform availability and job availability.*

---

## 5. SUPPORT RESPONSE TIMES

### 5.1 Support Tiers

| Priority | Description | Response Time | Resolution Target |
|----------|-------------|---------------|-------------------|
| **P1 - Critical** | Complete service outage | 1 hour | 4 hours |
| **P2 - High** | Major functionality impaired | 4 hours | 24 hours |
| **P3 - Normal** | Minor issue, workaround exists | 24 hours | 72 hours |
| **P4 - Low** | General question, feature request | 48 hours | Best effort |

### 5.2 Support Availability

**Free Tier:**
- Email support only
- Business hours (09:00-17:00 CET, Monday-Friday)
- Response time: P3 and P4 only

**Starter:**
- Email support
- Business hours
- Response time: P2, P3, P4

**Professional:**
- Email and chat support
- Extended hours (08:00-20:00 CET, Monday-Saturday)
- Response time: P1, P2, P3, P4

**Enterprise:**
- Email, chat, and phone support
- 24/7 support
- Dedicated account manager
- Response time: P1, P2, P3, P4
- Priority escalation

### 5.3 Support Channels

- **Email:** hello@mframe.io
- **Live Chat:** Available in platform (Professional and Enterprise)
- **Phone:** +47-XXX-XXXXX (Enterprise only)
- **Status Page:** https://status.mindframe.ai
- **Knowledge Base:** https://docs.mindframe.ai

---

## 6. SERVICE CREDITS

### 6.1 Credit Eligibility

Service Credits apply when Monthly Uptime Percentage falls below commitment:

| Monthly Uptime % | Service Credit | Max Credit per Month |
|------------------|----------------|----------------------|
| **99.9% - 99.0%** | 10% of monthly fee | 10% |
| **99.0% - 95.0%** | 25% of monthly fee | 25% |
| **95.0% - 90.0%** | 50% of monthly fee | 50% |
| **< 90.0%** | 100% of monthly fee | 100% |

### 6.2 Credit Calculation Example

**Scenario:** Professional plan ($99/month), 99.3% uptime (target: 99.5%)
- **Shortfall:** Falls in 99.9%-99.0% range
- **Credit:** 10% of monthly fee = $9.90
- **Applied:** As credit to next month's invoice

### 6.3 Credit Claim Process

To claim Service Credits:

1. **Submit Claim** within 30 days of incident
2. **Email:** hello@mframe.io
3. **Subject:** "SLA Credit Claim - [Month/Year]"
4. **Include:**
   - Account email
   - Dates/times of downtime experienced
   - Description of impact
   - Evidence (screenshots, logs if available)

**Review Timeline:** Claims reviewed within 15 business days

**Credit Issued:** Applied to next monthly invoice or refunded if account closed

### 6.4 Credit Limitations

Service Credits are:
-  The **sole remedy** for SLA violations
-  Capped at 100% of monthly fees
-  Valid only for paid subscriptions (not Free Tier)
- L Not redeemable for cash
- L Not transferable

---

## 7. MONITORING AND REPORTING

### 7.1 Status Page

**Public Status Page:** https://status.mindframe.ai

**Real-time Information:**
- Current system status (operational/degraded/down)
- Component-level status
- Incident history
- Scheduled maintenance calendar
- Performance metrics (response times, error rates)

**Subscribe to Updates:**
- Email notifications
- SMS alerts (Enterprise)
- Slack integration (Enterprise)
- RSS feed

### 7.2 Uptime Monitoring

Mindframe AI monitors availability using:
- **External monitoring:** Third-party uptime monitors (Pingdom, UptimeRobot)
- **Internal monitoring:** Datadog, Sentry
- **Geographic monitoring:** Multiple monitoring locations
- **Frequency:** 60-second checks

### 7.3 Monthly Reports

**Professional and Enterprise customers receive:**
- Monthly uptime report
- Performance metrics
- Incident summary
- Support ticket statistics
- Usage analytics

**Delivered:** First week of each month via email

---

## 8. INCIDENT MANAGEMENT

### 8.1 Incident Response Process

**Detection ’ Assessment ’ Communication ’ Resolution ’ Post-Mortem**

1. **Detection** (Automated monitoring or customer report)
2. **Assessment** (Severity classification, impact analysis)
3. **Communication** (Status page update, customer notifications)
4. **Resolution** (Fix deployed, verification)
5. **Post-Mortem** (Root cause analysis, prevention measures)

### 8.2 Communication During Incidents

**Updates Provided:**
- Initial notification: Within 30 minutes of confirmed incident
- Progress updates: Every 2 hours (P1), every 6 hours (P2)
- Resolution confirmation: Immediate upon fix
- Post-mortem report: Within 5 business days (for P1/P2 incidents)

### 8.3 Incident Severity Levels

**P1 - Critical:**
- Complete platform unavailability
- Data loss or corruption
- Security breach
- All income bots offline

**P2 - High:**
- Major functionality unavailable
- Significant performance degradation (>50% slower)
- Some income bots offline
- Payment processing failures

**P3 - Normal:**
- Minor functionality affected
- Workaround available
- Isolated issues
- UI glitches

**P4 - Low:**
- Cosmetic issues
- Documentation errors
- Feature requests
- General questions

---

## 9. DATA BACKUP AND RECOVERY

### 9.1 Backup Frequency

| Data Type | Backup Frequency | Retention Period |
|-----------|------------------|------------------|
| **Database (PostgreSQL)** | Every 6 hours | 30 days |
| **File Storage** | Daily | 30 days |
| **Configuration** | On change | 90 days |
| **Income Bot Data** | Every 6 hours | 90 days |

### 9.2 Recovery Time Objective (RTO)

**Target:** 4 hours for complete system recovery

### 9.3 Recovery Point Objective (RPO)

**Target:** Maximum 6 hours of data loss in catastrophic failure

### 9.4 Disaster Recovery

- **Geographic Redundancy:** Multi-region backups (EU and Norway)
- **Failover:** Automated failover for database
- **Testing:** Quarterly disaster recovery drills
- **Documentation:** Runbooks for all recovery scenarios

---

## 10. SECURITY COMMITMENTS

### 10.1 Security Standards

Mindframe AI commits to:
-  ISO 27001 aligned security practices
-  SOC 2 Type II compliance (in progress)
-  GDPR compliance
-  OWASP Top 10 protection
-  Regular penetration testing (annually)
-  Security patch management (critical patches within 48 hours)

### 10.2 Data Protection

- **Encryption at Rest:** AES-256
- **Encryption in Transit:** TLS 1.3
- **Password Storage:** bcrypt hashing
- **API Security:** Rate limiting, authentication, authorization
- **Database:** Encrypted backups, access logging

### 10.3 Security Incident Response

**Timeline:**
- **Detection to Customer Notification:** 72 hours (GDPR requirement)
- **Initial Assessment:** 2 hours for critical incidents
- **Remediation:** Variable based on severity
- **Post-Incident Report:** 5 business days

---

## 11. CHANGE MANAGEMENT

### 11.1 Platform Updates

**Release Schedule:**
- **Major releases:** Quarterly
- **Minor updates:** Monthly
- **Security patches:** As needed
- **Bug fixes:** Weekly

**Notification:**
- Breaking changes: 30 days advance notice
- New features: 7 days notice or same-day for non-breaking
- Security patches: Best effort, may be emergency deployed

### 11.2 API Versioning

- **Versioning:** Semantic versioning (v1, v2, etc.)
- **Deprecation Notice:** 6 months minimum
- **Legacy Support:** 12 months for deprecated APIs

---

## 12. LIMITATIONS AND EXCLUSIONS

### 12.1 Service Not Guaranteed

Mindframe AI does NOT guarantee:
- Income amounts from Income Bots (depends on external platforms)
- Job availability on third-party platforms
- Acceptance rates for freelance applications
- Survey qualification rates
- Third-party platform uptime (Upwork, UserTesting, etc.)
- OpenAI API availability or performance

### 12.2 SLA Exclusions

This SLA does NOT apply to:
- Beta features (marked as "Beta" or "Experimental")
- Free Tier accounts (best-effort support only)
- Downtime caused by customer actions
- Issues with customer's network or devices
- Third-party service outages beyond our control
- Force majeure events

### 12.3 Fair Use Policy

Mindframe AI reserves the right to:
- Throttle excessive API usage
- Suspend accounts violating Terms of Service
- Limit income bot operations if platforms impose restrictions
- Temporarily disable features for security reasons

---

## 13. AMENDMENTS

### 13.1 SLA Updates

Mindframe AI may update this SLA:
- **Minor changes:** 14 days notice via email
- **Material changes:** 30 days notice
- **Immediate changes:** Only for legal compliance or critical security

### 13.2 Notification Methods

- Email to account holder
- In-app notification
- Status page announcement
- Posted on website

### 13.3 Customer Rights

Customers may:
- Review changes before they take effect
- Object to material changes
- Terminate service if changes are unacceptable (with prorated refund)

---

## 14. CONTACT INFORMATION

**For SLA-related inquiries:**

**General Support:**
Email: hello@mframe.io
Chat: Available in platform (Professional+)
Phone: +47-XXX-XXXXX (Enterprise)

**Emergency (P1 incidents):**
Email: hello@mframe.io (Subject: [P1 URGENT])

**Account Management (Enterprise):**
Your dedicated account manager

**Status Updates:**
https://status.mindframe.ai

---

## 15. GOVERNING LAW

This SLA is governed by:
- **Jurisdiction:** Norwegian law
- **Disputes:** Oslo district court
- **Language:** English (binding version)

---

## 16. ENTIRE AGREEMENT

This SLA is part of and incorporated into:
1. Terms of Service
2. Data Processing Agreement (DPA)
3. Privacy Policy
4. Acceptable Use Policy

In case of conflict, order of precedence:
1. Enterprise Agreement (if applicable)
2. This SLA
3. Terms of Service

---

## 17. ACKNOWLEDGMENT

By using Mindframe AI Services, you acknowledge:
-  Understanding of this SLA
-  Agreement to SLA terms
-  Understanding of uptime commitments and limitations
-  Agreement that Service Credits are the sole remedy for SLA violations

---

**MINDFRAME AI**

Sondre Kjær, Founder
hello@mframe.io
Oslo, Norway

**Effective Date:** November 16, 2025
**Last Updated:** November 16, 2025
**Next Review:** May 16, 2026

---

**Status Page:** https://status.mindframe.ai
**Support:** hello@mframe.io
**Documentation:** https://docs.mindframe.ai

---

*This SLA represents our commitment to providing reliable, high-quality service to all Mindframe AI customers.*
