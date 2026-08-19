# MCP Release Readiness — Research Notes

_Date: 2026-08-19_

## Baseline reviewed

This product uses the MCP **2026-07-28** specification as a checklist baseline. It reports heuristic alignment signals and never certifies security, compliance, or legal conformity.

## Findings

The official transport specification defines stdio and Streamable HTTP. Stdio carries newline-delimited JSON-RPC over a client-launched subprocess. Streamable HTTP sends each message as an HTTP POST to one MCP endpoint, with a JSON or request-scoped SSE response. The 2026-07-28 release makes the protocol core stateless and retires the required `initialize`/`initialized` exchange and `Mcp-Session-Id` on the new path. Requests carry protocol metadata in `_meta` and may use `server/discover` for optional discovery.

The release formally deprecates legacy HTTP+SSE, with a minimum twelve-month window. It also deprecates Dynamic Client Registration for new implementations in favor of Client ID Metadata Documents (CIMD), while preserving compatibility fallback. Streamable HTTP adds `Mcp-Method` and `Mcp-Name` headers, and list responses can carry cache hints.

Enterprise-Managed Authorization (EMA) centralizes MCP access policy in the enterprise identity provider. The client declares extension support, authenticates through enterprise SSO, obtains an Identity Assertion JWT Authorization Grant (ID-JAG), and exchanges it with the MCP authorization server. A server-side review should check issuer, audience, signature, expiry, scope and claims validation. EMA is opt-in and client support varies.

The official Python and TypeScript SDK repositories expose server constructors, tool/resource registration, stdio and Streamable HTTP transports, and authorization integration points. The official servers repository provides reference implementations. Cloudflare’s MCP v2 material demonstrates stateless handlers and OAuth provider metadata. These patterns justify repository-wide static lexical evidence collection rather than executing customer code.

## Safety and limitations

The analyzer is local-only and read-only. It does not import, execute, attack, or mutate the target repository; it does not contact remote MCP endpoints; it cannot prove runtime behavior or resolve every framework abstraction. A non-demo scan requires the explicit `--i-have-authorization` flag, representing written owner consent. The report is a triage checklist, not a security verdict.

## References

[1] [MCP 2026-07-28 transport specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)

[2] [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)

[3] [Enterprise-Managed Authorization](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization)

[4] [Cloudflare: The next generation of MCP](https://blog.cloudflare.com/mcp-v2/)

[5] [Official Python SDK](https://github.com/modelcontextprotocol/python-sdk)

[6] [Official TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

[7] [Official MCP servers repository](https://github.com/modelcontextprotocol/servers)
