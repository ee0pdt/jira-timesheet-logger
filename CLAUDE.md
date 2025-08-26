# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a single-file Python CLI tool that reads CSV timesheet data and logs work entries to Jira via REST API. The project follows a simple architecture with comprehensive validation, error handling, and user-friendly output.

## Architecture

### Core Structure
- **Single main module**: `log-timesheet.py` contains all functionality
- **Configuration-driven**: Uses `.env` file for Jira credentials and domain
- **CSV-based data input**: Processes timesheet data from CSV files with specific column format
- **Stateless operations**: Each CSV row is processed independently with full validation

### Key Components
- **Validation layer**: Email, domain, ticket format, and hours validation with detailed error messages
- **Configuration management**: Environment-based config with fallbacks and normalization
- **API client**: Direct requests to Jira Cloud REST API v3 with rate limiting
- **Output system**: Colorized console output with clear success/failure indicators

### Data Flow
1. Load and validate configuration from `.env`
2. Parse CSV file with required columns: `Date`, `Jira Ticket Number`, `Work Description`, `Hours`
3. Validate each row (date format, ticket format, hours range)
4. Transform to Jira worklog API format (ISO datetime, comment structure)
5. Submit via HTTP POST with authentication and rate limiting

## Essential Development Commands

### Setup
```bash
# Install dependencies (including dev tools)
pip install -r requirements.txt
pip install black flake8 pytest pytest-cov
```

### IMPORTANT: Always Run Before Committing
After making code changes, always run these commands locally to avoid CI failures:

```bash
# 1. Format code (REQUIRED - CI will fail if not formatted)
black log-timesheet.py setup.py test_log_timesheet.py

# 2. Check linting
flake8 log-timesheet.py

# 3. Run tests
pytest

# 4. Test the tool with dry-run
python log-timesheet.py --dry-run --limit 3
```

### Running the Tool
```bash
# Always test with dry-run first
python log-timesheet.py --dry-run --limit 5

# Process specific CSV file
python log-timesheet.py --csv custom-timesheet.csv

# Full execution (only after dry-run testing)
python log-timesheet.py
```

## Configuration Requirements

### Environment Setup
The tool requires a `.env` file with:
- `JIRA_EMAIL`: Atlassian account email
- `JIRA_API_TOKEN`: API token from Atlassian account settings
- `JIRA_DOMAIN`: Domain without protocol (e.g., `company.atlassian.net`)
- `JIRA_CLOUD_ID`: Optional, can be blank

### CSV Data Format
Required columns in exact order:
- `Date`: YYYY-MM-DD format
- `Jira Ticket Number`: PROJECT-123 format (validated with regex)
- `Work Description`: Free text (empty defaults to "Work on {ticket}")
- `Hours`: Decimal format, must be 0 < hours <= 24

## Key Design Patterns

### Validation Strategy
- **Input validation at entry points**: All user inputs validated before processing
- **Graceful degradation**: Empty work descriptions get sensible defaults
- **Early failure**: Invalid data stops processing immediately with clear error messages

### Error Handling
- **Comprehensive validation**: Email format, domain format, ticket format, date parsing, hours range
- **Network resilience**: Request timeouts, rate limiting, detailed HTTP error reporting
- **User-friendly output**: Color-coded messages with actionable error descriptions

### Template File Pattern
- Use `.example` suffix for template files (`timesheet_data.csv.example`, `.env.example`)
- `.gitignore` protects actual data files while preserving templates
- Documentation includes copy commands for setup

## Testing Considerations

### Test Module Structure
Tests use dynamic module import to handle hyphenated filename (`log-timesheet.py`):
```python
spec = importlib.util.spec_from_file_location("log_timesheet", "log-timesheet.py")
```

### Validation Testing
Focus on boundary conditions for:
- Email validation (valid/invalid formats)
- Domain normalization (protocol removal, validation)
- Ticket format validation (PROJECT-123 pattern)
- Hours validation (positive, <= 24, decimal support)

### Integration Testing
Always test with `--dry-run` mode first before making actual API calls to avoid accidental data submission during development.

## Common CI Failures and Solutions

### Black Formatting Failures
- **Issue**: CI fails with "would reformat X files"
- **Solution**: Run `black *.py` locally before committing
- **Prevention**: Always format code as part of pre-commit routine

### Dependency Compatibility
- **Issue**: Python version compatibility problems (e.g., python-dotenv 1.0+ requires Python 3.8+)
- **Solution**: Check minimum versions in requirements.txt match python_requires in setup.py
- **Current**: Uses python-dotenv>=0.19.0 for Python 3.7+ compatibility

### Test Import Errors
- **Issue**: Tests can't import modules with hyphens in filename
- **Solution**: Use importlib.util.spec_from_file_location() pattern (already implemented)

## Security Considerations

- Never commit `.env` files or actual timesheet data
- All API communication uses HTTPS with proper authentication
- Input validation prevents injection attacks via CSV data
- Rate limiting respects Jira API limits to avoid account restrictions