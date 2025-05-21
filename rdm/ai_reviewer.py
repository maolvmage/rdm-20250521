#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI Reviewer

This module handles sending code to an AI model for review and processing the results.
It supports different programming languages and formats the review results.
"""

import os
import logging
import requests
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AIReviewer:
    """Class to review code using an AI model API."""
    
    # Language-specific prompts
    LANGUAGE_PROMPTS = {
        'java': "请对以下Java代码进行代码审查，找出潜在的问题，并提供改进建议和改进后的代码示例：",
        'c_cpp': "请对以下C/C++代码进行代码审查，找出潜在的问题，并提供改进建议和改进后的代码示例：",
        'go': "请对以下Go代码进行代码审查，找出潜在的问题，并提供改进建议和改进后的代码示例：",
        # Add more languages as needed
    }
    
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize the AI reviewer.
        
        Args:
            api_url: URL of the AI model API
            api_key: API key for authentication
        """
        self.api_url = api_url
        self.api_key = api_key
    
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a code file using the AI model.
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Dictionary containing review results
        """
        try:
            # Determine file language
            file_language = self._get_file_language(file_path)
            if not file_language:
                logger.warning(f"Unsupported file type: {file_path}")
                return {
                    'file_path': file_path,
                    'status': 'error',
                    'message': 'Unsupported file type',
                    'issues': [],
                    'suggestions': [],
                    'improved_code': ''
                }
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Get language-specific prompt
            prompt = self.LANGUAGE_PROMPTS.get(file_language, "请对以下代码进行代码审查，找出潜在的问题，并提供改进建议和改进后的代码示例：")
            
            # Send code to AI model for review
            review_result = self._call_ai_api(prompt, code_content, file_language)
            
            # Process and structure the review results
            processed_result = self._process_review_result(file_path, review_result, file_language)
            
            return processed_result
            
        except Exception as e:
            logger.error(f"Error reviewing file {file_path}: {str(e)}")
            return {
                'file_path': file_path,
                'status': 'error',
                'message': str(e),
                'issues': [],
                'suggestions': [],
                'improved_code': ''
            }
    
    def _call_ai_api(self, prompt: str, code: str, language: str) -> Dict[str, Any]:
        """
        Call the AI model API to review code.
        
        Args:
            prompt: Instruction prompt for the AI model
            code: Code content to review
            language: Programming language of the code
            
        Returns:
            Raw API response
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            # Construct the payload according to your AI model's API requirements
            # This is a generic example and should be adapted to your specific API
            payload = {
                'prompt': f"{prompt}\n\n```{language}\n{code}\n```",
                'max_tokens': 2000,
                'temperature': 0.3,
                'format': 'json'  # Request JSON response if supported
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60  # Adjust timeout as needed
            )
            
            response.raise_for_status()  # Raise exception for HTTP errors
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            raise
    
    def _process_review_result(self, file_path: str, raw_result: Dict[str, Any], language: str) -> Dict[str, Any]:
        """
        Process and structure the AI review results.
        
        Args:
            file_path: Path to the reviewed file
            raw_result: Raw API response
            language: Programming language of the code
            
        Returns:
            Structured review results
        """
        try:
            # This processing logic should be adapted to match your AI model's response format
            # This is a generic example assuming the AI returns a structured response
            
            # Extract content from AI response
            # The exact structure depends on your AI model's response format
            content = raw_result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Try to parse JSON if the response is in JSON format
            try:
                parsed_content = json.loads(content)
                issues = parsed_content.get('issues', [])
                suggestions = parsed_content.get('suggestions', [])
                improved_code = parsed_content.get('improved_code', '')
            except json.JSONDecodeError:
                # If not JSON, try to extract information from text
                # This is a simple example and may need to be enhanced
                issues = self._extract_issues(content)
                suggestions = self._extract_suggestions(content)
                improved_code = self._extract_improved_code(content, language)
            
            return {
                'file_path': file_path,
                'status': 'success',
                'language': language,
                'issues': issues,
                'suggestions': suggestions,
                'improved_code': improved_code
            }
            
        except Exception as e:
            logger.error(f"Error processing review result: {str(e)}")
            return {
                'file_path': file_path,
                'status': 'error',
                'message': f"Error processing review result: {str(e)}",
                'issues': [],
                'suggestions': [],
                'improved_code': ''
            }
    
    def _extract_issues(self, content: str) -> list:
        """Extract issues from text content."""
        # This is a simple example and should be enhanced for better extraction
        issues = []
        lines = content.split('\n')
        in_issues_section = False
        
        for line in lines:
            if '问题:' in line or '问题：' in line or 'Issues:' in line:
                in_issues_section = True
                continue
            elif '建议:' in line or '建议：' in line or 'Suggestions:' in line:
                in_issues_section = False
                continue
            
            if in_issues_section and line.strip() and not line.startswith('```'):
                # Remove numbering if present
                cleaned_line = line.strip()
                if cleaned_line[0].isdigit() and cleaned_line[1:3] in ['. ', '、', ') ']:
                    cleaned_line = cleaned_line[3:].strip()
                if cleaned_line:
                    issues.append(cleaned_line)
        
        return issues
    
    def _extract_suggestions(self, content: str) -> list:
        """Extract suggestions from text content."""
        # Similar to _extract_issues but for suggestions
        suggestions = []
        lines = content.split('\n')
        in_suggestions_section = False
        
        for line in lines:
            if '建议:' in line or '建议：' in line or 'Suggestions:' in line:
                in_suggestions_section = True
                continue
            elif '改进后的代码:' in line or '改进后的代码：' in line or 'Improved Code:' in line:
                in_suggestions_section = False
                continue
            
            if in_suggestions_section and line.strip() and not line.startswith('```'):
                # Remove numbering if present
                cleaned_line = line.strip()
                if cleaned_line[0].isdigit() and cleaned_line[1:3] in ['. ', '、', ') ']:
                    cleaned_line = cleaned_line[3:].strip()
                if cleaned_line:
                    suggestions.append(cleaned_line)
        
        return suggestions
    
    def _extract_improved_code(self, content: str, language: str) -> str:
        """Extract improved code from text content."""
        improved_code = ""
        lines = content.split('\n')
        in_code_section = False
        
        for i, line in enumerate(lines):
            if ('改进后的代码:' in line or '改进后的代码：' in line or 'Improved Code:' in line) and i < len(lines) - 1:
                in_code_section = True
                continue
            
            if in_code_section:
                if line.strip().startswith('```'):
                    if improved_code:  # If we've already started collecting code, this is the end
                        break
                    continue  # Skip the opening code fence
                improved_code += line + '\n'
        
        return improved_code.strip()
    
    def _get_file_language(self, file_path: str) -> Optional[str]:
        """
        Determine the programming language of a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language identifier or None if not supported
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.java']:
            return 'java'
        elif ext in ['.c', '.cpp', '.cc', '.h', '.hpp']:
            return 'c_cpp'
        elif ext in ['.go']:
            return 'go'
        
        return None
