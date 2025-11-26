# PR Reviewer - AI-Powered GitHub Pull Request Analysis

An intelligent FastAPI application that provides comprehensive automated code review for GitHub pull requests using OpenAI's GPT models and LangGraph workflows.

## 🚀 Live Demo

**Production URL**: https://pr-reviewer-mrvineetraj.onrender.com

> You can test reviewer from [`/docs`](https://pr-reviewer-mrvineetraj.onrender.com/docs) endpoint

## ✨ Features

- 🔍 **Comprehensive PR Analysis**: Automated walkthrough of code changes
- 📊 **Visual Diagrams**: Auto-generated sequence and activity diagrams using Mermaid
- 📝 **File Change Summary**: Structured table of all modified files
- 💬 **Inline Code Reviews**: Specific line-by-line feedback and suggestions
- 🎨 **Creative Touch**: Poetic descriptions of your code changes
- 🔐 **GitHub Integration**: Seamless posting of comments and reviews
- ⚡ **Background Processing**: Automated server keep-alive functionality

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI/ML**: OpenAI GPT-5.1, LangGraph
- **GitHub API**: Pull request diff analysis and commenting
- **Deployment**: Render (with auto-scaling)
- **Background Jobs**: Async task management

## 📋 API Endpoints

### Health Check

```http
GET /
```

**Response:**

```json
{
  "message": "hello from galaxy"
}
```

### Review Pull Request

```http
POST /api/v1/github/review
```

**Request Body:**

```json
{
  "owner": "string",
  "pull_number": 1,
  "repo": "string"
}
```

**Response (200 OK):**

```json
{
  "success": true,
  "message": "Review processed",
  "inline_review_description": "High level description for issues in code",
  "inline_reviews_count": 2
}
```

**Error Responses:**

- `403 Forbidden`: Not authorized (owner validation failed)
- `500 Internal Server Error`: Processing error

## 🔧 Local Development Setup

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key

### Installation Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd lyzr-intern
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment Configuration**

Create a `.env` file in the root directory:

```env
GITHUB_PAT_TOKEN=your_github_personal_access_token
OPENAI_API_KEY=your_openai_api_key
OWNER_USERNAME=your_github_username
API_ENDPOINT=http://localhost:8000
```

5. **Run the application**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 🔑 Environment Variables

| Variable           | Description                                        | Required |
| ------------------ | -------------------------------------------------- | -------- |
| `GITHUB_PAT_TOKEN` | GitHub Personal Access Token with repo permissions | ✅       |
| `OPENAI_API_KEY`   | OpenAI API key for GPT models                      | ✅       |
| `OWNER_USERNAME`   | GitHub username for authorization                  | ✅       |
| `API_ENDPOINT`     | API base URL (for keep-alive functionality)        | ✅       |

## 🎯 Usage Example

### Using cURL

```bash
curl -X POST "https://pr-reviewer-mrvineetraj.onrender.com/api/v1/github/review" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "mrvineetraj",
    "pull_number": 1,
    "repo": "testing-python-reviewer"
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "https://pr-reviewer-mrvineetraj.onrender.com/api/v1/github/review",
    json={
        "owner": "mrvineetraj",
        "pull_number": 1,
        "repo": "testing-python-reviewer"
    }
)

print(response.json())
```

## 🔄 Review Process Workflow

1. **Diff Extraction**: Fetches PR diff from GitHub
2. **Walkthrough Generation**: Creates comprehensive change summary
3. **File Analysis**: Generates structured file change table
4. **Diagram Creation**: Produces sequence and activity diagrams
5. **Creative Content**: Adds poetic description
6. **Comment Posting**: Posts main review comment to PR
7. **Inline Reviews**: Generates and posts specific code suggestions

## 📁 Project Structure

```
lyzr-intern/
├── app/
│   ├── core/
│   │   ├── config.py          # Environment configuration
│   │   └── prompt.py          # LLM prompt templates
│   ├── routes/
│   │   └── github/
│   │       ├── __init__.py    # API router
│   │       ├── actions.py     # Business logic
│   │       ├── schema.py      # Pydantic models
│   │       └── utils.py       # LangGraph workflow
│   └── services/
│       ├── cron.py           # Background tasks
│       ├── github_service.py # GitHub API integration
│       └── langgraph_nodes.py # LLM processing nodes
├── tests/
│   └── test_github_service.py
├── main.py                   # FastAPI application entry
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚨 Security & Authorization

- Only authorized GitHub users (matching `OWNER_USERNAME`) can trigger reviews
- GitHub PAT token is used for secure API access
- Environment variables are validated at startup

## 📊 Generated Content Examples

The application generates:

- **Walkthrough**: Detailed markdown summary of changes
- **File Table**: Structured comparison of modified files
- **Mermaid Diagrams**: Visual representation of code flow
- **Inline Reviews**: Specific improvement suggestions
- **Creative Content**: Poetic descriptions of changes

**Live API Documentation**: https://pr-reviewer-mrvineetraj.onrender.com/docs
