# Cover Letter Generator with CrewAI

A multi-agent application that automatically generates tailored cover letters by analyzing a resume and a job posting using [CrewAI](https://www.crewai.com/).

While the application is functional, I'm aware that similar results could be achieved using a smaller crew, however, it is a work that serves two purposes:
1. Putting in practice the knowledge acquired about CrewAI framework.
2. Generating a tailored cover letter for a specific job posting.

## How It Works

The application orchestrates a crew of six specialized AI agents (powered by `gpt-4o-mini`) that collaborate through a defined task pipeline:

| Agent | Role |
|---|---|
| **Talent Sourcer** | Extracts key requirements from the job posting |
| **Career Strategist** | Analyzes the resume and defines a positioning strategy |
| **Industry SME** | Identifies relevant technical skills from the job posting |
| **Resume Specialist** | Aligns resume strengths with the required technical skills |
| **Senior Technical Writer** | Drafts the cover letter based on strategy and alignment insights |
| **Senior Editor** | Polishes and finalizes the cover letter |

Some tasks run asynchronously (requirement gathering and technical skills management) to improve efficiency. The final output is saved to `compl_docs/cover_letter/base_cover_letter.md`.

## Project Structure

```
├── main.py                  # Entry point – defines agents, tasks, and crew
├── config/
│   ├── agents.yaml          # Agent role/goal/backstory configurations
│   └── tasks.yaml           # Task description/expected-output configurations
├── compl_docs/
│   ├── resume/              # Input resume file (TXT)
│   ├── job_post/            # Input job posting file (TXT)
│   └── cover_letter/        # Generated cover letter output (MD)
├── expl.ipynb               # Exploratory notebook
└── pyproject.toml           # Project metadata and dependencies
```

## Requirements

- Python 3.11.15
- An `OPENAI_API_KEY` environment variable set with a valid OpenAI API key

## Setup

```bash
# Create and activate the virtual environment
uv sync

# Set your API key
export OPENAI_API_KEY="your-key-here"
```

## Usage

1. Place your resume in `compl_docs/resume/[your_resume_name].txt`.
2. Place the job posting in `compl_docs/job_post/job_post_details.txt`.
3. Run the generator:

```bash
uv run python main.py
```

The generated cover letter will be written to `compl_docs/cover_letter/base_cover_letter.md`.
