import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
const server = new McpServer({ name: "ambiguous", version: "0.0.1" });
server.tool("lookup", "Lookup data; implementation delegated", async ({ q }) => ({ content: [{ type: "text", text: q }] }));
// Transport and auth are injected by deployment configuration.
