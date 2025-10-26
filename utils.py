import pandas as pd

COMMON_SKILLS = [
    "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go",
    "React", "Angular", "Vue", "Django", "Flask", "Node.js",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "SQL", "NoSQL",
    "HTML", "CSS", "TypeScript", "Machine Learning", "Data Science",
]

FIELDS = [
    "id", "source", "title", "company", "category", "job_type",
    "location", "url", "publication_date", "skills",
]


def extract_skills(text: str) -> str:
    found = [skill for skill in COMMON_SKILLS if skill.lower() in text.lower()]
    return ", ".join(found)


def save_jobs(jobs: list[dict], output="jobs.csv"):
    df = pd.DataFrame(jobs)
    for col in FIELDS:
        if col not in df.columns:
            df[col] = ""
    df = df[FIELDS]
    df.drop_duplicates(subset=["title", "company", "url"], inplace=True)
    df.to_csv(output, index=False)
    print(f"\n✅ Saved {len(df)} jobs to {output}")
