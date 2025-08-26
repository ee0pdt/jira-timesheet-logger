# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-26

### Added
- Initial release of Jira Timesheet Logger
- CSV-based timesheet data import
- Jira API integration for worklog creation
- Dry-run mode for testing without making changes
- Input validation for tickets, hours, and dates  
- Rate limiting to respect API limits
- Colorized console output
- Environment-based configuration (.env)
- Comprehensive error handling and reporting
- Command-line interface with multiple options
- MIT license
- Complete documentation (README, CONTRIBUTING)
- Setup script for Python package distribution

### Security
- Secure credential management via environment variables
- Automatic .env file exclusion from version control
- HTTPS-only API communication