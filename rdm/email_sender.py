#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Email Sender

This module handles sending email reports with the code review results.
"""

import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional

logger = logging.getLogger(__name__)

class EmailSender:
    """Class to send email reports."""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """
        Initialize the email sender.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            username: SMTP username
            password: SMTP password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_report(self, from_email: str, to_email: str, subject: str, report_path: str, cc_emails: Optional[List[str]] = None) -> bool:
        """
        Send an email with the code review report.
        
        Args:
            from_email: Sender email address
            to_email: Recipient email address
            subject: Email subject
            report_path: Path to the report file
            cc_emails: List of CC email addresses (optional)
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            msg['Subject'] = subject
            
            # Add email body
            body = f"""
            <html>
            <body>
                <p>您好，</p>
                <p>附件是代码审查报告，包含了对代码库的AI检视结果。</p>
                <p>报告包括：</p>
                <ul>
                    <li>检视出的代码问题</li>
                    <li>代码改进建议</li>
                    <li>代码改进示例</li>
                </ul>
                <p>此邮件由自动化系统发送，请勿直接回复。</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))
            
            # Read and attach the report file
            with open(report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # Attach as both plain text and file attachment
            msg.attach(MIMEText(report_content, 'plain'))
            
            # Also attach as a file
            with open(report_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype="md")
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(report_path))
                msg.attach(attachment)
            
            # Send email
            recipients = [to_email]
            if cc_emails:
                recipients.extend(cc_emails)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.username, self.password)
                server.sendmail(from_email, recipients, msg.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
