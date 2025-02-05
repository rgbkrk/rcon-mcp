# Minecraft Docker MCP

An MCP server for Minecraft-in-Docker that enables AI interactions with a running Minecraft server using itzg's docker-minecraft-server container.

* Expose server administration to AI clients like Claude Desktop, Cursor, and Zed.
* Allow models to programmatically create minecraft builds in game

LLMs have largely been trained on `rcon` commands, so there's a wide breadth of ability inherent in just exposing `rcon` to the model.

If you're already using the `itzg/minecraft-server` docker image, this MCP server will allow you to interact with your server via clients like Claude Desktop, Cursor, and Zed. The only requirement is that `mc` is the name of the container.

## Prerequisites

- A running Minecraft server in a Docker container named `mc`
- RCON enabled and properly configured

```bash
docker run -d --name mc -p 25565:25565 -e EULA=TRUE itzg/minecraft-server
```

To ensure you're able to use this server, try running an `rcon` command to see if you get a response.

```bash
docker exec -it mc rcon "list"
```

If you get a response, you're all set! If you don't, please refer to the [itzg/docker-minecraft-server](https://github.com/itzg/docker-minecraft-server) repository for troubleshooting.

## MCP Integration

This MCP server leverages itzg's docker-minecraft-server container's built-in RCON functionality to interact with the Minecraft server. The container provides the `rcon` command within the running container, making it an ideal target for MCP interactions.

### Connecting to Claude Desktop

Clone this repository and install the `rcon.py` tool using the MCP CLI.

```
mcp install rcon.py
```