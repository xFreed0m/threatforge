# ThreatForge Threat Modeling User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Understanding Threat Modeling](#understanding-threat-modeling)
4. [Using the Threat Modeling Interface](#using-the-threat-modeling-interface)
5. [File Upload and Management](#file-upload-and-management)
6. [AI-Powered Generation](#ai-powered-generation)
7. [Async vs Sync Processing](#async-vs-sync-processing)
8. [Job Monitoring](#job-monitoring)
9. [Best Practices](#best-practices)
10. [Examples and Templates](#examples-and-templates)
11. [Troubleshooting](#troubleshooting)

## Introduction

ThreatForge's AI-powered threat modeling feature helps security professionals and developers create comprehensive threat models for their systems. Using advanced AI models (OpenAI GPT and Anthropic Claude), the system analyzes your system descriptions and diagrams to identify potential security threats and provide mitigation strategies.

### What is Threat Modeling?

Threat modeling is a systematic approach to identifying, quantifying, and addressing security risks in software systems. It helps you:

- **Identify potential threats** to your system
- **Understand attack vectors** and vulnerabilities
- **Prioritize security controls** based on risk
- **Document security requirements** for development teams
- **Comply with security standards** and regulations

### Supported Frameworks

ThreatForge supports multiple threat modeling frameworks:

- **STRIDE**: Microsoft's framework for identifying threats (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
- **LINDDUN**: Privacy-focused threat modeling (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance)
- **PASTA**: Process for Attack Simulation and Threat Analysis
- **Attack Trees**: Hierarchical representation of attack scenarios

## Getting Started

### Prerequisites

1. **Access to ThreatForge**: Ensure you have access to the ThreatForge application
2. **System Knowledge**: Have a good understanding of the system you want to analyze
3. **Diagrams (Optional)**: Prepare system architecture diagrams if available

### Quick Start

1. **Navigate to Threat Modeling**: Click the "Threat Model Upload" button in the main interface
2. **Describe Your System**: Provide a detailed description of your system in the text area
3. **Select Framework**: Choose the appropriate threat modeling framework
4. **Choose AI Provider**: Select between OpenAI or Anthropic for analysis
5. **Generate Threat Model**: Click "Generate Threat Model" to start the analysis

## Understanding Threat Modeling

### Key Concepts

**Assets**: Valuable components of your system (data, services, infrastructure)
**Threat Actors**: Potential attackers (hackers, insiders, competitors)
**Attack Vectors**: Methods attackers use to exploit vulnerabilities
**Risk Assessment**: Evaluation of threat likelihood and impact
**Mitigation Strategies**: Controls and countermeasures to reduce risk

### Framework Comparison

| Framework | Focus | Best For | Key Benefits |
|-----------|-------|----------|--------------|
| **STRIDE** | General security threats | Software applications | Comprehensive coverage, Microsoft standard |
| **LINDDUN** | Privacy and data protection | Systems handling personal data | Privacy-focused, GDPR compliance |
| **PASTA** | Business context and risk | Enterprise systems | Business-aligned, risk-based approach |
| **Attack Trees** | Specific attack scenarios | Critical systems | Detailed analysis, attack path mapping |

## Using the Threat Modeling Interface

### Main Interface Components

1. **System Description**: Text area for describing your system
2. **Framework Selection**: Dropdown to choose threat modeling framework
3. **File Upload**: Optional diagram upload for additional context
4. **AI Provider**: Selection between OpenAI and Anthropic
5. **Generation Mode**: Toggle between sync and async processing
6. **Job Monitor**: Real-time tracking of async jobs

### Step-by-Step Process

#### Step 1: System Description
Provide a comprehensive description of your system:

**Good Example:**
```
Our web application is a customer portal that allows users to:
- Register and authenticate using email/password
- View and update their profile information
- Upload and download documents (PDF, images)
- Make payments using credit cards
- Access support tickets and chat with agents

The system uses:
- React frontend with Node.js backend
- PostgreSQL database for user data
- AWS S3 for file storage
- Stripe for payment processing
- Redis for session management
- Docker containers deployed on AWS ECS
```

**Poor Example:**
```
A website for customers.
```

#### Step 2: Framework Selection
Choose the framework based on your needs:

- **STRIDE**: For general security analysis
- **LINDDUN**: For privacy-focused systems
- **PASTA**: For business-critical applications
- **Attack Trees**: For detailed attack scenario analysis

#### Step 3: File Upload (Optional)
Upload system diagrams for enhanced analysis:

**Supported Formats:**
- **DRAWIO**: System architecture diagrams
- **PNG/JPG**: Screenshots and flowcharts
- **SVG**: Vector graphics
- **XML**: Structured diagrams

**Tips for Effective Diagrams:**
- Include data flow between components
- Show external interfaces and APIs
- Highlight sensitive data storage
- Include authentication and authorization points

#### Step 4: AI Provider Selection
Choose between available AI providers:

- **OpenAI**: Fast processing, good for general analysis
- **Anthropic**: More detailed analysis, better for complex systems

#### Step 5: Generation Mode
Select processing mode:

- **Sync Mode**: Immediate results, best for simple systems
- **Async Mode**: Background processing, best for complex analyses

## File Upload and Management

### Uploading Files

1. **Drag and Drop**: Simply drag files onto the upload area
2. **Click to Select**: Click the upload area to browse files
3. **Multiple Files**: Select multiple files at once
4. **Progress Tracking**: Monitor upload progress in real-time

### File Management

- **View Files**: See all uploaded files in the list
- **Delete Files**: Remove individual files or bulk delete
- **File Information**: View file type, size, and upload date
- **Reuse Files**: Select uploaded files for new analyses

### Best Practices for Diagrams

1. **Keep it Simple**: Focus on key components and data flows
2. **Show Boundaries**: Clearly indicate system boundaries
3. **Include Context**: Show external systems and interfaces
4. **Highlight Security**: Mark authentication and authorization points
5. **Data Classification**: Indicate sensitive data types

## AI-Powered Generation

### How AI Analysis Works

1. **Content Analysis**: AI analyzes your system description and diagrams
2. **Threat Identification**: Identifies potential threats using the selected framework
3. **Risk Assessment**: Evaluates likelihood and impact of each threat
4. **Mitigation Strategies**: Suggests controls and countermeasures
5. **Comprehensive Report**: Generates a detailed threat model document

### Understanding AI Output

The generated threat model includes:

1. **System Overview**: Summary of the analyzed system
2. **Asset Identification**: Key assets and components
3. **Threat Actors**: Potential attackers and motivations
4. **Threat Analysis**: Detailed threats with framework-specific categories
5. **Risk Assessment**: Threat ratings (High/Medium/Low)
6. **Mitigation Strategies**: Recommended security controls
7. **Security Recommendations**: Overall security improvements

### Interpreting Results

**High Risk Threats**: Require immediate attention and mitigation
**Medium Risk Threats**: Should be addressed in the near term
**Low Risk Threats**: Monitor and address as resources allow

## Async vs Sync Processing

### When to Use Sync Mode

- **Simple Systems**: Basic applications with few components
- **Quick Analysis**: Need results immediately
- **Testing**: Trying different parameters or frameworks
- **Small Diagrams**: Simple architecture diagrams

### When to Use Async Mode

- **Complex Systems**: Large applications with many components
- **Detailed Analysis**: Need comprehensive threat modeling
- **Large Diagrams**: Complex architecture diagrams
- **Background Processing**: Want to continue other work while processing

### Async Job Management

1. **Job Creation**: Submit async job and receive job ID
2. **Progress Monitoring**: Track job progress in real-time
3. **Status Updates**: Receive updates on processing stages
4. **Result Retrieval**: Access completed threat models
5. **Job Cancellation**: Cancel jobs if needed

## Job Monitoring

### Job Status Types

- **Pending**: Job created, waiting to start
- **Processing**: Job is actively running
- **Completed**: Job finished successfully
- **Failed**: Job encountered an error
- **Cancelled**: Job was cancelled by user

### Monitoring Features

- **Real-time Updates**: Automatic status refresh every 5 seconds
- **Progress Tracking**: Visual progress bars and percentages
- **Error Details**: Detailed error messages for failed jobs
- **Result Access**: Direct access to completed threat models
- **Job History**: View recent completed jobs

### Job Management Actions

- **View Status**: Check current job progress
- **Cancel Job**: Stop processing if needed
- **View Results**: Access completed threat models
- **Refresh**: Manually update job status
- **Cleanup**: Automatic cleanup of old jobs

## Best Practices

### System Description Best Practices

1. **Be Comprehensive**: Include all major components and data flows
2. **Include Context**: Describe external systems and interfaces
3. **Specify Technologies**: Mention specific technologies and platforms
4. **Highlight Security**: Describe authentication and authorization mechanisms
5. **Data Classification**: Indicate types of data handled

### Framework Selection Guidelines

- **STRIDE**: Use for general software applications
- **LINDDUN**: Use for systems handling personal or sensitive data
- **PASTA**: Use for business-critical enterprise systems
- **Attack Trees**: Use for systems requiring detailed attack analysis

### File Upload Best Practices

1. **Use Clear Diagrams**: Ensure diagrams are readable and well-organized
2. **Include Data Flows**: Show how data moves through the system
3. **Show Boundaries**: Clearly indicate system boundaries
4. **Highlight Security**: Mark authentication and authorization points
5. **Keep it Current**: Use up-to-date diagrams

### Analysis Best Practices

1. **Start Simple**: Begin with basic system descriptions
2. **Iterate**: Refine descriptions based on initial results
3. **Use Multiple Frameworks**: Try different frameworks for different perspectives
4. **Include Diagrams**: Upload diagrams for enhanced analysis
5. **Review Results**: Carefully review and validate AI-generated threats

### Risk Management

1. **Prioritize High-Risk Threats**: Focus on threats with high likelihood and impact
2. **Implement Controls**: Apply recommended mitigation strategies
3. **Monitor Progress**: Track implementation of security controls
4. **Regular Updates**: Update threat models as systems evolve
5. **Team Review**: Have security team review and validate results

## Examples and Templates

### Example 1: E-commerce Application

**System Description:**
```
Our e-commerce platform allows customers to:
- Browse products with search and filtering
- Create accounts with email verification
- Add items to shopping cart
- Complete purchases with credit card payments
- Track orders and view order history
- Contact customer support

Technical Stack:
- React frontend with TypeScript
- Node.js/Express backend API
- PostgreSQL database for products and orders
- Redis for session and cart management
- AWS S3 for product images
- Stripe for payment processing
- SendGrid for email notifications
- Docker containers on AWS ECS
```

**Recommended Framework:** STRIDE
**Processing Mode:** Async (complex system)

### Example 2: Healthcare Data Platform

**System Description:**
```
Our healthcare platform processes patient data including:
- Personal health records (PHR)
- Medical test results and diagnoses
- Prescription and medication data
- Insurance and billing information
- Appointment scheduling data

Users include patients, doctors, nurses, and administrators.

Technical Stack:
- Angular frontend
- Java Spring Boot backend
- Oracle database with encryption
- HIPAA-compliant data storage
- Multi-factor authentication
- Audit logging for all access
- API integrations with medical systems
```

**Recommended Framework:** LINDDUN
**Processing Mode:** Async (privacy-critical system)

### Example 3: Banking API

**System Description:**
```
Our banking API provides:
- Account balance and transaction history
- Fund transfers between accounts
- Bill payments and recurring payments
- Credit card management
- Investment portfolio access
- Loan applications and management

Security features:
- OAuth 2.0 authentication
- API rate limiting
- Transaction monitoring
- Fraud detection
- Encrypted data transmission
- Multi-factor authentication
```

**Recommended Framework:** PASTA
**Processing Mode:** Async (financial system)

## Troubleshooting

### Common Issues

#### Issue: "No LLM providers configured"
**Solution:** Ensure API keys are properly configured in the backend

#### Issue: "File upload failed"
**Solution:** Check file size (max 10MB) and format (supported types only)

#### Issue: "Job failed with error"
**Solution:** Check job error details and try with simpler system description

#### Issue: "Async job stuck in processing"
**Solution:** Wait for completion or cancel and retry with sync mode

#### Issue: "Poor quality threat model"
**Solution:** Provide more detailed system description and upload diagrams

### Performance Tips

1. **Use Async Mode**: For complex systems to avoid timeouts
2. **Optimize Descriptions**: Be comprehensive but concise
3. **Use Diagrams**: Upload relevant architecture diagrams
4. **Choose Right Framework**: Select appropriate framework for your use case
5. **Monitor Jobs**: Use job monitor for long-running analyses

### Getting Help

1. **Check Documentation**: Review this guide and README
2. **Test with Examples**: Try the provided examples
3. **Start Simple**: Begin with basic descriptions
4. **Iterate**: Refine based on results
5. **Contact Support**: Reach out for technical assistance

## Conclusion

ThreatForge's AI-powered threat modeling provides a powerful tool for identifying and addressing security risks in your systems. By following this guide and best practices, you can create comprehensive threat models that help protect your applications and data.

Remember to:
- Provide detailed system descriptions
- Choose appropriate frameworks
- Upload relevant diagrams
- Use async processing for complex systems
- Regularly update threat models
- Implement recommended mitigations

Happy threat modeling! 🛡️ 