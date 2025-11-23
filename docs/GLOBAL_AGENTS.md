# Global Agent Guide

This guide provides universal standards and best practices for all projects, ensuring consistency, quality, and maintainability across all development work.

## 📖 Global Documentation Standards

### Markdown Linting Rules

All markdown files must comply with strict linting standards to ensure consistency and readability. Follow these rules to maintain linting-free documentation:

#### Header Structure

- Use ATX-style headers (`#`, `##`, `###`) consistently
- Maintain proper header hierarchy (don't skip levels)
- Include a space between `#` and header text
- Keep headers under 80 characters when possible

#### Code Blocks

- Use fenced code blocks with language specification
- Include line numbers for code references when helpful
- Use inline code (`) for short code references
- Avoid HTML tags when markdown equivalents exist

#### Link Formatting

- Use reference-style links for repeated URLs
- Ensure all links have descriptive text
- Include file paths in links when referencing specific files
- Use absolute paths for cross-file references

#### List Formatting

- Use consistent list markers ( `-` for unordered, `1.` for ordered)
- Include blank lines before and after lists
- Maintain consistent indentation for nested lists
- Use trailing commas in list items when appropriate

#### Table Formatting

- Use consistent column alignment
- Include header separator lines with `|---|`
- Keep tables under 120 characters width when possible
- Use proper escaping for special characters in table cells

### Linting Tools Integration

#### markdownlint Configuration

Standard markdownlint rules to follow:

- MD001: Header levels should only increment by one level at a time
- MD003: Header style (ATX preferred)
- MD007: Unordered list indentation (2 spaces)
- MD013: Line length (120 characters max)
- MD022: Headers should be surrounded by blank lines
- MD024: Multiple headers with same content
- MD033: HTML allowed (minimal use)
- MD040: Fenced code blocks should have a language specified
- MD041: First line in file should be a top-level header

#### cSpell Configuration

- Use American English spelling consistently
- Add technical terms to project-specific dictionaries
- Verify proper nouns and brand names
- Check for commonly misspelled words

#### Handling Linting Errors

1. **Prevention**: Configure IDE extensions to show linting errors in real-time
2. **Validation**: Run linting tools before committing changes
3. **Correction**: Address all linting errors before merging
4. **Documentation**: Document any intentional rule exceptions

### Documentation Structure Standards

#### File Organization

- `README.md`: Project overview and quick start
- `CONTRIBUTING.md`: Contribution guidelines
- `CHANGELOG.md`: Version history and changes
- `LICENSE`: Legal information
- `docs/`: Additional documentation directory

#### Content Standards

- Include table of contents for files longer than 200 lines
- Use proper sectioning with descriptive headers
- Include code examples for complex concepts
- Provide troubleshooting sections for common issues

## 🔧 Code Quality Requirements

### General Standards

- Follow language-specific style guides (PEP 8 for Python, etc.)
- Use consistent naming conventions across projects
- Include type hints where language supports them
- Write self-documenting code with clear variable/function names

### Code Organization

- Separate concerns into logical modules/packages
- Use dependency injection patterns where appropriate
- Implement proper error handling and logging
- Follow SOLID principles for object-oriented design

### Documentation in Code

- Include docstrings for all public functions/classes
- Use inline comments for complex logic
- Document API endpoints with clear examples
- Maintain up-to-date type annotations

## 🧪 Testing Standards

### Test Coverage Requirements

- Minimum 80% code coverage for critical paths
- 100% coverage for security-related functions
- Test all public APIs and interfaces
- Include edge case and error condition testing

### Test Organization

- Separate unit, integration, and end-to-end tests
- Use descriptive test names that explain what is being tested
- Include setup and teardown methods for test isolation
- Mock external dependencies appropriately

### Test Documentation

- Include test documentation in README files
- Document test running procedures
- Provide test data fixtures and examples
- Document any test environment requirements

## 📋 Version Control Best Practices

### Commit Standards

- Use conventional commit messages (feat:, fix:, docs:, etc.)
- Keep commits focused on single logical changes
- Include issue references in commit messages
- Use present tense for commit messages

### Branch Strategy

- Use feature branches for new development
- Maintain clean main/master branch
- Use descriptive branch names
- Delete merged branches promptly

### Release Management

- Use semantic versioning (SemVer)
- Maintain CHANGELOG.md with version details
- Tag releases with version numbers
- Include release notes with breaking changes

## 🔄 Common Development Patterns

### Project Structure

```
project-name/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── config/                 # Configuration files
├── scripts/                # Build and utility scripts
├── requirements.txt        # Dependencies
├── README.md              # Project overview
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
└── LICENSE                # Legal information
```

### Configuration Management

- Use environment-specific configuration files
- Store secrets in environment variables or secure stores
- Include configuration validation
- Document all configuration options

### Error Handling

- Implement consistent error handling patterns
- Use appropriate HTTP status codes for APIs
- Include meaningful error messages
- Log errors with sufficient context

### Performance Considerations

- Implement caching strategies where appropriate
- Use efficient algorithms and data structures
- Monitor and optimize database queries
- Include performance testing in CI/CD

## 📝 Documentation Maintenance

### Regular Reviews

- Review and update documentation quarterly
- Verify code examples remain accurate
- Check all links and references
- Update version-specific information

### Contribution Guidelines

- Require documentation updates with feature changes
- Include documentation in code review process
- Use templates for consistent documentation
- Provide style guides for contributors

### Quality Assurance

- Run automated linting on all documentation
- Include documentation tests in CI/CD
- Use spell checking for all text content
- Validate code examples automatically

## 🛠️ Development Environment Setup

### Tooling Requirements

- Configure code formatting tools (prettier, black, etc.)
- Set up linting tools with consistent rules
- Use IDE extensions for real-time feedback
- Include pre-commit hooks for quality checks

### Dependency Management

- Use lock files for reproducible builds
- Regularly update dependencies
- Document security vulnerabilities
- Use semantic versioning for dependencies

## 📊 Metrics and Monitoring

### Code Quality Metrics

- Track code coverage over time
- Monitor code complexity metrics
- Measure documentation coverage
- Track bug fix turnaround time

### Documentation Metrics

- Monitor documentation freshness
- Track user engagement with documentation
- Measure documentation issue resolution time
- Analyze search patterns in documentation

## 🚀 Deployment and Release

### Documentation Deployment

- Automatically deploy documentation updates
- Use versioned documentation for releases
- Include deployment instructions
- Document rollback procedures

### Release Documentation

- Include release notes with all changes
- Document breaking changes clearly
- Provide migration guides for major updates
- Include compatibility information

## 🔒 Security Considerations

### Documentation Security

- Avoid including sensitive information in documentation
- Use secure practices for API key examples
- Document security best practices
- Include security update procedures

### Code Security

- Document security requirements
- Include security testing procedures
- Document vulnerability disclosure process
- Maintain security-related documentation

This guide serves as the foundation for maintaining high-quality, consistent documentation and code across all projects. Regular updates and refinements should be made based on team feedback and evolving best practices.
