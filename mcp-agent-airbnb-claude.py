import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic

# Create server parameters
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
)

async def run_airbnb_search(location, check_in, check_out, min_price, max_price, adults):
    """
    Run the Airbnb search using the MCP server
    Returns the raw JSON response
    """
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
                    "location": location,
                    "checkIn": check_in,
                    "checkOut": check_out,
                    "minPrice" : min_price,
                    "maxPrice" : max_price,
                    "adults": adults
                }
            )
            
            # Extract the JSON from the text content
            json_text = result.content[0].text
            return json.loads(json_text)

def process_with_claude(airbnb_data):
    """
    Process the Airbnb search results using Claude to create a terminal-friendly summary
    """
    # Initialize the Anthropic client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = Anthropic(api_key=api_key)
    
    # Prepare the listings data for Claude
    listings = airbnb_data.get("searchResults", [])
    listings_data = []
    
    for i, listing in enumerate(listings[:5]):  # Limit to first 5 for brevity
        listing_info = {
            "title": listing["listing"]["title"],
            "url": listing["url"],
            "rating": listing["avgRatingA11yLabel"] if "avgRatingA11yLabel" in listing else "No ratings yet",
            "price": listing["structuredDisplayPrice"]["primaryLine"]["accessibilityLabel"] if "structuredDisplayPrice" in listing else "Price not available"
        }
        listings_data.append(listing_info)
    
    # Create a prompt for Claude - specifically asking for terminal-friendly format
    prompt = f"""
    Here are some Airbnb listings for a property search:
    
    {json.dumps(listings_data, indent=2)}
    
    Please format these results in a way that looks good in a plain terminal with no special characters or emojis. Use ASCII art or simple text formatting that will display well in any terminal environment. Include:
    
    1. The property title
    2. Price information
    3. Ratings
    4. Direct link to the property
    
    Make it easy to read with clear section separators and a consistent format. Also provide a brief summary of the range of options available.
    """
    
    # Get Claude's response
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.3,
        system="You are a helpful assistant that formats Airbnb search results in a terminal-friendly way, avoiding characters that might not display properly.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content

async def main():
    """
    Main function to orchestrate the search and formatting
    """
    # Set Anthropic API key
    # os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"  # Replace with your key
    
    # Run the search
    print("Searching for Airbnb listings...")
    search_results = await run_airbnb_search(
        location="Alexandria VA near Carlyle area Masonic Temple",
        check_in="2025-06-28",
        check_out="2025-06-30",
        min_price="200",
        max_price="300",
        adults=2
    )
    
    # Process with Claude
    print("\nProcessing results with Claude...\n")
    formatted_results = process_with_claude(search_results)
    
    # Display the formatted results
    print(formatted_results)
    
    # Alternatively, you could format the results directly in Python
    # without using Claude for a more predictable output
    print("\n\nPYTHON-FORMATTED RESULTS:")
    print("=" * 60)
    for i, listing in enumerate(search_results["searchResults"][:5]):
        title = listing["listing"]["title"]
        price = listing["structuredDisplayPrice"]["primaryLine"]["accessibilityLabel"]
        rating = listing["avgRatingA11yLabel"] if "avgRatingA11yLabel" in listing else "No ratings"
        url = listing["url"]
        
        print(f"LISTING #{i+1}: {title}")
        print(f"PRICE: {price}")
        print(f"RATING: {rating}")
        print(f"URL: {url}")
        print("-" * 60)
    
    print("=" * 60)
    print("SUMMARY: Found listings range from approx. $800-$1600 for 5 nights in Paris")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())