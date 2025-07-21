# Contributing to ThreatForge

Thank you for your interest in contributing to ThreatForge! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+ 
- Node.js 16+
- Docker and Docker Compose
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/threatforge.git
   cd threatforge
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/xfreed0m/threatforge.git
   ```

## Development Setup

### Using Docker (Recommended)

For development with hot reloading:
```bash
docker-compose -f docker-compose.dev.yml up
```

For production-like environment:
```bash
docker-compose -f docker-compose.prod.yml up
```

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

#### Running the Application
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## Development Workflow

1. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our code standards

3. **Test your changes** thoroughly

4. **Commit your changes** with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add new scenario generation feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** from your fork to the main repository

### Commit Message Convention

We follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Code Standards

### Python (Backend)

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

#### Code Formatting
```bash
# Install development dependencies
pip install black isort flake8

# Format code
black .
isort .

# Check for style issues
flake8
```

### JavaScript/Vue.js (Frontend)

- Follow Vue.js style guide
- Use ES6+ features
- Use meaningful component and variable names
- Write JSDoc comments for complex functions
- Use Vue 3 Composition API for new components

#### Code Formatting
```bash
# Format code
npm run lint:fix
```

### General Guidelines

- Write self-documenting code
- Keep functions small and focused
- Use consistent naming conventions
- Add comments for complex business logic
- Remove unused imports and variables

## Testing

### Backend Testing

Run tests using pytest:
```bash
cd backend
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Frontend Testing

Run unit tests:
```bash
cd frontend
npm run test:unit
```

Run tests with coverage:
```bash
npm run test:coverage
```

### Testing Guidelines

- Write tests for new features and bug fixes
- Maintain or improve test coverage
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies appropriately

## Pull Request Process

1. **Ensure your code follows our standards** and passes all tests
2. **Update documentation** if needed
3. **Fill out the PR template** completely
4. **Request review** from maintainers
5. **Address feedback** promptly and professionally
6. **Squash commits** if requested before merging

### PR Requirements

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if necessary
- [ ] PR description clearly explains changes
- [ ] Breaking changes are documented

## Issue Reporting

When reporting issues, please include:

### Bug Reports
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, browser, versions)
- Screenshots or error logs if applicable

### Feature Requests
- Clear description of the desired feature
- Use case and motivation
- Proposed implementation approach (optional)
- Any breaking changes considerations

## Security Issues

If you discover a security vulnerability, please:
1. Create a public issue
2. Allow time for the issue to be addressed

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing others' private information
- Inappropriate sexual content or advances
- Other conduct that would be inappropriate in a professional setting

## Getting Help

- Check existing [issues](../../issues) and [discussions](../../discussions)
- Join our community chat [link if available]
- Ask questions in GitHub Discussions
- Contact maintainers directly for urgent matters

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Project documentation

Thank you for contributing to ThreatForge! 🚀 