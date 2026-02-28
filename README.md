# EscalationAgent-RAG
Agentic (RAG) system with Azure OpenAI and Azure AI Search. It aims to detect ongoing customer complaints and start escalation workflows. 

This project sets up an Agentic Retrieval-Augmented Generation (RAG) system with Azure OpenAI and Azure AI Search. It aims to detect ongoing customer complaints and start escalation workflows. The system looks at customer reviews, finds similar past issues through vector search, and employs an Azure AI Agent to decide if escalation is needed. 

##Problem Statement:
Customer support teams often overlook repeated product problems that are buried in large amounts of reviews. This system: Embeds incoming reviews Searches for similar past complaints Uses an AI reasoning agent to assess severity Escalates recurring issues automatically.

##Architectural Innovation:
This project implements a hybrid retrieval-reasoning architecture that fuses structured data features with unstructured textual embeddings to enable semantic history analysis with aggregation-driven decision logic. Pure RAG or semantic search systems lack this cross-signal aggregation capability, which is essential for detecting recurring patterns and triggering escalation workflows.

## Architecture Diagram
[View Architecture Diagram](images/escalation_ragsystem-diagram.png)

## Setup
python --version  
python -m venv .venv  
.venv\scripts\activate  
pip --version  
python -m pip install --upgrade pip  
pip install -r requirement.txt  
