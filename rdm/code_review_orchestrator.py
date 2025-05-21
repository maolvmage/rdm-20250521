#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
代码审查协调器

此脚本协调整个代码审查流程：
1. 从GitLab代码库下载文件
2. 将每个文件发送给AI模型进行代码审查
3. 为每个审查生成Markdown报告
4. 合并报告并通过邮件发送结果
"""

import os
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any

from gitlab_downloader import GitLabDownloader
from ai_reviewer import AIReviewer
from report_generator import ReportGenerator
from email_sender import EmailSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description='Code Review Orchestrator')

    parser.add_argument('--gitlab-url', type=str, default='https://192.168.50.9',
                        help='GitLab服务器URL')
    parser.add_argument('--gitlab-token', type=str, required=True,
                        help='GitLab私人访问令牌')
    parser.add_argument('--project-ids', type=int, nargs='+', required=True,
                        help='要审查的GitLab项目ID列表')
    parser.add_argument('--branches', type=str, nargs='+', default=['master'],
                        help='要审查的分支列表（默认为master）')
    parser.add_argument('--ai-api-url', type=str, required=True,
                        help='AI模型API的URL')
    parser.add_argument('--ai-api-key', type=str, required=True,
                        help='AI模型API的访问密钥')
    parser.add_argument('--output-dir', type=str, default='code_review_results',
                        help='存储审查结果的目录')
    parser.add_argument('--email-to', type=str, required=True,
                        help='接收报告的邮箱地址')
    parser.add_argument('--email-from', type=str, required=True,
                        help='发送报告的邮箱地址')
    parser.add_argument('--smtp-server', type=str, required=True,
                        help='SMTP服务器地址')
    parser.add_argument('--smtp-port', type=int, default=587,
                        help='SMTP服务器端口（默认为587）')
    parser.add_argument('--smtp-username', type=str, required=True,
                        help='SMTP用户名')
    parser.add_argument('--smtp-password', type=str, required=True,
                        help='SMTP密码')

    return parser.parse_args()

def main():
    """协调代码审查过程的主函数。"""
    args = parse_arguments()

    # 如果输出目录不存在，则创建它
    os.makedirs(args.output_dir, exist_ok=True)

    # 如果提供了多个项目，将项目ID映射到分支
    project_branch_map = {}
    if len(args.project_ids) == len(args.branches):
        project_branch_map = dict(zip(args.project_ids, args.branches))
    else:
        # 如果分支数量与项目数量不匹配，
        # 则为所有项目使用第一个分支
        project_branch_map = {pid: args.branches[0] for pid in args.project_ids}

    try:
        # 步骤1：从GitLab下载文件
        logger.info("开始从GitLab下载文件")
        downloader = GitLabDownloader(
            gitlab_url=args.gitlab_url,
            private_token=args.gitlab_token,
            output_dir=os.path.join(args.output_dir, 'downloaded_code')
        )

        downloaded_files = downloader.download_repositories(project_branch_map)
        logger.info(f"从GitLab下载了 {len(downloaded_files)} 个文件")

        # 步骤2：使用AI审查代码
        logger.info("开始AI代码审查")
        reviewer = AIReviewer(
            api_url=args.ai_api_url,
            api_key=args.ai_api_key
        )

        review_results = {}
        for file_path in downloaded_files:
            try:
                logger.info(f"审查文件: {file_path}")
                review_result = reviewer.review_file(file_path)
                review_results[file_path] = review_result
            except Exception as e:
                logger.error(f"审查文件 {file_path} 时出错: {str(e)}")

        # 步骤3：生成Markdown报告
        logger.info("生成Markdown报告")
        report_generator = ReportGenerator(
            output_dir=os.path.join(args.output_dir, 'reports')
        )

        report_files = report_generator.generate_reports(review_results)
        consolidated_report = report_generator.consolidate_reports(report_files)

        # 步骤4：发送合并后的报告邮件
        logger.info("发送合并报告的邮件")
        email_sender = EmailSender(
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            username=args.smtp_username,
            password=args.smtp_password
        )

        email_sender.send_report(
            from_email=args.email_from,
            to_email=args.email_to,
            subject=f"代码审查报告 - {datetime.now().strftime('%Y-%m-%d')}",
            report_path=consolidated_report
        )

        logger.info("代码审查过程成功完成")

    except Exception as e:
        logger.error(f"代码审查过程中出错: {str(e)}")
        raise

if __name__ == "__main__":
    main()
