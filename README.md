# 🔥 ThreatForge

[![GitHub stars](https://img.shields.io/github/stars/yourusername/threatforge?style=social)](https://github.com/yourusername/threatforge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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

## 🧪 Testing

### Backend Tests
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

## 📞 Support

- 📧 Email: support@threatforge.dev
- 💬 Discord: [Join our community](https://discord.gg/threatforge)
- 🐛 Issues: [GitHub Issues](https://github.com/xFreed0m/threatforge/issues)
- 📖 Documentation: [Wiki](https://github.com/xFreed0m/threatforge/wiki)

---

<div align="center">
Made with ❤️ by the ThreatForge team
</div>
