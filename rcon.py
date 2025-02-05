# server.py
import subprocess
from typing import Optional
# from enum import Enum
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Minecraft Admin")


@mcp.tool()
def rcon(command: str) -> str:
    """Issue commands to the Minecraft server via RCON. Best practices and common patterns include:

## Player Location & Building
1. ALWAYS get player coordinates first before building:
   - `data get entity player_name Pos`
   - This returns coordinates in format: [X.XXd, Y.XXd, Z.XXd]
   - Store these coordinates and use them as the base for building

2. Building Commands:
   - Direct placement: `setblock x y z block_type`
   - Fill command: `fill x1 y1 z1 x2 y2 z2 block_type [replace|keep|outline|hollow]`
   - Clone command: `clone x1 y1 z1 x2 y2 z2 dest_x dest_y dest_z`

3. Entity Commands:
   - Summon entities: `summon <entity_type> <x> <y> <z>`
   - Teleport entities: `tp @e[type=<entity_type>] <x> <y> <z>`
   - Execute as entities: `execute as @e[type=<entity_type>] at @s run <command>`

4. View/Perspective Commands:
   - Teleport to location: `tp @p x y z`
   - Spectate entity: `spectate <target> [player]`
   - Execute from position: `execute positioned x y z run <command>`

## Common Command Patterns
Item Commands:
- give rgbkrk coal 12
- give rgbkrk iron_axe[enchantments={levels:{"minecraft:sharpness":5,"minecraft:efficiency":5,"minecraft:fortune":5}}] 1 
- give @a iron_pickaxe[unbreakable={}] 

Effect Commands:
- effect give @a speed 300 2 
- effect give LoganTheParrot minecraft:night_vision 1000 1 
- effect give rgbkrk water_breathing infinite 1 true

Potion Commands:
- Basic item: give rgbkrk potion[minecraft:potion_contents={potion:"minecraft:fire_resistance"}]
- Multiple items: give rgbkrk potion[minecraft:potion_contents={potion:"minecraft:strength"}] 5
- Splash/lingering variants: give rgbkrk splash_potion[minecraft:potion_contents={potion:"minecraft:poison"}]

## Targeting Players
- Use `@a` for all players
- Use a player name to target a specific player (e.g. rgbkrk)
- Can get specific player coordinates: `data get entity player_name Pos`
- Position returns format: [X.XXd, Y.XXd, Z.XXd]

## Block Placement Best Practices
1. Get player coordinates first
2. Calculate relative positions from stored coordinates
3. Build structures using absolute coordinates
4. Test for block type existence before using (some modded blocks may not exist)

## Block States
- Use square brackets for block states: `block_type[property=value]`
- Example: `lantern[hanging=true]`
- Multiple properties use comma separation

## Relative vs Absolute Coordinates
- Absolute: Uses exact coordinates (x y z)
- Relative to player: Uses tilde notation (~)
  - `~` means current position
  - `~1` means one block offset
  - `~-1` means one block negative offset

## Common Gotchas
- NEVER build large structures relative to the player's current position. GET the location needed first.
- RCON needs player context for certain commands like `locate`
- Block placement might need block states specified
- Fill commands include both start and end coordinates
- Coordinates are exclusive (e.g., ~0 to ~15 creates a 16-block span)
- Test for block existence before using modded or unusual blocks
    
    """
    return subprocess.check_output(["docker", "exec", "mc", "rcon-cli", command]).decode("utf-8")


@mcp.tool()
def list_players() -> str:
    """List all currently connected players on the Minecraft server."""
    return rcon("list")


@mcp.tool()
def help(command: Optional[str] = None) -> str:
    """Get help for Minecraft commands."""
    return rcon(f"help {command}" if command else "help")


# class WeatherType(Enum):
#     CLEAR = "clear"
#     RAIN = "rain"
#     THUNDER = "thunder"

# @mcp.tool()
# def weather(type: WeatherType = WeatherType.CLEAR) -> str:
#     """Set the weather in the Minecraft world.
    
#     Args:
#         type: Weather type (clear, rain, thunder)
#     """
#     return rcon(f"weather {type.value}")


@mcp.tool()
def server_stats() -> str:
    """Get server statistics including CPU, memory usage, and uptime."""
    try:
        stats = subprocess.check_output(
            ["docker", "stats", "mc", "--no-stream", "--format", "{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"]
        ).decode("utf-8").strip()
        return f"Server Stats:\n{stats}"
    except subprocess.CalledProcessError as e:
        return f"Error getting server stats: {str(e)}"

@mcp.tool()
def server_logs(lines: int = 10) -> str:
    """Get recent server logs.
    
    Args:
        lines: Number of recent log lines to fetch (default: 10)
    """
    try:
        logs = subprocess.check_output(
            ["docker", "logs", "--tail", str(lines), "mc"]
        ).decode("utf-8")
        return logs
    except subprocess.CalledProcessError as e:
        return f"Error fetching logs: {str(e)}"

@mcp.tool()
def check_server_status() -> str:
    """Check if the Minecraft server is running and responsive."""
    try:
        status = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Status}}", "mc"]
        ).decode("utf-8").strip()
        
        if status == "running":
            # Try to execute a simple rcon command to verify server is responsive
            try:
                response = rcon("list")
                return f"Server is running and responsive.\nStatus: {status}\n{response}"
            except Exception as _:
                return f"Server is running but may not be fully initialized.\nStatus: {status}"
        else:
            return f"Server is not running. Status: {status}"
    except subprocess.CalledProcessError as e:
        return f"Error checking server status: {str(e)}"