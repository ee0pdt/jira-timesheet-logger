# Jira Timesheet Logger

A Python tool that reads timesheet data from CSV files and automatically logs work entries to Jira via the REST API.

## Features

- **CSV Integration**: Read timesheet entries from CSV files
- **Batch Processing**: Log multiple timesheet entries at once
- **Dry Run Mode**: Preview what will be logged before making actual changes
- **Rate Limiting**: Built-in delays to respect Jira API limits
- **Error Handling**: Detailed error reporting and validation
- **Colorized Output**: Easy-to-read console output with color coding
- **Flexible Configuration**: Environment-based configuration management

## Prerequisites

- Python 3.6 or higher
- Valid Jira Cloud instance with API access
- Jira API token (see setup instructions below)

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Copy the example CSV file and add your timesheet data:
   ```bash
   cp timesheet_data.csv.example timesheet_data.csv
   ```

3. Edit the `.env` file with your Jira credentials:
   ```bash
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token-here
   JIRA_DOMAIN=yourcompany.atlassian.net
   JIRA_CLOUD_ID=
   ```

### Getting Your Jira API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a descriptive name (e.g., "Timesheet Logger")
4. Copy the generated token and paste it into your `.env` file

## CSV Format

Your timesheet CSV file should have the following columns:

```csv
Date,Jira Ticket Number,Work Description,Hours
2024-01-15,PROJ-123,Investigated login flow and fixed OAuth redirect issue,2.5
2024-01-15,PROJ-124,Updated API documentation with new endpoints,1.0
2024-01-16,PROJ-125,,2.0
```

### Required Columns

- **Date**: Date in YYYY-MM-DD format
- **Jira Ticket Number**: The Jira issue key (e.g., PROJ-123)
- **Work Description**: Description of the work done (optional - if empty, defaults to "Work on {ticket}")
- **Hours**: Number of hours worked (decimal format supported)

## Usage

### Basic Usage

Log all entries from the default CSV file:
```bash
python log-timesheet.py
```

### Dry Run Mode

Preview what will be logged without making changes:
```bash
python log-timesheet.py --dry-run
```

### Custom CSV File

Use a different CSV file:
```bash
python log-timesheet.py --csv my-timesheet.csv
```

### Limit Entries (for Testing)

Process only the first N entries:
```bash
python log-timesheet.py --limit 5 --dry-run
```

### Command Line Options

- `--dry-run`: Show what would be logged without actually doing it
- `--csv FILENAME`: Specify CSV file to read (default: timesheet_data.csv)  
- `--limit N`: Limit number of entries to process
- `--help`: Show help message

## Examples

```bash
# Test with first 3 entries
python log-timesheet.py --dry-run --limit 3

# Log all entries from custom file
python log-timesheet.py --csv july-timesheet.csv

# Preview all entries before logging
python log-timesheet.py --dry-run
python log-timesheet.py  # Run for real after reviewing
```

## Output

The tool provides colorized output showing:
- ✓ Successfully logged entries (green)
- ✗ Failed entries with error details (red)  
- Summary statistics
- Dry run previews (yellow)

## Error Handling

The tool handles common issues:
- Missing or invalid CSV files
- Network connectivity problems
- Invalid Jira ticket numbers
- Authentication failures
- API rate limiting

## Security

- Never commit your `.env` file to version control
- API tokens should be treated as passwords
- The tool only has access to log work entries, not modify issues
- All API communication uses HTTPS

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Verify your email and API token in `.env`
- Ensure your Jira domain is correct

**"Issue not found"** 
- Check that ticket numbers in your CSV exist in Jira
- Verify you have permission to view the issues

**"Rate limit exceeded"**
- The tool includes built-in delays, but you may need to reduce batch sizes
- Try using `--limit` to process smaller batches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.