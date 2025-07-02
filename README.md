# MCP_Voice
MCP starter - voice and chat functionality with MCP boiler-plate potential
{
  `path`: `C:\\Users\\Josh\\Desktop\\MCP_Assistant\\MCP_Voice\\README.md`,
  `content`: `# MCP_Voice

MCP starter project with voice and chat functionality, featuring AI tool calling capabilities. Includes weather queries, mathematical calculations, and voice responses.

## Features
- 🎤 Voice input and audio responses
- 💬 Text chat interface
- 🔧 Tool calling (weather, calculator)
- 🤖 Multiple AI model support via Ollama
- 🐳 Docker containerization

## Dependencies

### Required
- **Ollama**: Download from [https://ollama.com/download](https://ollama.com/download)
- **Docker**: Download from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

## Setup Instructions

### 1. Install and Configure Ollama
```bash
# Install Ollama, then pull a compatible model
ollama pull qwq:32b
# Alternative models that work well:
# ollama pull deepseek-coder:6.7b
# ollama pull llama3.2:latest
```

### 2. Build and Run with Docker
```bash
# In the MCP_Voice project directory
docker build -t mcp-voice .
docker run -d --name mcp-voice-new -p 8000:8000 mcp-voice
```

### 3. Access the Interface
- Open `index.html` in your browser, or
- Navigate to `http://localhost:8000`

## Usage

### Text Chat
Type questions like:
- \"What's the weather in London?\"
- \"Calculate 25 + 17\"
- \"What's 15 times 8?\"

### Voice Input
1. Click the \"Voice\" tab
2. Use \"Start Recording\" to capture audio
3. Try auto-transcription or manual transcription
4. Send your message

## Current Configuration
- **Model**: qwq:32b (reasoning model with good tool calling)
- **Tools**: Weather API, Calculator
- **Audio**: Google Text-to-Speech (gTTS)

## Troubleshooting

### Common Issues
1. **Ollama connection**: Ensure Ollama is running (`ollama serve`)
2. **Docker networking**: Container uses `host.docker.internal:11434` to reach Ollama
3. **Model not found**: Pull the required model with `ollama pull qwq:32b`

### Logs
```bash
# View container logs
docker logs -f mcp-voice-new

# Check if Ollama is accessible
curl http://localhost:11434/api/tags
```

## Development

### File Structure
```
MCP_Voice/
├── mcp_server/          # Python backend
├── index.html           # Frontend interface
├── app.js              # Frontend JavaScript
├── Dockerfile          # Container configuration
└── requirements files   # Python dependencies
```

### Tool Calling
The system automatically detects intent and calls appropriate tools:
- Weather queries → Weather API
- Math questions → Calculator
- Results integrated into natural language responses
`
}