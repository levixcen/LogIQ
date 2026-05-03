import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-12-01-preview"
)

def read_log_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def chunk_logs(log_content, chunk_size=50):
    lines = log_content.strip().split('\n')
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunks.append('\n'.join(lines[i:i+chunk_size]))
    return chunks

def call_azure_openai(prompt):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

def build_analysis_prompt(log_chunk):
    return f"""
    You are a senior digital forensic analyst. Analyze the following Windows 
    Event Log entries and reason through them step by step.

    For each suspicious event you identify:
    1. State the timestamp and Event ID
    2. Explain what this event means in plain language
    3. Identify the MITRE ATT&CK tactic and technique it maps to
    4. Rate the severity as Low, Medium, or High
    5. Explain your reasoning

    Log entries:
    {log_chunk}

    Think step by step. If an event is benign, say so and move on.
    Only flag events that are genuinely suspicious.
    """

def build_report_prompt(all_findings):
    return f"""
    You are a senior digital forensic analyst writing a formal investigation report.
    Based on the following findings, produce a structured report with exactly these sections:

    CLASSIFICATION: CONFIDENTIAL
    REPORT ID: [generate a random alphanumeric ID like FR-2026-XXXX]
    DATE: {__import__('datetime').datetime.now().strftime('%B %d, %Y')}
    ANALYST: LogIQ Forensic AI Agent

    EXECUTIVE SUMMARY
    [2-3 sentences describing what happened]

    ATTACK TIMELINE
    [Chronological numbered list of events with timestamps]

    MITRE ATT&CK MAPPING
    [List each finding as: TACTIC | TECHNIQUE ID | TECHNIQUE NAME | SEVERITY]

    NARRATIVE
    [Plain language explanation of the attack from start to finish]

    RECOMMENDED NEXT STEPS
    [Numbered list of actions the investigator should take]

    ANALYST NOTES
    [Any caveats, limitations of the analysis, or areas needing human review]

    Findings to analyze:
    {all_findings}

    STRICT RULES:
    - Do not use markdown. No hashtags, no asterisks, no backticks.
    - Use plain text only with section headers exactly as shown above in capitals.
    - Write dates, times, and Event IDs clearly.
    - Write so a non-technical manager understands but a junior analyst can act on it.
    """

def run_agent(log_filepath):
    print(f"Starting forensic analysis of: {log_filepath}")
    
    print("Step 1: Reading log file...")
    log_content = read_log_file(log_filepath)
    
    print("Step 2: Chunking logs for analysis...")
    chunks = chunk_logs(log_content)
    print(f"Log split into {len(chunks)} chunks")
    
    print("Step 3: Analyzing each chunk...")
    all_findings = []
    for i, chunk in enumerate(chunks):
        print(f"  Analyzing chunk {i+1} of {len(chunks)}...")
        prompt = build_analysis_prompt(chunk)
        finding = call_azure_openai(prompt)
        all_findings.append(finding)
    
    print("Step 4: Generating forensic report...")
    report_prompt = build_report_prompt('\n\n'.join(all_findings))
    final_report = call_azure_openai(report_prompt)
    
    print("Step 5: Analysis complete.")
    return final_report

if __name__ == "__main__":
    report = run_agent('data/sample_log.txt')
    print("\n" + "="*50)
    print("FORENSIC REPORT")
    print("="*50)
    print(report)