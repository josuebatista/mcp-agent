import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
)

async def run():
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Call the search tool
            result = await session.call_tool(
                "airbnb_search", 
                arguments={
                    "location": "Paris, France",
                    "checkIn": "2025-06-28",
                    "checkOut": "2025-06-30",
                    "adults": 2
                }
            )
            
            # Print the results
            print("\nSearch Results:")
            print(result.content)

if __name__ == "__main__":
    asyncio.run(run())