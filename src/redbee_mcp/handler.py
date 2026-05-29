"""
Main handler for MCP requests.
Extracts business logic to enable reuse in both stdio and HTTP modes.
"""

import logging
from typing import List, Optional

from mcp.types import TextContent, Tool

from .logging_config import sanitize_for_log
from .models import RedBeeConfig
from .tool_dispatch import TOOL_HANDLERS
from .tools.auth import AUTH_TOOLS
from .tools.content import CONTENT_TOOLS
from .tools.purchases import PURCHASES_TOOLS
from .tools.system import SYSTEM_TOOLS
from .tools.user_management import USER_MANAGEMENT_TOOLS

logger = logging.getLogger(__name__)


class McpHandler:
    """Main handler for all MCP requests (stdio and HTTP modes)."""

    def __init__(self, config: Optional[RedBeeConfig] = None):
        self.config = config or RedBeeConfig.from_env()

    async def list_tools(self) -> List[Tool]:
        """List all available MCP tools for Red Bee Media."""
        tools: List[Tool] = []
        tools.extend(AUTH_TOOLS)
        tools.extend(CONTENT_TOOLS)
        tools.extend(USER_MANAGEMENT_TOOLS)
        tools.extend(PURCHASES_TOOLS)
        tools.extend(SYSTEM_TOOLS)
        logger.info("Red Bee MCP: %s available tools", len(tools))
        return tools

    async def call_tool(self, name: str, arguments: dict) -> List[TextContent]:
        """Dispatch a tool call to the registered handler."""
        if not self.config.customer or not self.config.business_unit:
            return [
                TextContent(
                    type="text",
                    text=(
                        "Missing configuration: REDBEE_CUSTOMER and REDBEE_BUSINESS_UNIT are required.\n\n"
                        "Configure them in mcp.json or as environment variables."
                    ),
                )
            ]

        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        args = arguments or {}
        try:
            logger.info(
                "Red Bee MCP: calling tool '%s' with arguments: %s",
                name,
                sanitize_for_log(args),
            )
            return await handler(self.config, args)
        except KeyError as exc:
            logger.error("Missing argument for tool %s: %s", name, exc)
            return [
                TextContent(
                    type="text",
                    text=f"Error executing tool {name}: missing required argument '{exc.args[0]}'",
                )
            ]
        except Exception as exc:
            logger.error("Error executing tool %s: %s", name, exc)
            return [TextContent(type="text", text=f"Error executing tool {name}: {exc}")]
