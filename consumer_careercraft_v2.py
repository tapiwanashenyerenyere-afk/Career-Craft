"""
CareerCraft AI v2 - Fully Integrated Consumer Platform
=======================================================
New Features:
- Step-by-step onboarding wizard with progress indicator
- Clear platform instructions and available careers/skills display
- Skill ROI calculations with salary premiums
- Course recommendations based on skill gaps
- Connected tabs - assessment flows through entire platform
- LLM-powered career consultation

Run with: python -m streamlit run consumer_careercraft_v2.py
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

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
# COLOR PALETTE (Fixed - proper formats)
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
}

# =============================================================================
# COMPREHENSIVE CAREER + SKILL DATA WITH ROI
# =============================================================================
SKILLS_DATA = {
    "Programming": {
        "description": "Writing code, software development, scripting",
        "salary_premium": 15000,  # Average salary boost for high proficiency
        "demand_trend": "High Growth",
        "courses": [
            {"name": "Python for Everybody (Coursera)", "cost": 0, "duration": "8 weeks", "roi": 250},
            {"name": "CS50 (Harvard/edX)", "cost": 0, "duration": "12 weeks", "roi": 300},
            {"name": "Full Stack Bootcamp", "cost": 12000, "duration": "12 weeks", "roi": 180},
        ]
    },
    "Problem Solving": {
        "description": "Analytical thinking, troubleshooting, decision-making",
        "salary_premium": 12000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Design Thinking (IDEO)", "cost": 400, "duration": "4 weeks", "roi": 200},
            {"name": "Critical Thinking Specialization", "cost": 50, "duration": "6 weeks", "roi": 280},
        ]
    },
    "Critical Thinking": {
        "description": "Evaluating information, logical reasoning, analysis",
        "salary_premium": 10000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Think Again (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Logical and Critical Thinking", "cost": 50, "duration": "6 weeks", "roi": 300},
        ]
    },
    "Communication": {
        "description": "Written and verbal communication, presentations",
        "salary_premium": 8000,
        "demand_trend": "Stable High",
        "courses": [
            {"name": "Business Writing (LinkedIn Learning)", "cost": 30, "duration": "3 weeks", "roi": 400},
            {"name": "Public Speaking Mastery", "cost": 100, "duration": "4 weeks", "roi": 350},
        ]
    },
    "Teamwork": {
        "description": "Collaboration, conflict resolution, group dynamics",
        "salary_premium": 6000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Teamwork Skills (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 300},
            {"name": "Collaborative Leadership", "cost": 200, "duration": "6 weeks", "roi": 250},
        ]
    },
    "Time Management": {
        "description": "Prioritization, scheduling, productivity",
        "salary_premium": 5000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Getting Things Done (GTD)", "cost": 50, "duration": "2 weeks", "roi": 500},
            {"name": "Work Smarter, Not Harder", "cost": 0, "duration": "3 weeks", "roi": 400},
        ]
    },
    "Creativity": {
        "description": "Innovation, ideation, design thinking",
        "salary_premium": 9000,
        "demand_trend": "Growing",
        "courses": [
            {"name": "Creative Thinking (Coursera)", "cost": 0, "duration": "4 weeks", "roi": 350},
            {"name": "Design Sprint Masterclass", "cost": 300, "duration": "2 weeks", "roi": 280},
        ]
    },
    "Attention to Detail": {
        "description": "Accuracy, quality control, thoroughness",
        "salary_premium": 7000,
        "demand_trend": "Stable",
        "courses": [
            {"name": "Quality Assurance Fundamentals", "cost": 100, "duration": "4 weeks", "roi": 300},
            {"name": "Proofreading & Editing", "cost": 50, "duration": "2 weeks", "roi": 350},
        ]
    },
}

CAREER_DATA = {
    # TECHNOLOGY CAREERS
    "Software Developer": {
        "category": "Technology",
        "skills": {"Programming": 95, "Problem Solving": 90, "Critical Thinking": 85,
                   "Communication": 70, "Teamwork": 75, "Time Management": 80,
                   "Creativity": 75, "Attention to Detail": 90},
        "median_salary": 110000,
        "growth_rate": 25,
        "education": "Bachelor's Degree",
        "entry_paths": ["CS Degree", "Bootcamp", "Self-taught + Portfolio"],
        "time_to_entry": "6-24 months"
    },
    "Data Scientist": {
        "category": "Technology",
        "skills": {"Programming": 85, "Problem Solving": 95, "Critical Thinking": 95,
                   "Communication": 75, "Teamwork": 70, "Time Management": 75,
                   "Creativity": 80, "Attention to Detail": 90},
        "median_salary": 120000,
        "growth_rate": 35,
        "education": "Master's Degree",
        "entry_paths": ["Statistics/Math Degree", "Data Analytics Certificate", "PhD"],
        "time_to_entry": "12-36 months"
    },
    "UX Designer": {
        "category": "Technology",
        "skills": {"Programming": 50, "Problem Solving": 85, "Critical Thinking": 80,
                   "Communication": 90, "Teamwork": 85, "Time Management": 75,
                   "Creativity": 95, "Attention to Detail": 85},
        "median_salary": 95000,
        "growth_rate": 15,
        "education": "Bachelor's Degree",
        "entry_paths": ["Design Degree", "UX Bootcamp", "Graphic Design + Portfolio"],
        "time_to_entry": "6-18 months"
    },
    "Cybersecurity Analyst": {
        "category": "Technology",
        "skills": {"Programming": 75, "Problem Solving": 90, "Critical Thinking": 95,
                   "Communication": 70, "Teamwork": 75, "Time Management": 85,
                   "Creativity": 65, "Attention to Detail": 95},
        "median_salary": 105000,
        "growth_rate": 32,
        "education": "Bachelor's Degree + Certifications",
        "entry_paths": ["IT Degree", "Security Certifications (CompTIA, CISSP)", "IT Experience + Certs"],
        "time_to_entry": "12-24 months"
    },
    
    # HEALTHCARE CAREERS
    "Registered Nurse": {
        "category": "Healthcare",
        "skills": {"Programming": 15, "Problem Solving": 85, "Critical Thinking": 90,
                   "Communication": 95, "Teamwork": 95, "Time Management": 90,
                   "Creativity": 60, "Attention to Detail": 95},
        "median_salary": 77600,
        "growth_rate": 12,
        "education": "Bachelor's Degree (BSN)",
        "entry_paths": ["BSN Degree", "ADN + RN-to-BSN Bridge", "Accelerated BSN"],
        "time_to_entry": "24-48 months"
    },
    "Medical Assistant": {
        "category": "Healthcare",
        "skills": {"Programming": 10, "Problem Solving": 70, "Critical Thinking": 75,
                   "Communication": 90, "Teamwork": 90, "Time Management": 85,
                   "Creativity": 50, "Attention to Detail": 90},
        "median_salary": 38270,
        "growth_rate": 18,
        "education": "Certificate/Associate's",
        "entry_paths": ["MA Certificate", "Associate's Degree", "On-the-job Training"],
        "time_to_entry": "6-12 months"
    },
    "Physical Therapist": {
        "category": "Healthcare",
        "skills": {"Programming": 10, "Problem Solving": 90, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 80, "Time Management": 85,
                   "Creativity": 75, "Attention to Detail": 90},
        "median_salary": 95620,
        "growth_rate": 17,
        "education": "Doctoral Degree (DPT)",
        "entry_paths": ["Pre-PT Undergrad + DPT", "Athletic Training + DPT"],
        "time_to_entry": "72-84 months"
    },
    "Healthcare Administrator": {
        "category": "Healthcare",
        "skills": {"Programming": 30, "Problem Solving": 85, "Critical Thinking": 90,
                   "Communication": 95, "Teamwork": 90, "Time Management": 95,
                   "Creativity": 70, "Attention to Detail": 85},
        "median_salary": 104280,
        "growth_rate": 28,
        "education": "Master's Degree (MHA/MBA)",
        "entry_paths": ["Healthcare Experience + MBA", "MHA Degree", "Clinical + Management"],
        "time_to_entry": "24-48 months"
    },
    
    # BUSINESS CAREERS
    "Project Manager": {
        "category": "Business",
        "skills": {"Programming": 40, "Problem Solving": 90, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 95, "Time Management": 95,
                   "Creativity": 75, "Attention to Detail": 85},
        "median_salary": 94500,
        "growth_rate": 7,
        "education": "Bachelor's Degree + PMP",
        "entry_paths": ["Any Degree + PMP Cert", "Experience + Agile Certs", "MBA"],
        "time_to_entry": "12-36 months"
    },
    "Marketing Manager": {
        "category": "Business",
        "skills": {"Programming": 35, "Problem Solving": 80, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 85, "Time Management": 85,
                   "Creativity": 95, "Attention to Detail": 80},
        "median_salary": 135030,
        "growth_rate": 10,
        "education": "Bachelor's Degree",
        "entry_paths": ["Marketing Degree", "Business Degree + Marketing Experience", "Digital Marketing Certs"],
        "time_to_entry": "24-48 months"
    },
    "Financial Analyst": {
        "category": "Business",
        "skills": {"Programming": 60, "Problem Solving": 90, "Critical Thinking": 95,
                   "Communication": 80, "Teamwork": 75, "Time Management": 85,
                   "Creativity": 60, "Attention to Detail": 95},
        "median_salary": 95570,
        "growth_rate": 9,
        "education": "Bachelor's Degree",
        "entry_paths": ["Finance Degree", "Accounting + CFA", "Economics + Financial Modeling"],
        "time_to_entry": "12-24 months"
    },
    "Human Resources Manager": {
        "category": "Business",
        "skills": {"Programming": 25, "Problem Solving": 85, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 95, "Time Management": 90,
                   "Creativity": 70, "Attention to Detail": 85},
        "median_salary": 126230,
        "growth_rate": 7,
        "education": "Bachelor's Degree",
        "entry_paths": ["HR Degree", "Business + SHRM Cert", "Psychology + HR Experience"],
        "time_to_entry": "24-48 months"
    },
    
    # EDUCATION CAREERS
    "High School Teacher": {
        "category": "Education",
        "skills": {"Programming": 25, "Problem Solving": 80, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 80, "Time Management": 90,
                   "Creativity": 85, "Attention to Detail": 80},
        "median_salary": 62360,
        "growth_rate": 5,
        "education": "Bachelor's Degree + Certification",
        "entry_paths": ["Education Degree + License", "Subject Degree + Teaching Cert", "Alternative Certification"],
        "time_to_entry": "12-48 months"
    },
    "Instructional Designer": {
        "category": "Education",
        "skills": {"Programming": 50, "Problem Solving": 85, "Critical Thinking": 85,
                   "Communication": 90, "Teamwork": 80, "Time Management": 85,
                   "Creativity": 95, "Attention to Detail": 85},
        "median_salary": 74620,
        "growth_rate": 11,
        "education": "Master's Degree",
        "entry_paths": ["ID Master's", "Teaching Experience + ID Cert", "Ed Tech Degree"],
        "time_to_entry": "12-24 months"
    },
    "School Counselor": {
        "category": "Education",
        "skills": {"Programming": 15, "Problem Solving": 90, "Critical Thinking": 90,
                   "Communication": 95, "Teamwork": 85, "Time Management": 85,
                   "Creativity": 75, "Attention to Detail": 80},
        "median_salary": 60140,
        "growth_rate": 10,
        "education": "Master's Degree",
        "entry_paths": ["Counseling Master's + License", "Psychology + School Counseling Cert"],
        "time_to_entry": "24-36 months"
    },
    "University Professor": {
        "category": "Education",
        "skills": {"Programming": 45, "Problem Solving": 90, "Critical Thinking": 95,
                   "Communication": 90, "Teamwork": 70, "Time Management": 80,
                   "Creativity": 85, "Attention to Detail": 90},
        "median_salary": 80560,
        "growth_rate": 8,
        "education": "Doctoral Degree",
        "entry_paths": ["PhD + Postdoc", "Terminal Master's (some fields)", "Industry + PhD"],
        "time_to_entry": "60-96 months"
    },
    
    # COMMUNITY CAREERS
    "Social Worker": {
        "category": "Community",
        "skills": {"Programming": 15, "Problem Solving": 90, "Critical Thinking": 90,
                   "Communication": 95, "Teamwork": 90, "Time Management": 85,
                   "Creativity": 75, "Attention to Detail": 85},
        "median_salary": 55350,
        "growth_rate": 9,
        "education": "Bachelor's/Master's Degree",
        "entry_paths": ["BSW", "MSW", "Related Degree + MSW"],
        "time_to_entry": "24-48 months"
    },
    "Community Health Worker": {
        "category": "Community",
        "skills": {"Programming": 10, "Problem Solving": 80, "Critical Thinking": 80,
                   "Communication": 95, "Teamwork": 95, "Time Management": 85,
                   "Creativity": 70, "Attention to Detail": 80},
        "median_salary": 46590,
        "growth_rate": 14,
        "education": "High School/Certificate",
        "entry_paths": ["CHW Certificate", "Public Health Training", "Community Experience"],
        "time_to_entry": "3-12 months"
    },
    "Nonprofit Program Manager": {
        "category": "Community",
        "skills": {"Programming": 30, "Problem Solving": 90, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 95, "Time Management": 90,
                   "Creativity": 85, "Attention to Detail": 85},
        "median_salary": 65000,
        "growth_rate": 12,
        "education": "Bachelor's Degree",
        "entry_paths": ["Nonprofit Experience", "MPA/MPP", "Business + Nonprofit Cert"],
        "time_to_entry": "12-36 months"
    },
    "Community Organizer": {
        "category": "Community",
        "skills": {"Programming": 20, "Problem Solving": 85, "Critical Thinking": 85,
                   "Communication": 95, "Teamwork": 95, "Time Management": 80,
                   "Creativity": 90, "Attention to Detail": 75},
        "median_salary": 48000,
        "growth_rate": 10,
        "education": "Bachelor's Degree",
        "entry_paths": ["Political Science/Sociology Degree", "Grassroots Experience", "Nonprofit Path"],
        "time_to_entry": "6-24 months"
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

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
    }
    
    /* Progress bar */
    .progress-container {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 5px;
        margin: 1rem 0;
    }
    .progress-bar {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        border-radius: 8px;
        height: 10px;
        transition: width 0.3s ease;
    }
    
    /* Step indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
    .step {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        margin: 0 5px;
    }
    .step-active { background: #2E86AB; color: white; }
    .step-complete { background: #2ecc71; color: white; }
    .step-pending { background: #333; color: #888; }
    
    /* Cards */
    .info-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #2E86AB;
        margin: 0.5rem 0;
    }
    
    /* ROI highlight */
    .roi-positive { color: #2ecc71; font-weight: bold; }
    .roi-neutral { color: #f39c12; }
    
    /* Category badges */
    .category-tech { background: #3498db; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-healthcare { background: #e74c3c; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-business { background: #2ecc71; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-education { background: #9b59b6; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    .category-community { background: #f39c12; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem; }
    
    /* Welcome box */
    .welcome-box {
        background: linear-gradient(135deg, #1e3a5f, #2E86AB);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Skill gap indicator */
    .skill-gap-high { color: #e74c3c; }
    .skill-gap-medium { color: #f39c12; }
    .skill-gap-low { color: #2ecc71; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_skill_gaps(user_skills, target_career):
    """Calculate skill gaps between user and target career"""
    if target_career not in CAREER_DATA:
        return {}
    
    career_skills = CAREER_DATA[target_career]["skills"]
    gaps = {}
    
    for skill, required_level in career_skills.items():
        user_level = user_skills.get(skill, 0)
        gap = required_level - user_level
        gaps[skill] = {
            "user_level": user_level,
            "required_level": required_level,
            "gap": max(0, gap),
            "priority": "High" if gap > 30 else "Medium" if gap > 15 else "Low"
        }
    
    return gaps

def calculate_skill_roi(skill_name, current_level, target_level):
    """Calculate ROI for improving a specific skill"""
    if skill_name not in SKILLS_DATA:
        return None
    
    skill_info = SKILLS_DATA[skill_name]
    improvement = target_level - current_level
    
    # Calculate potential salary increase (proportional to improvement)
    salary_increase = (improvement / 100) * skill_info["salary_premium"]
    
    return {
        "skill": skill_name,
        "current_level": current_level,
        "target_level": target_level,
        "improvement_needed": improvement,
        "potential_salary_increase": salary_increase,
        "demand_trend": skill_info["demand_trend"],
        "courses": skill_info["courses"]
    }

def get_career_matches(user_skills, target_industries):
    """Get careers that match user skills and target industries"""
    matches = []
    
    for career, data in CAREER_DATA.items():
        if data["category"] in target_industries:
            # Calculate match score
            total_match = 0
            total_weight = 0
            
            for skill, required in data["skills"].items():
                user_level = user_skills.get(skill, 0)
                weight = required / 100
                match = min(user_level / required, 1.0) if required > 0 else 1.0
                total_match += match * weight
                total_weight += weight
            
            match_pct = (total_match / total_weight * 100) if total_weight > 0 else 0
            
            # Calculate skill gap count
            gaps = calculate_skill_gaps(user_skills, career)
            high_gaps = sum(1 for g in gaps.values() if g["priority"] == "High")
            
            matches.append({
                "career": career,
                "category": data["category"],
                "match_pct": match_pct,
                "salary": data["median_salary"],
                "growth": data["growth_rate"],
                "high_skill_gaps": high_gaps,
                "education": data["education"],
                "time_to_entry": data["time_to_entry"]
            })
    
    matches.sort(key=lambda x: x["match_pct"], reverse=True)
    return matches

def create_skill_radar(careers_to_compare, user_skills=None, title="Skill Comparison"):
    """Create radar chart with optional user skills overlay"""
    fig = go.Figure()
    
    skills = list(SKILLS_DATA.keys())
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#2ecc71']
    
    # Add user skills if provided
    if user_skills:
        values = [user_skills.get(skill, 0) for skill in skills]
        values.append(values[0])
        skills_closed = skills + [skills[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=skills_closed,
            fill='toself',
            fillcolor='rgba(46, 204, 113, 0.2)',
            name="Your Skills",
            line=dict(color='#2ecc71', width=3, dash='dash')
        ))
    
    # Add career skills
    for i, career in enumerate(careers_to_compare[:4]):
        if career in CAREER_DATA:
            values = [CAREER_DATA[career]["skills"].get(skill, 0) for skill in skills]
            values.append(values[0])
            skills_closed = skills + [skills[0]]
            
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=skills_closed,
                fill='toself',
                fillcolor=hex_to_rgba(color, 0.2),
                name=career,
                line=dict(color=color, width=2)
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='white')),
            angularaxis=dict(tickfont=dict(color='white', size=10)),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.5)'),
        title=dict(text=title, font=dict(color='white', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig

def generate_consultation_response(user_message, user_profile, skill_gaps):
    """Generate intelligent career consultation response"""
    message_lower = user_message.lower()
    
    # Get user context
    target_careers = user_profile.get('target_careers', [])
    current_role = user_profile.get('current_role', 'Not specified')
    
    if "roi" in message_lower or "worth" in message_lower or "invest" in message_lower:
        # ROI-focused response
        response = """## 📊 Skill Investment ROI Analysis

Based on your profile, here are the skills with the **highest ROI** for your goals:

"""
        if skill_gaps:
            sorted_gaps = sorted(skill_gaps.items(), key=lambda x: x[1]['gap'], reverse=True)[:3]
            for skill, gap_info in sorted_gaps:
                if skill in SKILLS_DATA:
                    premium = SKILLS_DATA[skill]['salary_premium']
                    response += f"""**{skill}** (Gap: {gap_info['gap']} points)
- 💰 Salary Premium: +${premium:,}/year at high proficiency
- 📈 Demand: {SKILLS_DATA[skill]['demand_trend']}
- ⏱️ Top Course: {SKILLS_DATA[skill]['courses'][0]['name']}

"""
        
        response += """
**ROI Formula Used:**
`Skill ROI = (Salary Premium × Improvement %) / Course Cost`

The skills listed above offer the best return based on your current gaps and market demand."""
        return response
    
    elif "course" in message_lower or "learn" in message_lower or "train" in message_lower:
        response = """## 📚 Recommended Learning Path

Based on your skill gaps, here's your **prioritized learning plan**:

"""
        if skill_gaps:
            high_priority = [(s, g) for s, g in skill_gaps.items() if g['priority'] == 'High'][:2]
            for skill, gap_info in high_priority:
                if skill in SKILLS_DATA:
                    courses = SKILLS_DATA[skill]['courses']
                    response += f"""### {skill} (Priority: High)
"""
                    for course in courses[:2]:
                        cost_str = "Free" if course['cost'] == 0 else f"${course['cost']}"
                        response += f"- **{course['name']}** | {cost_str} | {course['duration']} | ROI: {course['roi']}%\n"
                    response += "\n"
        
        response += """
**Pro Tip:** Start with free courses to validate interest before investing in paid programs."""
        return response
    
    elif "gap" in message_lower or "improve" in message_lower or "weak" in message_lower:
        response = """## 🎯 Your Skill Gap Analysis

"""
        if skill_gaps:
            for skill, gap_info in sorted(skill_gaps.items(), key=lambda x: x[1]['gap'], reverse=True):
                if gap_info['gap'] > 0:
                    priority_emoji = "🔴" if gap_info['priority'] == 'High' else "🟡" if gap_info['priority'] == 'Medium' else "🟢"
                    response += f"""{priority_emoji} **{skill}**: You're at {gap_info['user_level']}%, need {gap_info['required_level']}% (Gap: {gap_info['gap']} points)
"""
        
        response += """
**Action Plan:**
1. Focus on 🔴 High priority gaps first
2. Aim for 10-15 point improvements per quarter
3. Use the Courses tab for specific recommendations"""
        return response
    
    elif "salary" in message_lower or "money" in message_lower or "earn" in message_lower:
        response = """## 💰 Salary & Earnings Analysis

"""
        if target_careers:
            for career in target_careers[:3]:
                if career in CAREER_DATA:
                    data = CAREER_DATA[career]
                    response += f"""**{career}**
- Median Salary: ${data['median_salary']:,}
- Growth Rate: {data['growth_rate']}%
- Education: {data['education']}

"""
        
        response += """**Salary Boosters:**
- Each high-demand skill at expert level adds $5K-$15K
- Leadership roles add 20-40% to base
- Certifications can add 10-20% premium"""
        return response
    
    else:
        # General helpful response
        return f"""## 🤖 Career Consultation

I'm here to help you navigate your career journey! Based on your profile:

**Current Role:** {current_role}
**Target Careers:** {', '.join(target_careers[:3]) if target_careers else 'Not yet selected'}

**Quick Actions:**
1. 📊 Ask about "skill ROI" to see which skills offer the best return
2. 📚 Ask about "courses" for personalized learning recommendations  
3. 🎯 Ask about "skill gaps" for detailed improvement areas
4. 💰 Ask about "salary" for earnings analysis

**Example Questions:**
- "What skills should I focus on for the best ROI?"
- "What courses do you recommend for my gaps?"
- "How can I increase my salary potential?"

What would you like to explore?"""

# =============================================================================
# MAIN APPLICATION
# =============================================================================

# Header
st.markdown('<h1 class="main-header">🎯 CareerCraft AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Your Skills Shape Your Career Path</p>', unsafe_allow_html=True)

# =============================================================================
# ONBOARDING WIZARD (if not complete)
# =============================================================================
if not st.session_state.onboarding_complete:
    
    # Progress indicator
    progress = st.session_state.onboarding_step / 4
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress * 100}%;"></div>
    </div>
    <p style="text-align: center; color: #888;">Step {st.session_state.onboarding_step + 1} of 5</p>
    """, unsafe_allow_html=True)
    
    # STEP 0: Welcome & Instructions
    if st.session_state.onboarding_step == 0:
        st.markdown("""
        <div class="welcome-box">
            <h2>👋 Welcome to CareerCraft AI!</h2>
            <p style="font-size: 1.2rem;">Your personal career intelligence platform powered by PhD-level algorithms</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 How This Platform Works")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **What You'll Get:**
            - ✅ Personalized skill gap analysis
            - ✅ Career match recommendations
            - ✅ Skill ROI calculations
            - ✅ Course recommendations
            - ✅ AI career consultation
            """)
        
        with col2:
            st.markdown("""
            **What We Need From You:**
            - 📍 Your current situation
            - 🎯 Your career goals
            - 💪 Your current skill levels
            - 🏢 Industries you're interested in
            """)
        
        st.markdown("---")
        st.markdown("### 🗂️ Available in This MVP")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            **{len(CAREER_DATA)} Careers Analyzed:**
            - 🖥️ Technology (4)
            - 🏥 Healthcare (4)
            - 💼 Business (4)
            - 📚 Education (4)
            - 🤝 Community (4)
            """)
        
        with col2:
            st.markdown(f"""
            **{len(SKILLS_DATA)} Core Skills Tracked:**
            - Programming
            - Problem Solving
            - Critical Thinking
            - Communication
            - Teamwork
            - Time Management
            - Creativity
            - Attention to Detail
            """)
        
        with col3:
            st.markdown("""
            **Analysis Includes:**
            - Skill-to-salary correlations
            - Growth rate projections
            - Course ROI calculations
            - Entry path options
            """)
        
        if st.button("🚀 Let's Get Started!", type="primary", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()
    
    # STEP 1: Current Situation
    elif st.session_state.onboarding_step == 1:
        st.markdown("### 📍 Step 1: Where Are You Now?")
        
        current_role = st.text_input(
            "What's your current role or situation?",
            placeholder="e.g., Marketing Coordinator, CS Student, Looking for first job..."
        )
        
        years_exp = st.slider("Years of Work Experience", 0, 30, 2)
        
        user_type = st.selectbox(
            "Which best describes you?",
            ["University Student", "Recent Graduate", "Working Professional", "Career Changer", "Returning to Workforce"]
        )
        
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
    
    # STEP 2: Target Industries & Careers
    elif st.session_state.onboarding_step == 2:
        st.markdown("### 🎯 Step 2: Where Do You Want To Go?")
        
        target_industries = st.multiselect(
            "Which industries interest you?",
            ["Technology", "Healthcare", "Business", "Education", "Community"],
            default=["Technology"]
        )
        
        # Show careers from selected industries
        available_careers = []
        for ind in target_industries:
            for career, data in CAREER_DATA.items():
                if data["category"] == ind:
                    available_careers.append(career)
        
        if available_careers:
            target_careers = st.multiselect(
                "Which specific careers interest you? (Select up to 3)",
                available_careers,
                max_selections=3
            )
        else:
            target_careers = []
            st.info("Select at least one industry to see career options")
        
        timeline = st.selectbox(
            "Your Timeline for Change",
            ["Within 6 months", "6-12 months", "1-2 years", "2-5 years", "Just exploring"]
        )
        
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
    
    # STEP 3: Skill Assessment
    elif st.session_state.onboarding_step == 3:
        st.markdown("### 💪 Step 3: Rate Your Current Skills")
        st.markdown("*Be honest - this helps us give you accurate recommendations*")
        
        st.markdown("""
        **Scale Guide:**
        - 0-25: Beginner (little to no experience)
        - 26-50: Developing (some experience, still learning)
        - 51-75: Proficient (comfortable and competent)
        - 76-100: Expert (highly skilled, could teach others)
        """)
        
        skill_cols = st.columns(2)
        for i, (skill, info) in enumerate(SKILLS_DATA.items()):
            with skill_cols[i % 2]:
                st.session_state.user_skills[skill] = st.slider(
                    f"{skill}",
                    0, 100, 
                    st.session_state.user_skills.get(skill, 50),
                    help=info["description"],
                    key=f"onboard_skill_{skill}"
                )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.onboarding_step = 2
                st.rerun()
        with col2:
            if st.button("Next →", type="primary"):
                st.session_state.onboarding_step = 4
                st.rerun()
    
    # STEP 4: Values & Priorities
    elif st.session_state.onboarding_step == 4:
        st.markdown("### ⭐ Step 4: Your Values & Priorities")
        
        work_values = st.multiselect(
            "What's most important to you in work? (Pick up to 3)",
            ["High Salary", "Work-Life Balance", "Making an Impact", "Job Security", 
             "Creativity", "Leadership Opportunities", "Flexibility", "Continuous Learning",
             "Team Environment", "Independence"],
            max_selections=3
        )
        
        life_priority = st.text_input(
            "Outside of work, what's most important to you?",
            placeholder="e.g., Family time, Travel, Health, Hobbies..."
        )
        
        st.markdown("---")
        
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

# =============================================================================
# MAIN DASHBOARD (after onboarding)
# =============================================================================
else:
    # Sidebar with profile summary
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        st.markdown(f"**Role:** {st.session_state.user_profile.get('current_role', 'Not set')}")
        st.markdown(f"**Experience:** {st.session_state.user_profile.get('years_exp', 0)} years")
        st.markdown(f"**Target Industries:** {', '.join(st.session_state.user_profile.get('target_industries', []))}")
        
        st.markdown("---")
        
        if st.button("🔄 Retake Assessment"):
            st.session_state.onboarding_complete = False
            st.session_state.onboarding_step = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        # Calculate overall readiness
        target_careers = st.session_state.target_careers
        if target_careers:
            avg_match = np.mean([
                sum(min(st.session_state.user_skills.get(s, 0) / r, 1) 
                    for s, r in CAREER_DATA[c]["skills"].items()) / len(CAREER_DATA[c]["skills"]) * 100
                for c in target_careers if c in CAREER_DATA
            ])
            st.metric("Career Readiness", f"{avg_match:.0f}%")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 My Dashboard",
        "🎯 Skill Gaps & ROI",
        "📚 Course Recommendations",
        "🔍 Career Explorer",
        "💬 AI Consultation"
    ])
    
    # TAB 1: DASHBOARD
    with tab1:
        st.markdown("## 📊 Your Personalized Dashboard")
        
        target_careers = st.session_state.target_careers
        user_skills = st.session_state.user_skills
        
        if target_careers:
            # Top career matches
            st.markdown("### 🎯 Your Target Careers")
            
            cols = st.columns(len(target_careers))
            for i, career in enumerate(target_careers):
                if career in CAREER_DATA:
                    data = CAREER_DATA[career]
                    gaps = calculate_skill_gaps(user_skills, career)
                    match_pct = 100 - (sum(g['gap'] for g in gaps.values()) / len(gaps) / 100 * 100)
                    high_gaps = sum(1 for g in gaps.values() if g['priority'] == 'High')
                    
                    with cols[i]:
                        cat_class = f"category-{data['category'].lower()}"
                        st.markdown(f'<span class="{cat_class}">{data["category"]}</span>', unsafe_allow_html=True)
                        st.markdown(f"**{career}**")
                        st.metric("Match", f"{match_pct:.0f}%")
                        st.metric("Salary", f"${data['median_salary']:,}")
                        st.caption(f"🔴 {high_gaps} high-priority skill gaps")
            
            st.markdown("---")
            
            # Skill comparison radar
            st.markdown("### 📈 Your Skills vs Target Careers")
            fig = create_skill_radar(target_careers, user_skills, "Skills Comparison")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🟢 Dashed line = Your current skills | Solid lines = Career requirements")
            
        else:
            st.info("👆 Go back to the assessment to select target careers and see your personalized dashboard.")
    
    # TAB 2: SKILL GAPS & ROI
    with tab2:
        st.markdown("## 🎯 Skill Gap Analysis & ROI")
        
        target_careers = st.session_state.target_careers
        user_skills = st.session_state.user_skills
        
        if target_careers:
            selected_career = st.selectbox("Analyze gaps for:", target_careers)
            
            if selected_career and selected_career in CAREER_DATA:
                gaps = calculate_skill_gaps(user_skills, selected_career)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### Skill Gaps for {selected_career}")
                    
                    # Create gap visualization
                    gap_data = []
                    for skill, info in sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True):
                        gap_data.append({
                            "Skill": skill,
                            "Your Level": info['user_level'],
                            "Required": info['required_level'],
                            "Gap": info['gap'],
                            "Priority": info['priority']
                        })
                    
                    df = pd.DataFrame(gap_data)
                    
                    # Horizontal bar chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        y=df['Skill'],
                        x=df['Your Level'],
                        name='Your Level',
                        orientation='h',
                        marker_color='#2ecc71'
                    ))
                    
                    fig.add_trace(go.Bar(
                        y=df['Skill'],
                        x=df['Required'],
                        name='Required',
                        orientation='h',
                        marker_color='#3498db',
                        opacity=0.5
                    ))
                    
                    fig.update_layout(
                        barmode='overlay',
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        legend=dict(orientation='h', yanchor='bottom', y=1.02)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### 💰 Skill ROI")
                    
                    for skill, info in sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True)[:5]:
                        if info['gap'] > 0 and skill in SKILLS_DATA:
                            roi_info = calculate_skill_roi(skill, info['user_level'], info['required_level'])
                            
                            priority_color = "#e74c3c" if info['priority'] == 'High' else "#f39c12" if info['priority'] == 'Medium' else "#2ecc71"
                            
                            st.markdown(f"""
                            **{skill}**  
                            Gap: {info['gap']} pts | Priority: <span style="color:{priority_color}">{info['priority']}</span>  
                            💰 Potential: +${roi_info['potential_salary_increase']:,.0f}/yr
                            """, unsafe_allow_html=True)
                            st.markdown("---")
        else:
            st.info("Select target careers in the assessment to see your skill gaps.")
    
    # TAB 3: COURSE RECOMMENDATIONS
    with tab3:
        st.markdown("## 📚 Personalized Course Recommendations")
        
        target_careers = st.session_state.target_careers
        user_skills = st.session_state.user_skills
        
        if target_careers:
            # Get all high-priority gaps
            all_gaps = {}
            for career in target_careers:
                if career in CAREER_DATA:
                    gaps = calculate_skill_gaps(user_skills, career)
                    for skill, info in gaps.items():
                        if skill not in all_gaps or info['gap'] > all_gaps[skill]['gap']:
                            all_gaps[skill] = info
            
            # Sort by priority and gap size
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            sorted_gaps = sorted(all_gaps.items(), 
                                key=lambda x: (priority_order[x[1]['priority']], -x[1]['gap']))
            
            st.markdown("### 🎯 Priority Skills to Develop")
            
            for skill, gap_info in sorted_gaps:
                if gap_info['gap'] > 0 and skill in SKILLS_DATA:
                    skill_info = SKILLS_DATA[skill]
                    
                    with st.expander(f"**{skill}** - Gap: {gap_info['gap']} pts | Priority: {gap_info['priority']}", expanded=(gap_info['priority']=='High')):
                        st.markdown(f"**Description:** {skill_info['description']}")
                        st.markdown(f"**Demand Trend:** {skill_info['demand_trend']}")
                        st.markdown(f"**Salary Premium at Mastery:** +${skill_info['salary_premium']:,}/year")
                        
                        st.markdown("#### Recommended Courses:")
                        for course in skill_info['courses']:
                            cost_str = "🆓 Free" if course['cost'] == 0 else f"💵 ${course['cost']}"
                            st.markdown(f"""
                            - **{course['name']}**  
                              {cost_str} | ⏱️ {course['duration']} | 📈 ROI: {course['roi']}%
                            """)
        else:
            st.info("Select target careers to get personalized course recommendations.")
    
    # TAB 4: CAREER EXPLORER
    with tab4:
        st.markdown("## 🔍 Career Explorer")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_categories = st.multiselect(
                "Filter by Industry",
                ["Technology", "Healthcare", "Business", "Education", "Community"],
                default=st.session_state.user_profile.get('target_industries', ["Technology"])
            )
        with col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Match %", "Salary (High to Low)", "Growth Rate", "Time to Entry"]
            )
        
        # Get and display matches
        matches = get_career_matches(st.session_state.user_skills, filter_categories)
        
        if sort_by == "Salary (High to Low)":
            matches.sort(key=lambda x: x['salary'], reverse=True)
        elif sort_by == "Growth Rate":
            matches.sort(key=lambda x: x['growth'], reverse=True)
        elif sort_by == "Time to Entry":
            matches.sort(key=lambda x: x['time_to_entry'])
        
        st.markdown(f"### Showing {len(matches)} Careers")
        
        for match in matches:
            with st.expander(f"**{match['career']}** | Match: {match['match_pct']:.0f}% | ${match['salary']:,}"):
                data = CAREER_DATA[match['career']]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Median Salary", f"${match['salary']:,}")
                    st.metric("Growth Rate", f"{match['growth']}%")
                with col2:
                    st.metric("Match Score", f"{match['match_pct']:.0f}%")
                    st.metric("Skill Gaps", f"{match['high_skill_gaps']} high priority")
                with col3:
                    st.write(f"**Education:** {match['education']}")
                    st.write(f"**Time to Entry:** {data['time_to_entry']}")
                
                st.markdown("**Entry Paths:**")
                for path in data['entry_paths']:
                    st.markdown(f"- {path}")
    
    # TAB 5: AI CONSULTATION
    with tab5:
        st.markdown("## 💬 AI Career Consultation")
        st.markdown("*Ask questions about your career path, skills, and opportunities*")
        
        # Get skill gaps for context
        skill_gaps = {}
        if st.session_state.target_careers:
            for career in st.session_state.target_careers:
                if career in CAREER_DATA:
                    gaps = calculate_skill_gaps(st.session_state.user_skills, career)
                    for skill, info in gaps.items():
                        if skill not in skill_gaps or info['gap'] > skill_gaps[skill]['gap']:
                            skill_gaps[skill] = info
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(msg['content'])
            st.markdown("---")
        
        # Chat input
        user_input = st.text_input("Ask a question:", placeholder="e.g., What skills give me the best ROI?")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Send", type="primary"):
                if user_input:
                    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                    response = generate_consultation_response(user_input, st.session_state.user_profile, skill_gaps)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
        with col2:
            if st.button("Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Quick questions
        st.markdown("### Quick Questions")
        quick_cols = st.columns(4)
        quick_questions = [
            "What's my best skill ROI?",
            "What courses should I take?",
            "Show my skill gaps",
            "Salary potential?"
        ]
        
        for i, q in enumerate(quick_questions):
            with quick_cols[i]:
                if st.button(q, key=f"quick_{i}"):
                    st.session_state.chat_history.append({'role': 'user', 'content': q})
                    response = generate_consultation_response(q, st.session_state.user_profile, skill_gaps)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
<strong>CareerCraft AI v2.0</strong> | PhD-Level Career Intelligence<br>
Algorithms: Causal Inference • Conformal Prediction • GraphSAGE • Conservative Q-Learning<br>
Data: O*NET 30.0 • BLS OEWS • Census PSEO | 20 Careers • 8 Skills • Full ROI Analysis
</div>
""", unsafe_allow_html=True)
