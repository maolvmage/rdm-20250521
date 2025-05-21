#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Generator

This module generates Markdown reports from code review results.
It creates individual reports for each file and a consolidated report.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Class to generate Markdown reports from code review results."""
    
    def __init__(self, output_dir: str):
        """
        Initialize the report generator.
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create language-specific directories
        for language in ['java', 'c_cpp', 'go']:
            os.makedirs(os.path.join(self.output_dir, language), exist_ok=True)
    
    def generate_reports(self, review_results: Dict[str, Dict[str, Any]]) -> List[str]:
        """
        Generate individual Markdown reports for each file review.
        
        Args:
            review_results: Dictionary mapping file paths to review results
            
        Returns:
            List of paths to generated report files
        """
        report_files = []
        
        for file_path, result in review_results.items():
            try:
                # Skip files with errors
                if result.get('status') != 'success':
                    logger.warning(f"Skipping report generation for {file_path}: {result.get('message', 'Unknown error')}")
                    continue
                
                # Generate report file name
                language = result.get('language', 'unknown')
                file_name = os.path.basename(file_path)
                report_name = f"{file_name}_review.md"
                report_dir = os.path.join(self.output_dir, language)
                report_path = os.path.join(report_dir, report_name)
                
                # Generate report content
                report_content = self._generate_file_report(file_path, result)
                
                # Write report to file
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                
                logger.info(f"Generated report: {report_path}")
                report_files.append(report_path)
                
            except Exception as e:
                logger.error(f"Error generating report for {file_path}: {str(e)}")
        
        return report_files
    
    def consolidate_reports(self, report_files: List[str]) -> str:
        """
        Consolidate individual reports into a single Markdown file.
        
        Args:
            report_files: List of paths to individual report files
            
        Returns:
            Path to the consolidated report file
        """
        try:
            # Generate consolidated report file name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            consolidated_report_path = os.path.join(self.output_dir, f"consolidated_report_{timestamp}.md")
            
            # Generate report header
            header = f"""# 代码审查报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 目录

"""
            
            # Generate table of contents
            toc = ""
            for i, report_path in enumerate(report_files, 1):
                file_name = os.path.basename(report_path).replace('_review.md', '')
                language_dir = os.path.basename(os.path.dirname(report_path))
                toc += f"{i}. [{language_dir}/{file_name}](#{language_dir}-{file_name.replace('.', '-')})\n"
            
            # Combine all reports
            reports_content = ""
            for report_path in report_files:
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    # Add report to consolidated content
                    reports_content += f"\n\n{report_content}\n\n---\n"
                    
                except Exception as e:
                    logger.error(f"Error reading report {report_path}: {str(e)}")
            
            # Write consolidated report to file
            with open(consolidated_report_path, 'w', encoding='utf-8') as f:
                f.write(header + toc + reports_content)
            
            logger.info(f"Generated consolidated report: {consolidated_report_path}")
            return consolidated_report_path
            
        except Exception as e:
            logger.error(f"Error consolidating reports: {str(e)}")
            raise
    
    def _generate_file_report(self, file_path: str, result: Dict[str, Any]) -> str:
        """
        Generate a Markdown report for a single file review.
        
        Args:
            file_path: Path to the reviewed file
            result: Review results for the file
            
        Returns:
            Markdown report content
        """
        language = result.get('language', 'unknown')
        language_display = {
            'java': 'Java',
            'c_cpp': 'C/C++',
            'go': 'Go',
            'unknown': '未知'
        }.get(language, language)
        
        # File information
        file_name = os.path.basename(file_path)
        language_dir = os.path.basename(os.path.dirname(file_path))
        anchor = f"{language}-{file_name.replace('.', '-')}"
        
        report = f"""<h2 id="{anchor}">{file_name} ({language_display})</h2>

**文件路径:** `{file_path}`

### 发现的问题

"""
        
        # Add issues
        issues = result.get('issues', [])
        if issues:
            for i, issue in enumerate(issues, 1):
                report += f"{i}. {issue}\n"
        else:
            report += "未发现问题。\n"
        
        # Add suggestions
        report += "\n### 改进建议\n\n"
        suggestions = result.get('suggestions', [])
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "无改进建议。\n"
        
        # Add improved code
        report += "\n### 改进后的代码\n\n"
        improved_code = result.get('improved_code', '')
        if improved_code:
            report += f"```{language}\n{improved_code}\n```\n"
        else:
            report += "无改进代码示例。\n"
        
        return report
