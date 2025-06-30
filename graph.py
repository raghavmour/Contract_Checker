from state import AgentState
from subgraph import sub_graph
from Extract_clause import extract_clauses
from clause_sender import ReRanker_Sender
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
import os
from extract_clause_sender import extract_clause_sender
import streamlit as st
from clause_sender_node import clause_sender_node

if not st.secrets:
    from dotenv import load_dotenv

    load_dotenv()  # Load variables from .env
graph = StateGraph(AgentState)

graph.add_node("extract_clauses", extract_clauses)
graph.add_node("clause_sender_node", clause_sender_node)
graph.add_node("SubGraph", sub_graph)

graph.add_conditional_edges(
    "clause_sender_node", ReRanker_Sender, {"SubGraph": "SubGraph"}
)

graph.add_conditional_edges(
    START,
    extract_clause_sender,
    {
        "extract_clauses": "extract_clauses",
    },
)

graph.add_edge("extract_clauses", "clause_sender_node")
graph.add_edge("SubGraph", END)

app = graph.compile()

# state = {
#     "contract": """
#     Vendor Contract
# Nexlify Solutions and [Vendor Name]
# Effective Date: June 25, 2025Contract ID: NS-VC-2025-001
# This Vendor Contract ("Contract") is entered into between Nexlify Solutions, a manufacturing company specializing in industrial equipment, located at [Nexlify Address], and [Vendor Name], located at [Vendor Address], collectively referred to as the "Parties." This Contract outlines the terms and conditions for the provision of [products/services, e.g., precision tools] to Nexlify Solutions.

# 1. Payment Terms
# 1.1 Payment Schedule

# Payments will be made within 45 days of invoice receipt (Net 45).
# Early payment discount: 2% if paid within 10 days.
# Late payment penalty: 1.5% monthly interest on overdue invoices, calculated daily after a 5-day grace period.Example: A $10,000 invoice unpaid after 45 days incurs $150 monthly interest, prorated daily.Compliance: Correct, aligns with Procurement Policy Section 2.2.

# 1.2 Invoice Requirements

# Invoices must be submitted in PDF format via the vendor portal (https://vendor.nexlifysolutions.com).
# Invoices must include Purchase Order (PO) number, detailed service/product description, billing period, vendor tax ID, and bank details.
# Submission deadline: Within 7 days of service completion or product delivery.
# Non-compliant invoices will be rejected within 3 business days with an explanation.Compliance: Correct, aligns with Procurement Policy Section 2.2.

# 1.3 Payment Methods

# Preferred method: ACH or wire transfer for efficiency.
# Checks issued for vendors without electronic payment capabilities, mailed within 5 business days of approval.
# Incorrect Clause: For international vendors, payments will be made in local currency without requiring SWIFT or IBAN codes.Compliance Issue: Violates Procurement Policy Section 2.2, which mandates SWIFT or IBAN codes for international vendors to comply with foreign exchange regulations.

# 1.4 Dispute Resolution

# Invoice disputes must be raised within 10 days via the vendor portal with supporting documentation.
# Disputes resolved within 15 days by Procurement and Finance Teams, with escalation to the Procurement Director if unresolved.Compliance: Correct, aligns with Procurement Policy Section 2.2.


# 2. Warranty Requirements
# 2.1 Warranty Period

# Equipment: Minimum 2-year warranty against manufacturing defects, covering parts and labor for critical components (e.g., motors, controllers).
# Services: 90-day warranty for rework of defective services (e.g., software errors).
# Incorrect Clause: No extended warranties required for equipment valued over $50,000.Compliance Issue: Violates Procurement Policy Section 3.2, which requires extended warranties (3-5 years) for high-value equipment exceeding $50,000.

# 2.2 Warranty Terms

# Vendors must repair or replace defective items at no cost, including shipping and installation.
# Warranty claims processed within 14 days of notification, with temporary replacements for critical equipment.Compliance: Correct, aligns with Procurement Policy Section 3.2.

# 2.3 Documentation

# Vendors must provide warranty certificates at contract signing, specifying coverage, duration, and claim procedures.
# Incorrect Clause: Warranty terms will be provided verbally during onboarding, not included in the contract.Compliance Issue: Violates Procurement Policy Section 3.2, which requires warranty terms to be explicitly stated in the contract and digital copies uploaded to the vendor portal.


# 3. Service Level Agreements (SLAs)
# 3.1 Uptime Guarantee

# Critical services (e.g., production tracking software): 98% monthly uptime.
# Non-critical services: 95% monthly uptime.
# Uptime calculated as: (Total Available Minutes - Downtime) / Total Available Minutes * 100, measured monthly.
# Downtime excludes scheduled maintenance (requires 7 days prior notice, outside 8 AM-6 PM).Compliance: Correct, aligns with Vendor SLA Standards Section 2.2.

# 3.2 Penalties for Non-Compliance

# Uptime below 98% for critical services: 5% credit per 1% below target, capped at 25% of invoice.
# Uptime below 95% for non-critical services: 3% credit per 1% below target, capped at 15% of invoice.
# Incorrect Clause: Penalties will be applied as a fixed $500 fine, regardless of uptime percentage.Compliance Issue: Violates Vendor SLA Standards Section 3.2, which specifies percentage-based credits tied to the invoice value, not a fixed fine.

# 3.3 Support Response Times

# Critical issues: Response within 4 hours, resolution within 24 hours.
# Non-critical issues: Response within 24 hours, resolution within 72 hours.
# Issues reported via vendor portal with ticket number, description, impact, and urgency.Compliance: Correct, aligns with Vendor SLA Standards Section 4.2.


# 4. Termination Clauses
# 4.1 Standard Termination

# 30 days written notice required, delivered via certified mail or vendor portal.
# Termination effective after outstanding deliverables are completed.Compliance: Correct, aligns with Legal Compliance Guidelines Section 2.2.

# 4.2 Termination for Cause

# Immediate termination for material breach, fraud, or insolvency, with evidence provided within 48 hours.
# Vendors have 5 days to appeal with documentation.Compliance: Correct, aligns with Legal Compliance Guidelines Section 2.2.

# 4.3 Mutual Termination

# Incorrect Clause: Vendors may terminate unilaterally with 10 days notice without penalties.Compliance Issue: Violates Legal Compliance Guidelines Section 2.2, which states unilateral termination by vendors with less than 30 days notice is non-compliant and may result in penalties or legal action.


# 5. Indemnity
# 5.1 Indemnification Scope

# Vendor indemnifies Nexlify Solutions against claims related to services, products, negligence, or regulatory violations.
# Includes legal fees, settlements, damages, and third-party claims.
# Vendor must provide proof of insurance at contract signing.Compliance: Correct, aligns with Legal Compliance Guidelines Section 3.2.

# 5.2 Incorrect Clause

# Indemnity clauses will be negotiated post-contract signing.Compliance Issue: Violates Legal Compliance Guidelines Section 3.2, which requires indemnity clauses to be explicitly stated in the contract and non-compliant clauses revised within 7 days of review.


# 6. Liability
# 6.1 Liability Limits

# Vendor maintains $1M general liability insurance per occurrence, with certificates submitted annually.
# Cyber liability insurance of $2M for vendors handling sensitive data.Compliance: Correct, aligns with Legal Compliance Guidelines Section 4.2.

# 6.2 Limitation of Liability

# Nexlify Solutions liability capped at contract value.
# Incorrect Clause: Nexlify Solutions will cover indirect damages, such as lost profits, caused by vendor negligence.Compliance Issue: Violates Legal Compliance Guidelines Section 4.2, which excludes indirect damages unless explicitly agreed.


# 7. Governing Law
# 7.1 Primary Governing Law

# Governed by New York, NY, USA law, aligned with Nexlify Solutions headquarters.
# Disputes resolved via binding arbitration in New York, following American Arbitration Association rules.Compliance: Correct, aligns with Legal Compliance Guidelines Section 5.2.

# 7.2 Allowed Jurisdictions

# Singapore permitted for Asia-Pacific vendors with prior Legal Department approval.
# Incorrect Clause: Tokyo, Japan, is allowed as a governing jurisdiction without Legal Department approval.Compliance Issue: Violates Legal Compliance Guidelines Section 5.2, which requires written approval from the Legal Department for jurisdictions like Tokyo, supported by a risk assessment.


# 8. Contact Information

# Procurement Team: procurement@nextifysolutions.com
# Legal Department: legal@nextifysolutions.com
# Vendor Manager: vendors@nexlifysolutions.com
# Vendor Portal: https://vendor.nexlifysolutions.com


# 9. Signatures
# Nexlify SolutionsName: [Authorized Representative]Title: [Title]Date: [Date]
# VendorName: [Authorized Representative]Title: [Title]Date: [Date]
#     """
# }

# response = app.invoke(state)

# print(response["answer"])
