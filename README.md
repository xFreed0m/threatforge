# 🔥 ThreatForge

AI-powered cybersecurity tabletop exercise scenario generator that creates comprehensive, realistic scenarios for security training and incident response exercises.

## ✨ Features

- **AI-Powered Generation**: Create detailed scenarios using OpenAI GPT or Anthropic Claude
- **Customizable Parameters**: Company size, industry, threat actors, and more
- **Cost Estimation**: See estimated costs before generation
- **Export Options**: Download scenarios as text files
- **Modern UI**: Responsive design with dark/light theme support
- **Real-time Generation**: Fast, async scenario creation

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Validation**: Pydantic v2
- **AI Integration**: OpenAI API, Anthropic API
- **Database**: SQLite (PostgreSQL ready)
- **Testing**: pytest, pytest-cov

### Frontend
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **UI Components**: PrimeVue 4
- **HTTP Client**: Axios
- **Styling**: CSS Variables with theme support

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- API keys for OpenAI and/or Anthropic

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd threatforge
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=your_openai_key_here
   # ANTHROPIC_API_KEY=your_anthropic_key_here
   # SECRET_KEY=your_secret_key_here
   ```

5. **Run the development servers**

   **Backend** (from `backend/` directory):
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Frontend** (from `frontend/` directory):
   ```bash
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 Usage

1. **Fill out the scenario form** with your requirements:
   - Company name and industry
   - Company size (small to enterprise)
   - Threat actor type
   - Exercise duration
   - AI provider preference

2. **Generate scenarios** with a single click

3. **Review and export** your generated scenario

## 🔧 Development

### Code Quality
The project uses several tools to maintain code quality:

- **Python**: Black (formatting), Ruff (linting)
- **Vue**: ESLint (linting)

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm run test
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend (ready for production)
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
threatforge/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   │   ├── core/          # Configuration
│   │   │   ├── models/        # Database models
│   │   │   ├── schemas/       # Pydantic models
│   │   │   └── services/      # Business logic
│   │   ├── tests/             # Test files
│   │   └── requirements.txt   # Python dependencies
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/    # Vue components
│   │   │   ├── assets/        # Static assets
│   │   │   └── views/         # Page components
│   │   ├── package.json       # Node dependencies
│   │   └── vite.config.js     # Vite configuration
│   └── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Vue.js](https://vuejs.org/)
- UI components from [PrimeVue](https://primevue.org/)
- AI capabilities powered by [OpenAI](https://openai.com/) and [Anthropic](https://anthropic.com/)

## Backend Environment Setup

Create a `.env` file in `backend/` or set environment variables for:

```
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
ENVIRONMENT=development
```

- At least one API key is required for scenario generation endpoints to work.
- For CI/testing, the backend will use a mock LLM provider if `ENVIRONMENT` is set to `test` or `ci` or if no API keys are present.
