# BananaPY - BananAPI Lib for Python

This wrapper is made to support the API of https://bananapi.ml.

Please visit that website to get details on getting an API key and documentation.

**Notes**

- Join the [official Discord server](https://discord.gg/3Nxb7yZ) for more help.

- This wrapper is still early in production and may contain bugs. Please report them to the Discord server above.

**Installing**

Run on your Command Prompt:

`pip install -U bananapy`

**Usage Example**

```py
import bananapy

client = bananapy.Client("token")
# Using abandon endpoint
await client.abandon("I love fortnite") # returns the Buffer
```