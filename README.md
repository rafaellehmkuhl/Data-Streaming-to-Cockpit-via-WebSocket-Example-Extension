# BlueOS WebSocket Streamer Extension

An example BlueOS extension demonstrating how to create a WebSocket server that exposes data-lake variables for Cockpit to consume.

This extension runs a minimal WebSocket server that streams various test variables at 10Hz for Cockpit to consume via its data-lake.

## Variables Streamed

| Variable | Description |
|----------|-------------|
| `test-connection-status` | Connection status (sent once on connect) |
| `test-counter` | Incrementing counter |
| `test-random` | Random integer 0-99 |
| `test-sine` | Sine wave value |
| `test-boolean` | Alternating true/false |
| `test-timestamp` | Current timestamp (ms) |
| `test-quoted-string` | Quoted string cycling through different value types |

## Installation

1. Build the Docker image or install via BlueOS Extension Manager
2. Enable the extension in BlueOS

## WebSocket Endpoint

```
ws://<blueos-ip>:8765
```
