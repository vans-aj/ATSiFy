from typing import Dict, List


def extract_resume_sections(parsed_resume: Dict) -> Dict[str, object]:
    exp_entries = [e for e in parsed_resume.get('experience', []) if isinstance(e, dict)]
    edu_entries = [e for e in parsed_resume.get('education', []) if isinstance(e, dict)]
    proj_entries = [p for p in parsed_resume.get('projects', []) if isinstance(p, dict)]
    skills: List[str] = parsed_resume.get('skills', [])
    summary = (parsed_resume.get('professional_summary') or '').strip()

    return {
        'exp_entries': exp_entries,
        'edu_entries': edu_entries,
        'proj_entries': proj_entries,
        'skills': skills,
        'summary': summary,
    }
