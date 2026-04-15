"""
Recruitment AI MCP Server
Hiring automation tools powered by MEOK AI Labs.
"""


import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import time
import re
import hashlib
from datetime import date
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("recruitment-ai", instructions="MEOK AI Labs MCP Server")

_call_counts: dict[str, list[float]] = defaultdict(list)
FREE_TIER_LIMIT = 30
WINDOW = 86400


def _check_rate_limit(tool_name: str) -> None:
    now = time.time()
    _call_counts[tool_name] = [t for t in _call_counts[tool_name] if now - t < WINDOW]
    if len(_call_counts[tool_name]) >= FREE_TIER_LIMIT:
        raise ValueError(f"Rate limit exceeded for {tool_name}. Free tier: {FREE_TIER_LIMIT}/day.")
    _call_counts[tool_name].append(now)


SALARY_BENCHMARKS = {
    "software_engineer": {"junior": (35000, 55000), "mid": (55000, 80000), "senior": (80000, 120000), "lead": (110000, 150000)},
    "data_scientist": {"junior": (38000, 55000), "mid": (55000, 85000), "senior": (85000, 125000), "lead": (115000, 155000)},
    "product_manager": {"junior": (35000, 50000), "mid": (50000, 75000), "senior": (75000, 110000), "lead": (100000, 140000)},
    "designer": {"junior": (28000, 42000), "mid": (42000, 65000), "senior": (65000, 95000), "lead": (85000, 120000)},
    "marketing": {"junior": (25000, 38000), "mid": (38000, 55000), "senior": (55000, 80000), "lead": (75000, 110000)},
    "sales": {"junior": (22000, 35000), "mid": (35000, 55000), "senior": (55000, 85000), "lead": (75000, 120000)},
    "devops": {"junior": (35000, 52000), "mid": (52000, 78000), "senior": (78000, 115000), "lead": (105000, 145000)},
    "qa_engineer": {"junior": (28000, 42000), "mid": (42000, 62000), "senior": (62000, 90000), "lead": (85000, 115000)},
    "project_manager": {"junior": (30000, 45000), "mid": (45000, 65000), "senior": (65000, 90000), "lead": (85000, 120000)},
    "hr": {"junior": (24000, 35000), "mid": (35000, 50000), "senior": (50000, 72000), "lead": (68000, 95000)},
}

LOCATION_MULTIPLIERS = {
    "london": 1.30, "new_york": 1.45, "san_francisco": 1.55, "berlin": 0.95,
    "amsterdam": 1.05, "paris": 1.10, "sydney": 1.05, "toronto": 1.00,
    "singapore": 1.15, "remote": 0.90, "us": 1.20, "uk": 1.00, "eu": 0.95,
}

INTERVIEW_TEMPLATES = {
    "behavioral": [
        "Tell me about a time you had to deal with a difficult team member. What was the outcome?",
        "Describe a situation where you had to meet a tight deadline. How did you prioritize?",
        "Give an example of when you received critical feedback. How did you respond?",
        "Tell me about a project that failed. What did you learn?",
        "Describe a time you went above and beyond your role.",
    ],
    "technical": [
        "Walk me through the architecture of a system you designed recently.",
        "How would you approach debugging a production issue affecting 10% of users?",
        "Explain the trade-offs between consistency and availability in distributed systems.",
        "Describe your experience with CI/CD pipelines and deployment strategies.",
        "How do you approach code reviews? What do you look for?",
    ],
    "leadership": [
        "How do you handle underperforming team members?",
        "Describe your approach to setting team goals and tracking progress.",
        "How do you balance technical debt with feature development?",
        "Tell me about a time you had to make an unpopular decision.",
        "How do you foster innovation within your team?",
    ],
    "culture_fit": [
        "What type of work environment brings out your best work?",
        "How do you handle disagreements with colleagues?",
        "What motivates you beyond compensation?",
        "How do you stay current with industry trends?",
        "Describe your ideal manager.",
    ],
}


@mcp.tool()
def generate_job_description(
    title: str,
    department: str,
    level: str = "mid",
    skills: list[str] | None = None,
    company_name: str = "Our Company",
    remote: bool = False,
    key_responsibilities: list[str] | None = None, api_key: str = "") -> dict:
    """Generate a professional job description.

    Args:
        title: Job title (e.g. "Software Engineer", "Product Manager")
        department: Department (e.g. "Engineering", "Marketing")
        level: Seniority level: junior, mid, senior, lead
        skills: Required skills list
        company_name: Company name
        remote: Whether the role is remote
        key_responsibilities: Custom responsibilities (auto-generated if omitted)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("generate_job_description")

    level = level.lower()
    skills = skills or []

    exp_map = {"junior": "0-2", "mid": "2-5", "senior": "5-8", "lead": "8+"}
    years = exp_map.get(level, "2-5")

    level_prefix = {"junior": "Junior ", "mid": "", "senior": "Senior ", "lead": "Lead "}.get(level, "")
    full_title = f"{level_prefix}{title}"

    if not key_responsibilities:
        base_responsibilities = [
            f"Collaborate with cross-functional teams in {department}",
            f"Deliver high-quality work aligned with {company_name}'s goals",
            "Participate in planning, estimation, and review processes",
            "Mentor and support team members' growth",
            "Identify and implement process improvements",
        ]
        if level in ("senior", "lead"):
            base_responsibilities.extend([
                "Lead technical/strategic decisions for key initiatives",
                "Drive architecture and best practices across the team",
                "Represent the team in stakeholder discussions",
            ])
        key_responsibilities = base_responsibilities

    requirements = [f"{years} years of experience in {department.lower()} or related field"]
    for skill in skills[:8]:
        requirements.append(f"Proficiency in {skill}")
    requirements.extend([
        "Strong communication and collaboration skills",
        "Ability to work in a fast-paced environment",
    ])

    benefits = [
        "Competitive salary and equity package",
        "Health, dental, and vision insurance",
        "Flexible working hours",
        "Professional development budget",
        "Annual team retreats",
    ]
    if remote:
        benefits.append("Fully remote with home office stipend")

    return {
        "title": full_title,
        "department": department,
        "company": company_name,
        "location": "Remote" if remote else "Office-based (hybrid available)",
        "experience_required": f"{years} years",
        "responsibilities": key_responsibilities,
        "requirements": requirements,
        "nice_to_have": [f"Experience with {s}" for s in skills[3:6]] if len(skills) > 3 else [],
        "benefits": benefits,
        "generated_date": date.today().isoformat(),
    }


@mcp.tool()
def score_cv(
    cv_text: str,
    required_skills: list[str],
    preferred_skills: list[str] | None = None,
    min_years_experience: int = 0,
    required_education: str = "", api_key: str = "") -> dict:
    """Score and analyze a CV/resume against job requirements.

    Args:
        cv_text: Full text of the CV/resume
        required_skills: Must-have skills
        preferred_skills: Nice-to-have skills
        min_years_experience: Minimum years of experience required
        required_education: Required education level (e.g. "bachelor", "master")
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("score_cv")

    cv_lower = cv_text.lower()
    preferred_skills = preferred_skills or []

    # Skill matching
    required_matches = []
    required_misses = []
    for skill in required_skills:
        if skill.lower() in cv_lower:
            required_matches.append(skill)
        else:
            required_misses.append(skill)

    preferred_matches = [s for s in preferred_skills if s.lower() in cv_lower]

    # Experience extraction
    year_patterns = re.findall(r'(\d+)\+?\s*years?\s*(?:of\s+)?(?:experience|exp)', cv_lower)
    detected_years = max([int(y) for y in year_patterns], default=0)

    # Education detection
    edu_levels = {"phd": 5, "doctorate": 5, "master": 4, "msc": 4, "mba": 4,
                  "bachelor": 3, "bsc": 3, "ba ": 3, "degree": 3, "diploma": 2, "certificate": 1}
    detected_edu = 0
    detected_edu_name = "not detected"
    for level, score in edu_levels.items():
        if level in cv_lower:
            if score > detected_edu:
                detected_edu = score
                detected_edu_name = level

    # Scoring
    skill_score = (len(required_matches) / len(required_skills) * 60) if required_skills else 60
    preferred_score = (len(preferred_matches) / len(preferred_skills) * 15) if preferred_skills else 15
    exp_score = min(15, (detected_years / max(min_years_experience, 1)) * 15) if min_years_experience else 15

    required_edu_level = edu_levels.get(required_education.lower(), 0)
    edu_score = 10 if detected_edu >= required_edu_level else (detected_edu / max(required_edu_level, 1)) * 10

    total = round(skill_score + preferred_score + exp_score + edu_score, 1)

    if total >= 80:
        recommendation = "STRONG_MATCH - Recommend for interview"
    elif total >= 60:
        recommendation = "GOOD_MATCH - Consider for interview"
    elif total >= 40:
        recommendation = "PARTIAL_MATCH - Review manually"
    else:
        recommendation = "WEAK_MATCH - Does not meet minimum requirements"

    return {
        "overall_score": total,
        "recommendation": recommendation,
        "skills": {
            "required_matched": required_matches,
            "required_missing": required_misses,
            "required_match_rate": f"{len(required_matches)}/{len(required_skills)}",
            "preferred_matched": preferred_matches,
        },
        "experience": {
            "detected_years": detected_years,
            "required_years": min_years_experience,
            "meets_requirement": detected_years >= min_years_experience,
        },
        "education": {
            "detected": detected_edu_name,
            "required": required_education or "none",
            "meets_requirement": detected_edu >= required_edu_level,
        },
        "score_breakdown": {
            "required_skills": round(skill_score, 1),
            "preferred_skills": round(preferred_score, 1),
            "experience": round(exp_score, 1),
            "education": round(edu_score, 1),
        },
    }


@mcp.tool()
def generate_interview_questions(
    role: str,
    level: str = "mid",
    categories: list[str] | None = None,
    count: int = 10,
    skills_to_probe: list[str] | None = None, api_key: str = "") -> dict:
    """Generate tailored interview questions for a role.

    Args:
        role: Job role (e.g. "Software Engineer")
        level: Seniority: junior, mid, senior, lead
        categories: Question types: behavioral, technical, leadership, culture_fit
        count: Total number of questions (max 20)
        skills_to_probe: Specific skills to ask about
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("generate_interview_questions")

    count = min(count, 20)
    categories = categories or ["behavioral", "technical"]
    skills_to_probe = skills_to_probe or []

    questions = []
    for cat in categories:
        template_qs = INTERVIEW_TEMPLATES.get(cat, INTERVIEW_TEMPLATES["behavioral"])
        for q in template_qs:
            questions.append({"question": q, "category": cat, "difficulty": level})

    # Add skill-specific questions
    for skill in skills_to_probe[:5]:
        questions.append({
            "question": f"Describe your experience with {skill}. What's the most complex problem you've solved using it?",
            "category": "technical",
            "difficulty": level,
        })
        questions.append({
            "question": f"How would you evaluate whether {skill} is the right choice for a new project?",
            "category": "technical",
            "difficulty": level,
        })

    # Level-specific additions
    if level in ("senior", "lead"):
        questions.append({
            "question": f"As a {level} {role}, how would you handle a major technical disagreement within your team?",
            "category": "leadership",
            "difficulty": level,
        })

    selected = questions[:count]

    return {
        "role": role,
        "level": level,
        "question_count": len(selected),
        "questions": selected,
        "interview_tips": [
            "Use the STAR method (Situation, Task, Action, Result) to evaluate answers",
            "Allow candidates time to think before answering",
            "Take structured notes for consistent evaluation",
            f"Calibrate expectations for {level}-level candidates",
        ],
    }


@mcp.tool()
def benchmark_salary(
    role: str,
    level: str = "mid",
    location: str = "uk",
    currency: str = "GBP", api_key: str = "") -> dict:
    """Get salary benchmarks for a role by level and location.

    Args:
        role: Role category (software_engineer, data_scientist, product_manager, designer, marketing, sales, devops, qa_engineer, project_manager, hr)
        level: Seniority: junior, mid, senior, lead
        location: Location key (london, new_york, san_francisco, berlin, remote, us, uk, eu, etc.)
        currency: Output currency code
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("benchmark_salary")

    role_key = role.lower().replace(" ", "_")
    level_key = level.lower()
    location_key = location.lower().replace(" ", "_")

    benchmarks = SALARY_BENCHMARKS.get(role_key)
    if not benchmarks:
        closest = min(SALARY_BENCHMARKS.keys(), key=lambda k: sum(c1 != c2 for c1, c2 in zip(k, role_key)))
        benchmarks = SALARY_BENCHMARKS[closest]
        role_key = closest

    range_data = benchmarks.get(level_key, benchmarks.get("mid"))
    multiplier = LOCATION_MULTIPLIERS.get(location_key, 1.0)

    low = round(range_data[0] * multiplier, -3)
    high = round(range_data[1] * multiplier, -3)
    median = round((low + high) / 2, -3)

    fx_rates = {"GBP": 1.0, "USD": 1.27, "EUR": 1.17, "AUD": 1.93, "CAD": 1.72, "SGD": 1.71}
    fx = fx_rates.get(currency.upper(), 1.0)

    return {
        "role": role_key,
        "level": level_key,
        "location": location_key,
        "currency": currency.upper(),
        "salary_range": {
            "low": round(low * fx, -3),
            "median": round(median * fx, -3),
            "high": round(high * fx, -3),
        },
        "location_multiplier": multiplier,
        "data_source": "MEOK AI Labs Salary Index 2026",
        "note": "Figures are base salary estimates. Total compensation may include bonus, equity, and benefits.",
    }


@mcp.tool()
def draft_offer_letter(
    candidate_name: str,
    role: str,
    salary: float,
    currency: str = "GBP",
    start_date: str = "",
    company_name: str = "Our Company",
    benefits: list[str] | None = None,
    probation_months: int = 3,
    notice_period_weeks: int = 4,
    annual_leave_days: int = 25,
    reporting_to: str = "", api_key: str = "") -> dict:
    """Draft a professional offer letter for a candidate.

    Args:
        candidate_name: Full name of the candidate
        role: Job title offered
        salary: Annual base salary
        currency: Currency code
        start_date: Proposed start date (YYYY-MM-DD)
        company_name: Company name
        benefits: List of benefits to include
        probation_months: Probation period in months
        notice_period_weeks: Notice period in weeks
        annual_leave_days: Annual leave entitlement
        reporting_to: Manager's name/title
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("draft_offer_letter")

    if not start_date:
        start_date = date.fromordinal(date.today().toordinal() + 30).isoformat()

    benefits = benefits or [
        "Private health insurance",
        "Pension contribution (employer 5%)",
        "Professional development budget",
        "Flexible working arrangements",
    ]

    monthly_salary = round(salary / 12, 2)

    letter = {
        "type": "OFFER_LETTER",
        "date": date.today().isoformat(),
        "candidate_name": candidate_name,
        "company_name": company_name,
        "position": role,
        "compensation": {
            "annual_salary": salary,
            "monthly_salary": monthly_salary,
            "currency": currency.upper(),
        },
        "terms": {
            "start_date": start_date,
            "probation_period": f"{probation_months} months",
            "notice_period": f"{notice_period_weeks} weeks",
            "annual_leave": f"{annual_leave_days} days",
            "working_hours": "37.5 hours per week",
        },
        "benefits": benefits,
        "reporting_to": reporting_to or "To be confirmed",
        "response_deadline": date.fromordinal(date.today().toordinal() + 7).isoformat(),
        "letter_body": (
            f"Dear {candidate_name},\n\n"
            f"We are delighted to offer you the position of {role} at {company_name}. "
            f"Following our interviews, we were thoroughly impressed and believe you will be "
            f"an excellent addition to our team.\n\n"
            f"Your annual salary will be {currency.upper()} {salary:,.2f}, paid monthly. "
            f"Your proposed start date is {start_date}, subject to satisfactory references "
            f"and right-to-work verification.\n\n"
            f"This offer is subject to a {probation_months}-month probation period. "
            f"You will be entitled to {annual_leave_days} days of annual leave plus public holidays.\n\n"
            f"Please confirm your acceptance by signing and returning this letter "
            f"within 7 days.\n\n"
            f"We look forward to welcoming you to {company_name}.\n\n"
            f"Yours sincerely,\n{company_name} HR Team"
        ),
    }

    return letter


if __name__ == "__main__":
    mcp.run()
