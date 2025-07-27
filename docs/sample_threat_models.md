# Sample Threat Models

This document provides sample threat models for different types of systems to help you understand the expected output format and quality.

## Sample 1: E-commerce Web Application (STRIDE Framework)

### System Description
```
Our e-commerce platform allows customers to browse products, create accounts, add items to cart, complete purchases with credit card payments, track orders, and contact customer support. The system uses React frontend, Node.js backend, PostgreSQL database, Redis for sessions, AWS S3 for images, Stripe for payments, and Docker containers on AWS ECS.
```

### Generated Threat Model

**System Overview**
The e-commerce platform is a web-based application that handles customer transactions, user data, and payment processing. The system consists of a React frontend, Node.js backend API, PostgreSQL database, Redis session management, AWS S3 file storage, and Stripe payment processing.

**Asset Identification**
- Customer personal data (names, emails, addresses)
- Payment information (credit card data via Stripe)
- Product catalog and inventory data
- Order history and transaction records
- User authentication credentials
- Session data and user preferences
- Product images and media files

**Threat Actors**
- Cybercriminals seeking financial gain
- Competitors attempting corporate espionage
- Disgruntled employees with insider access
- Script kiddies testing vulnerabilities
- Organized crime groups targeting payment data

**Threat Analysis (STRIDE Framework)**

**Spoofing Threats:**
- **High Risk**: Attackers could create fake login pages to steal user credentials
- **Medium Risk**: Email spoofing to trick users into revealing sensitive information
- **Mitigation**: Implement multi-factor authentication, use HTTPS, validate email domains

**Tampering Threats:**
- **High Risk**: Unauthorized modification of order data or product prices
- **Medium Risk**: Manipulation of session data to gain elevated privileges
- **Mitigation**: Input validation, data integrity checks, secure session management

**Repudiation Threats:**
- **Medium Risk**: Users denying they placed orders or made payments
- **Low Risk**: System administrators denying they made configuration changes
- **Mitigation**: Comprehensive audit logging, digital signatures, transaction receipts

**Information Disclosure Threats:**
- **High Risk**: Unauthorized access to customer personal and payment data
- **Medium Risk**: Exposure of internal system configuration and API endpoints
- **Mitigation**: Data encryption, access controls, API security, secure headers

**Denial of Service Threats:**
- **Medium Risk**: DDoS attacks targeting the web application
- **Low Risk**: Database connection exhaustion attacks
- **Mitigation**: DDoS protection, rate limiting, resource monitoring, CDN usage

**Elevation of Privilege Threats:**
- **High Risk**: Regular users gaining administrative access
- **Medium Risk**: API users accessing unauthorized resources
- **Mitigation**: Role-based access control, API authentication, privilege separation

**Risk Assessment**
- **High Risk Threats**: 4 identified (require immediate attention)
- **Medium Risk Threats**: 8 identified (should be addressed in near term)
- **Low Risk Threats**: 2 identified (monitor and address as resources allow)

**Mitigation Strategies**
1. Implement comprehensive authentication and authorization
2. Use HTTPS for all communications
3. Encrypt sensitive data at rest and in transit
4. Implement input validation and output encoding
5. Set up monitoring and alerting systems
6. Regular security testing and penetration testing
7. Employee security training and awareness

**Security Recommendations**
- Conduct regular security assessments
- Implement a bug bounty program
- Use security headers and CSP policies
- Regular dependency updates and vulnerability scanning
- Implement automated security testing in CI/CD pipeline
- Create incident response plan and procedures

---

## Sample 2: Healthcare Data Platform (LINDDUN Framework)

### System Description
```
Our healthcare platform processes patient data including personal health records, medical test results, diagnoses, prescriptions, insurance information, and appointment data. Users include patients, doctors, nurses, and administrators. The system uses Angular frontend, Java Spring Boot backend, Oracle database with encryption, HIPAA-compliant storage, multi-factor authentication, and audit logging.
```

### Generated Threat Model

**System Overview**
The healthcare platform is a critical system that handles sensitive patient health information, medical records, and healthcare operations. The system serves multiple user types including patients, healthcare providers, and administrative staff.

**Asset Identification**
- Patient personal health records (PHR)
- Medical test results and diagnostic data
- Prescription and medication information
- Insurance and billing data
- Appointment scheduling information
- Healthcare provider credentials
- Audit logs and access records

**Threat Actors**
- Healthcare data thieves seeking to sell medical information
- Insiders with legitimate access but malicious intent
- Competitors attempting to gain business intelligence
- Hackers targeting healthcare systems for ransom
- Nation-state actors seeking medical intelligence

**Threat Analysis (LINDDUN Framework)**

**Linkability Threats:**
- **High Risk**: Ability to link patient data across different visits or providers
- **Medium Risk**: Correlation of patient activities across system modules
- **Mitigation**: Data anonymization, access controls, audit logging

**Identifiability Threats:**
- **High Risk**: Direct identification of patients from stored data
- **Medium Risk**: Indirect identification through data combination
- **Mitigation**: Data minimization, pseudonymization, access restrictions

**Non-repudiation Threats:**
- **Medium Risk**: Users denying they accessed or modified patient records
- **Low Risk**: System denying it processed certain transactions
- **Mitigation**: Comprehensive audit trails, digital signatures, access logging

**Detectability Threats:**
- **Medium Risk**: Unauthorized access going undetected
- **Low Risk**: Data breaches not being discovered promptly
- **Mitigation**: Real-time monitoring, intrusion detection, alerting systems

**Disclosure of Information Threats:**
- **High Risk**: Unauthorized disclosure of patient health information
- **Medium Risk**: Accidental exposure of sensitive data
- **Mitigation**: Data encryption, access controls, training, secure disposal

**Unawareness Threats:**
- **Medium Risk**: Users unaware of data collection and usage
- **Low Risk**: Patients not understanding their privacy rights
- **Mitigation**: Clear privacy policies, user consent, transparency

**Non-compliance Threats:**
- **High Risk**: Violation of HIPAA regulations and requirements
- **Medium Risk**: Non-compliance with state privacy laws
- **Mitigation**: Regular compliance audits, policy enforcement, training

**Risk Assessment**
- **High Risk Threats**: 4 identified (critical for HIPAA compliance)
- **Medium Risk Threats**: 6 identified (important for patient privacy)
- **Low Risk Threats**: 2 identified (should be addressed)

**Mitigation Strategies**
1. Implement HIPAA-compliant data handling procedures
2. Use strong encryption for data at rest and in transit
3. Implement role-based access controls with least privilege
4. Regular security training for all staff
5. Comprehensive audit logging and monitoring
6. Data backup and disaster recovery procedures
7. Regular security assessments and penetration testing

**Security Recommendations**
- Conduct regular HIPAA compliance audits
- Implement data loss prevention (DLP) solutions
- Use multi-factor authentication for all users
- Regular security awareness training
- Implement automated compliance monitoring
- Create incident response plan for data breaches
- Regular vulnerability assessments and patching

---

## Sample 3: Banking API (PASTA Framework)

### System Description
```
Our banking API provides account balance and transaction history, fund transfers between accounts, bill payments, credit card management, investment portfolio access, and loan applications. Security features include OAuth 2.0 authentication, API rate limiting, transaction monitoring, fraud detection, encrypted data transmission, and multi-factor authentication.
```

### Generated Threat Model

**System Overview**
The banking API is a critical financial system that handles customer accounts, transactions, and financial data. The system provides secure access to banking services through authenticated API endpoints with comprehensive security controls.

**Asset Identification**
- Customer account information and balances
- Transaction history and financial records
- Payment and transfer data
- Credit card and loan information
- Investment portfolio data
- Authentication credentials and tokens
- Audit logs and compliance records

**Threat Actors**
- Financial cybercriminals seeking monetary gain
- Organized crime groups targeting banking systems
- Nation-state actors seeking financial intelligence
- Insiders with access to financial data
- Competitors attempting to gain business intelligence

**Threat Analysis (PASTA Framework)**

**Business Context Threats:**
- **High Risk**: Regulatory non-compliance leading to fines and penalties
- **Medium Risk**: Reputation damage from security incidents
- **Mitigation**: Regular compliance audits, security governance, risk management

**Attack Vector Analysis:**
- **High Risk**: API endpoint exploitation and abuse
- **Medium Risk**: Authentication bypass and session hijacking
- **Mitigation**: API security, rate limiting, authentication controls

**Threat Intelligence:**
- **High Risk**: Known banking malware and attack patterns
- **Medium Risk**: Emerging threats targeting financial institutions
- **Mitigation**: Threat intelligence feeds, security monitoring, incident response

**Risk Assessment:**
- **High Risk**: Financial fraud and unauthorized transactions
- **Medium Risk**: Data breaches and information disclosure
- **Mitigation**: Fraud detection, monitoring, security controls

**Attack Simulation:**
- **High Risk**: Automated attacks on API endpoints
- **Medium Risk**: Social engineering targeting bank employees
- **Mitigation**: Penetration testing, security training, monitoring

**Risk Assessment**
- **High Risk Threats**: 5 identified (critical for financial security)
- **Medium Risk Threats**: 4 identified (important for compliance)
- **Low Risk Threats**: 1 identified (should be monitored)

**Mitigation Strategies**
1. Implement comprehensive fraud detection and prevention
2. Use strong authentication and authorization controls
3. Regular security testing and penetration testing
4. Implement transaction monitoring and anomaly detection
5. Use encryption for all sensitive data
6. Regular compliance audits and reporting
7. Comprehensive incident response procedures

**Security Recommendations**
- Implement real-time fraud detection systems
- Use behavioral analytics for anomaly detection
- Regular security assessments and penetration testing
- Implement comprehensive logging and monitoring
- Regular security training for all staff
- Create incident response plan for financial crimes
- Regular regulatory compliance audits

---

## Template: Custom System Threat Model

### System Description Template
```
[Your system name] is a [type of application] that allows users to:
- [Primary function 1]
- [Primary function 2]
- [Primary function 3]
- [Primary function 4]

The system uses:
- [Frontend technology]
- [Backend technology]
- [Database technology]
- [Other key technologies]
- [Security features]
```

### Threat Model Structure Template

**System Overview**
[Brief description of the system and its purpose]

**Asset Identification**
- [Asset 1]: [Description]
- [Asset 2]: [Description]
- [Asset 3]: [Description]

**Threat Actors**
- [Actor 1]: [Motivation]
- [Actor 2]: [Motivation]
- [Actor 3]: [Motivation]

**Threat Analysis ([Framework])**
[Framework-specific threat categories with risk levels and mitigations]

**Risk Assessment**
- **High Risk Threats**: [Number] identified
- **Medium Risk Threats**: [Number] identified
- **Low Risk Threats**: [Number] identified

**Mitigation Strategies**
1. [Strategy 1]
2. [Strategy 2]
3. [Strategy 3]
4. [Strategy 4]

**Security Recommendations**
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

---

## Best Practices for Using Samples

1. **Customize for Your System**: Use these samples as starting points, but customize them for your specific system
2. **Update Regularly**: Threat models should be updated as systems evolve
3. **Validate Results**: Have security experts review and validate AI-generated threats
4. **Implement Mitigations**: Don't just document threats - implement the recommended mitigations
5. **Monitor and Review**: Regularly review threat models and update based on new threats

## Next Steps

1. **Start with a Sample**: Use one of these samples as a template for your system
2. **Customize the Description**: Modify the system description to match your application
3. **Choose Appropriate Framework**: Select the framework that best fits your use case
4. **Generate Your Threat Model**: Use ThreatForge to generate a custom threat model
5. **Review and Refine**: Review the results and refine your system description if needed
6. **Implement Recommendations**: Put the security recommendations into practice 