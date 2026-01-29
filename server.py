#!/usr/bin/env python3
"""
BlueOS WebSocket Extension - Data Lake Variable Streamer

This extension demonstrates how to create a WebSocket server that streams
data-lake variables to Cockpit. Cockpit connects to this server via its
"Generic WebSocket Connections" feature and automatically populates the
Data Lake with the received variables.

Data Format:
    Cockpit expects messages in the format: variableName=variableValue
    - Numbers: test-counter=42
    - Floats: test-sine=0.707
    - Booleans: test-boolean=true
    - Strings: test-string=This is a string.
    - Strings: test-quoted-string="99"

Architecture:
    - The server uses asyncio for non-blocking I/O
    - Each client connection spawns its own handler coroutine
    - Multiple clients can connect simultaneously
    - Disconnections are handled gracefully without affecting other clients
"""

import asyncio
import math
import random
import time

import websockets
from websockets.exceptions import ConnectionClosed

# Test values for the quoted string variable - demonstrates that Cockpit
# correctly handles quoted strings even when they look like other types
QUOTED_VALUES = ["123", "true", "false", "456.789", "hello world", "0", ""]


async def handler(websocket):
    """
    Handle a single WebSocket client connection.

    This coroutine is spawned automatically by the websockets library
    for each new client connection. It runs independently, so multiple
    clients can be served concurrently.

    The handler sends various test variables at 10Hz to demonstrate
    different data types that Cockpit's Data Lake can handle.

    Args:
        websocket: The WebSocket connection object provided by the library.
                   Used to send messages and check connection state.
    """
    print(f"Client connected: {websocket.remote_address}")

    # Send an initial status variable so Cockpit knows the connection succeeded
    await websocket.send("test-connection-status=connected")

    counter = 0
    try:
        while True:
            counter += 1

            # Integer: simple incrementing counter
            await websocket.send(f"test-counter={counter}")

            # Integer: random value between 0-99
            await websocket.send(f"test-random={random.randint(0, 99)}")

            # Float: sine wave oscillating between -1 and 1
            # The 0.1 multiplier controls the wave frequency
            await websocket.send(f"test-sine={math.sin(counter * 0.1):.3f}")

            # Boolean: alternates between true/false each tick
            await websocket.send(f"test-boolean={str(counter % 2 == 0).lower()}")

            # Integer: Unix timestamp in milliseconds
            await websocket.send(f"test-timestamp={int(time.time() * 1000)}")

            # String: a simple string
            await websocket.send(f"test-string=This is a string.")

            # Quoted string: cycles through different values to test string handling
            # Values in quotes are always treated as strings, even if they look like numbers
            quoted_value = QUOTED_VALUES[counter % len(QUOTED_VALUES)]
            await websocket.send(f'test-quoted-string="{quoted_value}"')

            # Log progress every second (every 10th tick at 10Hz)
            if counter % 10 == 0:
                print(f"Sent all 6 variables to {websocket.remote_address} (tick #{counter})")

            # Sleep for 100ms = 10 updates per second (10 Hz)
            await asyncio.sleep(0.1)

    except ConnectionClosed:
        # Client disconnected - this is normal behavior, not an error
        # The handler simply exits and the coroutine is cleaned up
        print(f"Client disconnected: {websocket.remote_address}")


async def main():
    """
    Start the WebSocket server and run forever.

    The server binds to 0.0.0.0 (all interfaces) so it can be reached
    from outside the Docker container. The port must match the one
    exposed in manifest.json.
    """
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        print("Sending test data at 10 Hz...")
        # Keep the server running indefinitely
        await asyncio.Future()


if __name__ == "__main__":
    # Entry point: run the async main function
    asyncio.run(main())
