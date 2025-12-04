"""
CareerCraft AI v2.2 - Fully Integrated Consumer Platform
=========================================================
EXPANDED: 20 Technical Skills + 15 Other Skills + 50 Careers

New in v2.2:
- 20 Technical Skills (Programming, Data, Cloud, etc.)
- 15 Other Skills (Cognitive + Soft Skills)
- 50 Careers across 8 categories
- Practice frequency weighting (our data moat)
- Readiness bands with honest "1 in X" language
- Model versioning for future calibration
- Quick Mode for faster skill assessment

Data Sources: O*NET 30.0, BLS OEWS May 2023

Run with: python -m streamlit run consumer_careercraft_v2.2.py
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# =============================================================================
# MODEL VERSIONING (for Phase 2 calibration)
# =============================================================================
MODEL_VERSIONS = {
    "practice_weight_version": "1.0",
    "readiness_band_version": "1.0",
    "roi_coefficients_version": "1.0",
    "payload_version": "2.2",
    "skills_version": "2.0",  # 35 skills
    "careers_version": "2.0",  # 50 careers
}

# =============================================================================
# PRACTICE FREQUENCY WEIGHTING (Our Data Moat)
# =============================================================================
def practice_weight(freq: str) -> float:
    """Weight skill level by practice frequency."""
    freq = (freq or "").lower().strip()
    if freq in ["often", "weekly", "daily", "weekly+"]:
        return 1.2
    elif freq in ["sometimes", "monthly", "a few times"]:
        return 1.0
    elif freq in ["rarely", "never", "rarely/never"]:
        return 0.8
    return 1.0

def calculate_effective_level(base_level: int, practice_freq: str) -> float:
    """Calculate effective skill level after practice frequency adjustment."""
    return min(100, base_level * practice_weight(practice_freq))

def get_readiness_band(readiness_score: float) -> tuple:
    """Map readiness score to honest bands with '1 in X' language."""
    if readiness_score >= 75:
        return ("balanced", "Balanced path (about 1 in 2 if you follow through)", "#2ecc71")
    elif readiness_score >= 55:
        return ("stretch", "Stretch path (about 1 in 3-4 if you commit seriously)", "#f39c12")
    else:
        return ("long_shot", "Long-shot path (about 1 in 5+; consider alternatives)", "#e74c3c")

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="CareerCraft AI - Skills + Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# COLOR PALETTE
# =============================================================================
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'tech': '#3498db',
    'healthcare': '#e74c3c',
    'business': '#2ecc71',
    'education': '#9b59b6',
    'community': '#f39c12',
    'mental_health': '#1abc9c',
    'trades': '#e67e22',
    'creative': '#9b59b6',
}

def hex_to_rgba(hex_color, alpha=0.3):
    """Convert hex color to rgba string"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

CATEGORY_COLORS = {
    "Technology": (COLORS['tech'], hex_to_rgba(COLORS['tech'])),
    "Healthcare": (COLORS['healthcare'], hex_to_rgba(COLORS['healthcare'])),
    "Business": (COLORS['business'], hex_to_rgba(COLORS['business'])),
    "Education": (COLORS['education'], hex_to_rgba(COLORS['education'])),
    "Community": (COLORS['community'], hex_to_rgba(COLORS['community'])),
    "Mental Health": (COLORS['mental_health'], hex_to_rgba(COLORS['mental_health'])),
    "Trades": (COLORS['trades'], hex_to_rgba(COLORS['trades'])),
    "Creative": (COLORS['creative'], hex_to_rgba(COLORS['creative'])),
}

# =============================================================================
# TECHNICAL SKILLS (20 Skills)
# Source: O*NET, BLS wage data, industry research
# =============================================================================
TECHNICAL_SKILLS = {
    "Programming & Coding": {
        "category": "Technical",
        "description": "Writing code in languages like Python, Java, JavaScript, C++",
        "salary_premium": 22000,
        "demand_trend": "High Growth",
        "courses": [
            {"name": "Python for Everybody (Coursera)", "cost": 0, "duration": "8 weeks", "roi": 250},
            {"name": "CS50 (Harvard/edX)", "cost": 0, "duration": "12 weeks", "roi": 300},
            {"name": "Full Stack Bootcamp", "cost": 12000, "duration": "12 weeks", "roi": 180},
        ]
    },
    "Data Analysis & Statistics": {
        "category": "Technical",
        "description": "Statistical analysis, data visualization, Excel, SQL, R",
        "salary_premium": 18000,
        "demand_trend": "High Growth",
        "courses": [
            {"name": "Google Data Analytics Certificate", "cost": 0, "duration": "6 months", "roi": 280},
            {"name": "SQL for Data Science", "cost": 50, "duration": "4 weeks", "roi": 320},
            {"name": "Statistics with R (Duke)", "cost": 0, "duration": "5 months", "roi": 260},
        ]
    },
    "Cloud Computing": {
        "category": "Technical",
        "description": "AWS, Azure, GCP, cloud architecture, deployment, DevOps",
        "salary_premium": 25000,
        "demand_trend": "High Growth",
        "courses": [
            {"name": "AWS Cloud Practitioner", "cost": 100, "duration": "4 weeks", "roi": 350},
            {"name": "Azure Fundamentals (AZ-900)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Google Cloud Associate", "cost": 200, "duration": "8 weeks", "roi": 280},
        ]
    },
    "Machine Learning & AI": {
        "category": "Technical",
        "description": "ML algorithms, neural networks, TensorFlow, PyTorch, NLP",
        "salary_premium": 35000,
        "demand_trend": "Very High Growth",
        "courses": [
            {"name": "Machine Learning (Stanford/Coursera)", "cost": 0, "duration": "11 weeks", "roi": 400},
            {"name": "Deep Learning Specialization", "cost": 50, "duration": "5 months", "roi": 350},
            {"name": "Fast.ai Practical Deep Learning", "cost": 0, "duration": "8 weeks", "roi": 380},
        ]
    },
    "Cybersecurity": {
        "category": "Technical",
        "description": "Network security, ethical hacking, compliance, risk assessment",
        "salary_premium": 20000,
        "demand_trend": "Very High Growth",
        "courses": [
            {"name": "CompTIA Security+", "cost": 370, "duration": "8 weeks", "roi": 280},
            {"name": "Google Cybersecurity Certificate", "cost": 0, "duration": "6 months", "roi": 300},
            {"name": "Certified Ethical Hacker (CEH)", "cost": 1200, "duration": "12 weeks", "roi": 220},
        ]
    },
    "Database Management": {
        "category": "Technical",
        "description": "SQL, NoSQL, database design, PostgreSQL, MongoDB",
        "salary_premium": 15000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "SQL Bootcamp (Udemy)", "cost": 20, "duration": "4 weeks", "roi": 400},
            {"name": "MongoDB University", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Database Design Certificate", "cost": 200, "duration": "6 weeks", "roi": 280},
        ]
    },
    "Web Development": {
        "category": "Technical",
        "description": "HTML, CSS, JavaScript, React, Node.js, responsive design",
        "salary_premium": 16000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "freeCodeCamp Web Dev", "cost": 0, "duration": "12 weeks", "roi": 350},
            {"name": "The Odin Project", "cost": 0, "duration": "16 weeks", "roi": 320},
            {"name": "Meta Front-End Certificate", "cost": 0, "duration": "7 months", "roi": 280},
        ]
    },
    "Digital Marketing": {
        "category": "Technical",
        "description": "SEO, SEM, social media marketing, Google Analytics, PPC",
        "salary_premium": 12000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Google Digital Marketing Certificate", "cost": 0, "duration": "6 months", "roi": 250},
            {"name": "HubSpot Inbound Marketing", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Meta Social Media Marketing", "cost": 0, "duration": "5 months", "roi": 260},
        ]
    },
    "Financial Analysis": {
        "category": "Technical",
        "description": "Financial modeling, Excel, valuation, forecasting, FP&A",
        "salary_premium": 18000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Financial Modeling (CFI)", "cost": 500, "duration": "8 weeks", "roi": 220},
            {"name": "Excel for Finance (LinkedIn)", "cost": 30, "duration": "4 weeks", "roi": 350},
            {"name": "CFA Level 1 Prep", "cost": 1000, "duration": "6 months", "roi": 180},
        ]
    },
    "Medical/Clinical Skills": {
        "category": "Technical",
        "description": "Patient care, clinical procedures, medical terminology, EMR",
        "salary_premium": 12000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Medical Terminology Certificate", "cost": 200, "duration": "6 weeks", "roi": 200},
            {"name": "BLS/ACLS Certification", "cost": 150, "duration": "1 week", "roi": 400},
            {"name": "EMR/EHR Training", "cost": 100, "duration": "2 weeks", "roi": 300},
        ]
    },
    "Accounting & Bookkeeping": {
        "category": "Technical",
        "description": "GAAP, financial statements, QuickBooks, tax preparation",
        "salary_premium": 10000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Intuit Bookkeeping Certificate", "cost": 0, "duration": "4 months", "roi": 280},
            {"name": "CPA Exam Prep", "cost": 2000, "duration": "6 months", "roi": 200},
            {"name": "QuickBooks Certification", "cost": 150, "duration": "2 weeks", "roi": 350},
        ]
    },
    "UX/UI Design": {
        "category": "Technical",
        "description": "User research, wireframing, Figma, prototyping, usability",
        "salary_premium": 15000,
        "demand_trend": "High Growth",
        "courses": [
            {"name": "Google UX Design Certificate", "cost": 0, "duration": "6 months", "roi": 280},
            {"name": "Figma UI Design", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Interaction Design (IxDF)", "cost": 100, "duration": "8 weeks", "roi": 260},
        ]
    },
    "Project Management Tools": {
        "category": "Technical",
        "description": "Jira, Asana, MS Project, Agile/Scrum methodologies",
        "salary_premium": 14000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Google Project Management Certificate", "cost": 0, "duration": "6 months", "roi": 280},
            {"name": "PMP Certification Prep", "cost": 500, "duration": "8 weeks", "roi": 220},
            {"name": "Scrum Master Certification", "cost": 200, "duration": "2 weeks", "roi": 320},
        ]
    },
    "CAD & Technical Drawing": {
        "category": "Technical",
        "description": "AutoCAD, SolidWorks, technical drafting, 3D modeling",
        "salary_premium": 12000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "AutoCAD Essentials", "cost": 100, "duration": "6 weeks", "roi": 250},
            {"name": "SolidWorks Certification", "cost": 200, "duration": "8 weeks", "roi": 230},
            {"name": "Technical Drawing Fundamentals", "cost": 50, "duration": "4 weeks", "roi": 280},
        ]
    },
    "Network Administration": {
        "category": "Technical",
        "description": "TCP/IP, routing, firewalls, network troubleshooting, Cisco",
        "salary_premium": 14000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "CompTIA Network+", "cost": 350, "duration": "8 weeks", "roi": 260},
            {"name": "Cisco CCNA", "cost": 330, "duration": "12 weeks", "roi": 280},
            {"name": "Network Fundamentals (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 300},
        ]
    },
    "Video Production & Editing": {
        "category": "Technical",
        "description": "Video editing, Adobe Premiere, Final Cut, filming techniques",
        "salary_premium": 10000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Adobe Premiere Pro Masterclass", "cost": 20, "duration": "6 weeks", "roi": 300},
            {"name": "Video Production (LinkedIn)", "cost": 30, "duration": "4 weeks", "roi": 280},
            {"name": "YouTube Creator Academy", "cost": 0, "duration": "2 weeks", "roi": 350},
        ]
    },
    "Graphic Design": {
        "category": "Technical",
        "description": "Adobe Creative Suite, Photoshop, Illustrator, visual design",
        "salary_premium": 9000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Adobe Creative Suite Basics", "cost": 20, "duration": "8 weeks", "roi": 280},
            {"name": "Graphic Design Specialization (CalArts)", "cost": 0, "duration": "6 months", "roi": 250},
            {"name": "Canva Design School", "cost": 0, "duration": "2 weeks", "roi": 400},
        ]
    },
    "Sales Technology": {
        "category": "Technical",
        "description": "Salesforce, CRM systems, sales automation, pipeline management",
        "salary_premium": 11000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Salesforce Administrator", "cost": 0, "duration": "8 weeks", "roi": 300},
            {"name": "HubSpot Sales Software", "cost": 0, "duration": "3 weeks", "roi": 350},
            {"name": "CRM Fundamentals", "cost": 50, "duration": "4 weeks", "roi": 280},
        ]
    },
    "Laboratory Techniques": {
        "category": "Technical",
        "description": "Lab safety, specimen handling, diagnostic equipment",
        "salary_premium": 8000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Clinical Lab Technician Cert", "cost": 500, "duration": "12 weeks", "roi": 200},
            {"name": "Lab Safety Certification", "cost": 100, "duration": "2 weeks", "roi": 350},
            {"name": "Phlebotomy Certification", "cost": 300, "duration": "4 weeks", "roi": 280},
        ]
    },
    "Legal Research & Writing": {
        "category": "Technical",
        "description": "Legal databases, case research, legal document drafting",
        "salary_premium": 12000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Paralegal Certificate", "cost": 1500, "duration": "6 months", "roi": 200},
            {"name": "Legal Research (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Westlaw/LexisNexis Training", "cost": 200, "duration": "2 weeks", "roi": 280},
        ]
    },
}

# =============================================================================
# OTHER SKILLS (15 Skills - Cognitive + Soft Skills)
# =============================================================================
OTHER_SKILLS = {
    "Critical Thinking": {
        "category": "Cognitive",
        "description": "Evaluating information, logical reasoning, analysis",
        "salary_premium": 12000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Think Again (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Logical and Critical Thinking", "cost": 50, "duration": "6 weeks", "roi": 300},
            {"name": "Decision Making (LinkedIn)", "cost": 30, "duration": "3 weeks", "roi": 320},
        ]
    },
    "Problem Solving": {
        "category": "Cognitive",
        "description": "Analytical thinking, troubleshooting, root cause analysis",
        "salary_premium": 14000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Design Thinking (IDEO)", "cost": 400, "duration": "4 weeks", "roi": 200},
            {"name": "Problem Solving Specialization", "cost": 50, "duration": "6 weeks", "roi": 280},
            {"name": "Six Sigma Yellow Belt", "cost": 200, "duration": "4 weeks", "roi": 250},
        ]
    },
    "Strategic Thinking": {
        "category": "Cognitive",
        "description": "Long-term planning, business strategy, competitive analysis",
        "salary_premium": 18000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Business Strategy (Wharton)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Strategic Management Certificate", "cost": 500, "duration": "8 weeks", "roi": 220},
            {"name": "Competitive Strategy", "cost": 50, "duration": "6 weeks", "roi": 280},
        ]
    },
    "Creativity & Innovation": {
        "category": "Cognitive",
        "description": "Ideation, design thinking, creative problem solving",
        "salary_premium": 10000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Creative Thinking (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Design Sprint Masterclass", "cost": 300, "duration": "2 weeks", "roi": 280},
            {"name": "Innovation Management", "cost": 0, "duration": "6 weeks", "roi": 260},
        ]
    },
    "Research & Analysis": {
        "category": "Cognitive",
        "description": "Information gathering, synthesis, market/academic research",
        "salary_premium": 11000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Research Methods (Coursera)", "cost": 0, "duration": "6 weeks", "roi": 280},
            {"name": "Market Research Certificate", "cost": 300, "duration": "4 weeks", "roi": 250},
            {"name": "UX Research Fundamentals", "cost": 150, "duration": "4 weeks", "roi": 300},
        ]
    },
    "Communication": {
        "category": "Soft",
        "description": "Written and verbal communication, presentations",
        "salary_premium": 10000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Business Writing (LinkedIn)", "cost": 30, "duration": "3 weeks", "roi": 400},
            {"name": "Public Speaking Mastery", "cost": 20, "duration": "4 weeks", "roi": 350},
            {"name": "Technical Communication", "cost": 0, "duration": "4 weeks", "roi": 320},
        ]
    },
    "Leadership": {
        "category": "Soft",
        "description": "Team leadership, motivation, vision-setting, influence",
        "salary_premium": 20000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Leading People (Michigan)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Executive Leadership Program", "cost": 2000, "duration": "12 weeks", "roi": 180},
            {"name": "Situational Leadership", "cost": 500, "duration": "2 weeks", "roi": 250},
        ]
    },
    "Teamwork & Collaboration": {
        "category": "Soft",
        "description": "Working in teams, conflict resolution, collaboration",
        "salary_premium": 7000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Teamwork Skills (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Collaborative Leadership", "cost": 200, "duration": "6 weeks", "roi": 250},
            {"name": "High-Performing Teams (edX)", "cost": 0, "duration": "4 weeks", "roi": 280},
        ]
    },
    "Emotional Intelligence": {
        "category": "Soft",
        "description": "Self-awareness, empathy, relationship management",
        "salary_premium": 12000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Emotional Intelligence (Yale)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Developing EQ at Work", "cost": 100, "duration": "6 weeks", "roi": 300},
            {"name": "Empathy in Leadership", "cost": 50, "duration": "3 weeks", "roi": 320},
        ]
    },
    "Time Management": {
        "category": "Soft",
        "description": "Prioritization, scheduling, productivity",
        "salary_premium": 6000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Getting Things Done (GTD)", "cost": 50, "duration": "2 weeks", "roi": 500},
            {"name": "Work Smarter, Not Harder", "cost": 0, "duration": "3 weeks", "roi": 400},
            {"name": "Productivity Masterclass", "cost": 100, "duration": "4 weeks", "roi": 350},
        ]
    },
    "Attention to Detail": {
        "category": "Soft",
        "description": "Accuracy, quality control, thoroughness",
        "salary_premium": 8000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Quality Assurance Fundamentals", "cost": 100, "duration": "4 weeks", "roi": 300},
            {"name": "Proofreading & Editing", "cost": 50, "duration": "2 weeks", "roi": 350},
            {"name": "Detail-Oriented Thinking", "cost": 0, "duration": "3 weeks", "roi": 320},
        ]
    },
    "Customer Service": {
        "category": "Soft",
        "description": "Client relations, conflict resolution, service excellence",
        "salary_premium": 5000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Customer Service Fundamentals", "cost": 0, "duration": "3 weeks", "roi": 350},
            {"name": "Client Relationship Management", "cost": 100, "duration": "4 weeks", "roi": 300},
            {"name": "Handling Difficult Customers", "cost": 50, "duration": "2 weeks", "roi": 320},
        ]
    },
    "Adaptability": {
        "category": "Soft",
        "description": "Flexibility, learning agility, handling change",
        "salary_premium": 9000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Adaptability and Resiliency", "cost": 30, "duration": "3 weeks", "roi": 350},
            {"name": "Growth Mindset", "cost": 0, "duration": "2 weeks", "roi": 400},
            {"name": "Change Management Fundamentals", "cost": 200, "duration": "4 weeks", "roi": 280},
        ]
    },
    "Negotiation": {
        "category": "Soft",
        "description": "Deal-making, conflict resolution, persuasion",
        "salary_premium": 15000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Successful Negotiation (Michigan)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Negotiation Mastery (Harvard)", "cost": 1500, "duration": "6 weeks", "roi": 220},
            {"name": "Salary Negotiation Workshop", "cost": 50, "duration": "1 week", "roi": 500},
        ]
    },
    "Mentoring & Coaching": {
        "category": "Soft",
        "description": "Developing others, feedback delivery, coaching",
        "salary_premium": 10000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Coaching Skills for Managers", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "ICF Coaching Fundamentals", "cost": 500, "duration": "8 weeks", "roi": 220},
            {"name": "Effective Feedback (LinkedIn)", "cost": 30, "duration": "2 weeks", "roi": 350},
        ]
    },
}

# Combine all skills
SKILLS_DATA = {**TECHNICAL_SKILLS, **OTHER_SKILLS}

# Key skills for Quick Mode
KEY_SKILLS = [
    "Programming & Coding", "Data Analysis & Statistics", "Cloud Computing",
    "Digital Marketing", "Financial Analysis", "Medical/Clinical Skills",
    "Critical Thinking", "Problem Solving", "Communication",
    "Leadership", "Emotional Intelligence", "Adaptability"
]

# =============================================================================
# CAREER DATA (50 Careers across 8 Categories)
# =============================================================================
CAREER_DATA = {
    # TECHNOLOGY (10)
    "Software Developer": {
        "category": "Technology",
        "skills": {"Programming & Coding": 95, "Problem Solving": 90, "Critical Thinking": 85, "Communication": 70, "Teamwork & Collaboration": 75, "Time Management": 80, "Database Management": 70, "Attention to Detail": 85},
        "median_salary": 124200, "growth_rate": 25, "education": "Bachelor's Degree",
        "entry_paths": ["CS Degree", "Coding Bootcamp", "Self-taught + Portfolio"], "time_to_entry": "6-24 months"
    },
    "Data Scientist": {
        "category": "Technology",
        "skills": {"Data Analysis & Statistics": 95, "Programming & Coding": 85, "Machine Learning & AI": 85, "Critical Thinking": 95, "Communication": 75, "Research & Analysis": 90, "Problem Solving": 90, "Strategic Thinking": 80},
        "median_salary": 103500, "growth_rate": 35, "education": "Master's Degree",
        "entry_paths": ["Statistics/Math Degree", "Data Analytics Certificate", "PhD"], "time_to_entry": "12-36 months"
    },
    "Cloud Engineer": {
        "category": "Technology",
        "skills": {"Cloud Computing": 95, "Programming & Coding": 80, "Network Administration": 75, "Cybersecurity": 70, "Problem Solving": 90, "Critical Thinking": 85, "Communication": 70, "Attention to Detail": 85},
        "median_salary": 125000, "growth_rate": 28, "education": "Bachelor's + Certs",
        "entry_paths": ["CS Degree + AWS/Azure Certs", "IT Experience + Cloud Certs"], "time_to_entry": "12-24 months"
    },
    "Cybersecurity Analyst": {
        "category": "Technology",
        "skills": {"Cybersecurity": 95, "Network Administration": 80, "Problem Solving": 90, "Critical Thinking": 95, "Attention to Detail": 95, "Communication": 70, "Research & Analysis": 85, "Adaptability": 80},
        "median_salary": 112000, "growth_rate": 32, "education": "Bachelor's + Certs",
        "entry_paths": ["IT Degree", "Security Certifications", "IT Experience + Certs"], "time_to_entry": "12-24 months"
    },
    "UX Designer": {
        "category": "Technology",
        "skills": {"UX/UI Design": 95, "Research & Analysis": 85, "Creativity & Innovation": 90, "Communication": 90, "Teamwork & Collaboration": 85, "Problem Solving": 85, "Emotional Intelligence": 75, "Attention to Detail": 85},
        "median_salary": 97500, "growth_rate": 15, "education": "Bachelor's Degree",
        "entry_paths": ["Design Degree", "UX Bootcamp", "Graphic Design + Portfolio"], "time_to_entry": "6-18 months"
    },
    "DevOps Engineer": {
        "category": "Technology",
        "skills": {"Cloud Computing": 90, "Programming & Coding": 85, "Network Administration": 75, "Problem Solving": 90, "Critical Thinking": 85, "Teamwork & Collaboration": 80, "Attention to Detail": 90, "Adaptability": 85},
        "median_salary": 115000, "growth_rate": 22, "education": "Bachelor's Degree",
        "entry_paths": ["CS/IT Degree", "Developer + Ops Experience", "DevOps Bootcamp"], "time_to_entry": "12-36 months"
    },
    "Product Manager": {
        "category": "Technology",
        "skills": {"Strategic Thinking": 95, "Communication": 95, "Problem Solving": 90, "Leadership": 85, "Data Analysis & Statistics": 75, "Creativity & Innovation": 85, "Teamwork & Collaboration": 90, "Customer Service": 80},
        "median_salary": 130000, "growth_rate": 18, "education": "Bachelor's Degree",
        "entry_paths": ["Engineering + MBA", "Design + Business", "Domain Expert + PM Cert"], "time_to_entry": "24-48 months"
    },
    "Machine Learning Engineer": {
        "category": "Technology",
        "skills": {"Machine Learning & AI": 95, "Programming & Coding": 95, "Data Analysis & Statistics": 90, "Critical Thinking": 95, "Problem Solving": 95, "Research & Analysis": 85, "Communication": 70, "Attention to Detail": 90},
        "median_salary": 150000, "growth_rate": 40, "education": "Master's/PhD",
        "entry_paths": ["CS/Math PhD", "MS + ML Experience", "Strong Portfolio"], "time_to_entry": "24-60 months"
    },
    "IT Support Specialist": {
        "category": "Technology",
        "skills": {"Problem Solving": 85, "Communication": 85, "Customer Service": 90, "Network Administration": 60, "Critical Thinking": 75, "Time Management": 80, "Adaptability": 85, "Attention to Detail": 75},
        "median_salary": 57910, "growth_rate": 6, "education": "Associate's/Certificate",
        "entry_paths": ["CompTIA A+", "IT Certificate", "Help Desk Experience"], "time_to_entry": "3-12 months"
    },
    "Data Engineer": {
        "category": "Technology",
        "skills": {"Programming & Coding": 90, "Database Management": 95, "Cloud Computing": 85, "Data Analysis & Statistics": 80, "Problem Solving": 90, "Critical Thinking": 85, "Attention to Detail": 90, "Communication": 65},
        "median_salary": 112000, "growth_rate": 30, "education": "Bachelor's Degree",
        "entry_paths": ["CS/Data Science Degree", "Software Dev + Data Focus"], "time_to_entry": "12-24 months"
    },
    
    # HEALTHCARE (7)
    "Registered Nurse": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 95, "Communication": 95, "Critical Thinking": 90, "Emotional Intelligence": 90, "Teamwork & Collaboration": 95, "Time Management": 90, "Attention to Detail": 95, "Adaptability": 85},
        "median_salary": 81220, "growth_rate": 6, "education": "Bachelor's (BSN)",
        "entry_paths": ["BSN Degree", "ADN + RN-to-BSN Bridge", "Accelerated BSN"], "time_to_entry": "24-48 months"
    },
    "Physical Therapist": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 95, "Communication": 95, "Problem Solving": 90, "Critical Thinking": 85, "Emotional Intelligence": 85, "Attention to Detail": 90, "Time Management": 85, "Adaptability": 80},
        "median_salary": 97720, "growth_rate": 15, "education": "Doctoral (DPT)",
        "entry_paths": ["Pre-PT Undergrad + DPT", "Athletic Training + DPT"], "time_to_entry": "72-84 months"
    },
    "Healthcare Administrator": {
        "category": "Healthcare",
        "skills": {"Leadership": 90, "Communication": 95, "Strategic Thinking": 90, "Problem Solving": 85, "Financial Analysis": 70, "Time Management": 95, "Teamwork & Collaboration": 90, "Medical/Clinical Skills": 50},
        "median_salary": 110680, "growth_rate": 28, "education": "Master's (MHA/MBA)",
        "entry_paths": ["Healthcare Experience + MBA", "MHA Degree", "Clinical + Management"], "time_to_entry": "24-48 months"
    },
    "Pharmacist": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 95, "Attention to Detail": 98, "Critical Thinking": 90, "Communication": 85, "Customer Service": 85, "Problem Solving": 85, "Time Management": 85, "Research & Analysis": 80},
        "median_salary": 132750, "growth_rate": 3, "education": "Doctoral (PharmD)",
        "entry_paths": ["Pre-Pharmacy + PharmD", "Pharmacy Tech + PharmD"], "time_to_entry": "72-96 months"
    },
    "Medical Assistant": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 80, "Communication": 90, "Customer Service": 90, "Attention to Detail": 90, "Teamwork & Collaboration": 85, "Time Management": 85, "Emotional Intelligence": 80, "Adaptability": 80},
        "median_salary": 38270, "growth_rate": 14, "education": "Certificate/Associate's",
        "entry_paths": ["MA Certificate", "Associate's Degree", "On-the-job Training"], "time_to_entry": "6-12 months"
    },
    "Physician Assistant": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 95, "Critical Thinking": 95, "Communication": 95, "Problem Solving": 90, "Emotional Intelligence": 85, "Attention to Detail": 95, "Time Management": 90, "Adaptability": 85},
        "median_salary": 126010, "growth_rate": 27, "education": "Master's Degree",
        "entry_paths": ["Pre-Med + PA Program", "Healthcare Experience + PA School"], "time_to_entry": "60-84 months"
    },
    "Dental Hygienist": {
        "category": "Healthcare",
        "skills": {"Medical/Clinical Skills": 90, "Communication": 90, "Attention to Detail": 95, "Customer Service": 90, "Time Management": 85, "Emotional Intelligence": 80, "Critical Thinking": 75, "Adaptability": 75},
        "median_salary": 81400, "growth_rate": 7, "education": "Associate's Degree",
        "entry_paths": ["Dental Hygiene Program", "Dental Assisting + Bridge"], "time_to_entry": "24-36 months"
    },
    
    # BUSINESS (8)
    "Project Manager": {
        "category": "Business",
        "skills": {"Project Management Tools": 95, "Communication": 95, "Leadership": 85, "Problem Solving": 90, "Time Management": 95, "Strategic Thinking": 80, "Teamwork & Collaboration": 90, "Attention to Detail": 85},
        "median_salary": 95370, "growth_rate": 7, "education": "Bachelor's + PMP",
        "entry_paths": ["Any Degree + PMP Cert", "Experience + Agile Certs", "MBA"], "time_to_entry": "12-36 months"
    },
    "Financial Analyst": {
        "category": "Business",
        "skills": {"Financial Analysis": 95, "Data Analysis & Statistics": 90, "Critical Thinking": 95, "Communication": 80, "Attention to Detail": 95, "Problem Solving": 85, "Time Management": 85, "Strategic Thinking": 80},
        "median_salary": 96220, "growth_rate": 9, "education": "Bachelor's Degree",
        "entry_paths": ["Finance Degree", "Accounting + CFA", "Economics + Financial Modeling"], "time_to_entry": "12-24 months"
    },
    "Marketing Manager": {
        "category": "Business",
        "skills": {"Digital Marketing": 90, "Communication": 95, "Creativity & Innovation": 95, "Strategic Thinking": 90, "Data Analysis & Statistics": 75, "Leadership": 80, "Project Management Tools": 80, "Customer Service": 75},
        "median_salary": 140040, "growth_rate": 6, "education": "Bachelor's Degree",
        "entry_paths": ["Marketing Degree", "Business + Marketing Experience", "Digital Marketing Certs"], "time_to_entry": "24-48 months"
    },
    "Human Resources Manager": {
        "category": "Business",
        "skills": {"Communication": 95, "Emotional Intelligence": 95, "Leadership": 85, "Problem Solving": 85, "Critical Thinking": 85, "Time Management": 90, "Teamwork & Collaboration": 90, "Negotiation": 85},
        "median_salary": 130000, "growth_rate": 5, "education": "Bachelor's Degree",
        "entry_paths": ["HR Degree", "Business + SHRM Cert", "Psychology + HR Experience"], "time_to_entry": "24-48 months"
    },
    "Accountant": {
        "category": "Business",
        "skills": {"Accounting & Bookkeeping": 95, "Attention to Detail": 95, "Critical Thinking": 85, "Communication": 75, "Time Management": 90, "Problem Solving": 80, "Financial Analysis": 80, "Adaptability": 70},
        "median_salary": 78000, "growth_rate": 4, "education": "Bachelor's Degree",
        "entry_paths": ["Accounting Degree", "Finance + CPA", "Business + Accounting Certs"], "time_to_entry": "12-24 months"
    },
    "Business Analyst": {
        "category": "Business",
        "skills": {"Data Analysis & Statistics": 90, "Communication": 90, "Critical Thinking": 90, "Problem Solving": 90, "Strategic Thinking": 80, "Attention to Detail": 85, "Project Management Tools": 75, "Adaptability": 80},
        "median_salary": 93000, "growth_rate": 11, "education": "Bachelor's Degree",
        "entry_paths": ["Business/IT Degree", "Domain Experience + BA Cert", "MBA"], "time_to_entry": "12-36 months"
    },
    "Sales Manager": {
        "category": "Business",
        "skills": {"Communication": 95, "Leadership": 90, "Negotiation": 95, "Strategic Thinking": 85, "Emotional Intelligence": 85, "Sales Technology": 80, "Customer Service": 90, "Adaptability": 85},
        "median_salary": 130600, "growth_rate": 4, "education": "Bachelor's Degree",
        "entry_paths": ["Sales Experience + Promotion", "Business Degree", "Any Degree + Sales Track"], "time_to_entry": "24-48 months"
    },
    "Management Consultant": {
        "category": "Business",
        "skills": {"Strategic Thinking": 95, "Problem Solving": 95, "Communication": 95, "Data Analysis & Statistics": 85, "Critical Thinking": 95, "Leadership": 80, "Adaptability": 90, "Time Management": 85},
        "median_salary": 98000, "growth_rate": 10, "education": "Bachelor's/MBA",
        "entry_paths": ["Top MBA", "Big 4 Accounting + Transition", "Industry Expert + MBA"], "time_to_entry": "24-60 months"
    },
    
    # EDUCATION (6)
    "High School Teacher": {
        "category": "Education",
        "skills": {"Communication": 95, "Emotional Intelligence": 90, "Critical Thinking": 85, "Creativity & Innovation": 85, "Time Management": 90, "Adaptability": 85, "Problem Solving": 80, "Leadership": 75},
        "median_salary": 62360, "growth_rate": 1, "education": "Bachelor's + Cert",
        "entry_paths": ["Education Degree + License", "Subject Degree + Teaching Cert", "Alternative Certification"], "time_to_entry": "12-48 months"
    },
    "Instructional Designer": {
        "category": "Education",
        "skills": {"Creativity & Innovation": 95, "Communication": 90, "Critical Thinking": 85, "Problem Solving": 85, "Project Management Tools": 80, "Research & Analysis": 80, "UX/UI Design": 70, "Attention to Detail": 85},
        "median_salary": 74620, "growth_rate": 11, "education": "Master's Degree",
        "entry_paths": ["ID Master's", "Teaching Experience + ID Cert", "Ed Tech Degree"], "time_to_entry": "12-24 months"
    },
    "School Counselor": {
        "category": "Education",
        "skills": {"Emotional Intelligence": 95, "Communication": 95, "Critical Thinking": 90, "Problem Solving": 90, "Adaptability": 85, "Time Management": 85, "Leadership": 75, "Research & Analysis": 70},
        "median_salary": 60140, "growth_rate": 5, "education": "Master's Degree",
        "entry_paths": ["Counseling Master's + License", "Psychology + School Counseling Cert"], "time_to_entry": "24-36 months"
    },
    "University Professor": {
        "category": "Education",
        "skills": {"Research & Analysis": 95, "Communication": 90, "Critical Thinking": 95, "Creativity & Innovation": 85, "Time Management": 80, "Leadership": 70, "Problem Solving": 85, "Attention to Detail": 85},
        "median_salary": 80840, "growth_rate": 8, "education": "Doctoral Degree",
        "entry_paths": ["PhD + Postdoc", "Terminal Master's (some fields)", "Industry + PhD"], "time_to_entry": "60-96 months"
    },
    "Corporate Trainer": {
        "category": "Education",
        "skills": {"Communication": 95, "Creativity & Innovation": 85, "Emotional Intelligence": 85, "Problem Solving": 80, "Time Management": 85, "Adaptability": 85, "Leadership": 75, "Attention to Detail": 75},
        "median_salary": 63080, "growth_rate": 6, "education": "Bachelor's Degree",
        "entry_paths": ["HR/Education Degree", "Industry Expert + Training Cert", "Teaching + Corporate Transition"], "time_to_entry": "12-24 months"
    },
    "Education Administrator": {
        "category": "Education",
        "skills": {"Leadership": 95, "Communication": 95, "Strategic Thinking": 90, "Problem Solving": 85, "Time Management": 90, "Emotional Intelligence": 85, "Critical Thinking": 85, "Adaptability": 80},
        "median_salary": 99940, "growth_rate": 4, "education": "Master's Degree",
        "entry_paths": ["Teaching Experience + Admin Cert", "Ed Leadership Master's", "MBA + Education Focus"], "time_to_entry": "36-60 months"
    },
    
    # MENTAL HEALTH (5)
    "Clinical Psychologist": {
        "category": "Mental Health",
        "skills": {"Emotional Intelligence": 98, "Communication": 95, "Critical Thinking": 95, "Research & Analysis": 90, "Problem Solving": 90, "Attention to Detail": 85, "Adaptability": 85, "Time Management": 80},
        "median_salary": 85330, "growth_rate": 6, "education": "Doctoral (PhD/PsyD)",
        "entry_paths": ["Psychology PhD", "PsyD Program", "Research Track + Clinical"], "time_to_entry": "96-120 months"
    },
    "Licensed Counselor (LPC)": {
        "category": "Mental Health",
        "skills": {"Emotional Intelligence": 95, "Communication": 95, "Critical Thinking": 90, "Problem Solving": 85, "Adaptability": 85, "Time Management": 80, "Attention to Detail": 75, "Research & Analysis": 70},
        "median_salary": 49710, "growth_rate": 18, "education": "Master's Degree",
        "entry_paths": ["Counseling Master's", "Psychology + Counseling Cert", "Social Work + Transition"], "time_to_entry": "36-60 months"
    },
    "Marriage & Family Therapist": {
        "category": "Mental Health",
        "skills": {"Emotional Intelligence": 98, "Communication": 95, "Critical Thinking": 90, "Problem Solving": 90, "Adaptability": 85, "Negotiation": 80, "Research & Analysis": 75, "Time Management": 80},
        "median_salary": 56570, "growth_rate": 15, "education": "Master's Degree",
        "entry_paths": ["MFT Master's", "Counseling + MFT Track", "Social Work + Family Focus"], "time_to_entry": "36-60 months"
    },
    "Psychiatric Nurse Practitioner": {
        "category": "Mental Health",
        "skills": {"Medical/Clinical Skills": 90, "Emotional Intelligence": 95, "Communication": 95, "Critical Thinking": 90, "Adaptability": 90, "Attention to Detail": 90, "Problem Solving": 85, "Teamwork & Collaboration": 85},
        "median_salary": 125900, "growth_rate": 40, "education": "Master's (MSN)",
        "entry_paths": ["BSN + Psych MSN", "RN Experience + MSN", "Direct Entry MSN"], "time_to_entry": "48-72 months"
    },
    "Substance Abuse Counselor": {
        "category": "Mental Health",
        "skills": {"Emotional Intelligence": 95, "Communication": 95, "Adaptability": 90, "Problem Solving": 85, "Critical Thinking": 80, "Time Management": 80, "Customer Service": 80, "Attention to Detail": 75},
        "median_salary": 48520, "growth_rate": 18, "education": "Bachelor's/Master's",
        "entry_paths": ["Counseling Degree", "Psychology + CADC Cert", "Recovery Experience + Training"], "time_to_entry": "24-48 months"
    },
    
    # COMMUNITY (4)
    "Social Worker": {
        "category": "Community",
        "skills": {"Emotional Intelligence": 95, "Communication": 95, "Critical Thinking": 90, "Problem Solving": 90, "Adaptability": 90, "Time Management": 85, "Teamwork & Collaboration": 85, "Customer Service": 85},
        "median_salary": 55350, "growth_rate": 7, "education": "Bachelor's/Master's",
        "entry_paths": ["BSW", "MSW", "Related Degree + MSW"], "time_to_entry": "24-48 months"
    },
    "Community Health Worker": {
        "category": "Community",
        "skills": {"Communication": 95, "Emotional Intelligence": 90, "Customer Service": 90, "Adaptability": 90, "Problem Solving": 80, "Time Management": 80, "Critical Thinking": 75, "Teamwork & Collaboration": 85},
        "median_salary": 48200, "growth_rate": 14, "education": "High School/Certificate",
        "entry_paths": ["CHW Certificate", "Public Health Training", "Community Experience"], "time_to_entry": "3-12 months"
    },
    "Nonprofit Program Manager": {
        "category": "Community",
        "skills": {"Leadership": 90, "Communication": 95, "Project Management Tools": 85, "Strategic Thinking": 85, "Problem Solving": 85, "Time Management": 90, "Adaptability": 85, "Emotional Intelligence": 85},
        "median_salary": 65000, "growth_rate": 9, "education": "Bachelor's Degree",
        "entry_paths": ["Nonprofit Experience + Promotion", "MPA/MBA", "Social Work + Management"], "time_to_entry": "24-48 months"
    },
    "Case Manager": {
        "category": "Community",
        "skills": {"Communication": 95, "Emotional Intelligence": 90, "Problem Solving": 90, "Time Management": 90, "Critical Thinking": 85, "Attention to Detail": 85, "Adaptability": 90, "Customer Service": 90},
        "median_salary": 45760, "growth_rate": 10, "education": "Bachelor's Degree",
        "entry_paths": ["Social Work Degree", "Human Services + Experience", "Psychology + Case Mgmt Cert"], "time_to_entry": "12-24 months"
    },
    
    # TRADES (4)
    "Electrician": {
        "category": "Trades",
        "skills": {"Problem Solving": 90, "Critical Thinking": 85, "Attention to Detail": 95, "Time Management": 85, "Communication": 75, "Adaptability": 85, "Customer Service": 80, "CAD & Technical Drawing": 60},
        "median_salary": 60240, "growth_rate": 6, "education": "Apprenticeship",
        "entry_paths": ["Electrical Apprenticeship", "Trade School + Apprenticeship", "Military Training"], "time_to_entry": "48-60 months"
    },
    "HVAC Technician": {
        "category": "Trades",
        "skills": {"Problem Solving": 90, "Attention to Detail": 90, "Critical Thinking": 80, "Customer Service": 85, "Time Management": 85, "Communication": 80, "Adaptability": 85, "Teamwork & Collaboration": 70},
        "median_salary": 51390, "growth_rate": 5, "education": "Certificate/Apprenticeship",
        "entry_paths": ["HVAC Program", "Apprenticeship", "Military Training"], "time_to_entry": "12-24 months"
    },
    "Construction Manager": {
        "category": "Trades",
        "skills": {"Leadership": 90, "Problem Solving": 90, "Communication": 90, "Project Management Tools": 95, "Time Management": 95, "Critical Thinking": 85, "Attention to Detail": 85, "Negotiation": 80},
        "median_salary": 101480, "growth_rate": 5, "education": "Bachelor's Degree",
        "entry_paths": ["Construction Management Degree", "Trade Experience + Degree", "Engineering + Experience"], "time_to_entry": "48-72 months"
    },
    "Plumber": {
        "category": "Trades",
        "skills": {"Problem Solving": 90, "Attention to Detail": 90, "Critical Thinking": 80, "Customer Service": 85, "Time Management": 85, "Communication": 75, "Adaptability": 85, "CAD & Technical Drawing": 50},
        "median_salary": 59880, "growth_rate": 2, "education": "Apprenticeship",
        "entry_paths": ["Plumbing Apprenticeship", "Trade School", "Helper + Training"], "time_to_entry": "48-60 months"
    },
    
    # CREATIVE (6)
    "Graphic Designer": {
        "category": "Creative",
        "skills": {"Graphic Design": 95, "Creativity & Innovation": 95, "Communication": 85, "Attention to Detail": 90, "UX/UI Design": 70, "Time Management": 85, "Adaptability": 85, "Problem Solving": 75},
        "median_salary": 57990, "growth_rate": 3, "education": "Bachelor's Degree",
        "entry_paths": ["Graphic Design Degree", "Art + Digital Skills", "Self-taught + Portfolio"], "time_to_entry": "12-48 months"
    },
    "Content Writer/Copywriter": {
        "category": "Creative",
        "skills": {"Communication": 95, "Creativity & Innovation": 90, "Research & Analysis": 85, "Attention to Detail": 90, "Time Management": 85, "Critical Thinking": 80, "Digital Marketing": 70, "Adaptability": 85},
        "median_salary": 73150, "growth_rate": 4, "education": "Bachelor's Degree",
        "entry_paths": ["English/Communications Degree", "Journalism", "Any Degree + Writing Portfolio"], "time_to_entry": "6-24 months"
    },
    "Video Producer": {
        "category": "Creative",
        "skills": {"Video Production & Editing": 95, "Creativity & Innovation": 95, "Communication": 90, "Project Management Tools": 80, "Problem Solving": 85, "Time Management": 85, "Teamwork & Collaboration": 85, "Attention to Detail": 85},
        "median_salary": 73500, "growth_rate": 8, "education": "Bachelor's Degree",
        "entry_paths": ["Film/Media Degree", "Communications + Production Experience", "Self-taught + Portfolio"], "time_to_entry": "12-36 months"
    },
    "Social Media Manager": {
        "category": "Creative",
        "skills": {"Digital Marketing": 95, "Creativity & Innovation": 90, "Communication": 95, "Data Analysis & Statistics": 70, "Time Management": 85, "Adaptability": 90, "Customer Service": 85, "Strategic Thinking": 75},
        "median_salary": 64000, "growth_rate": 10, "education": "Bachelor's Degree",
        "entry_paths": ["Marketing/Communications Degree", "Digital Marketing Cert", "Content Creator + Strategy"], "time_to_entry": "12-24 months"
    },
    "Photographer": {
        "category": "Creative",
        "skills": {"Creativity & Innovation": 95, "Attention to Detail": 90, "Communication": 85, "Customer Service": 85, "Time Management": 80, "Problem Solving": 75, "Adaptability": 85, "Video Production & Editing": 60},
        "median_salary": 40000, "growth_rate": 4, "education": "Certificate/Bachelor's",
        "entry_paths": ["Photography Program", "Art Degree + Specialization", "Self-taught + Portfolio"], "time_to_entry": "6-24 months"
    },
    "UI/UX Researcher": {
        "category": "Creative",
        "skills": {"Research & Analysis": 95, "Communication": 90, "Critical Thinking": 90, "Emotional Intelligence": 85, "UX/UI Design": 80, "Data Analysis & Statistics": 75, "Problem Solving": 85, "Attention to Detail": 85},
        "median_salary": 95000, "growth_rate": 15, "education": "Bachelor's/Master's",
        "entry_paths": ["Psychology/HCI Degree", "UX Design + Research Focus", "Social Science + UX Cert"], "time_to_entry": "12-36 months"
    },
}

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 0
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'user_skills' not in st.session_state:
    st.session_state.user_skills = {skill: 50 for skill in SKILLS_DATA.keys()}
if 'target_careers' not in st.session_state:
    st.session_state.target_careers = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'practice_freq' not in st.session_state:
    st.session_state.practice_freq = {}
if 'quick_mode' not in st.session_state:
    st.session_state.quick_mode = False

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; background: linear-gradient(135deg, #2E86AB, #A23B72); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: bold; }
    .progress-container { background: #1a1a2e; border-radius: 10px; padding: 5px; margin: 1rem 0; }
    .progress-bar { background: linear-gradient(90deg, #2E86AB, #A23B72); border-radius: 8px; height: 10px; transition: width 0.3s ease; }
    .step { flex: 1; text-align: center; padding: 10px; border-radius: 5px; margin: 0 5px; }
    .step-active { background: #2E86AB; color: white; }
    .step-complete { background: #2ecc71; color: white; }
    .step-pending { background: #333; color: #888; }
    .info-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 15px; padding: 1.5rem; border: 1px solid #2E86AB; margin: 0.5rem 0; }
    .roi-positive { color: #2ecc71; font-weight: bold; }
    .category-technology { background: #3498db; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-healthcare { background: #e74c3c; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-business { background: #2ecc71; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-education { background: #9b59b6; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-community { background: #f39c12; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-mental-health { background: #1abc9c; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-trades { background: #e67e22; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-creative { background: #9b59b6; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .welcome-box { background: linear-gradient(135deg, #1e3a5f, #2E86AB); border-radius: 20px; padding: 2rem; text-align: center; margin: 2rem 0; }
    .skill-gap-high { color: #e74c3c; }
    .skill-gap-medium { color: #f39c12; }
    .skill-gap-low { color: #2ecc71; }
    .skill-category-header { background: linear-gradient(90deg, #2E86AB, #1a1a2e); padding: 10px 15px; border-radius: 8px; margin: 15px 0 10px 0; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def calculate_skill_gaps(user_skills, target_career):
    if target_career not in CAREER_DATA:
        return {}
    career_skills = CAREER_DATA[target_career]["skills"]
    gaps = {}
    for skill, required_level in career_skills.items():
        user_level = user_skills.get(skill, 0)
        gap = required_level - user_level
        gaps[skill] = {"user_level": user_level, "required_level": required_level, "gap": max(0, gap), "priority": "High" if gap > 30 else "Medium" if gap > 15 else "Low"}
    return gaps

def calculate_skill_roi(skill_name, current_level, target_level):
    if skill_name not in SKILLS_DATA:
        return None
    skill_info = SKILLS_DATA[skill_name]
    improvement = target_level - current_level
    salary_increase = (improvement / 100) * skill_info["salary_premium"]
    return {"skill": skill_name, "current_level": current_level, "target_level": target_level, "improvement_needed": improvement, "potential_salary_increase": salary_increase, "demand_trend": skill_info["demand_trend"], "courses": skill_info["courses"]}

def get_career_matches(user_skills, target_industries):
    matches = []
    practice_freq = st.session_state.get('practice_freq', {})
    for career, data in CAREER_DATA.items():
        if data["category"] in target_industries:
            total_match = 0
            total_weight = 0
            for skill, required in data["skills"].items():
                user_level = user_skills.get(skill, 0)
                freq = practice_freq.get(skill, "Sometimes")
                effective_level = calculate_effective_level(user_level, freq)
                weight = required / 100
                match = min(effective_level / required, 1.0) if required > 0 else 1.0
                total_match += match * weight
                total_weight += weight
            match_pct = (total_match / total_weight * 100) if total_weight > 0 else 0
            gaps = calculate_skill_gaps(user_skills, career)
            high_gaps = sum(1 for g in gaps.values() if g["priority"] == "High")
            matches.append({"career": career, "category": data["category"], "match_pct": match_pct, "salary": data["median_salary"], "growth": data["growth_rate"], "high_skill_gaps": high_gaps, "education": data["education"], "time_to_entry": data["time_to_entry"]})
    matches.sort(key=lambda x: x["match_pct"], reverse=True)
    return matches

def hex_to_rgba(hex_color, alpha=0.3):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

def create_skill_radar(careers_to_compare, user_skills=None, title="Skill Comparison"):
    fig = go.Figure()
    all_skills = set()
    for career in careers_to_compare:
        if career in CAREER_DATA:
            all_skills.update(CAREER_DATA[career]["skills"].keys())
    skills = sorted(list(all_skills))[:10]
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#2ecc71']
    if user_skills:
        values = [user_skills.get(skill, 0) for skill in skills]
        values.append(values[0])
        skills_closed = skills + [skills[0]]
        fig.add_trace(go.Scatterpolar(r=values, theta=skills_closed, fill='toself', fillcolor='rgba(46, 204, 113, 0.2)', name="Your Skills", line=dict(color='#2ecc71', width=3, dash='dash')))
    for i, career in enumerate(careers_to_compare[:4]):
        if career in CAREER_DATA:
            values = [CAREER_DATA[career]["skills"].get(skill, 0) for skill in skills]
            values.append(values[0])
            skills_closed = skills + [skills[0]]
            color = colors[i % len(colors)]
            fig.add_trace(go.Scatterpolar(r=values, theta=skills_closed, fill='toself', fillcolor=hex_to_rgba(color, 0.2), name=career, line=dict(color=color, width=2)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='white')), angularaxis=dict(tickfont=dict(color='white', size=9)), bgcolor='rgba(0,0,0,0)'), showlegend=True, legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.5)'), title=dict(text=title, font=dict(color='white', size=16)), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
    return fig

# =============================================================================
# MAIN APPLICATION
# =============================================================================
if not st.session_state.onboarding_complete:
    st.markdown('<h1 class="main-header">🎯 CareerCraft AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888;">Skills + Career Intelligence Platform</p>', unsafe_allow_html=True)
    
    steps = ["Welcome", "Situation", "Goals", "Skills", "Values"]
    current_step = st.session_state.onboarding_step
    progress_pct = (current_step / (len(steps) - 1)) * 100 if current_step > 0 else 0
    st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {progress_pct}%"></div></div>', unsafe_allow_html=True)
    
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i < current_step:
                st.markdown(f'<div class="step step-complete">✓ {step}</div>', unsafe_allow_html=True)
            elif i == current_step:
                st.markdown(f'<div class="step step-active">● {step}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step step-pending">○ {step}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.onboarding_step == 0:
        st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
        st.markdown("### 👋 Welcome to CareerCraft AI")
        st.markdown("Get personalized career insights powered by **real labor market data**")
        st.markdown('</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**📊 {len(CAREER_DATA)} Careers**")
            st.markdown("Across 8 industries")
        with col2:
            st.markdown(f"**💡 {len(SKILLS_DATA)} Skills**")
            st.markdown("20 Technical + 15 Core")
        with col3:
            st.markdown("**📈 Real Data**")
            st.markdown("O*NET + BLS Sources")
        if st.button("🚀 Let's Get Started!", type="primary", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()
    
    elif st.session_state.onboarding_step == 1:
        st.markdown("### 📍 Step 1: Where Are You Now?")
        current_role = st.text_input("What's your current role or situation?", placeholder="e.g., Marketing Coordinator, CS Student...")
        years_exp = st.slider("Years of Work Experience", 0, 30, 2)
        user_type = st.selectbox("Which best describes you?", ["University Student", "Recent Graduate", "Working Professional", "Career Changer", "Returning to Workforce"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.onboarding_step = 0
                st.rerun()
        with col2:
            if st.button("Next →", type="primary"):
                st.session_state.user_profile['current_role'] = current_role
                st.session_state.user_profile['years_exp'] = years_exp
                st.session_state.user_profile['user_type'] = user_type
                st.session_state.onboarding_step = 2
                st.rerun()
    
    elif st.session_state.onboarding_step == 2:
        st.markdown("### 🎯 Step 2: Where Do You Want To Go?")
        target_industries = st.multiselect("Which industries interest you?", list(CATEGORY_COLORS.keys()), default=["Technology"])
        available_careers = [career for career, data in CAREER_DATA.items() if data["category"] in target_industries]
        if available_careers:
            target_careers = st.multiselect("Which specific careers interest you? (Select up to 3)", available_careers, max_selections=3)
        else:
            target_careers = []
            st.info("Select at least one industry to see career options")
        timeline = st.selectbox("Your Timeline for Change", ["Within 6 months", "6-12 months", "1-2 years", "2-5 years", "Just exploring"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.onboarding_step = 1
                st.rerun()
        with col2:
            if st.button("Next →", type="primary"):
                st.session_state.user_profile['target_industries'] = target_industries
                st.session_state.user_profile['target_careers'] = target_careers
                st.session_state.target_careers = target_careers
                st.session_state.user_profile['timeline'] = timeline
                st.session_state.onboarding_step = 3
                st.rerun()
    
    elif st.session_state.onboarding_step == 3:
        st.markdown("### 💪 Step 3: Rate Your Current Skills")
        st.markdown("*Be honest AND tell us how often you practice - both matter!*")
        quick_mode = st.checkbox("⚡ Quick Mode (rate 12 key skills only)", value=st.session_state.quick_mode, help="Reduces assessment time significantly")
        st.session_state.quick_mode = quick_mode
        st.markdown("**Scale:** 0-25: Beginner | 26-50: Developing | 51-75: Proficient | 76-100: Expert")
        
        if quick_mode:
            st.info(f"⚡ Quick Mode: Rating {len(KEY_SKILLS)} key skills. Others default to 50.")
            skills_to_show = {k: v for k, v in SKILLS_DATA.items() if k in KEY_SKILLS}
        else:
            skills_to_show = SKILLS_DATA
        
        technical = {k: v for k, v in skills_to_show.items() if v.get('category') == 'Technical'}
        cognitive = {k: v for k, v in skills_to_show.items() if v.get('category') == 'Cognitive'}
        soft = {k: v for k, v in skills_to_show.items() if v.get('category') == 'Soft'}
        
        for cat_name, cat_skills in [("💻 Technical Skills", technical), ("🧠 Cognitive Skills", cognitive), ("🤝 Soft Skills", soft)]:
            if cat_skills:
                st.markdown(f'<div class="skill-category-header">{cat_name}</div>', unsafe_allow_html=True)
                for skill, info in cat_skills.items():
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.session_state.user_skills[skill] = st.slider(skill, 0, 100, st.session_state.user_skills.get(skill, 50), help=info["description"], key=f"skill_{skill}")
                    with col2:
                        freq_opts = ["Often (weekly+)", "Sometimes", "Rarely/Never"]
                        curr = st.session_state.practice_freq.get(skill, "Sometimes")
                        idx = freq_opts.index(curr) if curr in freq_opts else 1
                        st.session_state.practice_freq[skill] = st.selectbox("Practice", freq_opts, index=idx, key=f"freq_{skill}", label_visibility="collapsed")
                    base = st.session_state.user_skills[skill]
                    freq = st.session_state.practice_freq[skill]
                    weight = practice_weight(freq)
                    if weight != 1.0:
                        effective = calculate_effective_level(base, freq)
                        st.caption(f"Effective: {base} × {weight} = **{effective:.0f}** {'↑' if weight > 1 else '↓'}")
        
        if quick_mode:
            for skill in SKILLS_DATA:
                if skill not in KEY_SKILLS:
                    if skill not in st.session_state.user_skills:
                        st.session_state.user_skills[skill] = 50
                    if skill not in st.session_state.practice_freq:
                        st.session_state.practice_freq[skill] = "Sometimes"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.onboarding_step = 2
                st.rerun()
        with col2:
            if st.button("Next →", type="primary"):
                st.session_state.onboarding_step = 4
                st.rerun()
    
    elif st.session_state.onboarding_step == 4:
        st.markdown("### ⭐ Step 4: Your Values & Priorities")
        work_values = st.multiselect("What's most important to you in work? (Pick up to 3)", ["High Salary", "Work-Life Balance", "Making an Impact", "Job Security", "Creativity", "Leadership Opportunities", "Flexibility", "Continuous Learning", "Team Environment", "Independence"], max_selections=3)
        life_priority = st.text_input("Outside of work, what's most important to you?", placeholder="e.g., Family time, Travel, Health, Hobbies...")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.onboarding_step = 3
                st.rerun()
        with col2:
            if st.button("🎉 Complete Assessment", type="primary"):
                st.session_state.user_profile['work_values'] = work_values
                st.session_state.user_profile['life_priority'] = life_priority
                st.session_state.onboarding_complete = True
                st.rerun()

else:
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        st.markdown(f"**Role:** {st.session_state.user_profile.get('current_role', 'Not set')}")
        st.markdown(f"**Type:** {st.session_state.user_profile.get('user_type', 'Not set')}")
        if st.button("🔄 Restart Assessment"):
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 0
            st.rerun()
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        target_careers = st.session_state.target_careers
        if target_careers:
            practice_freq = st.session_state.get('practice_freq', {})
            readiness_scores = []
            for c in target_careers:
                if c in CAREER_DATA:
                    career_skills = CAREER_DATA[c]["skills"]
                    total_match = 0
                    for skill, required in career_skills.items():
                        user_level = st.session_state.user_skills.get(skill, 0)
                        freq = practice_freq.get(skill, "Sometimes")
                        effective_level = calculate_effective_level(user_level, freq)
                        match = min(effective_level / required, 1.0) if required > 0 else 1.0
                        total_match += match
                    readiness_scores.append((total_match / len(career_skills)) * 100)
            avg_readiness = np.mean(readiness_scores) if readiness_scores else 0
            band_name, band_label, band_color = get_readiness_band(avg_readiness)
            st.metric("Career Readiness", f"{avg_readiness:.0f}%")
            st.markdown(f"<span style='color: {band_color}; font-weight: bold;'>{band_name.upper()}</span>", unsafe_allow_html=True)
            st.caption(band_label)
            with st.expander("ℹ️ Methodology"):
                st.caption(f"Model v{MODEL_VERSIONS['payload_version']}")
                st.caption(f"Skills: {len(TECHNICAL_SKILLS)} Technical + {len(OTHER_SKILLS)} Other")
                st.caption(f"Careers: {len(CAREER_DATA)}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🎯 Skill Gaps", "📚 Courses", "🔍 Explorer", "💬 Consult"])
    
    with tab1:
        st.markdown("## 📊 Your Career Dashboard")
        target_careers = st.session_state.target_careers
        user_skills = st.session_state.user_skills
        if target_careers:
            st.markdown("### 🎯 Your Target Careers")
            cols = st.columns(len(target_careers))
            practice_freq = st.session_state.get('practice_freq', {})
            for i, career in enumerate(target_careers):
                if career in CAREER_DATA:
                    data = CAREER_DATA[career]
                    gaps = calculate_skill_gaps(user_skills, career)
                    total_match = 0
                    for skill, gap_info in gaps.items():
                        freq = practice_freq.get(skill, "Sometimes")
                        effective = calculate_effective_level(gap_info['user_level'], freq)
                        required = gap_info['required_level']
                        match = min(effective / required, 1.0) if required > 0 else 1.0
                        total_match += match
                    readiness = (total_match / len(gaps) * 100) if gaps else 0
                    band_name, band_label, band_color = get_readiness_band(readiness)
                    high_gaps = sum(1 for g in gaps.values() if g['priority'] == 'High')
                    with cols[i]:
                        cat_class = f"category-{data['category'].lower().replace(' ', '-')}"
                        st.markdown(f'<span class="{cat_class}">{data["category"]}</span>', unsafe_allow_html=True)
                        st.markdown(f"**{career}**")
                        st.metric("Readiness", f"{readiness:.0f}%")
                        st.markdown(f"<small style='color: {band_color};'>{band_name.title()}</small>", unsafe_allow_html=True)
                        st.metric("Salary", f"${data['median_salary']:,}")
                        st.caption(f"🔴 {high_gaps} high-priority gaps")
            st.markdown("---")
            st.markdown("### 📈 Skills Comparison")
            fig = create_skill_radar(target_careers, user_skills, "Your Skills vs Career Requirements")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select target careers in your assessment to see your dashboard.")
    
    with tab2:
        st.markdown("## 🎯 Skill Gaps & ROI Analysis")
        if target_careers:
            selected_career = st.selectbox("Select career to analyze:", target_careers)
            if selected_career:
                gaps = calculate_skill_gaps(user_skills, selected_career)
                sorted_gaps = sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True)
                st.markdown("### Priority Skills to Develop")
                for skill, gap_info in sorted_gaps:
                    if gap_info['gap'] > 0:
                        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[gap_info['priority']]
                        with st.expander(f"{priority_color} {skill} (Gap: {gap_info['gap']} points)"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Your Level:** {gap_info['user_level']}")
                                st.markdown(f"**Required:** {gap_info['required_level']}")
                            with col2:
                                if skill in SKILLS_DATA:
                                    premium = SKILLS_DATA[skill]['salary_premium']
                                    st.markdown(f"**Salary Premium:** +${premium:,}/yr")
                                    st.markdown(f"**Demand:** {SKILLS_DATA[skill]['demand_trend']}")
        else:
            st.info("Complete your assessment to see skill gap analysis.")
    
    with tab3:
        st.markdown("## 📚 Recommended Courses")
        if target_careers:
            career = st.selectbox("Courses for:", target_careers, key="course_career")
            gaps = calculate_skill_gaps(user_skills, career)
            sorted_gaps = sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True)[:5]
            for skill, gap_info in sorted_gaps:
                if skill in SKILLS_DATA and gap_info['gap'] > 10:
                    st.markdown(f"### {skill}")
                    courses = SKILLS_DATA[skill]['courses']
                    for course in courses:
                        cost = "Free" if course['cost'] == 0 else f"${course['cost']}"
                        st.markdown(f"- **{course['name']}** ({cost}, {course['duration']})")
        else:
            st.info("Complete your assessment to see course recommendations.")
    
    with tab4:
        st.markdown("## 🔍 Career Explorer")
        industries = st.multiselect("Filter by industry:", list(CATEGORY_COLORS.keys()), default=list(CATEGORY_COLORS.keys()))
        matches = get_career_matches(user_skills, industries)
        for match in matches[:10]:
            with st.expander(f"**{match['career']}** | {match['match_pct']:.0f}% Match | ${match['salary']:,}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match", f"{match['match_pct']:.0f}%")
                with col2:
                    st.metric("Salary", f"${match['salary']:,}")
                with col3:
                    st.metric("Growth", f"{match['growth']}%")
                st.markdown(f"**Education:** {match['education']}")
                st.markdown(f"**Timeline:** {match['time_to_entry']}")
    
    with tab5:
        st.markdown("## 💬 Career Consultation")
        st.info("Ask about: ROI analysis, course recommendations, career comparisons")
        user_input = st.text_input("Ask me anything about your career path:", placeholder="e.g., What skills have the best ROI?")
        if user_input:
            st.markdown("### Response")
            if "roi" in user_input.lower():
                st.markdown("**Top ROI Skills for your goals:**")
                for skill in ["Machine Learning & AI", "Cloud Computing", "Leadership"]:
                    if skill in SKILLS_DATA:
                        st.markdown(f"- **{skill}**: +${SKILLS_DATA[skill]['salary_premium']:,}/year potential")
            elif "course" in user_input.lower():
                st.markdown("**Check the Courses tab for personalized recommendations based on your skill gaps.**")
            else:
                st.markdown("I can help you with ROI analysis, course recommendations, and career comparisons. Try asking about specific skills or careers!")

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
CareerCraft AI v{MODEL_VERSIONS['payload_version']} | Data: O*NET 30.0 • BLS OEWS May 2023 | {len(CAREER_DATA)} Careers • {len(SKILLS_DATA)} Skills
<br><small>⚠️ Readiness bands are heuristic estimates. This is decision support, not career advice.</small>
</div>
""", unsafe_allow_html=True)
