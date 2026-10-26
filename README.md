# mcp-vpsretainer

MCP server for VPS Hosting Retainer - Managed Caddy/Debian ops.

## Tools

### get_vps_health
Get VPS health status including CPU, memory, disk usage.

**Parameters:**
- `vps_id` (string, required): VPS identifier

### get_metrics
Get detailed VPS metrics (CPU, memory, disk, network).

**Parameters:**
- `vps_id` (string, required): VPS identifier

### get_alerts
Get alerts for a VPS.

**Parameters:**
- `vps_id` (string, required): VPS identifier

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Connecting to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vpsretainer": {
      "command": "python",
      "args": ["/path/to/mcp-vpsretainer/main.py"],
      "cwd": "/path/to/mcp-vpsretainer"
    }
  }
}
```

## License

MIT