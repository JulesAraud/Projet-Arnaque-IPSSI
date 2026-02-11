class MCPServer:

    def __init__(self):
        self.tools = {}

    def register_tool(self, name, fn):
        self.tools[name] = fn

    def call(self, name):
        if name in self.tools:
            return self.tools[name]()
        return None
