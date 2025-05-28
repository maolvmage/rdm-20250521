rdm/
├── ai-review/          # 核心模块
│   ├── code_review_orchestrator.py  # 主流程控制
│   ├── gitlab_downloader.py         # GitLab集成
│   └── test_code_review.py          # 单元测试
├── daily/             # 日常数据处理脚本
└── nginx-data-analysis/  # 日志分析工具# 自动化代码审查系统

## 功能概述
- GitLab代码下载（<mcfile name="gitlab_downloader.py" path="rdm/ai-review/gitlab_downloader.py"></mcfile>）
- AI代码审查（<mcfile name="ai_reviewer.py" path="rdm/ai-review/ai_reviewer.py"></mcfile>）
- Markdown报告生成（<mcfile name="report_generator.py" path="rdm/ai-review/report_generator.py"></mcfile>）
- 邮件通知（<mcfile name="email_sender.py" path="rdm/ai-review/email_sender.py"></mcfile>）

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python -m rdm.ai-review.code_review_orchestrator \
  --gitlab-token your_token \
  --project-ids 270 \
  --ai-api-url AI_ENDPOINT \
  --ai-api-key AI_KEY \
  --email-to report@example.com