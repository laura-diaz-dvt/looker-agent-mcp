from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000") #edit with your url

tools = toolbox.load_toolset('looker_tools')

# To import only one tool
# tools = toolbox.load_tool('make_dashboard')

root_agent = Agent(
    model='gemini-2.5-flash',
    name='looker_agent',
    description = "Assistant that helps explore and analyze data in Looker using MCP Toolbox.",
    instruction = "Answer user questions by using Looker MCP Toolbox tools to explore models, run queries, and manage dashboards/looks.",
    tools=tools,
)
