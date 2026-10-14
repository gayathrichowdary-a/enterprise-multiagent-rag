# Adaptive Multi-Agent RAG with Source Reliability Ranking and Retrieval Quality Assessment for Enterprise Knowledge Management

## 1. Project Overview

The **Adaptive Multi-Agent RAG with Source Reliability Ranking and Retrieval Quality Assessment for Enterprise Knowledge Management** project is an AI-powered web application designed to help users retrieve, analyze, compare, and understand information from uploaded knowledge documents.

The system combines Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), document embeddings, vector-based retrieval, source reliability ranking, and a multi-agent workflow.

Unlike a basic document chatbot, the application provides a complete user interface with authentication, document ingestion, conversational question answering, source reliability monitoring, knowledge graph visualization, document comparison, conversation memory, and chat history.

The main purpose is to improve how information is retrieved and how the reliability of knowledge sources is assessed before users depend on the generated answers.

## 2. Problem Statement

Enterprise organizations maintain information across policies, technical manuals, internal documentation, reports, and other knowledge sources. Finding accurate information across these documents can be difficult.

Traditional question-answering systems may retrieve incomplete or less reliable information, which can affect the usefulness of generated answers. A generated response may also be difficult to evaluate if the system does not provide sufficient information about the sources used.

This project addresses these challenges by developing a document-based RAG application that integrates source authority information, reliability scoring, retrieval workflows, and knowledge exploration features.

## 3. Objectives

The primary objectives of this project are:

## 3. Objectives

1. To develop an adaptive multi-agent Retrieval-Augmented Generation (RAG) system for enterprise knowledge management that retrieves relevant information from uploaded documents and generates context-grounded answers.

2. To implement source reliability ranking based on authority, cross-verification, and recency, along with retrieval quality assessment to evaluate the relevance and sufficiency of retrieved information.

3. To evaluate the effectiveness of the proposed system through experimental testing and comparison with baseline RAG methods using appropriate evaluation metrics.

## 4. Key Features

### 4.1 User Authentication

The application includes login and signup interfaces to provide an authenticated entry point to the application.

### 4.2 Enterprise Document Upload

Users can upload supported documents for processing and indexing. The supported file types in the current implementation are:

- PDF
- DOCX
- TXT
- CSV
- PNG
- JPG and JPEG

The upload module includes a maximum file size of 10 MB per file and allows users to assign an enterprise department and source authority tier.

### 4.3 Document Processing and Indexing

Uploaded documents are processed through a document-loading and text-chunking workflow. The extracted text is converted into embeddings and stored in a FAISS vector store for similarity-based retrieval.

The application also checks file hashes to identify unchanged documents and reuse existing vector indexes when available.

### 4.4 AI-Powered Document Chat

The chat interface allows users to ask questions about their uploaded knowledge sources. Retrieved document content is used as context for generating answers through the configured language-model workflow.

### 4.5 Multi-Agent Workflow

The project includes agent-related modules and a LangGraph workflow directory to organize AI processing tasks.

The workflow supports the project's multi-agent RAG design. The exact responsibilities and execution order of the agents should be documented according to the implemented workflow.

### 4.6 Source Reliability Ranking

The source ranking dashboard displays registered knowledge sources, authority tiers, reliability information, and a ranked source leaderboard.

The reliability calculation defined in the source-ranking module combines three factors:

- Authority score: 50% weight
- Cross-verification factor: 30% weight
- Recency score: 20% weight

The implemented calculation is:

Reliability Score = 100 × (0.50 × Authority Score + 0.30 × Verification Factor + 0.20 × Recency Score)

The verification factor is normalized using the verified-triplet count, while the recency component uses exponential time decay.

The initial reliability values assigned during document ingestion are also based on the selected authority tier. These initial values and the composite calculation should be distinguished when describing the implementation in research documentation.

### 4.7 Retrieval Quality Assessment

The project aims to assess whether retrieved information is relevant and sufficient for answering a query. The exact quality-assessment method, its thresholds, and its evaluation procedure should be documented from the corresponding implementation and experimental results.

### 4.8 Knowledge Graph

The knowledge graph page provides a visual interface for exploring relationships between knowledge items, according to the graph functionality implemented in the application.

### 4.9 Document Comparison

The comparison page allows users to examine information across documents and supports knowledge analysis beyond single-document question answering.

### 4.10 Conversation Memory and Chat History

The application includes separate interfaces for conversation memory and previous chat sessions, helping users revisit earlier interactions and continue their work.

### 4.11 Dashboard and Settings

The dashboard provides navigation to the main application modules. The settings page provides the application's available configuration options.

## 5. System Workflow

The intended high-level workflow is:

1. User logs in or creates an account.
2. User uploads enterprise knowledge documents.
3. The application extracts text and divides it into chunks.
4. The embedding component converts text chunks into vector representations.
5. The vector store indexes the document representations.
6. User submits a question through the chat interface.
7. The retrieval workflow identifies potentially relevant document content.
8. Source reliability information and retrieval quality assessment are applied according to the implemented methods.
9. The configured LLM workflow generates a response using retrieved context.
10. Users can explore source rankings, compare documents, inspect the knowledge graph, and revisit conversation history.

The exact order of retrieval assessment, agent execution, and response generation must match the implemented workflow.

## 6. Technology Stack

The repository identifies the following technologies and libraries:

| Component | Technology |
|---|---|
| Programming language | Python |
| Web application | Streamlit |
| AI workflow orchestration | LangGraph |
| LLM integration | LangChain integrations, including Groq and Google Generative AI packages |
| Embedding models | Sentence Transformers library |
| Vector store | FAISS |
| Document processing | PyPDF, python-docx and project-specific loaders |
| Data processing | Pandas |
| Visualization | Plotly |
| Configuration | python-dotenv |
| User database | Project authentication/database modules |

The exact active LLM provider, model identifier, embedding model, and model configuration should be confirmed from the configuration and execution code.

## 7. Dataset and Knowledge Sources

### Dataset Used for Experimental Evaluation
## Dataset and Knowledge Sources

The system uses user-uploaded documents as its knowledge sources. Supported documents are processed and indexed to enable retrieval-augmented question answering. These documents provide the context used by the system to retrieve relevant information, assess source reliability, and generate answers.

The application supports PDF, DOCX, TXT, CSV, PNG, JPG, and JPEG files.

### Document Collection Used by the Application

The application supports user-uploaded documents as knowledge sources. The documents used in the application's demonstration and the dataset used for experimental evaluation should be identified separately if they are different.

The dataset name, origin, licensing conditions, size, and experimental usage must be documented accurately.

## 8. Source Reliability Method

The source reliability method combines source authority, cross-verification, and document recency.

The weighted calculation implemented in the source-ranking module is:

R = 100 × (0.50A + 0.30V + 0.20T)

Where:

- R = Composite reliability score expressed as a percentage
- A = Normalized authority score
- V = Normalized cross-verification factor
- T = Recency score calculated using exponential decay

The verification factor is normalized using the verified-triplet count. The recency score is calculated using an exponential decay function based on document age.

The formula, normalization ranges, default values, and the relationship between the formula and the scores assigned during document ingestion should be reported consistently with the actual code.

## 9. Experimental Evaluation

The system should be evaluated using the actual experimental setup and recorded results.

The evaluation may include the following, where these metrics were actually measured:

- Retrieval relevance and ranking quality
- Source reliability scoring
- Retrieval sufficiency or quality assessment
- Answer correctness and faithfulness to retrieved evidence
- Response latency
- Comparison against baseline RAG methods

### Results Table

| Method | Metric | Actual result |
|---|---|---|
| Baseline method | [Actual metric] | [Measured value] |
| Proposed system | [Same metric] | [Measured value] |

Add further rows for each tested method and metric. Include the evaluation dataset, number of test cases, experimental configuration, and calculation procedure.

Do not report unmeasured values or claim improvements unless supported by the experiments.

## 10. Project Structure

The repository contains the following main modules:

```text
enterprise-multiagent-rag/
├── agents/               # Agent-related components
├── auth/                 # Login, signup, and database modules
├── dashboard/            # Application pages and user interface
├── database/             # Database-related components
├── graph/                # Graph-related components
├── langgraph_workflow/   # Workflow orchestration
├── llm/                  # Language-model integrations
├── loaders/              # Document loading
├── memory/               # Conversation memory
├── rag/                  # RAG and retrieval components
├── tools/                # Supporting tools
├── uploads/              # Uploaded document storage
├── utils/                # Utility functions
├── vector_store/         # Vector index storage
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

This is a high-level view of the repository. The files and responsibilities inside each folder should be checked against the current source code.

## 11. Installation and Execution

### Prerequisites

- Python version compatible with the project's dependencies
- Git
- Access to the configured LLM provider, where required
- Required model and API configuration

### Clone the Repository

```bash
git clone https://github.com/gayathrichowdary-a/enterprise-multiagent-rag.git
cd enterprise-multiagent-rag
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create or update the local `.env` file according to the configuration expected by the application. Add only the required credentials and settings.

Never publish API keys, passwords, access tokens, private datasets, or sensitive user information to GitHub.

### Run the Application

```bash
streamlit run app.py
```

The application should open in a browser. Confirm that all required configuration values and model access are available before running it.

## 12. Screenshots

Screenshots of the actual running application are provided to demonstrate the user interface and main features.

The recommended screenshots are:

1. Login and signup pages
2. Main dashboard or home page
3. Enterprise document upload page
4. Chat interface showing a query and answer
5. Knowledge graph visualization
6. Document comparison page
7. Conversation memory or chat history
8. Settings page

See the `docs/images/` directory for the screenshots included in this documentation.

## 13. Limitations

The reliability of generated answers depends on the quality of uploaded documents, document extraction, retrieval, embedding representations, and the configured language model.

Source reliability scores depend on the selected authority tiers, the implemented verification signals, and recency settings. They should not be interpreted as independently verified truth scores without suitable validation.

Experimental conclusions should be limited to the tested dataset, queries, configurations, and evaluation methods.

## 14. Future Work

Potential future work includes broader benchmark evaluation, additional baseline comparisons, improved retrieval-quality assessment, validation of source reliability scores, and testing on larger and more diverse enterprise knowledge collections.

## 15. Research and Reproducibility

This repository documents the implementation of the project. Research claims should be supported by the actual implementation, dataset documentation, experimental results, and relevant scholarly references.

## 16. Repository

GitHub: https://github.com/gayathrichowdary-a/enterprise-multiagent-rag

