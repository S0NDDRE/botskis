# DATA PROCESSING AGREEMENT (DPA)

**Last Updated:** November 16, 2025
**Effective Date:** November 16, 2025

---

## PARTIES

This Data Processing Agreement ("DPA") is entered into between:

**DATA CONTROLLER** ("Customer", "you"):
The entity or individual subscribing to Mindframe AI Services

**DATA PROCESSOR** ("Mindframe AI", "we", "us"):
- **Legal Entity:** Mindframe AI
- **Founder:** Sondre Kjær
- **Email:** hello@mframe.io
- **Address:** Oslo, Norway
- **Website:** https://mindframe.ai / https://mframe.io

This DPA forms part of and is incorporated into the Terms of Service between the parties.

---

## 1. DEFINITIONS

**"Data Protection Laws"** means all applicable laws and regulations relating to the processing of Personal Data, including the EU General Data Protection Regulation 2016/679 ("GDPR") and the Norwegian Personal Data Act.

**"Personal Data"** means any information relating to an identified or identifiable natural person processed by Mindframe AI on behalf of Customer.

**"Processing"** has the meaning given in Data Protection Laws and includes any operation performed on Personal Data.

**"Data Subject"** means an identified or identifiable natural person to whom Personal Data relates.

**"Sub-processor"** means any third party engaged by Mindframe AI to process Personal Data.

**"Services"** means all Mindframe AI platform services including AI Marketplace, Income Bots, Learning Platform, and related services.

---

## 2. SCOPE OF PROCESSING

### 2.1 Subject Matter
Provision of AI-powered automation platform and income generation services.

### 2.2 Duration
From the Effective Date until termination of Services plus 30 days for data return/deletion.

### 2.3 Nature and Purpose of Processing
- Providing AI agent marketplace and deployment
- Operating income generation bots (Freelance, Testing, Survey, Writing)
- Delivering learning platform and courses
- Customer account management
- Payment processing
- Technical support
- Platform analytics and improvement

### 2.4 Types of Personal Data

**Account Data:** Name, email, phone, company, job title, profile information
**Authentication Data:** Login credentials (hashed), tokens, 2FA data
**Usage Data:** IP addresses, browser type, device info, usage logs, feature interactions
**Income Bot Data:** Platform credentials (encrypted), job applications, earnings, transaction data
**Payment Data:** Billing info, payment methods (tokenized), transaction history
**Support Data:** Support tickets, chat transcripts, email correspondence
**Learning Data:** Course progress, quiz results, certificates, preferences

### 2.5 Categories of Data Subjects
- Platform users (individuals and businesses)
- Customer employees and contractors
- Customer's end users
- Support contacts

---

## 3. CUSTOMER OBLIGATIONS

Customer warrants that:
- ✅ It has lawful basis for processing Personal Data
- ✅ It has obtained necessary consents from Data Subjects
- ✅ Its instructions comply with Data Protection Laws
- ✅ It will not instruct unlawful processing

---

## 4. MINDFRAME AI OBLIGATIONS

### 4.1 Processing Instructions
Process Personal Data only:
- As necessary to provide Services
- On documented instructions from Customer
- As specified in Terms of Service
- As configured in account settings

### 4.2 Confidentiality
Ensure authorized personnel:
- Are subject to confidentiality obligations
- Receive data protection training
- Access data only as necessary

### 4.3 Security Measures

**Technical Security:**
- Encryption: AES-256 (at rest), TLS 1.3 (in transit)
- Authentication: bcrypt password hashing, JWT tokens
- Rate limiting and DDoS protection
- Automated encrypted backups
- Intrusion detection systems
- Security audit logging

**Organizational Security:**
- Role-based access control (RBAC)
- Security incident response procedures
- Employee security training
- Regular security assessments
- Data minimization practices
- Secure development lifecycle
- Business continuity planning

**Infrastructure:**
- Google Cloud Platform (ISO 27001 certified)
- Data center: europe-north1 (Finland/Norway)
- Network segmentation and firewalls
- Regular penetration testing

### 4.4 Sub-processors

**Current Sub-processors:**

| Sub-processor | Service | Location | Purpose | Safeguards |
|---------------|---------|----------|---------|------------|
| Google Cloud Platform | Infrastructure | EU (europe-north1) | Hosting, database, storage | EU-based, ISO 27001 |
| OpenAI | AI Services | USA | AI agent functionality | Standard Contractual Clauses |
| Stripe | Payments | USA/Ireland | Payment processing | Standard Contractual Clauses |
| SendGrid | Email | USA | Transactional emails | Standard Contractual Clauses |
| Sentry | Monitoring | USA | Error tracking | Standard Contractual Clauses |
| Vipps | Payments | Norway | Norwegian payments | EU-based |

**Sub-processor Changes:**
- 30 days advance written notice of new Sub-processors
- Customer may object for legitimate data protection reasons
- If unresolved, Customer may terminate Services

### 4.5 Data Subject Rights Assistance

Mindframe AI will assist Customer in responding to Data Subject requests:

**Right of Access:** Data export tools (JSON/CSV format)
**Right to Rectification:** Account settings for data correction
**Right to Erasure:** Account deletion functionality
**Right to Restriction:** Disable specific processing activities
**Right to Data Portability:** Structured data export
**Right to Object:** Opt-out of optional processing

**Response Time:** Within 72 hours of Customer request

### 4.6 Data Breach Notification

In case of Personal Data Breach:

**Timeline:** Notify Customer within 72 hours of awareness

**Information Provided:**
- Nature of the breach
- Categories and approximate number of Data Subjects affected
- Likely consequences
- Measures taken or proposed to address breach
- Contact point for more information

**Contact:** hello@mframe.io (Subject: [URGENT] Data Breach Notification)

**Documentation:** All breaches logged and remediation tracked

### 4.7 Audits
Customer may:
- Request compliance audit reports (SOC 2, ISO 27001)
- Conduct on-site audit with 30 days notice (once per year)
- Engage third-party auditor at Customer's expense

---

## 5. DATA TRANSFERS

### 5.1 Primary Location
**EEA:** All primary data stored in Europe (europe-north1 - Finland/Norway)

### 5.2 Transfers Outside EEA
Some Sub-processors located outside EEA with appropriate safeguards:
- OpenAI (USA) - Standard Contractual Clauses (SCCs)
- Stripe (USA/Ireland) - Standard Contractual Clauses
- SendGrid (USA) - Standard Contractual Clauses
- Sentry (USA) - Standard Contractual Clauses

### 5.3 Transfer Safeguards
- Standard Contractual Clauses approved by EU Commission
- Transfer Impact Assessments conducted
- Additional technical safeguards (encryption, access controls)

---

## 6. DATA RETENTION AND DELETION

### 6.1 Retention Periods
- **Active accounts:** Duration of use
- **Inactive accounts:** 90 days after last login
- **Deleted accounts:** 30 days recovery period, then permanent deletion
- **Backups:** 30 days, then deleted
- **Logs:** 90 days maximum

### 6.2 Data Deletion Upon Termination
Within 30 days of termination, Mindframe AI shall:
1. Delete or return all Personal Data
2. Provide written certification of deletion
3. Delete from all backup systems
4. Exception: Data required by law (with notice to Customer)

---

## 7. LIABILITY

### 7.1 Processor Liability
Mindframe AI liable for damages caused by:
- Processing in violation of GDPR
- Acting outside lawful instructions
- Failing to implement appropriate security measures

### 7.2 Indemnification
Mindframe AI indemnifies Customer for:
- Supervisory authority fines due to Mindframe AI breach
- Data Subject claims due to Mindframe AI Processing violations
- Reasonable costs defending such claims

### 7.3 Limitation
Subject to limitations in Terms of Service, except where prohibited by Data Protection Laws.

---

## 8. TERM AND TERMINATION

**Term:** Effective Date until Services termination plus 30 days

**Termination:** Automatic upon Services termination or Customer written request

**Survival:** Confidentiality, liability, and deletion obligations survive termination

---

## 9. GENERAL PROVISIONS

### 9.1 Governing Law
Norwegian law and GDPR

### 9.2 Jurisdiction
Oslo, Norway courts

### 9.3 Amendments
- To comply with Data Protection Laws: Immediate
- Other changes: 30 days notice, Customer may object and terminate

### 9.4 Order of Precedence
1. This DPA
2. Terms of Service
3. Other agreements

### 9.5 Severability
Invalid provisions severed; remaining provisions remain in effect

---

## 10. CONTACT INFORMATION

**Data Protection Inquiries:**
Mindframe AI
Attention: Data Protection Officer
Email: hello@mframe.io
Address: Oslo, Norway

**Supervisory Authority:**
Datatilsynet (Norwegian Data Protection Authority)
Website: https://www.datatilsynet.no
Email: postkasse@datatilsynet.no

---

## 11. ACKNOWLEDGMENT

By using Mindframe AI Services, Customer acknowledges:
- ✅ Reading and understanding this DPA
- ✅ Agreement to be bound by these terms
- ✅ Authority to enter into this DPA
- ✅ Responsibility for compliance with Data Protection Laws

---

**FOR MINDFRAME AI:**

Sondre Kjær, Founder
hello@mframe.io
Date: November 16, 2025

---

*This DPA complies with GDPR Articles 28, 32, 33, 44-50 and applicable Norwegian law.*

**Last Review Date:** November 16, 2025
**Next Review Date:** May 16, 2026
