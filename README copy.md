# 代码审查自动化工具

这个工具可以自动从GitLab代码库下载代码文件，使用AI模型进行代码审查，生成审查报告，并通过邮件发送结果。

## 功能特点

1. 从GitLab代码库中下载文件
2. 支持Java、C/C++和Go等多种编程语言
3. 使用公司私有化部署的AI大模型进行代码检视
4. 生成详细的Markdown格式审查报告
5. 将报告通过邮件发送给指定收件人

## 安装依赖

```bash
pip install python-gitlab requests
```

## 使用方法

### 命令行参数

```bash
python code_review_orchestrator.py \
    --gitlab-url https://your-gitlab-server.com \
    --gitlab-token YOUR_GITLAB_TOKEN \
    --project-ids 123 456 \
    --branches master develop \
    --ai-api-url https://your-ai-api-url.com/api \
    --ai-api-key YOUR_AI_API_KEY \
    --output-dir code_review_results \
    --email-to recipient@example.com \
    --email-from sender@example.com \
    --smtp-server smtp.example.com \
    --smtp-port 587 \
    --smtp-username your_username \
    --smtp-password your_password
```

### 参数说明

- `--gitlab-url`: GitLab服务器URL
- `--gitlab-token`: GitLab私人访问令牌
- `--project-ids`: 要审查的GitLab项目ID列表
- `--branches`: 要审查的分支列表（默认为master）
- `--ai-api-url`: AI模型API的URL
- `--ai-api-key`: AI模型API的访问密钥
- `--output-dir`: 存储审查结果的目录（默认为code_review_results）
- `--email-to`: 接收报告的邮箱地址
- `--email-from`: 发送报告的邮箱地址
- `--smtp-server`: SMTP服务器地址
- `--smtp-port`: SMTP服务器端口（默认为587）
- `--smtp-username`: SMTP用户名
- `--smtp-password`: SMTP密码

## 模块说明

- `code_review_orchestrator.py`: 主程序，协调整个代码审查流程
- `gitlab_downloader.py`: 从GitLab下载代码文件
- `ai_reviewer.py`: 使用AI模型进行代码审查
- `report_generator.py`: 生成Markdown格式的审查报告
- `email_sender.py`: 发送包含审查报告的邮件

## 输出结果

1. 下载的代码文件保存在 `{output_dir}/downloaded_code` 目录下
2. 单个文件的审查报告保存在 `{output_dir}/reports/{language}` 目录下
3. 合并后的审查报告保存在 `{output_dir}/reports` 目录下
4. 所有操作的日志保存在 `code_review_{timestamp}.log` 文件中

## 注意事项

- 确保GitLab令牌具有足够的权限来访问项目和文件
- 确保AI模型API的URL和密钥正确
- 确保SMTP服务器信息正确，且账户有权限发送邮件
- 对于大型代码库，审查过程可能需要较长时间