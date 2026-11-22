to debug and run the mcp inspector need to follow the below steps

First have uv installed using brew install uv/pip install uv

To test the server and get it run on mcp inspector run the below command:

     uv run fastmcp dev inspector main.py

To run the server use the below command:
    uv run fastmcp run main.py

As the servers which are on local can be connected to the clients both local and remote client for example claude desktop

To add our local mcp server on claude desktop or any mcp client use the below command:
    uv run fastmcp install claude-desktop main.py