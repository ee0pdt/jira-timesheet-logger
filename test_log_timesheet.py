#!/usr/bin/env python3

"""
Test suite for Jira Timesheet Logger

Run with: python -m pytest test_log_timesheet.py
"""

import pytest
import importlib.util
import sys
from unittest.mock import patch, mock_open

# Import the module with hyphen in name
spec = importlib.util.spec_from_file_location("log_timesheet", "log-timesheet.py")
log_timesheet = importlib.util.module_from_spec(spec)
sys.modules["log_timesheet"] = log_timesheet
spec.loader.exec_module(log_timesheet)

# Import functions from the module
validate_email = log_timesheet.validate_email
validate_domain = log_timesheet.validate_domain
validate_ticket_format = log_timesheet.validate_ticket_format
validate_hours = log_timesheet.validate_hours
Colors = log_timesheet.Colors


class TestValidation:
    """Test validation functions"""
    
    def test_validate_email_valid(self):
        """Test valid email formats"""
        assert validate_email("user@example.com") == True
        assert validate_email("test.user+tag@company.co.uk") == True
        assert validate_email("123@domain.org") == True
    
    def test_validate_email_invalid(self):
        """Test invalid email formats"""
        assert validate_email("notanemail") == False
        assert validate_email("@domain.com") == False
        assert validate_email("user@") == False
        assert validate_email("user.domain.com") == False
    
    def test_validate_domain_valid(self):
        """Test valid domain formats"""
        assert validate_domain("company.atlassian.net") == "company.atlassian.net"
        assert validate_domain("https://company.atlassian.net") == "company.atlassian.net"
        assert validate_domain("company.atlassian.net/") == "company.atlassian.net"
    
    def test_validate_domain_invalid(self):
        """Test invalid domain formats"""
        with pytest.raises(ValueError):
            validate_domain("invalid")
        with pytest.raises(ValueError):
            validate_domain("spaces in domain.com")
    
    def test_validate_ticket_format_valid(self):
        """Test valid ticket formats"""
        assert validate_ticket_format("PROJ-123") == True
        assert validate_ticket_format("ABC-1") == True  
        assert validate_ticket_format("PROJECT123-999") == True
        assert validate_ticket_format("proj-123") == True  # Should handle lowercase
    
    def test_validate_ticket_format_invalid(self):
        """Test invalid ticket formats"""
        assert validate_ticket_format("123-PROJ") == False
        assert validate_ticket_format("PROJ") == False
        assert validate_ticket_format("-123") == False
        assert validate_ticket_format("PROJ-") == False
        assert validate_ticket_format("") == False
    
    def test_validate_hours_valid(self):
        """Test valid hour values"""
        assert validate_hours("8") == 8.0
        assert validate_hours("0.5") == 0.5
        assert validate_hours("24") == 24.0
        assert validate_hours("1.25") == 1.25
    
    def test_validate_hours_invalid(self):
        """Test invalid hour values"""
        with pytest.raises(ValueError, match="Hours must be positive"):
            validate_hours("0")
        
        with pytest.raises(ValueError, match="Hours must be positive"):
            validate_hours("-1")
        
        with pytest.raises(ValueError, match="Hours cannot exceed 24"):
            validate_hours("25")
        
        with pytest.raises(ValueError, match="Invalid hours value"):
            validate_hours("abc")


class TestColors:
    """Test color constants are defined"""
    
    def test_colors_defined(self):
        """Ensure all color constants are defined"""
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN') 
        assert hasattr(Colors, 'YELLOW')
        assert hasattr(Colors, 'BLUE')
        assert hasattr(Colors, 'NC')
        
        # Ensure they're strings
        assert isinstance(Colors.RED, str)
        assert isinstance(Colors.GREEN, str)
        assert isinstance(Colors.YELLOW, str)
        assert isinstance(Colors.BLUE, str)
        assert isinstance(Colors.NC, str)


if __name__ == "__main__":
    pytest.main([__file__])