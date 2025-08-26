#!/usr/bin/env python3

"""
Jira Timesheet Logger

A Python tool that reads timesheet data from CSV files and automatically 
logs work entries to Jira via the REST API.

Author: Pete Thorne
License: MIT
Repository: https://github.com/petethorne/jira-timesheet-logger
"""

import csv
import sys
import os
import argparse
from datetime import datetime, timezone
from typing import Dict
import requests
from dotenv import load_dotenv
import time
import re

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def validate_email(email: str) -> bool:
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_domain(domain: str) -> str:
    """Validate and normalize Jira domain"""
    # Remove https:// if present
    domain = domain.replace('https://', '').replace('http://', '')
    
    # Remove trailing slash if present
    domain = domain.rstrip('/')
    
    # Basic domain validation
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
        raise ValueError(f"Invalid domain format: {domain}")
    
    return domain

def validate_ticket_format(ticket: str) -> bool:
    """Validate Jira ticket format (PROJECT-123)"""
    return re.match(r'^[A-Z][A-Z0-9]*-[0-9]+$', ticket.upper()) is not None

def validate_hours(hours_str: str) -> float:
    """Validate and convert hours to float"""
    try:
        hours = float(hours_str)
        if hours <= 0:
            raise ValueError("Hours must be positive")
        if hours > 24:
            raise ValueError("Hours cannot exceed 24 in a day")
        return hours
    except ValueError as e:
        raise ValueError(f"Invalid hours value '{hours_str}': {e}")

def load_config() -> Dict[str, str]:
    """Load and validate configuration from .env file"""
    # Load .env file from the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    if not os.path.exists(env_path):
        print(f"{Colors.RED}Error: .env file not found at {env_path}{Colors.NC}")
        print(f"Please copy .env.example to .env and fill in your credentials")
        print(f"You can create an API token at: https://id.atlassian.com/manage-profile/security/api-tokens")
        sys.exit(1)
    
    load_dotenv(env_path)
    
    config = {
        'email': os.getenv('JIRA_EMAIL', '').strip(),
        'token': os.getenv('JIRA_API_TOKEN', '').strip(),
        'domain': os.getenv('JIRA_DOMAIN', '').strip(),
        'cloud_id': os.getenv('JIRA_CLOUD_ID', '').strip()
    }
    
    # Check required fields (cloud_id is optional)
    required_fields = ['email', 'token', 'domain']
    missing = [k for k in required_fields if not config[k]]
    
    if missing:
        print(f"{Colors.RED}Error: Missing required environment variables: {', '.join(missing)}{Colors.NC}")
        print("Please check your .env file and ensure all required fields are filled in")
        sys.exit(1)
    
    # Validate email format
    if not validate_email(config['email']):
        print(f"{Colors.RED}Error: Invalid email format: {config['email']}{Colors.NC}")
        sys.exit(1)
    
    # Validate and normalize domain
    try:
        config['domain'] = validate_domain(config['domain'])
    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        print("Domain should be in format: yourcompany.atlassian.net")
        sys.exit(1)
    
    return config

def log_worklog(config: Dict[str, str], ticket: str, hours: str, date_str: str, comment: str, dry_run: bool = False) -> bool:
    """Log a worklog entry to Jira with validation"""
    
    # Validate ticket format
    ticket = ticket.strip().upper()
    if not validate_ticket_format(ticket):
        print(f"  {Colors.RED}✗ Invalid ticket format: {ticket} (should be like PROJ-123){Colors.NC}")
        return False
    
    # Validate hours
    try:
        hours_float = validate_hours(hours)
    except ValueError as e:
        print(f"  {Colors.RED}✗ {e}{Colors.NC}")
        return False
    
    # Convert date to ISO format (9 AM on the specified date)
    try:
        date_obj = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        # Check if date is not too far in the future
        current_date = datetime.now().date()
        if date_obj.date() > current_date:
            print(f"  {Colors.YELLOW}⚠ Warning: Future date detected: {date_str}{Colors.NC}")
        
        start_datetime = date_obj.replace(hour=9, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        started = start_datetime.isoformat().replace('+00:00', '.000+0000')
    except ValueError as e:
        print(f"{Colors.RED}  ✗ Could not parse date: {date_str} - {e} (expected format: YYYY-MM-DD){Colors.NC}")
        return False
    
    print(f"  {Colors.BLUE}{ticket}{Colors.NC} - {hours_float}h - {date_str}")
    print(f"    Comment: {comment[:100]}{'...' if len(comment) > 100 else ''}")
    
    if dry_run:
        print(f"    {Colors.YELLOW}[DRY RUN] Would log {hours_float} hours{Colors.NC}")
        return True
    
    # Prepare worklog data - Jira Cloud API format
    worklog_data = {
        "timeSpent": f"{hours_float}h",
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment
                        }
                    ]
                }
            ]
        },
        "started": started
    }
    
    # Make API request
    url = f"https://{config['domain']}/rest/api/3/issue/{ticket}/worklog"
    
    try:
        response = requests.post(
            url,
            json=worklog_data,
            auth=(config['email'], config['token']),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print(f"    {Colors.GREEN}✓ Successfully logged{Colors.NC}")
            return True
        else:
            print(f"    {Colors.RED}✗ Failed to log worklog (Status: {response.status_code}){Colors.NC}")
            if response.text:
                print(f"    {Colors.RED}Error: {response.text}{Colors.NC}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"    {Colors.RED}✗ Request failed: {e}{Colors.NC}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Log timesheet entries to Jira')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be logged without actually doing it')
    parser.add_argument('--csv', default='timesheet_data.csv', help='CSV file to read (default: timesheet_data.csv)')
    parser.add_argument('--limit', type=int, help='Limit number of entries to process (for testing)')
    
    args = parser.parse_args()
    
    print(f"{Colors.BLUE}Jira Timesheet Logger{Colors.NC}")
    print(f"{Colors.BLUE}====================={Colors.NC}")
    if args.dry_run:
        print(f"{Colors.YELLOW}DRY RUN MODE - No actual changes will be made{Colors.NC}")
    print()
    
    # Load configuration
    config = load_config()
    print(f"Jira Domain: {Colors.BLUE}{config['domain']}{Colors.NC}")
    print(f"Email: {Colors.BLUE}{config['email']}{Colors.NC}")
    print()
    
    # Check if CSV file exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, args.csv)
    
    if not os.path.exists(csv_path):
        print(f"{Colors.RED}Error: CSV file '{csv_path}' not found{Colors.NC}")
        sys.exit(1)
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            total_entries = 0
            successful_entries = 0
            failed_entries = 0
            
            print(f"Processing CSV file: {Colors.BLUE}{csv_path}{Colors.NC}")
            print()
            
            for i, row in enumerate(reader):
                date = row.get('Date', '').strip()
                ticket = row.get('Jira Ticket Number', '').strip()
                work_description = row.get('Work Description', '').strip()
                hours = row.get('Hours', '').strip()
                
                # Skip empty or zero hour entries
                if not all([date, ticket, hours]) or float(hours) == 0:
                    continue
                
                total_entries += 1
                
                # Apply limit if specified
                if args.limit and total_entries > args.limit:
                    print(f"{Colors.YELLOW}Reached limit of {args.limit} entries{Colors.NC}")
                    break
                
                # Handle empty work description gracefully
                if work_description:
                    comment = work_description
                else:
                    comment = f"Work on {ticket}"
                
                if log_worklog(config, ticket, hours, date, comment, args.dry_run):
                    successful_entries += 1
                else:
                    failed_entries += 1
                
                print()
                
                # Add small delay to avoid rate limiting (only for real requests)
                if not args.dry_run:
                    time.sleep(0.5)
            
            # Summary
            print(f"{Colors.BLUE}Summary:{Colors.NC}")
            print(f"  Total entries processed: {total_entries}")
            print(f"  {Colors.GREEN}Successfully logged: {successful_entries}{Colors.NC}")
            if failed_entries > 0:
                print(f"  {Colors.RED}Failed: {failed_entries}{Colors.NC}")
            
            if args.dry_run:
                print()
                print(f"{Colors.YELLOW}This was a dry run. To actually log the entries, run without --dry-run{Colors.NC}")
                
    except FileNotFoundError:
        print(f"{Colors.RED}Error: CSV file '{args.csv}' not found{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()