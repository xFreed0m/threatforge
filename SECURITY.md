# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

**Note:** We recommend always using the latest stable release for the best security posture.

## Reporting a Vulnerability

The ThreatForge team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report Security Issues

**For security vulnerabilities, please create a public issue** with the following information:

1. **Create a GitHub Issue**: [Report Security Issue](https://github.com/xfreed0m/threatforge/issues/new?assignees=&labels=security&template=&title=%5BSECURITY%5D+)

2. **Use the `[SECURITY]` prefix** in your issue title

3. **Include the following information**:
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Versions affected
   - Any potential impact assessment
   - Suggested fix (if you have one)

### What to Include in Your Report

Please provide as much information as possible to help us understand and resolve the issue:

**Required Information:**
- **Vulnerability Type**: What kind of vulnerability is it? (e.g., XSS, SQL injection, authentication bypass)
- **Impact**: What is the potential impact of this vulnerability?
- **Affected Components**: Which parts of ThreatForge are affected?
- **Reproduction Steps**: Clear steps to reproduce the vulnerability
- **Affected Versions**: Which versions of ThreatForge are affected?

**Additional Helpful Information:**
- Screenshots or video demonstrations
- Proof-of-concept code (if applicable)
- Suggested remediation
- References to similar vulnerabilities or security best practices

### Response Timeline

We aim to respond to security reports according to the following timeline:

- **Initial Response**: Within 48 hours of issue creation
- **Vulnerability Assessment**: Within 1 week
- **Fix Development**: Depends on complexity, but we prioritize security issues
- **Fix Release**: Critical vulnerabilities will be released as soon as possible

### Security Update Process

1. **Triage**: We'll assess the vulnerability and determine its severity
2. **Fix Development**: Our team will develop and test a fix
3. **Release**: We'll release the fix and notify users through:
   - GitHub release notes
   - Issue updates
   - Security advisories (for critical vulnerabilities)

## Security Best Practices for Users

As a threat modeling and security scenario generation tool, ThreatForge handles sensitive security information. Please follow these best practices:

### For Users
- **Keep Updated**: Always use the latest version of ThreatForge
- **Secure Configuration**: Follow the configuration guidelines in our documentation
- **Access Control**: Limit access to ThreatForge instances to authorized personnel only
- **Data Handling**: Be cautious with sensitive threat intelligence data
- **Environment Security**: Ensure your deployment environment follows security best practices

### For Contributors
- **Secure Development**: Follow secure coding practices
- **Dependency Management**: Keep dependencies updated and monitor for vulnerabilities
- **Code Review**: All code changes undergo security-focused review
- **Testing**: Include security tests for new features
- **Documentation**: Document security implications of new features

## Security Features

ThreatForge implements several security measures:

- **Input Validation**: All user inputs are validated and sanitized
- **Authentication**: Secure authentication mechanisms (when implemented)
- **Authorization**: Role-based access controls (when implemented)
- **Logging**: Security events are logged for audit purposes
- **Dependencies**: Regular dependency updates and vulnerability scanning

## Scope

This security policy covers:

- **ThreatForge Core Application**: Backend API and frontend interface
- **Dependencies**: Third-party libraries and packages
- **Configuration**: Default configurations and deployment recommendations
- **Documentation**: Security-related documentation and examples

**Out of Scope:**
- Third-party integrations or plugins not maintained by the ThreatForge team
- User-specific configurations that deviate from recommended practices
- Infrastructure security (this is the responsibility of the deploying organization)

## Recognition

We value the security community's efforts in making ThreatForge more secure. Contributors who report valid security vulnerabilities will be:

- **Acknowledged** in our security advisories (with permission)
- **Listed** in our contributors documentation
- **Credited** in release notes for security fixes

## Contact

For questions about this security policy or ThreatForge security in general:

- **GitHub Issues**: [Create an issue](https://github.com/xfreed0m/threatforge/issues)
- **Security Issues**: [Report Security Issue](https://github.com/xfreed0m/threatforge/issues/new?assignees=&labels=security&template=&title=%5BSECURITY%5D+)
- **General Questions**: Use our [GitHub Discussions](https://github.com/xfreed0m/threatforge/discussions)

## Legal

By reporting security vulnerabilities, you agree that:

- You will not publicly disclose the vulnerability until we have had a reasonable opportunity to address it
- You will not access or modify data that does not belong to you
- You will not perform testing that could harm ThreatForge or its users
- Your testing is limited to your own systems or systems you have explicit permission to test

Thank you for helping keep ThreatForge and our users safe!

---

**Last Updated**: July 2025 