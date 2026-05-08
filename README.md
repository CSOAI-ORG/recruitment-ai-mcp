[![recruitment-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/recruitment-ai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/recruitment-ai-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/recruitment-ai-mcp)](https://pypi.org/project/recruitment-ai-mcp/)

[![recruitment-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/recruitment-ai-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/recruitment-ai-mcp)

<div align="center">

# Recruitment Ai MCP

**Recruitment AI MCP Server**

[![PyPI](https://img.shields.io/pypi/v/meok-recruitment-ai-mcp)](https://pypi.org/project/meok-recruitment-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Recruitment AI MCP Server
Hiring automation tools powered by MEOK AI Labs.

## Tools

| Tool | Description |
|------|-------------|
| `generate_job_description` | Generate a professional job description. |
| `score_cv` | Score and analyze a CV/resume against job requirements. |
| `generate_interview_questions` | Generate tailored interview questions for a role. |
| `benchmark_salary` | Get salary benchmarks for a role by level and location. |
| `draft_offer_letter` | Draft a professional offer letter for a candidate. |

## Installation

```bash
pip install meok-recruitment-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "recruitment-ai": {
      "command": "python",
      "args": ["-m", "meok_recruitment_ai_mcp.server"]
    }
  }
}
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
<!-- mcp-name: io.github.CSOAI-ORG/recruitment-ai-mcp -->
