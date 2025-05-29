# RDM - 自动化代码审查系统

## 项目概述
RDM是一个自动化代码审查工具，主要功能包括从GitLab下载代码、使用AI进行代码审查、生成Markdown格式的审查报告以及发送邮件通知。旨在提高代码审查效率和质量。

### 主要特性
- GitLab代码下载与集成
- AI驱动的代码分析与审查
- 可定制的报告生成
- 邮件通知系统
- 支持多种项目类型分析

## 目录结构
```
rdm/
├── ai-review/          # 核心模块
│   ├── code_review_orchestrator.py  # 主流程控制
│   ├── gitlab_downloader.py         # GitLab集成
│   └── test_code_review.py          # 单元测试
├── daily/             # 日常数据处理脚本
└── nginx-data-analysis/  # 日志分析工具
```

## 安装指南

### 使用pip安装
```bash
pip install -r requirements.txt
```

### 使用Poetry安装（推荐）
```bash
poetry install
```

### 环境变量配置
需要设置以下环境变量：
- `GITLAB_TOKEN`: GitLab访问令牌
- `AI_API_URL`: AI服务端点
- `AI_API_KEY`: AI服务密钥
- `EMAIL_CONFIG`: 邮件服务器配置

## 使用说明

### 快速开始
```bash
python -m rdm.ai-review.code_review_orchestrator \
  --gitlab-token your_token \
  --project-ids 270 \
  --ai-api-url AI_ENDPOINT \
  --ai-api-key AI_KEY \
  --email-to report@example.com
```

### 命令行参数
| 参数 | 描述 | 必填 |
|------|------|------|
| --gitlab-token | GitLab访问令牌 | 是 |
| --project-ids | 要审查的项目ID | 是 |
| --ai-api-url | AI服务URL | 是 |
| --ai-api-key | AI服务密钥 | 是 |
| --email-to | 报告接收邮箱 | 否 |

### 典型工作流程
1. 从GitLab下载指定项目代码
2. 使用AI服务分析代码
3. 生成Markdown格式审查报告
4. 发送报告到指定邮箱

## 开发指南

### 模块架构
- `gitlab_downloader.py`: 处理GitLab API交互
- `ai_reviewer.py`: 封装AI审查逻辑
- `report_generator.py`: 报告生成器
- `email_sender.py`: 邮件通知模块

### 运行测试
```bash
python -m pytest rdm/ai-review/test_code_review.py
```

## 贡献指南
欢迎通过Pull Request贡献代码，请确保：
- 遵循PEP8代码风格
- 添加适当的单元测试
- 更新相关文档

## 其他信息
- 许可证: MIT
- 联系方式: 项目维护者邮箱