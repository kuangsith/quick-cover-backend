# quickCover - Backend

**quickCover** is a lightweight backend service that generates personalized cover letters for job applications using Google's Gemini AI. Users provide key inputs—such as resume text, job title, and company name—and the API responds with a tailored, professional cover letter in seconds.

## ✨ Features

- AI-generated cover letters based on user input
- Lightweight and fast, designed for real-time use
- Stateless backend with no database or authentication (yet)
- Built with Python and deployed via Google Cloud Run

## 🧠 Tech Stack

- **Language:** Python 3
- **AI Provider:** Google Gemini via Vertex AI or PaLM API
- **Framework:** Flask / FastAPI *(adjust based on your actual setup)*
- **Deployment:** Google Cloud Run + Netlify (frontend), Docker
- **Frontend:** React (separate repo)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Access to Gemini API with valid credentials
- Docker (for containerization)
- Google Cloud SDK (for deployment to Cloud Run)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/kuangsith/quick-cover-backend.git
cd quick-cover-backend
