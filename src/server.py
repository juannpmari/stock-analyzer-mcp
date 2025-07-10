from mcp.server.fastmcp import FastMCP
from tools.analysis import analysis_mcp
from tools.market_data import market_data_mcp

mcp = FastMCP("Market analyzer")

mcp.mount("market_data", market_data_mcp)
mcp.mount("analysis", analysis_mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")
