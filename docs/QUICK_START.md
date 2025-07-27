# ThreatForge Quick Start Guide

Get up and running with AI-powered threat modeling in 5 minutes! 🚀

## Prerequisites

- ✅ ThreatForge application running
- ✅ Basic understanding of your system
- ✅ (Optional) System architecture diagrams

## Quick Start Steps

### 1. Navigate to Threat Modeling
Click the **"Threat Model Upload"** button in the main interface to access the threat modeling feature.

### 2. Start the Tutorial (Recommended)
Click the **"Tutorial"** button to get an interactive walkthrough of the threat modeling process.

### 3. Describe Your System
In the **System Description** field, provide a comprehensive overview of your system:

```
Example:
Our web application allows users to:
- Register and login with email/password
- View and edit their profile
- Upload and download files
- Make payments with credit cards

The system uses:
- React frontend with Node.js backend
- PostgreSQL database
- AWS S3 for file storage
- Stripe for payments
```

### 4. Choose Your Framework
Select the appropriate threat modeling framework:

- **STRIDE** - General security threats (recommended for beginners)
- **LINDDUN** - Privacy-focused analysis
- **PASTA** - Business context and risk
- **Attack Trees** - Detailed attack scenarios

### 5. Select AI Provider
Choose between available AI providers:
- **OpenAI** - Fast processing, good for general analysis
- **Anthropic** - More detailed analysis, better for complex systems

### 6. Choose Processing Mode
- **Sync Mode** - Immediate results (good for simple systems)
- **Async Mode** - Background processing with progress tracking (good for complex systems)

### 7. Generate Your Threat Model
Click **"Generate Threat Model"** and wait for the AI analysis to complete.

### 8. Review Results
The generated threat model will include:
- System overview and asset identification
- Threat actors and attack vectors
- Risk assessment (High/Medium/Low)
- Mitigation strategies and recommendations

## What You'll Get

Your threat model will provide:

### 📋 System Overview
Summary of your analyzed system and its components

### 🎯 Threat Analysis
Detailed threats organized by your chosen framework:
- **STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- **LINDDUN**: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance
- **PASTA**: Business context, attack vectors, threat intelligence, risk assessment, attack simulation
- **Attack Trees**: Hierarchical attack scenarios and paths

### 📊 Risk Assessment
Each threat rated by:
- **High Risk**: Require immediate attention
- **Medium Risk**: Should be addressed in near term
- **Low Risk**: Monitor and address as resources allow

### 🛡️ Mitigation Strategies
Recommended security controls and countermeasures for each threat

### 📈 Security Recommendations
Overall security posture improvements and best practices

## Pro Tips

### For Better Results:
1. **Be Specific**: Include details about technologies, data types, and user roles
2. **Upload Diagrams**: Add system architecture diagrams for enhanced analysis
3. **Use Async Mode**: For complex systems to avoid timeouts
4. **Try Different Frameworks**: Get different perspectives on your system
5. **Review and Refine**: Update your description based on initial results

### Example System Descriptions:

**E-commerce Platform:**
```
Our e-commerce site allows customers to browse products, create accounts, add items to cart, complete purchases with credit cards, track orders, and contact support. Uses React frontend, Node.js backend, PostgreSQL database, Redis sessions, AWS S3 for images, and Stripe for payments.
```

**Healthcare Application:**
```
Our healthcare platform processes patient data including health records, test results, diagnoses, prescriptions, insurance info, and appointments. Users include patients, doctors, nurses, and admins. Uses Angular frontend, Java Spring Boot backend, Oracle database with encryption, HIPAA-compliant storage, and multi-factor authentication.
```

**Banking API:**
```
Our banking API provides account balances, transaction history, fund transfers, bill payments, credit card management, investment access, and loan applications. Security features include OAuth 2.0 authentication, API rate limiting, transaction monitoring, fraud detection, encrypted transmission, and multi-factor authentication.
```

## Next Steps

After generating your threat model:

1. **Review Threats**: Carefully examine each identified threat
2. **Prioritize**: Focus on high-risk threats first
3. **Implement Controls**: Put recommended mitigations into practice
4. **Monitor**: Set up monitoring for identified attack vectors
5. **Update**: Refresh your threat model as your system evolves
6. **Train Team**: Share results with your development and security teams

## Getting Help

- **Tutorial**: Use the built-in tutorial for step-by-step guidance
- **Documentation**: Check the full [Threat Modeling Guide](THREAT_MODELING_GUIDE.md)
- **Examples**: Review [Sample Threat Models](sample_threat_models.md)
- **Support**: Contact your system administrator for technical assistance

## Common Issues

**"No AI providers available"**
- Check that API keys are configured in the backend

**"Generation failed"**
- Try with a simpler system description
- Check that your description is comprehensive enough

**"Job stuck in processing"**
- Use sync mode for simpler systems
- Wait for async jobs to complete (can take several minutes)

**"Poor quality results"**
- Provide more detailed system descriptions
- Upload relevant architecture diagrams
- Try different frameworks for different perspectives

---

**Ready to start?** Click the "Threat Model Upload" button and begin your first threat model! 🛡️ 