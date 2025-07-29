# 🔥 ThreatForge

[![GitHub stars](https://img.shields.io/github/stars/xfreed0m/threatforge?style=social)](https://github.com/xfreed0m/threatforge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/Security-Scanned-green.svg)](https://github.com/xfreed0m/threatforge/actions/workflows/security.yml)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)

AI-powered cybersecurity tabletop exercise scenario generator that creates comprehensive, realistic scenarios for security training and incident response exercises.

![ThreatForge Demo](docs/demo.gif)

## ✨ Features

- 🤖 **Multi-AI Provider Support** - Generate scenarios using OpenAI GPT or Anthropic Claude
- 🎯 **Smart Scenario Generation** - Create detailed, realistic cybersecurity scenarios
- 🔄 **Reroll Capability** - Regenerate specific sections of scenarios on-demand
- 💰 **Cost Estimation** - Compare costs across different AI providers before generation
- 🏢 **Customizable Parameters** - Company size, industry, threat actors, technologies
- 📊 **Scenario History** - Track and review previously generated scenarios
- 🎨 **Modern UI** - Responsive design with cyberpunk theme
- ⚡ **Real-time Generation** - Fast, async scenario creation
- 📱 **Export Options** - Download scenarios as text files
- 🔧 **Production Ready** - Docker support with nginx and gunicorn

## 🚀 Quick Start

### Docker (Recommended)

```bash
# One-liner deployment
docker-compose -f docker-compose.prod.yml up -d

# Visit the application
open http://localhost
```

That's it! The application will be available at `http://localhost` with both frontend and backend running.

## 🛠️ Tech Stack

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0+-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5.3+-orange.svg)
![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0+-red.svg)

- **Framework**: FastAPI with async support
- **Validation**: Pydantic v2 for data validation
- **AI Integration**: OpenAI API, Anthropic API
- **Server**: Gunicorn with uvicorn workers
- **Testing**: pytest, pytest-cov
- **Code Quality**: Black, Ruff

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)
![Vite](https://img.shields.io/badge/Vite-5.0+-purple.svg)
![PrimeVue](https://img.shields.io/badge/PrimeVue-4.0+-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-20+-green.svg)

- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite for fast development
- **UI Components**: PrimeVue 4
- **HTTP Client**: Axios
- **Styling**: CSS Variables with cyberpunk theme

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Nginx](https://img.shields.io/badge/Nginx-1.25+-green.svg)

- **Containerization**: Multi-stage Docker builds
- **Web Server**: Nginx for static file serving and API proxy
- **Process Manager**: Gunicorn for production WSGI serving

## 🔧 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker (optional, for containerized development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/xFreed0m/threatforge.git
   cd threatforge
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run Development Servers**

   **Backend** (from `backend/` directory):
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Frontend** (from `frontend/` directory):
   ```bash
   npm run dev
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Development

```bash
# Development with hot-reloading
docker-compose -f docker-compose.dev.yml up

# Access at http://localhost:3000 (frontend) and http://localhost:8000 (backend)
```

## 🔒 Security

ThreatForge implements comprehensive security scanning to prevent secrets from being exposed:

### Automated Security Scanning
- **TruffleHog**: Scans for verified secrets in git history
- **GitLeaks**: Comprehensive secret detection with custom patterns
- **Pre-commit hooks**: Prevent secrets from being committed
- **Weekly scans**: Automated security audits

### Security Features
- ✅ **Secret Detection**: Automated scanning for API keys, tokens, and credentials
- ✅ **False Positive Filtering**: Excludes test data and examples
- ✅ **Git History Scanning**: Full repository history analysis
- ✅ **Pre-commit Protection**: Hooks prevent accidental secret commits
- ✅ **SARIF Reports**: Integration with GitHub Security tab

### Running Security Scans Locally
```bash
# Quick setup (recommended)
./scripts/setup-security.sh

# Manual setup
pip install pre-commit
pre-commit install

# Run GitLeaks scan (no license required for personal repos)
gitleaks detect --config-path=.gitleaks.toml --verbose

# Run TruffleHog scan
trufflehog --only-verified --fail .
```

## 🧪 Testing
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Code Quality
```bash
# Backend
cd backend
black .
ruff check .

# Frontend
cd frontend
npm run lint
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Keys (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Application Settings
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./threatforge.db

# Optional: Custom ports
FRONTEND_PORT=80
BACKEND_PORT=8000
```

### API Key Setup

1. **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Anthropic**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

At least one API key is required for scenario generation. For testing, the application will use a mock provider if no keys are configured.

## 📖 Usage

1. **Fill out the scenario form** with your requirements:
   - Company name and industry
   - Company size (small to enterprise)
   - Threat actor type (ransomware, APT, insider, etc.)
   - Exercise duration
   - Technologies and participants
   - AI provider preference

2. **Generate scenarios** with a single click

3. **Use the reroll feature** to regenerate specific sections

4. **Compare costs** across different AI providers

5. **Review and export** your generated scenario

## 🏗️ Project Structure

```
threatforge/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic & AI services
│   ├── tests/              # Test files
│   └── requirements.txt    # Python dependencies
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── assets/         # Static assets
│   │   └── views/          # Page components
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── docker/                 # Docker configuration
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── nginx.conf
├── docs/                   # Documentation
├── docker-compose.dev.yml  # Development setup
├── docker-compose.prod.yml # Production setup
└── README.md
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style (Black for Python, ESLint for JavaScript)
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 🗺️ Roadmap

### Upcoming Features
- 🔐 **Multi-user Support** - User authentication and scenario sharing
- 📊 **Analytics Dashboard** - Usage statistics and scenario metrics
- 🔄 **Scenario Templates** - Pre-built templates for common scenarios
- 📱 **Mobile App** - Native mobile application
- 🌐 **Multi-language Support** - Internationalization
- 🔗 **API Integrations** - Connect with security tools and platforms
- 📈 **Advanced Analytics** - Scenario effectiveness tracking
- 🎯 **Custom AI Models** - Fine-tuned models for specific industries

### Version 2.0 Goals
- **Collaborative Editing** - Real-time scenario collaboration
- **Advanced AI Features** - Custom model training
- **Enterprise Features** - SSO, RBAC, audit logs
- **API Marketplace** - Third-party integrations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Vue.js](https://vuejs.org/)
- UI components from [PrimeVue](https://primevue.org/)
- AI capabilities powered by [OpenAI](https://openai.com/) and [Anthropic](https://anthropic.com/)
- Icons from [Heroicons](https://heroicons.com/)

## Threat Modeling File Upload Feature

This feature provides AI-powered threat modeling analysis for cybersecurity systems. Users can upload diagram files or provide text descriptions of systems to generate comprehensive threat models using various frameworks.

### Supported File Types
- DRAWIO (.drawio) - Diagram files for system architecture
- PNG (.png) - Image files
- JPG (.jpg) - Image files  
- SVG (.svg) - Vector graphics
- XML (.xml) - XML-based diagrams

### File Size Limit
- Maximum file size: 10MB

### AI-Powered Threat Modeling
The system uses advanced AI models (OpenAI GPT and Anthropic Claude) to generate comprehensive threat models based on:

- **System descriptions** - Text-based descriptions of systems, architectures, or components
- **Uploaded diagrams** - Visual representations of system architecture
- **Multiple frameworks** - STRIDE, LINDDUN, PASTA, and Attack Trees analysis

### Generated Threat Models Include
1. **System Overview** - Brief description of the analyzed system
2. **Asset Identification** - Key assets, data, and components
3. **Threat Actors** - Potential attackers and their motivations
4. **Threat Analysis** - Detailed threats using the selected framework
5. **Risk Assessment** - Threat ratings (High/Medium/Low) based on likelihood and impact
6. **Mitigation Strategies** - Recommended controls and countermeasures
7. **Security Recommendations** - Overall security posture improvements

### API Endpoints
- `POST /api/threat-model/upload` — Upload a diagram file (multipart/form-data, field: `file`)
- `GET /api/threat-model/files` — List uploaded files
- `DELETE /api/threat-model/files/{file_id}` — Delete a file by its ID
- `POST /api/threat-model/generate` — Generate AI-powered threat model (synchronous)
- `POST /api/threat-model/generate-async` — Generate AI-powered threat model (asynchronous)
- `GET /api/threat-model/jobs/{job_id}` — Get async job status and progress
- `DELETE /api/threat-model/jobs/{job_id}` — Cancel an async job
- `GET /api/threat-model/jobs` — List recent jobs
- `POST /api/threat-model/estimate-cost` — Estimate costs across all AI providers
- `GET /api/threat-model/providers` — Get available AI providers

#### Example Async Threat Model Generation Request
```sh
curl -X POST "http://localhost:8000/api/threat-model/generate-async" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "A web application with user authentication and database storage",
    "framework": "STRIDE",
    "file_id": "optional-uploaded-file-id",
    "llm_provider": "openai"
  }'
```

#### Example Job Status Check
```sh
curl -X GET "http://localhost:8000/api/threat-model/jobs/{job_id}"
```

#### Example Threat Model Generation Request
```sh
curl -X POST "http://localhost:8000/api/threat-model/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "A web application with user authentication and database storage",
    "framework": "STRIDE",
    "file_id": "optional-uploaded-file-id",
    "llm_provider": "openai"
  }'
```

#### Example Cost Estimation Request
```sh
curl -X POST "http://localhost:8000/api/threat-model/estimate-cost" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "A cloud-based microservices application",
    "framework": "STRIDE",
    "llm_provider": "openai"
  }'
```

### Frontend Usage
- Use the "Threat Model Upload" button at the top of the app to switch to the threat modeling interface
- Upload supported diagram files for additional context (optional)
- Provide a detailed system description in the text area
- Select a threat modeling framework (STRIDE, LINDDUN, PASTA, Attack Trees)
- Choose an AI provider (OpenAI or Anthropic)
- Generate comprehensive threat models with cost estimation
- Export results in multiple formats (Text, Markdown, JSON, PDF)

### Features
- **Drag & Drop Upload** - Easy file upload with visual feedback
- **Multi-file Support** - Upload and manage multiple diagram files
- **Bulk Operations** - Select and delete multiple files at once
- **Progress Tracking** - Real-time upload progress indicators
- **Cost Comparison** - Compare costs across different AI providers
- **Export Options** - Download threat models in various formats
- **Form Validation** - Real-time validation and error handling
- **Async Processing** - Background job processing for complex analyses
- **Progress Monitoring** - Real-time job status and progress tracking
- **Result Caching** - Automatic caching to avoid regenerating similar models
- **Job Management** - View, cancel, and manage async generation jobs
- **Dual Generation Modes** - Choose between synchronous and asynchronous processing
- **Visual Threat Modeling** - Interactive diagram-based threat modeling
- **Component Library** - Pre-built components for common system elements
- **Threat Mapping** - Visual threat assignment to system components
- **Advanced Export** - Professional PDF reports and executive summaries
- **Compliance Reports** - Framework-specific compliance analysis
- **Custom Templates** - Configurable export templates and formats

---

<div align="center">
Made with ❤️ by the ThreatForge team
</div>

## 📚 Documentation

### User Guides
- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Threat Modeling User Guide](docs/THREAT_MODELING_GUIDE.md)** - Comprehensive guide to threat modeling
- **[Best Practices](docs/BEST_PRACTICES.md)** - Best practices for effective threat modeling
- **[Sample Threat Models](docs/sample_threat_models.md)** - Examples and templates

### Features Overview

#### 🤖 AI-Powered Threat Modeling
- **Multiple Frameworks**: STRIDE, LINDDUN, PASTA, Attack Trees
- **AI Providers**: OpenAI GPT and Anthropic Claude integration
- **Async Processing**: Background job processing with progress tracking
- **Intelligent Caching**: Automatic result caching for similar requests

#### 🎨 Visual Threat Modeling
- **Interactive Diagrams**: Drag-and-drop system component creation
- **Component Library**: Pre-built components for common system elements
- **Threat Mapping**: Visual threat assignment to system components
- **Real-time Collaboration**: Multi-user threat modeling sessions
- **Diagram Export**: Export diagrams in multiple formats

#### 📊 Advanced Export Options
- **PDF Reports**: Professional PDF reports with executive summaries
- **Executive Summaries**: High-level summaries for stakeholders
- **Technical Reports**: Detailed technical analysis for security teams
- **Compliance Reports**: Compliance-focused reports with controls mapping
- **Custom Templates**: Configurable export templates and formats

#### 🔄 Workflow Integration
- **File Upload**: Support for DRAWIO, PNG, JPG, SVG, XML diagrams
- **Job Monitoring**: Real-time tracking of async threat model generation
- **Cost Comparison**: Compare costs across different AI providers
- **Export Integration**: Export to various formats and platforms

### API Documentation
- **Threat Modeling API**: `POST /api/threat-model/generate`, `POST /api/threat-model/generate-async`
- **File Management**: `POST /api/threat-model/upload`, `GET /api/threat-model/files`, `DELETE /api/threat-model/files/clear`
- **Job Management**: `GET /api/threat-model/jobs/{job_id}`, `DELETE /api/threat-model/jobs/{job_id}`
- **Cost Estimation**: `POST /api/threat-model/estimate-cost`
- **Provider Information**: `GET /api/threat-model/providers`

### Interactive Features
- **Built-in Tutorial**: Click the "Tutorial" button in the threat modeling interface
- **Visual Modeling**: Switch between text-based and visual threat modeling
- **Real-time Job Monitoring**: Track async threat model generation progress
- **Cost Comparison**: Compare costs across different AI providers
- **Advanced Export**: Generate professional reports in multiple formats

---
