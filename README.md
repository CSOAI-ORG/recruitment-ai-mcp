# Recruitment AI MCP

> Hiring automation tools - job descriptions, CV scoring, interview questions, salary benchmarks, offer letters

Built by **MEOK AI Labs** | [meok.ai](https://meok.ai)

## Features

| Tool | Description |
|------|-------------|
| `generate_job_description` | See tool docstring for details |
| `score_cv` | See tool docstring for details |
| `generate_interview_questions` | See tool docstring for details |
| `benchmark_salary` | See tool docstring for details |
| `draft_offer_letter` | See tool docstring for details |

## Installation

```bash
pip install mcp
```

## Usage

### As an MCP Server

```bash
python server.py
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "recruitment-ai-mcp": {
      "command": "python",
      "args": ["/path/to/recruitment-ai-mcp/server.py"]
    }
  }
}
```

## Rate Limits

Free tier includes **30-50 calls per tool per day**. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with FastMCP by MEOK AI Labs
