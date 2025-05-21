#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the code review system.
This script tests each component individually to ensure they work correctly.
"""

import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from gitlab_downloader import GitLabDownloader
from ai_reviewer import AIReviewer
from report_generator import ReportGenerator
from email_sender import EmailSender

class TestGitLabDownloader(unittest.TestCase):
    """Test the GitLab downloader module."""
    
    @patch('gitlab.Gitlab')
    def test_init(self, mock_gitlab):
        """Test initialization of GitLabDownloader."""
        # Setup
        mock_instance = MagicMock()
        mock_gitlab.return_value = mock_instance
        
        # Execute
        downloader = GitLabDownloader(
            gitlab_url='https://example.com',
            private_token='token123',
            output_dir='/tmp/output'
        )
        
        # Assert
        mock_gitlab.assert_called_once_with(
            url='https://example.com',
            private_token='token123',
            ssl_verify=False
        )
        mock_instance.auth.assert_called_once()
        self.assertEqual(downloader.gitlab_url, 'https://example.com')
        self.assertEqual(downloader.private_token, 'token123')
        self.assertEqual(downloader.output_dir, '/tmp/output')

class TestAIReviewer(unittest.TestCase):
    """Test the AI reviewer module."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a sample Java file
        self.java_file = os.path.join(self.temp_dir, 'Test.java')
        with open(self.java_file, 'w', encoding='utf-8') as f:
            f.write("""
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    @patch('requests.post')
    def test_review_file(self, mock_post):
        """Test reviewing a file."""
        # Setup
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': '{"issues": ["No issues found"], "suggestions": ["No suggestions"], "improved_code": ""}'
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        reviewer = AIReviewer(
            api_url='https://api.example.com',
            api_key='key123'
        )
        
        # Execute
        result = reviewer.review_file(self.java_file)
        
        # Assert
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['language'], 'java')
        mock_post.assert_called_once()

class TestReportGenerator(unittest.TestCase):
    """Test the report generator module."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.report_generator = ReportGenerator(output_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_generate_reports(self):
        """Test generating reports."""
        # Setup
        review_results = {
            '/path/to/file.java': {
                'file_path': '/path/to/file.java',
                'status': 'success',
                'language': 'java',
                'issues': ['Issue 1', 'Issue 2'],
                'suggestions': ['Suggestion 1'],
                'improved_code': 'public class Better {}'
            }
        }
        
        # Execute
        report_files = self.report_generator.generate_reports(review_results)
        
        # Assert
        self.assertEqual(len(report_files), 1)
        self.assertTrue(os.path.exists(report_files[0]))
        
        # Check report content
        with open(report_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('Issue 1', content)
            self.assertIn('Issue 2', content)
            self.assertIn('Suggestion 1', content)
            self.assertIn('public class Better {}', content)

class TestEmailSender(unittest.TestCase):
    """Test the email sender module."""
    
    @patch('smtplib.SMTP')
    def test_send_report(self, mock_smtp):
        """Test sending an email report."""
        # Setup
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Create a temporary report file
        temp_dir = tempfile.mkdtemp()
        report_path = os.path.join(temp_dir, 'report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('# Test Report\n\nThis is a test report.')
        
        email_sender = EmailSender(
            smtp_server='smtp.example.com',
            smtp_port=587,
            username='user',
            password='pass'
        )
        
        # Execute
        result = email_sender.send_report(
            from_email='from@example.com',
            to_email='to@example.com',
            subject='Test Report',
            report_path=report_path
        )
        
        # Assert
        self.assertTrue(result)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('user', 'pass')
        mock_server.sendmail.assert_called_once()
        
        # Clean up
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
