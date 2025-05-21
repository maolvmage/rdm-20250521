import os
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class GitLabDownloader:
    LANGUAGE_EXTENSIONS = {
        'python': ['.py'],
        'java': ['.java'],
        'javascript': ['.js'],
        'typescript': ['.ts'],
        'go': ['.go'],
        'rust': ['.rs'],
        'cpp': ['.cpp', '.h'],
        'c': ['.c', '.h'],
        'ruby': ['.rb'],
        'php': ['.php'],
        'html': ['.html'],
        'css': ['.css'],
        'sql': ['.sql'],
        'json': ['.json'],
        'yaml': ['.yaml', '.yml'],
        'markdown': ['.md'],
        'text': ['.txt']
    }

    def __init__(self, gitlab_url: str, private_token: str, output_dir: str):
        self.gl = gitlab.Gitlab(gitlab_url, private_token=private_token, ssl_verify=False)
        self.output_dir = output_dir

    def download_repositories(self, project_branch_map: Dict[int, str]) -> List[str]:
        downloaded_files = []

        for project_id, branch in project_branch_map.items():
            try:
                project_files = self.download_project_files(project_id, branch)
                downloaded_files.extend(project_files)
            except Exception as e:
                logger.error(f"Error downloading files from project {project_id}, branch {branch}: {str(e)}")

        return downloaded_files

    def download_project_files(self, project_id: int, branch: str) -> List[str]:
        downloaded_files = []

        try:
            project = self.gl.projects.get(project_id)
            logger.info(f"Accessing project: {project.name} (ID: {project_id})")

            project_dir = os.path.join(self.output_dir, f"{project_id}_{project.name}")
            os.makedirs(project_dir, exist_ok=True)

            items = project.repository_tree(ref=branch, recursive=True, all=True)

            supported_extensions = [ext for exts in self.LANGUAGE_EXTENSIONS.values() for ext in exts]
            file_items = [
                item for item in items
                if item['type'] == 'blob' and any(item['path'].endswith(ext) for ext in supported_extensions)
            ]

            for item in file_items:
                try:
                    file_path = item['path']

                    file_language = self._get_file_language(file_path)
                    if not file_language:
                        continue

                    file_content = project.files.get(file_path, ref=branch).decode()

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
        for language, extensions in self.LANGUAGE_EXTENSIONS.items():
            if any(file_path.endswith(ext) for ext in extensions):
                return language
        return ''