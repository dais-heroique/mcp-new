from sse_starlette.sse import EventSourceResponse
import subprocess, requests
transport = SseServerTransport("/sse")
def register_client(metadata):
    return requests.post("/register", json=metadata)
def dangerous_tool(command):
    subprocess.run(command, shell=True)
