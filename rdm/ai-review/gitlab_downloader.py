#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitLab下载器

此模块处理从GitLab代码库下载文件。
它支持从多个项目和分支下载文件。
"""

import os
import logging
import gitlab
from typing import Dict, List, Set, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class GitLabDownloader:
    """用于从GitLab代码库下载文件的类。"""

    # 按编程语言分类的文件扩展名
    LANGUAGE_EXTENSIONS = {
        'java': ['.java'],
        'c_cpp': ['.c', '.cpp', '.cc', '.h', '.hpp'],
        'go': ['.go'],
        # 根据需要添加更多语言
    }

    def __init__(self, gitlab_url: str, private_token: str, output_dir: str):
        """
        初始化GitLab下载器。

        参数:
            gitlab_url: GitLab服务器的URL
            private_token: GitLab API的私人访问令牌
            output_dir: 保存下载文件的目录
        """
        self.gitlab_url = gitlab_url
        self.private_token = private_token
        self.output_dir = output_dir
        self.gl = None

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize GitLab client
        self._init_gitlab_client()

    def _init_gitlab_client(self):
        """Initialize the GitLab client."""
        try:
            self.gl = gitlab.Gitlab(
                url=self.gitlab_url,
                private_token=self.private_token,
                ssl_verify=False  # Note: In production, consider proper SSL verification
            )
            self.gl.auth()
            logger.info(f"Successfully authenticated with GitLab server at {self.gitlab_url}")
        except Exception as e:
            logger.error(f"Failed to initialize GitLab client: {str(e)}")
            raise

    def download_repositories(self, project_branch_map: Dict[int, str]) -> List[str]:
        """
        Download files from multiple GitLab repositories.

        Args:
            project_branch_map: Dictionary mapping project IDs to branch names

        Returns:
            List of paths to downloaded files
        """
        downloaded_files = []

        for project_id, branch in project_branch_map.items():
            try:
                project_files = self.download_project_files(project_id, branch)
                downloaded_files.extend(project_files)
            except Exception as e:
                logger.error(f"Error downloading files from project {project_id}, branch {branch}: {str(e)}")

        return downloaded_files

    def download_project_files(self, project_id: int, branch: str) -> List[str]:
        """
        Download files from a specific GitLab project and branch.

        Args:
            project_id: GitLab project ID
            branch: Branch name

        Returns:
            List of paths to downloaded files
        """
        downloaded_files = []

        try:
            # Get project
            project = self.gl.projects.get(project_id)
            logger.info(f"Accessing project: {project.name} (ID: {project_id})")

            # Create project directory
            project_dir = os.path.join(self.output_dir, f"{project_id}_{project.name}")
            os.makedirs(project_dir, exist_ok=True)

            # Get repository tree (recursive)
            items = project.repository_tree(ref=branch, recursive=True, all=True)

            # Filter items to only include files with supported extensions
            supported_extensions = [ext for exts in self.LANGUAGE_EXTENSIONS.values() for ext in exts]
            file_items = [
                item for item in items
                if item['type'] == 'blob' and any(item['path'].endswith(ext) for ext in supported_extensions)
            ]

            # Download each file
            for item in file_items:
                try:
                    file_path = item['path']

                    # Determine language based on file extension
                    file_language = self._get_file_language(file_path)
                    if not file_language:
                        continue  # Skip files with unsupported extensions

                    # Get file content
                    file_content = project.files.get(file_path, ref=branch).decode()

                    # Save file to disk
                    local_path = os.path.join(project_dir, file_path)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    with open(local_path, 'w', encoding='utf-8') as f:
                        f.write(file_content)

                    logger.debug(f"Downloaded file: {local_path}")
                    downloaded_files.append(local_path)

                except Exception as e:
                    logger.error(f"Error downloading file {item['path']}: {str(e)}")

            logger.info(f"Downloaded {len(downloaded_files)} files from project {project.name}")

        except Exception as e:
            logger.error(f"Error accessing project {project_id}: {str(e)}")
            raise

        return downloaded_files

    def _get_file_language(self, file_path: str) -> str:
        """
        Determine the programming language of a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            Language name or None if not supported
        """
        for language, extensions in self.LANGUAGE_EXTENSIONS.items():
            if any(file_path.endswith(ext) for ext in extensions):
                return language
        return None
