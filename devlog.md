# Devlog

## Day 1 - April 21 2026

**What I am building:**
An AI-powered post-incident forensic reconstruction agent that ingests 
Windows Event Logs, reasons through attack sequences autonomously, maps 
findings to MITRE ATT&CK, and generates structured investigation reports 
using Azure OpenAI.

**Why this problem:**
After a year in cybersecurity, I noticed that post-incident investigation 
requires analysts to manually reconstruct entire attack sequences from 
thousands of raw log lines, a process that demands senior-level expertise 
most teams in Southeast Asia simply do not have access to. While general 
AI tools can analyze logs, none produce structured, framework-grounded 
forensic reports that investigators can directly use or submit. This agent 
fills that gap.

**What I did today:**
- Set up GitHub repo and folder structure
- Wrote README with project overview
- Writing agent skeleton with placeholder Azure OpenAI calls
- Drafting architecture diagram

**Blockers:**
- Azure access not working yet, using placeholder logic for now

**Tomorrow:**
- Sort Azure access
- Replace placeholder with real Azure OpenAI call
- Test agent with sample log file

## Day 3 - April 28 2026

**What I did today:**
- Set up Azure OpenAI resource (logiq-openai) in Korea Central
- Deployed GPT-4o model via Azure AI Foundry
- Replaced placeholder with real Azure OpenAI API call
- Successfully tested agent producing a full forensic report
- Agent correctly identified MITRE ATT&CK techniques T1059.003, 
  T1059.001, T1053.005, and T1110 from sample logs

**What the agent produced:**
A complete forensic report including executive summary, attack timeline, 
MITRE ATT&CK mapping, plain language narrative, and recommended next steps.


## Day 3 continued - April 28 2026

**What I did:**
- Built Flask web UI with blue and purple DFIR themed interface
- Added analysis steps panel showing agent reasoning in real time
- Tested UI end to end with sample_log.txt, confirmed report renders in browser
- Installed python-evtx and built EVTX converter script
- Downloaded EVTX-ATTACK-SAMPLES from GitHub by sbousseaden
- Converted real Windows Event Log (4794 DSRM password change) to text
- Tested agent with real forensic log, produced full investigation report
- Agent correctly identified Group Policy modification, mapped to MITRE 
  ATT&CK T1053, flagged Administrator account usage on domain controller
- Created synthetic attack_scenario.txt covering full attack chain: 
  phishing, macro execution, PowerShell download, persistence, credential 
  dumping via mimikatz, data exfiltration, log clearing

**What is working:**
- Azure OpenAI connected and producing real forensic reports
- Web UI live at localhost:5000
- EVTX to text conversion pipeline working
- Agent reasoning correctly through real world log data

**What is left:**
- Deploy to Azure App Service so it runs in the cloud
- Test with attack_scenario.txt for richer demo output
- Risk and safety evaluation section
- Record demo video
- Devpost submission form

## Day 9 - May 03 2026

**What I did today:**
- Redesigned UI to chat interface inspired by real SOC platforms
- Implemented blue and purple DFIR color theme with black background
- Added real-time analysis steps panel showing agent reasoning
- Fixed report formatting to render structured sections with blue headers
- Added MITRE ATT&CK technique badges with purple styling
- Implemented follow-up Q&A chat feature connected to real Azure OpenAI
- Fixed formatChatResponse function scope bug causing chat failures
- Tested full end-to-end flow: log upload, report generation, follow-up questions
- Confirmed output matches SANS-style incident response report format
- Verified agent correctly handles follow-up questions using report context

**What LogIQ can do right now:**
- Accept .txt and .log files via chat interface
- Autonomously reason through Windows Event Logs step by step
- Map findings to MITRE ATT&CK framework with tactic, technique ID, and severity
- Generate SANS-aligned forensic report with classification, report ID, timeline, narrative
- Answer follow-up questions about the incident based on report context
- Respond like a senior forensic analyst to junior analyst questions

**Stack used:**
- Azure OpenAI GPT-4o via Azure AI Foundry
- Flask web framework
- Python agent with chunking and multi-step reasoning
- Deployed locally, Azure App Service deployment pending

**Remaining:**
- Architecture diagram
- Demo video recording
- Devpost submission

**Reflection:**
LogIQ is designed for junior forensic analysts in Southeast Asia who lack
access to senior DFIR expertise. The tool closes that gap by making
expert-level forensic reasoning accessible through a simple chat interface.

