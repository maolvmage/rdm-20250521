import gitlab
import re
from datetime import datetime

gitlab_url = 'https://192.168.50.9'
token = 'BijvXcQMAazKXDRvzdMy'
project_branch_map = {
    270: 'master'
}  # 每个项目对应的分支
since = '2024-03-01T00:00:00Z'
until = '2024-03-02T23:59:59Z'

def get_code_changes(project_id, branch):
    gl = gitlab.Gitlab(gitlab_url, private_token=token, ssl_verify=False)
    project = gl.projects.get(project_id)
    commits = project.commits.list(ref_name=branch, since=since, until=until, all=True)
    stats = {'additions': 0, 'deletions': 0, 'modifications': 0, 'modified_functions': {}}
    
    for commit in commits:
        commit_details = project.commits.get(commit.id)
        stats['additions'] += commit_details.stats['additions']
        stats['deletions'] += commit_details.stats['deletions']
        
        # 获取 commit 的 diff 信息
        diffs = commit_details.diff()
        for diff in diffs:
            if diff['new_path'].endswith('.py'):
                modified_functions = extract_modified_functions(diff['diff'])
                stats['modified_functions'][diff['new_path']] = modified_functions
    
    stats['modifications'] = stats['additions'] + stats['deletions']
    return stats

def extract_modified_functions(diff_text):
    """
    解析 diff 文本，提取修改的 Python 函数
    """
    modified_functions = set()
    diff_lines = diff_text.split('\n')
    
    function_pattern = re.compile(r'^[+-]\s*def\s+(\w+)\(')  # 匹配 Python 函数定义
    for line in diff_lines:
        match = function_pattern.match(line)
        if match:
            modified_functions.add(match.group(1))
    
    return list(modified_functions)

if __name__ == '__main__':
    all_code_changes = {}
    for project_id, branch in project_branch_map.items():
        print(f"统计项目 {project_id} 分支 {branch} 的代码变更:")
        code_changes = get_code_changes(project_id, branch)
        all_code_changes[(project_id, branch)] = code_changes
        print(f"新增代码行数: {code_changes['additions']}")
        print(f"删除代码行数: {code_changes['deletions']}")
        # print(f"修改代码行数: {code_changes['modifications']}")
        # print("修改的函数:")
        # for file, functions in code_changes['modified_functions'].items():
        #     print(f"{file}: {functions}")
        print("-----------------------------------")