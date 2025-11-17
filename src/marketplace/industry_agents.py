"""
Industry-Specific AI Agents for Mindframe Marketplace
Specialized agents for Healthcare, Education, Transport, Legal, and Construction
"""
from typing import Dict

# ============================================================================
# HEALTHCARE / MEDICAL AGENTS (8)
# ============================================================================

HEALTHCARE_AGENTS = {}

HEALTHCARE_AGENTS["healthcare_appointment_booking"] = {
    "id": "healthcare_appointment_booking",
    "name": "Healthcare Appointment Booking Agent",
    "description": "Automated patient appointment scheduling with calendar sync and SMS reminders",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 49,
    "rating": 4.9,
    "downloads": 3421,
    "author": "Mindframe Healthcare",
    "verified": True,
    "gdpr_compliant": True,
    "hipaa_compliant": True,
    "features": [
        "Real-time calendar integration",
        "Automated SMS/email reminders",
        "No-show reduction algorithms",
        "Multi-provider scheduling",
        "Patient history integration",
        "Insurance verification",
        "Waitlist management"
    ],
    "use_cases": [
        "Medical clinics",
        "Dental offices",
        "Physical therapy centers",
        "Mental health practices"
    ],
    "compliance": {
        "hipaa": True,
        "gdpr": True,
        "phi_encryption": True
    }
}

HEALTHCARE_AGENTS["prescription_refill_automator"] = {
    "id": "prescription_refill_automator",
    "name": "Prescription Refill Automation Agent",
    "description": "Automates prescription refill requests and pharmacy communication",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 79,
    "rating": 4.8,
    "downloads": 2156,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Automatic refill request processing",
        "Pharmacy integration",
        "Patient notification system",
        "Medication interaction checking",
        "Dosage verification",
        "Insurance pre-authorization"
    ],
    "integrations": ["CVS", "Walgreens", "Local Pharmacies", "EMR Systems"]
}

HEALTHCARE_AGENTS["patient_follow_up"] = {
    "id": "patient_follow_up",
    "name": "Patient Follow-Up Care Agent",
    "description": "Automated post-treatment follow-ups and recovery monitoring",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 59,
    "rating": 4.9,
    "downloads": 1987,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Personalized follow-up schedules",
        "Symptom tracking via SMS/email",
        "Recovery milestone monitoring",
        "Escalation to care team if needed",
        "Patient satisfaction surveys",
        "Outcome tracking"
    ]
}

HEALTHCARE_AGENTS["medical_records_organizer"] = {
    "id": "medical_records_organizer",
    "name": "Medical Records Organizer Agent",
    "description": "Automatically organizes and indexes patient medical records",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 99,
    "rating": 4.7,
    "downloads": 1543,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "OCR document scanning",
        "Automatic categorization",
        "HIPAA-compliant storage",
        "Quick search and retrieval",
        "Version control",
        "Audit trail logging"
    ]
}

HEALTHCARE_AGENTS["insurance_claim_processor"] = {
    "id": "insurance_claim_processor",
    "name": "Insurance Claim Processing Agent",
    "description": "Automates medical insurance claim submission and tracking",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 129,
    "rating": 4.8,
    "downloads": 2876,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Automated claim submission",
        "CPT/ICD-10 code validation",
        "Denial management",
        "Reimbursement tracking",
        "Pre-authorization handling",
        "Insurance verification"
    ],
    "integrations": ["Blue Cross", "Aetna", "UnitedHealth", "Medicare"]
}

HEALTHCARE_AGENTS["hipaa_compliance_monitor"] = {
    "id": "hipaa_compliance_monitor",
    "name": "HIPAA Compliance Monitoring Agent",
    "description": "Monitors and ensures HIPAA compliance across your practice",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 149,
    "rating": 4.9,
    "downloads": 987,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Continuous compliance monitoring",
        "Access log auditing",
        "Privacy breach detection",
        "Staff training tracking",
        "Risk assessment automation",
        "Incident reporting"
    ]
}

HEALTHCARE_AGENTS["symptom_pre_screener"] = {
    "id": "symptom_pre_screener",
    "name": "Patient Symptom Pre-Screening Agent",
    "description": "AI-powered symptom checker for patient intake triage",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 69,
    "rating": 4.6,
    "downloads": 1765,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Symptom-based triage",
        "Urgency classification",
        "Pre-appointment preparation",
        "COVID-19 screening",
        "Integration with intake forms",
        "Escalation protocols"
    ],
    "disclaimer": "Not a substitute for professional medical advice"
}

HEALTHCARE_AGENTS["lab_result_notifier"] = {
    "id": "lab_result_notifier",
    "name": "Lab Result Notification Agent",
    "description": "Automated patient notification for lab results availability",
    "category": "healthcare",
    "industry": "Healthcare",
    "price": 39,
    "rating": 4.7,
    "downloads": 2134,
    "author": "Mindframe Healthcare",
    "verified": True,
    "hipaa_compliant": True,
    "features": [
        "Secure result delivery",
        "Patient portal integration",
        "Abnormal result flagging",
        "Follow-up scheduling",
        "Multi-channel notifications",
        "Provider alerts"
    ]
}


# ============================================================================
# EDUCATION / E-LEARNING AGENTS (8)
# ============================================================================

EDUCATION_AGENTS = {}

EDUCATION_AGENTS["student_enrollment_automator"] = {
    "id": "student_enrollment_automator",
    "name": "Student Enrollment Automation Agent",
    "description": "Streamlines student registration and enrollment processes",
    "category": "education",
    "industry": "Education",
    "price": 59,
    "rating": 4.8,
    "downloads": 1876,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Online application processing",
        "Document verification",
        "Payment integration",
        "Course selection assistance",
        "Waitlist management",
        "Automated confirmations"
    ],
    "use_cases": [
        "Universities",
        "Online courses",
        "Training programs",
        "K-12 schools"
    ]
}

EDUCATION_AGENTS["assignment_grading_assistant"] = {
    "id": "assignment_grading_assistant",
    "name": "AI Assignment Grading Assistant",
    "description": "Automated grading for essays, quizzes, and assignments",
    "category": "education",
    "industry": "Education",
    "price": 79,
    "rating": 4.7,
    "downloads": 3421,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Essay scoring with rubrics",
        "Multiple choice auto-grading",
        "Plagiarism detection",
        "Personalized feedback generation",
        "Grade book integration",
        "Progress tracking"
    ],
    "integrations": ["Canvas", "Blackboard", "Moodle", "Google Classroom"]
}

EDUCATION_AGENTS["course_content_generator"] = {
    "id": "course_content_generator",
    "name": "Course Content Generation Agent",
    "description": "AI-powered course material and curriculum creator",
    "category": "education",
    "industry": "Education",
    "price": 99,
    "rating": 4.9,
    "downloads": 2156,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Lesson plan generation",
        "Quiz creation",
        "Study guide generation",
        "Video script writing",
        "Learning objective alignment",
        "Multi-format export (PDF, SCORM)"
    ]
}

EDUCATION_AGENTS["student_support_chatbot"] = {
    "id": "student_support_chatbot",
    "name": "24/7 Student Support Chatbot",
    "description": "Always-on student support for common questions and issues",
    "category": "education",
    "industry": "Education",
    "price": 49,
    "rating": 4.6,
    "downloads": 2987,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "FAQ automation",
        "Assignment help guidance",
        "Technical support triage",
        "Course navigation assistance",
        "24/7 availability",
        "Multi-language support"
    ]
}

EDUCATION_AGENTS["attendance_tracker"] = {
    "id": "attendance_tracker",
    "name": "Automated Attendance Tracking Agent",
    "description": "Smart attendance monitoring and reporting system",
    "category": "education",
    "industry": "Education",
    "price": 39,
    "rating": 4.7,
    "downloads": 1654,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "QR code check-in",
        "Geolocation verification",
        "Absence notifications",
        "Attendance analytics",
        "Integration with SIS",
        "Parent notifications"
    ]
}

EDUCATION_AGENTS["parent_communication_agent"] = {
    "id": "parent_communication_agent",
    "name": "Parent Communication Automation Agent",
    "description": "Automated updates and communication with parents",
    "category": "education",
    "industry": "Education",
    "price": 45,
    "rating": 4.8,
    "downloads": 1432,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Progress report generation",
        "Behavior incident notifications",
        "Event reminders",
        "Grade updates",
        "Two-way messaging",
        "Translation support"
    ]
}

EDUCATION_AGENTS["exam_scheduler"] = {
    "id": "exam_scheduler",
    "name": "Exam & Test Scheduling Agent",
    "description": "Automated exam scheduling and room allocation",
    "category": "education",
    "industry": "Education",
    "price": 55,
    "rating": 4.7,
    "downloads": 987,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Conflict detection",
        "Room capacity management",
        "Invigilator assignment",
        "Student notifications",
        "Special accommodations",
        "Calendar integration"
    ]
}

EDUCATION_AGENTS["learning_progress_analyzer"] = {
    "id": "learning_progress_analyzer",
    "name": "Learning Progress Analysis Agent",
    "description": "AI-powered student performance analytics and insights",
    "category": "education",
    "industry": "Education",
    "price": 89,
    "rating": 4.9,
    "downloads": 1234,
    "author": "Mindframe Education",
    "verified": True,
    "features": [
        "Performance trend analysis",
        "At-risk student identification",
        "Personalized learning recommendations",
        "Predictive analytics",
        "Visual dashboards",
        "Intervention suggestions"
    ]
}


# ============================================================================
# TRANSPORT / LOGISTICS AGENTS (8)
# ============================================================================

TRANSPORT_AGENTS = {}

TRANSPORT_AGENTS["route_optimization"] = {
    "id": "route_optimization",
    "name": "AI Route Optimization Agent",
    "description": "Intelligent route planning for maximum efficiency",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 99,
    "rating": 4.9,
    "downloads": 2543,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Multi-stop route optimization",
        "Real-time traffic integration",
        "Fuel cost optimization",
        "Time window constraints",
        "Driver skill matching",
        "Weather consideration"
    ],
    "integrations": ["Google Maps", "Waze", "HERE Maps", "TomTom"]
}

TRANSPORT_AGENTS["delivery_status_updater"] = {
    "id": "delivery_status_updater",
    "name": "Delivery Status Update Agent",
    "description": "Automated delivery tracking and customer notifications",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 49,
    "rating": 4.8,
    "downloads": 3876,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Real-time GPS tracking",
        "Automated customer notifications",
        "ETA calculations",
        "Proof of delivery capture",
        "Exception handling",
        "Multi-channel updates (SMS/email)"
    ]
}

TRANSPORT_AGENTS["fleet_management"] = {
    "id": "fleet_management",
    "name": "Fleet Management Automation Agent",
    "description": "Complete fleet operations and maintenance management",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 149,
    "rating": 4.8,
    "downloads": 1654,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Vehicle maintenance scheduling",
        "Fuel consumption tracking",
        "Driver behavior monitoring",
        "Compliance management",
        "Telematics integration",
        "Cost analytics"
    ]
}

TRANSPORT_AGENTS["warehouse_inventory_tracker"] = {
    "id": "warehouse_inventory_tracker",
    "name": "Warehouse Inventory Tracking Agent",
    "description": "Real-time inventory management and stock optimization",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 79,
    "rating": 4.7,
    "downloads": 2134,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Barcode/RFID scanning",
        "Stock level monitoring",
        "Automatic reorder triggers",
        "Bin location management",
        "Pick/pack optimization",
        "Inventory forecasting"
    ]
}

TRANSPORT_AGENTS["shipment_tracking_notifier"] = {
    "id": "shipment_tracking_notifier",
    "name": "Shipment Tracking Notification Agent",
    "description": "Multi-carrier shipment tracking and alerts",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 39,
    "rating": 4.8,
    "downloads": 4321,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Multi-carrier integration",
        "Automated tracking updates",
        "Delay detection and alerts",
        "Customer self-service portal",
        "Delivery confirmation",
        "Exception management"
    ],
    "integrations": ["UPS", "FedEx", "DHL", "USPS", "PostNord"]
}

TRANSPORT_AGENTS["driver_communication"] = {
    "id": "driver_communication",
    "name": "Driver Communication Agent",
    "description": "Automated dispatch and driver communication system",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 55,
    "rating": 4.7,
    "downloads": 1765,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "Automated job assignments",
        "Turn-by-turn navigation",
        "Two-way messaging",
        "Break management",
        "Hours of service tracking",
        "Emergency alerts"
    ]
}

TRANSPORT_AGENTS["load_planning_optimizer"] = {
    "id": "load_planning_optimizer",
    "name": "Load Planning Optimization Agent",
    "description": "AI-powered cargo loading and consolidation",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 89,
    "rating": 4.8,
    "downloads": 1234,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "3D load visualization",
        "Weight distribution optimization",
        "Container utilization",
        "Mixed cargo handling",
        "Loading sequence planning",
        "Fragile item protection"
    ]
}

TRANSPORT_AGENTS["customs_documentation"] = {
    "id": "customs_documentation",
    "name": "Customs Documentation Agent",
    "description": "Automated customs paperwork and compliance",
    "category": "transport",
    "industry": "Transport & Logistics",
    "price": 119,
    "rating": 4.9,
    "downloads": 876,
    "author": "Mindframe Logistics",
    "verified": True,
    "features": [
        "HS code classification",
        "Automated form generation",
        "Compliance checking",
        "Duty calculation",
        "Multi-country support",
        "Document archiving"
    ]
}


# ============================================================================
# LEGAL / LAW FIRM AGENTS (8)
# ============================================================================

LEGAL_AGENTS = {}

LEGAL_AGENTS["case_management"] = {
    "id": "case_management",
    "name": "Legal Case Management Agent",
    "description": "Complete case lifecycle management and tracking",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 149,
    "rating": 4.9,
    "downloads": 1543,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Case intake automation",
        "Deadline tracking",
        "Court date management",
        "Document organization",
        "Client communication",
        "Billing integration"
    ],
    "disclaimer": "Not a substitute for legal advice"
}

LEGAL_AGENTS["document_review_assistant"] = {
    "id": "document_review_assistant",
    "name": "AI Document Review Assistant",
    "description": "Automated legal document analysis and review",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 199,
    "rating": 4.8,
    "downloads": 2134,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Contract clause extraction",
        "Risk identification",
        "Compliance checking",
        "Redlining suggestions",
        "Precedent matching",
        "Multi-language support"
    ]
}

LEGAL_AGENTS["client_intake_automator"] = {
    "id": "client_intake_automator",
    "name": "Client Intake Automation Agent",
    "description": "Streamlined new client onboarding and screening",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 79,
    "rating": 4.7,
    "downloads": 1876,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Conflict checking",
        "Client questionnaires",
        "Document collection",
        "Engagement letter generation",
        "Payment setup",
        "CRM integration"
    ]
}

LEGAL_AGENTS["billing_time_tracker"] = {
    "id": "billing_time_tracker",
    "name": "Legal Billing & Time Tracking Agent",
    "description": "Automated billable hour tracking and invoice generation",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 89,
    "rating": 4.8,
    "downloads": 2543,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Automatic time capture",
        "Task-based billing",
        "Invoice generation",
        "Trust accounting",
        "Payment processing",
        "Expense tracking"
    ]
}

LEGAL_AGENTS["court_date_reminder"] = {
    "id": "court_date_reminder",
    "name": "Court Date & Deadline Reminder Agent",
    "description": "Never miss a court date or filing deadline",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 45,
    "rating": 4.9,
    "downloads": 1987,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Multi-layered reminders",
        "Calendar synchronization",
        "Statute of limitations tracking",
        "Team notifications",
        "Escalation protocols",
        "Conflict detection"
    ]
}

LEGAL_AGENTS["contract_analysis"] = {
    "id": "contract_analysis",
    "name": "Contract Analysis Agent",
    "description": "AI-powered contract review and risk assessment",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 169,
    "rating": 4.9,
    "downloads": 1432,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Key term extraction",
        "Obligation identification",
        "Risk scoring",
        "Clause comparison",
        "Missing clause detection",
        "Negotiation suggestions"
    ]
}

LEGAL_AGENTS["legal_research_assistant"] = {
    "id": "legal_research_assistant",
    "name": "AI Legal Research Assistant",
    "description": "Automated case law and statute research",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 129,
    "rating": 4.7,
    "downloads": 1765,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Case law search",
        "Statute citation",
        "Precedent finding",
        "Shepardizing automation",
        "Brief generation assistance",
        "Jurisdiction filtering"
    ],
    "integrations": ["Westlaw", "LexisNexis", "Fastcase"]
}

LEGAL_AGENTS["compliance_checker"] = {
    "id": "compliance_checker",
    "name": "Legal Compliance Monitoring Agent",
    "description": "Continuous regulatory compliance monitoring",
    "category": "legal",
    "industry": "Legal & Law Firms",
    "price": 159,
    "rating": 4.8,
    "downloads": 987,
    "author": "Mindframe Legal",
    "verified": True,
    "features": [
        "Regulatory change monitoring",
        "Policy compliance checking",
        "Audit trail generation",
        "Risk assessment",
        "Training requirement tracking",
        "Reporting automation"
    ]
}


# ============================================================================
# CONSTRUCTION / BUILDING AGENTS (8)
# ============================================================================

CONSTRUCTION_AGENTS = {}

CONSTRUCTION_AGENTS["project_timeline_manager"] = {
    "id": "project_timeline_manager",
    "name": "Construction Project Timeline Manager",
    "description": "AI-powered project scheduling and milestone tracking",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 119,
    "rating": 4.8,
    "downloads": 1654,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Critical path analysis",
        "Resource leveling",
        "Weather delay prediction",
        "Milestone tracking",
        "Gantt chart automation",
        "Progress reporting"
    ]
}

CONSTRUCTION_AGENTS["material_order_automator"] = {
    "id": "material_order_automator",
    "name": "Material Ordering Automation Agent",
    "description": "Automated material procurement and inventory management",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 89,
    "rating": 4.7,
    "downloads": 2134,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Automated reordering",
        "Supplier price comparison",
        "Delivery scheduling",
        "Waste reduction",
        "Budget tracking",
        "Vendor management"
    ]
}

CONSTRUCTION_AGENTS["safety_inspection_checker"] = {
    "id": "safety_inspection_checker",
    "name": "Safety Inspection & Compliance Agent",
    "description": "Automated safety checks and OSHA compliance monitoring",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 149,
    "rating": 4.9,
    "downloads": 1432,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Daily safety checklists",
        "Incident reporting",
        "OSHA compliance tracking",
        "Photo documentation",
        "Corrective action tracking",
        "Training verification"
    ]
}

CONSTRUCTION_AGENTS["permit_application_tracker"] = {
    "id": "permit_application_tracker",
    "name": "Building Permit Application Tracker",
    "description": "Automated permit application and approval tracking",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 79,
    "rating": 4.7,
    "downloads": 1765,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Application preparation",
        "Document submission",
        "Status tracking",
        "Renewal reminders",
        "Compliance verification",
        "Multi-jurisdiction support"
    ]
}

CONSTRUCTION_AGENTS["subcontractor_coordinator"] = {
    "id": "subcontractor_coordinator",
    "name": "Subcontractor Coordination Agent",
    "description": "Automated subcontractor scheduling and communication",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 99,
    "rating": 4.8,
    "downloads": 1543,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Automated scheduling",
        "Conflict resolution",
        "Payment tracking",
        "Performance monitoring",
        "Document management",
        "Communication hub"
    ]
}

CONSTRUCTION_AGENTS["progress_photo_documenter"] = {
    "id": "progress_photo_documenter",
    "name": "Progress Photo Documentation Agent",
    "description": "Automated construction progress photography and reporting",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 59,
    "rating": 4.6,
    "downloads": 2876,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Scheduled photo capture",
        "360-degree documentation",
        "Time-lapse creation",
        "Comparison views",
        "Cloud storage",
        "Client portal access"
    ]
}

CONSTRUCTION_AGENTS["invoice_payment_tracker"] = {
    "id": "invoice_payment_tracker",
    "name": "Construction Invoice & Payment Tracker",
    "description": "Automated billing, invoicing, and payment tracking",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 69,
    "rating": 4.8,
    "downloads": 1987,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Progress billing automation",
        "Change order tracking",
        "Lien waiver management",
        "Payment reminders",
        "Cash flow forecasting",
        "Integration with accounting"
    ]
}

CONSTRUCTION_AGENTS["equipment_maintenance_scheduler"] = {
    "id": "equipment_maintenance_scheduler",
    "name": "Equipment Maintenance Scheduling Agent",
    "description": "Preventive maintenance scheduling for construction equipment",
    "category": "construction",
    "industry": "Construction & Building",
    "price": 85,
    "rating": 4.7,
    "downloads": 1234,
    "author": "Mindframe Construction",
    "verified": True,
    "features": [
        "Maintenance scheduling",
        "Usage tracking",
        "Downtime minimization",
        "Part inventory management",
        "Service history logging",
        "Cost tracking"
    ]
}


# ============================================================================
# COMBINED DICTIONARY
# ============================================================================

INDUSTRY_AGENTS = {}
INDUSTRY_AGENTS.update(HEALTHCARE_AGENTS)
INDUSTRY_AGENTS.update(EDUCATION_AGENTS)
INDUSTRY_AGENTS.update(TRANSPORT_AGENTS)
INDUSTRY_AGENTS.update(LEGAL_AGENTS)
INDUSTRY_AGENTS.update(CONSTRUCTION_AGENTS)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_agents_by_industry(industry: str):
    """Get all agents for a specific industry"""
    return {
        k: v for k, v in INDUSTRY_AGENTS.items()
        if v.get("industry") == industry
    }


def get_healthcare_agents():
    """Get all healthcare agents"""
    return HEALTHCARE_AGENTS


def get_education_agents():
    """Get all education agents"""
    return EDUCATION_AGENTS


def get_transport_agents():
    """Get all transport/logistics agents"""
    return TRANSPORT_AGENTS


def get_legal_agents():
    """Get all legal/law firm agents"""
    return LEGAL_AGENTS


def get_construction_agents():
    """Get all construction/building agents"""
    return CONSTRUCTION_AGENTS


def get_industry_stats():
    """Get statistics for industry agents"""
    return {
        "total_industry_agents": len(INDUSTRY_AGENTS),
        "healthcare": len(HEALTHCARE_AGENTS),
        "education": len(EDUCATION_AGENTS),
        "transport": len(TRANSPORT_AGENTS),
        "legal": len(LEGAL_AGENTS),
        "construction": len(CONSTRUCTION_AGENTS),
        "industries_covered": 5
    }
