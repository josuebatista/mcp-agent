# MCP Agent for Airbnb

This repository contains Python scripts that leverage the Model Control Protocol (MCP) to interact with Airbnb's services and process listing data using Anthropic's Claude AI.

## Scripts Overview

- **simple-mcp-airbnb-v0.py**: Basic implementation that searches for Airbnb listings in Paris with debugging code to examine the response structure.

- **simple-mcp-airbnb-v1.py**: Simplified version that performs an Airbnb search for Paris listings and displays the raw results.

- **mcp-agent-airbnb-claude.py**: Advanced implementation that:
  - Searches for Airbnb listings in Alexandria, VA
  - Processes search results using Claude AI to create terminal-friendly output
  - Includes a Python-based formatter as an alternative to AI processing

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js and npm

### Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd mcp-agent
   ```

2. Install Python dependencies:
   ```
   pip install mcp-python-client anthropic
   ```

3. Install the Airbnb MCP server:
   ```
   npm install -g @openbnb/mcp-server-airbnb
   ```

### Environment Setup

Set up your Anthropic API key as an environment variable:

```bash
# For Linux/macOS
export ANTHROPIC_API_KEY="your-api-key-here"

# For Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# For Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

For persistent setup, add this to your shell profile (.bashrc, .zshrc, etc.).

## Usage

Run any of the scripts directly with Python:

```bash
# Basic Airbnb search example
python simple-mcp-airbnb-v1.py

# Advanced search with Claude processing
python mcp-agent-airbnb-claude.py
```

## Customizing Searches

To customize your search parameters, modify the arguments in the `run_airbnb_search` function call:

```python
search_results = await run_airbnb_search(
    location="Your desired location",
    check_in="YYYY-MM-DD",
    check_out="YYYY-MM-DD",
    min_price="100",  # Optional
    max_price="500",  # Optional
    adults=2
)
```

## Troubleshooting

- **MCP Server Connection Issues**: Ensure the npm package `@openbnb/mcp-server-airbnb` is correctly installed
- **Claude API Errors**: Verify your ANTHROPIC_API_KEY is correctly set and valid
- **JSON Parsing Errors**: The Airbnb API response format may change; check the response structure if errors occur

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.