# Warning control
import warnings

warnings.filterwarnings("ignore")

import os
import yaml
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool

openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
read_resume = FileReadTool(file_path="./compl_docs/resume/CV_Miguel_Barrera.txt")
read_job_post = FileReadTool(file_path="./compl_docs/job_post/job_post_details.txt")

# Define file paths for YAML configurations
files = {"agents": "config/agents.yaml", "tasks": "config/tasks.yaml"}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, "r") as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs["agents"]
tasks_config = configs["tasks"]

# Creating Agents
talent_sourcer_agent = Agent(
    config=agents_config["talent_sourcer_agent"], tools=[read_job_post]
)

career_strategist_agent = Agent(
    config=agents_config["career_strategist_agent"], tools=[read_resume]
)

industry_subject_matter_expert_agent = Agent(
    config=agents_config["industry_subject_matter_expert_agent"], tools=[read_job_post]
)

resume_specialist_agent = Agent(
    config=agents_config["resume_specialist_agent"], tools=[read_resume]
)

senior_technical_writer_agent = Agent(
    config=agents_config["senior_technical_writer_agent"]
)

senior_editor_agent = Agent(config=agents_config["senior_editor_agent"])

# Creating Tasks
requirement_gathering = Task(
    config=tasks_config["requirement_gathering"],
    agent=talent_sourcer_agent,
    async_execution=True,
)

strategy_definition = Task(
    config=tasks_config["strategy_definition"],
    agent=career_strategist_agent,
    context=[requirement_gathering],
)

technical_skills_management = Task(
    config=tasks_config["technical_skills_management"],
    agent=industry_subject_matter_expert_agent,
    async_execution=True,
)

alignment_optimization = Task(
    config=tasks_config["alignment_optimization"],
    agent=resume_specialist_agent,
    context=[technical_skills_management],
)

cover_letter_development = Task(
    config=tasks_config["cover_letter_development"],
    agent=senior_technical_writer_agent,
    context=[strategy_definition, alignment_optimization],
)

cover_letter_editing = Task(
    config=tasks_config["cover_letter_editing"],
    agent=senior_editor_agent,
    context=[cover_letter_development],
    output_file="./compl_docs/cover_letter/base_cover_letter.md",
)

# Creating Crew
crew = Crew(
    agents=[
        talent_sourcer_agent,
        career_strategist_agent,
        industry_subject_matter_expert_agent,
        resume_specialist_agent,
        senior_technical_writer_agent,
        senior_editor_agent,
    ],
    tasks=[
        requirement_gathering,
        strategy_definition,
        technical_skills_management,
        alignment_optimization,
        cover_letter_development,
        cover_letter_editing,
    ],
    verbose=True,
    memory=True,
)

result = crew.kickoff()
