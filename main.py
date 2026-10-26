#!/usr/bin/env python3
"""MCP server for vpsretainer - VPS Hosting Retainer"""

import json
import os
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("mcp-vpsretainer")

# Simulated data
VPS_INVENTORY = {
    "vps-001": {
        "id": "vps-001",
        "name": "Web Server 1",
        "provider": "DigitalOcean",
        "ip": "1.2.3.4",
        "ssh_port": 22,
        "username": "root",
        "ssh_key_path": "~/.ssh/id_rsa",
        "os": "Debian 12",
        "caddy_version": "2.7.5",
        "status": "active",
        "created_at": "2024-01-15T10:00:00",
        "last_check": "2024-12-25T10:00:00"
    },
    "vps-002": {
        "id": "vps-002",
        "name": "API Server",
        "provider": "Linode",
        "ip": "5.6.7.8",
        "ssh_port": 22,
        "username": "root",
        "ssh_key_path": "~/.ssh/id_rsa",
        "os": "Ubuntu 22.04",
        "caddy_version": "2.7.5",
        "status": "maintenance",
        "created_at": "2024-03-10T10:00:00",
        "last_check": "2024-12-25T09:00:00"
    },
    "vps-003": {
        "id": "vps-003",
        "name": "Database Server",
        "provider": "Hetzner",
        "ip": "9.10.11.12",
        "ssh_port": 22,
        "username": "root",
        "ssh_key_path": "~/.ssh/id_rsa",
        "os": "Debian 12",
        "caddy_version": "2.7.5",
        "status": "active",
        "created_at": "2024-06-01T10:00:00",
        "last_check": "2024-12-25T10:30:00"
    }
}

SERVICES = {
    "svc-001": {
        "id": "svc-001",
        "vps_id": "vps-001",
        "name": "Main Website",
        "type": "caddy",
        "config": {"domain": "example.com", "email": "admin@example.com"},
        "status": "running",
        "port": 443,
        "domain": "example.com"
    },
    "svc-002": {
        "id": "svc-002",
        "vps_id": "vps-001",
        "name": "API Gateway",
        "type": "docker",
        "config": {"image": "nginx:latest", "port": 8080},
        "status": "running",
        "port": 8080,
        "domain": "api.example.com"
    },
    "svc-003": {
        "id": "svc-003",
        "vps_id": "vps-002",
        "name": "Database",
        "type": "systemd",
        "config": {"service": "postgresql"},
        "status": "stopped",
        "port": 5432,
        "domain": ""
    }
}

app = Server("mcp-vpsretainer")

TOOLS = [
    Tool(
        name="get_vps_health",
        description="Get VPS health status",
        inputSchema={
            "type": "object",
            "properties": {
                "vps_id": {"type": "string", "description": "VPS identifier"}
            },
            "required": ["vps_id"]
        }
    ),
    Tool(
        name="get_metrics",
        description="Get VPS metrics (CPU, memory, disk, network)",
        inputSchema={
            "type": "object",
            "properties": {
                "vps_id": {"type": "string", "description": "VPS identifier"}
            },
            "required": ["vps_id"]
        }
    ),
    Tool(
        name="get_alerts",
        description="Get alerts for a VPS",
        inputSchema={
            "type": "object",
            "properties": {
                "vps_id": {"type": "string", "description": "VPS identifier"}
            },
            "required": ["vps_id"]
        }
    )
]

app = Server("mcp-vpsretainer")

@app.list_tools()
async def list_tools():
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_vps_health":
        vps_id = arguments.get("vps_id")
        
        vps = VPS_INVENTORY.get(vps_id)
        if not vps:
            return [TextContent(type="text", text=json.dumps({"error": f"VPS not found: {vps_id}"}))]
        
        # Simulate health check
        import random
        cpu_usage = round(10 + random.random() * 70, 1)
        memory_usage = round(20 + random.random() * 60, 1)
        disk_usage = round(30 + random.random() * 50, 1)
        
        health = "healthy"
        if cpu_usage > 80 or memory_usage > 85 or disk_usage > 90:
            health = "warning"
        if cpu_usage > 95 or memory_usage > 95:
            health = "critical"
        
        result = {
            "status": "ok",
            "tool": "get_vps_health",
            "vps": {
                "id": vps["id"],
                "name": vps["name"],
                "provider": vps["provider"],
                "ip": vps["ip"],
                "os": vps["os"],
                "status": vps["status"],
                "health": health,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
                "uptime_days": 45,
                "last_check": datetime.now().isoformat()
            }
        }
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "get_metrics":
        vps_id = arguments.get("vps_id")
        
        vps = VPS_INVENTORY.get(vps_id)
        if not vps:
            return [TextContent(type="text", text=json.dumps({"error": f"VPS not found: {vps_id}"}))]
        
        import random
        metrics = {
            "cpu": {
                "usage_percent": round(10 + random.random() * 70, 1),
                "cores": 4,
                "load_average": [round(0.5 + random.random() * 2, 2) for _ in range(3)]
            },
            "memory": {
                "total_gb": 8,
                "used_gb": round(2 + random.random() * 4, 1),
                "usage_percent": round(25 + random.random() * 50, 1)
            },
            "disk": {
                "total_gb": 160,
                "used_gb": round(40 + random.random() * 60, 1),
                "usage_percent": round(30 + random.random() * 40, 1)
            },
            "network": {
                "rx_mbps": round(random.random() * 100, 1),
                "tx_mbps": round(random.random() * 50, 1)
            },
            "collected_at": datetime.now().isoformat()
        }
        
        return [TextContent(type="text", text=json.dumps({"status": "ok", "tool": "get_metrics", "vps_id": vps_id, "metrics": metrics}))]
    
    elif name == "get_alerts":
        vps_id = arguments.get("vps_id")
        
        vps = VPS_INVENTORY.get(vps_id)
        if not vps:
            return [TextContent(type="text", text=json.dumps({"error": f"VPS not found: {vps_id}"}))]
        
        # Simulated alerts
        import random
        alerts = []
        if random.random() < 0.3:
            alerts.append({
                "id": f"alert-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "cpu_high",
                "severity": "warning",
                "message": "CPU usage above 80%",
                "timestamp": datetime.now().isoformat()
            })
        if random.random() < 0.2:
            alerts.append({
                "id": f"alert-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "disk_space",
                "severity": "warning",
                "message": "Disk usage above 85%",
                "timestamp": datetime.now().isoformat()
            })
        
        return [TextContent(type="text", text=json.dumps({
            "status": "ok",
            "tool": "get_alerts",
            "vps_id": vps_id,
            "alerts": alerts,
            "checked_at": datetime.now().isoformat()
        }))]
    
    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def serve():
        reader, writer = await stdio_server()
        await app.run(reader, writer)
    
    asyncio.run(serve())