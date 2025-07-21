#!/bin/bash

# ThreatForge Security Setup Script
# This script installs and configures security scanning tools

set -e

echo "🔒 Setting up ThreatForge Security Scanning..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f ".gitleaks.toml" ]; then
    print_error "Please run this script from the ThreatForge project root directory"
    exit 1
fi

print_status "Installing pre-commit hooks..."

# Install pre-commit
if command -v pip &> /dev/null; then
    pip install pre-commit
    pre-commit install
    print_status "Pre-commit hooks installed successfully"
else
    print_warning "pip not found. Please install pre-commit manually: pip install pre-commit"
fi

# Install GitLeaks
print_status "Installing GitLeaks..."

if command -v brew &> /dev/null; then
    # macOS
    brew install gitleaks
elif command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/install.sh | sh -s -- -b /usr/local/bin
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/install.sh | sh -s -- -b /usr/local/bin
else
    print_warning "Package manager not found. Please install GitLeaks manually from https://github.com/gitleaks/gitleaks"
fi

# Install TruffleHog
print_status "Installing TruffleHog..."

if command -v pip &> /dev/null; then
    pip install trufflehog
elif command -v brew &> /dev/null; then
    brew install trufflesecurity/trufflehog/trufflehog
else
    print_warning "Please install TruffleHog manually from https://github.com/trufflesecurity/trufflehog"
fi

# Test installations
print_status "Testing security tools..."

# Test GitLeaks
if command -v gitleaks &> /dev/null; then
    print_status "GitLeaks is installed"
    gitleaks version
else
    print_warning "GitLeaks not found in PATH"
fi

# Test TruffleHog
if command -v trufflehog &> /dev/null; then
    print_status "TruffleHog is installed"
    trufflehog --version
else
    print_warning "TruffleHog not found in PATH"
fi

# Test pre-commit
if command -v pre-commit &> /dev/null; then
    print_status "Pre-commit is installed"
    pre-commit --version
else
    print_warning "Pre-commit not found in PATH"
fi

# Run initial security scan
print_status "Running initial security scan..."

if command -v gitleaks &> /dev/null; then
    echo "Running GitLeaks scan..."
    gitleaks detect --config-path=.gitleaks.toml --verbose --source . || {
        print_warning "GitLeaks found potential issues. Please review the output above."
    }
else
    print_warning "Skipping GitLeaks scan (not installed)"
fi

if command -v trufflehog &> /dev/null; then
    echo "Running TruffleHog scan..."
    trufflehog --only-verified --fail . || {
        print_warning "TruffleHog found potential issues. Please review the output above."
    }
else
    print_warning "Skipping TruffleHog scan (not installed)"
fi

print_status "Security setup complete!"

echo ""
echo "🔒 Security Features Enabled:"
echo "  • Pre-commit hooks will run on every commit"
echo "  • GitLeaks will scan for secrets (no license required for personal repos)"
echo "  • TruffleHog will verify potential secrets"
echo "  • GitHub Actions will run security scans on PRs"
echo ""
echo "📋 Next Steps:"
echo "  1. Make sure your .env file is in .gitignore"
echo "  2. Never commit API keys or secrets"
echo "  3. Use .env.example for documentation"
echo "  4. Run 'pre-commit run --all-files' to test all hooks"
echo ""
echo "🛡️  Your repository is now protected against secret leaks!" 