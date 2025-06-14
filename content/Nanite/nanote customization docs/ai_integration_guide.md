# AI Models and Applications Integration Guide for Nanite

This document provides a comprehensive guide for integrating AI models and applications into the Nanite Linux distribution. It details the process of selecting, configuring, and integrating various AI components to create a cohesive AI-powered operating system.

## AI Model Integration Strategy

Nanite's approach to AI model integration follows these key principles:

1. **Local-first processing**: Prioritize models that can run locally on user hardware
2. **Tiered model selection**: Provide models of varying sizes to accommodate different hardware capabilities
3. **Modular architecture**: Allow easy addition, removal, or updating of models
4. **Unified API access**: Provide consistent interfaces for applications to access AI capabilities

## Ollama Integration

Ollama serves as the primary framework for managing and running LLMs in Nanite. Here's how to integrate it into the build process:

### Installation and Configuration

The Ollama installation was already covered in the Live-build configuration with the `0100-install-ollama.hook.chroot` script. Let's enhance this integration with additional configuration:

Create `config/includes.chroot/etc/ollama/config`:

```json
{
  "models_path": "/usr/share/nanite/models",
  "gpu_layers": "auto",
  "cpu_threads": 4
}
```

### Model Preloading Script

Create `config/hooks/live/0110-preload-ollama-models.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Preloading essential LLM models..."

# Start Ollama service
systemctl start ollama

# Wait for service to be fully up
sleep 5

# Pull essential models
ollama pull mistral:latest
ollama pull phi3:mini
ollama pull llama3:8b

# Create a custom model with specific parameters for Nanite
cat > /tmp/nanite-assistant.modelfile << EOF
FROM mistral:latest
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
SYSTEM You are Nanite Assistant, an AI helper integrated into the Nanite Linux distribution. You help users with system tasks, development, and creative work. You run locally on the user's computer, respecting their privacy.
EOF

# Build the custom model
ollama create nanite-assistant -f /tmp/nanite-assistant.modelfile

echo "LLM models preloaded successfully."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0110-preload-ollama-models.hook.chroot
```

## LangChain Integration

LangChain provides a framework for building applications with LLMs. Let's integrate it into Nanite:

### Installation and Configuration

Create `config/hooks/live/0210-setup-langchain.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Setting up LangChain framework..."

# Install LangChain and related packages
pip3 install langchain langchain-community langchain-experimental langchainhub

# Create directory for LangChain templates
mkdir -p /usr/share/nanite/langchain/templates
chmod 755 /usr/share/nanite/langchain/templates

# Create a basic RAG template
cat > /usr/share/nanite/langchain/templates/basic_rag.py << EOF
#!/usr/bin/env python3
"""
Basic Retrieval-Augmented Generation (RAG) template for Nanite
"""
import sys
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA

def create_rag_from_text(file_path, query, model_name="nanite-assistant"):
    # Load document
    loader = TextLoader(file_path)
    documents = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(model="mistral")
    vectorstore = Chroma.from_documents(chunks, embeddings)
    
    # Create retriever
    retriever = vectorstore.as_retriever()
    
    # Create LLM
    llm = Ollama(model=model_name)
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    # Run query
    result = qa_chain.run(query)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python basic_rag.py <file_path> <query>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    query = sys.argv[2]
    
    result = create_rag_from_text(file_path, query)
    print(result)
EOF

chmod +x /usr/share/nanite/langchain/templates/basic_rag.py

# Create a symbolic link to make it accessible from PATH
ln -s /usr/share/nanite/langchain/templates/basic_rag.py /usr/local/bin/nanite-rag

echo "LangChain framework setup completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0210-setup-langchain.hook.chroot
```

## Text-to-Speech and Speech-to-Text Integration

Let's integrate speech capabilities using Whisper for speech recognition and Piper for text-to-speech:

### Installation and Configuration

Create `config/hooks/live/0220-setup-speech.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Setting up speech recognition and synthesis..."

# Install Whisper for speech recognition
pip3 install -U openai-whisper

# Install Piper for text-to-speech
pip3 install piper-tts

# Create directory for speech models
mkdir -p /usr/share/nanite/speech/models
chmod 755 /usr/share/nanite/speech/models

# Download a small Whisper model
python3 -c "import whisper; whisper.load_model('base')"

# Create a simple speech interface script
cat > /usr/local/bin/nanite-speech << EOF
#!/usr/bin/env python3
"""
Nanite Speech Interface - Provides speech recognition and synthesis
"""
import sys
import os
import argparse
import tempfile
import subprocess
import whisper

def transcribe_audio(audio_file):
    """Transcribe audio file to text using Whisper"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def synthesize_speech(text, output_file):
    """Convert text to speech using Piper"""
    with tempfile.NamedTemporaryFile(suffix='.txt') as temp:
        temp.write(text.encode('utf-8'))
        temp.flush()
        subprocess.run(["piper", "--model", "/usr/share/nanite/speech/models/en_US-lessac-medium.onnx", 
                       "--output_file", output_file, "--file", temp.name], check=True)

def main():
    parser = argparse.ArgumentParser(description="Nanite Speech Interface")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe audio to text")
    transcribe_parser.add_argument("audio_file", help="Path to audio file")
    
    # Synthesize command
    synthesize_parser = subparsers.add_parser("synthesize", help="Synthesize text to speech")
    synthesize_parser.add_argument("text", help="Text to synthesize")
    synthesize_parser.add_argument("--output", "-o", default="output.wav", help="Output audio file")
    
    args = parser.parse_args()
    
    if args.command == "transcribe":
        text = transcribe_audio(args.audio_file)
        print(text)
    elif args.command == "synthesize":
        synthesize_speech(args.text, args.output)
        print(f"Speech synthesized to {args.output}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
EOF

chmod +x /usr/local/bin/nanite-speech

echo "Speech recognition and synthesis setup completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0220-setup-speech.hook.chroot
```

## AI Assistant Integration

Let's create a system-wide AI assistant that can be accessed from any application:

### Installation and Configuration

Create `config/hooks/live/0300-setup-ai-assistant.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Setting up system-wide AI assistant..."

# Create directory for assistant
mkdir -p /usr/share/nanite/assistant
chmod 755 /usr/share/nanite/assistant

# Create the assistant service
cat > /usr/share/nanite/assistant/nanite-assistant-service.py << EOF
#!/usr/bin/env python3
"""
Nanite AI Assistant Service - Provides system-wide AI assistance
"""
import os
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from langchain_community.llms import Ollama

# Initialize the LLM
llm = Ollama(model="nanite-assistant")

class AssistantHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/health':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self._set_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/query':
            query = data.get('query', '')
            context = data.get('context', '')
            
            # Prepare prompt with context if provided
            prompt = query
            if context:
                prompt = f"Context: {context}\n\nQuery: {query}"
            
            # Get response from LLM
            response = llm(prompt)
            
            self._set_headers()
            self.wfile.write(json.dumps({"response": response}).encode())
        
        elif self.path == '/command':
            command = data.get('command', '')
            
            # Prepare prompt for command interpretation
            prompt = f"Interpret this command and convert it to a bash command that can be executed on a Linux system: '{command}'"
            
            # Get response from LLM
            response = llm(prompt)
            
            self._set_headers()
            self.wfile.write(json.dumps({"interpreted_command": response}).encode())
        
        else:
            self._set_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AssistantHandler)
    print(f"Starting Nanite AI Assistant service on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
EOF

chmod +x /usr/share/nanite/assistant/nanite-assistant-service.py

# Create systemd service for the assistant
cat > /etc/systemd/system/nanite-assistant.service << EOF
[Unit]
Description=Nanite AI Assistant Service
After=network.target ollama.service

[Service]
ExecStart=/usr/share/nanite/assistant/nanite-assistant-service.py
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl enable nanite-assistant.service

# Create a GUI client for the assistant
cat > /usr/share/nanite/assistant/nanite-assistant-gui.py << EOF
#!/usr/bin/env python3
"""
Nanite AI Assistant GUI - Graphical interface for the AI assistant
"""
import sys
import json
import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango

class AssistantWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Nanite AI Assistant")
        self.set_default_size(600, 400)
        self.set_border_width(10)
        
        # Create main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        
        # Create chat history display
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        vbox.pack_start(scrolled_window, True, True, 0)
        
        self.chat_buffer = Gtk.TextBuffer()
        self.chat_view = Gtk.TextView(buffer=self.chat_buffer)
        self.chat_view.set_editable(False)
        self.chat_view.set_wrap_mode(Gtk.WrapMode.WORD)
        
        # Set up text formatting
        self.chat_view.override_font(Pango.FontDescription("Sans 11"))
        scrolled_window.add(self.chat_view)
        
        # Create input area
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(input_box, False, False, 0)
        
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Ask Nanite Assistant...")
        self.entry.connect("activate", self.on_send_clicked)
        input_box.pack_start(self.entry, True, True, 0)
        
        send_button = Gtk.Button.new_with_label("Send")
        send_button.connect("clicked", self.on_send_clicked)
        input_box.pack_start(send_button, False, False, 0)
        
        # Initialize chat
        self.add_message("Nanite Assistant", "Hello! I'm your AI assistant. How can I help you today?")
    
    def add_message(self, sender, message):
        end_iter = self.chat_buffer.get_end_iter()
        
        # Format based on sender
        if sender == "You":
            self.chat_buffer.insert(end_iter, f"{sender}: ", -1)
            self.chat_buffer.insert(end_iter, f"{message}\n\n", -1)
        else:
            self.chat_buffer.insert(end_iter, f"{sender}: ", -1)
            self.chat_buffer.insert(end_iter, f"{message}\n\n", -1)
        
        # Scroll to bottom
        mark = self.chat_buffer.create_mark(None, self.chat_buffer.get_end_iter(), False)
        self.chat_view.scroll_to_mark(mark, 0.0, False, 0.0, 0.0)
    
    def on_send_clicked(self, widget):
        query = self.entry.get_text()
        if not query:
            return
        
        # Add user message to chat
        self.add_message("You", query)
        self.entry.set_text("")
        
        # Send query to assistant service
        try:
            response = requests.post(
                "http://localhost:8000/query",
                json={"query": query}
            )
            data = response.json()
            self.add_message("Nanite Assistant", data["response"])
        except Exception as e:
            self.add_message("System", f"Error: {str(e)}")

def main():
    win = AssistantWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
EOF

chmod +x /usr/share/nanite/assistant/nanite-assistant-gui.py

# Create desktop entry for the assistant
cat > /usr/share/applications/nanite-assistant.desktop << EOF
[Desktop Entry]
Name=Nanite AI Assistant
Comment=AI assistance powered by local LLMs
Exec=/usr/share/nanite/assistant/nanite-assistant-gui.py
Icon=/usr/share/nanite/icons/ai-assistant.png
Terminal=false
Type=Application
Categories=Utility;AI;
EOF

# Create a simple CLI client
cat > /usr/local/bin/nanite-ask << EOF
#!/bin/bash
# Simple CLI client for Nanite AI Assistant

if [ -z "\$1" ]; then
    echo "Usage: nanite-ask <question>"
    exit 1
fi

query="\$*"
response=\$(curl -s -X POST -H "Content-Type: application/json" -d "{\"query\": \"\$query\"}" http://localhost:8000/query)
echo \$response | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
EOF

chmod +x /usr/local/bin/nanite-ask

echo "System-wide AI assistant setup completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0300-setup-ai-assistant.hook.chroot
```

## Image Generation Integration

Let's integrate Stable Diffusion for image generation capabilities:

### Installation and Configuration

Create `config/hooks/live/0400-setup-image-generation.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Setting up image generation capabilities..."

# Install required packages
pip3 install diffusers transformers accelerate

# Create directory for image generation
mkdir -p /usr/share/nanite/image-gen
chmod 755 /usr/share/nanite/image-gen

# Create a simple image generation script
cat > /usr/local/bin/nanite-image-gen << EOF
#!/usr/bin/env python3
"""
Nanite Image Generator - Generate images from text prompts
"""
import os
import argparse
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

def generate_image(prompt, output_path, negative_prompt="", width=512, height=512, steps=30, guidance_scale=7.5):
    """Generate an image from a text prompt using Stable Diffusion"""
    # Load model
    model_id = "stabilityai/stable-diffusion-2-1-base"
    
    # Use GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("Warning: Running on CPU. This will be slow.")
    
    # Load pipeline
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)
    
    # Generate image
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=guidance_scale
    ).images[0]
    
    # Save image
    image.save(output_path)
    print(f"Image saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Nanite Image Generator")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--output", "-o", default="generated_image.png", help="Output image path")
    parser.add_argument("--negative", "-n", default="", help="Negative prompt (what to avoid)")
    parser.add_argument("--width", "-W", type=int, default=512, help="Image width")
    parser.add_argument("--height", "-H", type=int, default=512, help="Image height")
    parser.add_argument("--steps", "-s", type=int, default=30, help="Number of inference steps")
    parser.add_argument("--guidance", "-g", type=float, default=7.5, help="Guidance scale")
    
    args = parser.parse_args()
    
    generate_image(
        args.prompt,
        args.output,
        args.negative,
        args.width,
        args.height,
        args.steps,
        args.guidance
    )

if __name__ == "__main__":
    main()
EOF

chmod +x /usr/local/bin/nanite-image-gen

# Create a desktop entry for the image generator
cat > /usr/share/applications/nanite-image-generator.desktop << EOF
[Desktop Entry]
Name=Nanite Image Generator
Comment=Generate images from text descriptions
Exec=xfce4-terminal -e "nanite-image-gen"
Icon=/usr/share/nanite/icons/image-gen.png
Terminal=false
Type=Application
Categories=Graphics;AI;
EOF

echo "Image generation setup completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0400-setup-image-generation.hook.chroot
```

## Code Assistant Integration

Let's integrate a code assistant to help with programming tasks:

### Installation and Configuration

Create `config/hooks/live/0500-setup-code-assistant.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Setting up code assistant..."

# Create directory for code assistant
mkdir -p /usr/share/nanite/code-assistant
chmod 755 /usr/share/nanite/code-assistant

# Create a code assistant script
cat > /usr/local/bin/nanite-code-assist << EOF
#!/usr/bin/env python3
"""
Nanite Code Assistant - AI-powered coding assistance
"""
import os
import sys
import argparse
import tempfile
import subprocess
from langchain_community.llms import Ollama

def get_code_completion(prompt, model="nanite-assistant"):
    """Get code completion from LLM"""
    llm = Ollama(model=model)
    response = llm(prompt)
    return response

def extract_code_blocks(text):
    """Extract code blocks from markdown-formatted text"""
    lines = text.split('\n')
    code_blocks = []
    in_code_block = False
    current_block = []
    
    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                in_code_block = False
                if current_block:
                    code_blocks.append('\n'.join(current_block))
                    current_block = []
            else:
                # Start of code block
                in_code_block = True
        elif in_code_block:
            # Inside code block
            current_block.append(line)
    
    return code_blocks

def main():
    parser = argparse.ArgumentParser(description="Nanite Code Assistant")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Complete code snippet")
    complete_parser.add_argument("file", help="File containing code to complete")
    
    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Explain code")
    explain_parser.add_argument("file", help="File containing code to explain")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate code from description")
    generate_parser.add_argument("description", help="Description of code to generate")
    generate_parser.add_argument("--language", "-l", default="python", help="Programming language")
    
    args = parser.parse_args()
    
    if args.command == "complete":
        with open(args.file, 'r') as f:
            code = f.read()
        
        prompt = f"Complete the following code. Only return the completed code, no explanations:\n\n```\n{code}\n```"
        response = get_code_completion(prompt)
        
        code_blocks = extract_code_blocks(response)
        if code_blocks:
            print(code_blocks[0])
        else:
            print(response)
    
    elif args.command == "explain":
        with open(args.file, 'r') as f:
            code = f.read()
        
        prompt = f"Explain the following code in detail:\n\n```\n{code}\n```"
        response = get_code_completion(prompt)
        print(response)
    
    elif args.command == "generate":
        prompt = f"Generate {args.language} code for the following description. Only return the code, no explanations:\n\n{args.description}"
        response = get_code_completion(prompt)
        
        code_blocks = extract_code_blocks(response)
        if code_blocks:
            print(code_blocks[0])
        else:
            print(response)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
EOF

chmod +x /usr/local/bin/nanite-code-assist

# Create VSCode extension integration script
cat > /usr/share/nanite/code-assistant/setup-vscode-extensions.sh << EOF
#!/bin/bash
# Install AI-related VSCode extensions

# GitHub Copilot
code --install-extension GitHub.copilot

# Code GPT
code --install-extension DanielSanMedium.dscodegpt

# Tabnine
code --install-extension TabNine.tabnine-vscode

# IntelliCode
code --install-extension VisualStudioExptTeam.vscodeintellicode

echo "VSCode AI extensions installed."
EOF

chmod +x /usr/share/nanite/code-assistant/setup-vscode-extensions.sh

echo "Code assistant setup completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0500-setup-code-assistant.hook.chroot
```

## Documentation and User Guide

Let's create comprehensive documentation for the AI features:

### Creating Documentation

Create `config/includes.chroot/usr/share/doc/nanite/ai-features.md`:

```markdown
# Nanite AI Features Guide

This guide provides an overview of the AI features integrated into Nanite Linux and how to use them effectively.

## Available AI Models

Nanite comes with several pre-installed AI models:

1. **Mistral** - General-purpose LLM for various tasks
2. **Phi-3 Mini** - Lightweight model for basic tasks
3. **Llama 3 (8B)** - Advanced reasoning and instruction following
4. **Nanite Assistant** - Custom-tuned model for system assistance

## AI Assistant

The Nanite AI Assistant provides system-wide AI assistance through both GUI and CLI interfaces.

### GUI Interface

Launch the assistant from the Applications menu or by clicking the assistant icon in the panel. You can ask questions, request information, or get help with system tasks.

### CLI Interface

Use the `nanite-ask` command to interact with the assistant from the terminal:

```bash
nanite-ask How do I install Python packages?
```

## Language Models (LLMs)

Nanite uses Ollama to manage and run language models. Here are some common commands:

```bash
# List available models
ollama list

# Pull additional models
ollama pull codellama

# Run a specific model in chat mode
ollama run llama3
```

## Retrieval-Augmented Generation (RAG)

Nanite includes a basic RAG system for knowledge-based queries. Use the `nanite-rag` command:

```bash
# Query a document
nanite-rag /path/to/document.txt "What is the main topic of this document?"
```

## Speech Recognition and Synthesis

Nanite includes speech capabilities through the `nanite-speech` command:

```bash
# Transcribe audio to text
nanite-speech transcribe audio.mp3

# Convert text to speech
nanite-speech synthesize "Hello, this is Nanite speaking" --output hello.wav
```

## Image Generation

Generate images from text descriptions using the `nanite-image-gen` command:

```bash
# Generate an image
nanite-image-gen "A futuristic city with flying cars" --output city.png
```

## Code Assistance

Get AI-powered coding help with the `nanite-code-assist` command:

```bash
# Generate code from description
nanite-code-assist generate "A function that calculates fibonacci numbers" --language python

# Complete code
nanite-code-assist complete mycode.py

# Explain code
nanite-code-assist explain mycode.py
```

## Extending AI Capabilities

Nanite is designed to be extensible. Here are some ways to enhance its AI capabilities:

### Adding New Models

```bash
# Pull additional models from Ollama
ollama pull <model-name>

# Create custom models
ollama create mymodel -f Modelfile
```

### Customizing the AI Assistant

Edit the assistant configuration in `/etc/nanite/assistant.conf` to customize its behavior.

### Installing Additional AI Tools

Nanite is compatible with most Python-based AI tools. Install them using pip:

```bash
pip install <package-name>
```

## Troubleshooting

If you encounter issues with AI features:

1. Check if Ollama service is running: `systemctl status ollama`
2. Check if AI Assistant service is running: `systemctl status nanite-assistant`
3. Check GPU acceleration: `nvidia-smi` or `rocm-smi`
4. Check logs: `journalctl -u ollama` or `journalctl -u nanite-assistant`

For more help, refer to the full documentation in `/usr/share/doc/nanite/`.
```

## Integration Testing Script

Create a script to test the AI integration:

Create `config/hooks/live/9000-test-ai-integration.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Testing AI integration..."

# Test Ollama
echo "Testing Ollama..."
if systemctl is-active --quiet ollama; then
    echo "✓ Ollama service is running"
else
    echo "✗ Ollama service is not running"
fi

# Test model availability
echo "Testing model availability..."
if ollama list | grep -q "mistral"; then
    echo "✓ Mistral model is available"
else
    echo "✗ Mistral model is not available"
fi

# Test AI Assistant service
echo "Testing AI Assistant service..."
if systemctl is-active --quiet nanite-assistant; then
    echo "✓ AI Assistant service is running"
else
    echo "✗ AI Assistant service is not running"
fi

# Test basic LLM functionality
echo "Testing basic LLM functionality..."
if echo "Hello" | ollama run mistral -c 2>/dev/null | grep -q "."; then
    echo "✓ LLM is responding"
else
    echo "✗ LLM is not responding"
fi

echo "AI integration tests completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/9000-test-ai-integration.hook.chroot
```

## Conclusion

This comprehensive guide details the integration of various AI models and applications into the Nanite Linux distribution. By following these steps, you'll create a cohesive AI-powered operating system with:

1. Local LLM capabilities through Ollama
2. A system-wide AI assistant accessible via GUI and CLI
3. Speech recognition and synthesis
4. Image generation capabilities
5. Code assistance tools
6. Retrieval-Augmented Generation (RAG) for knowledge-based queries

The integration is designed to be modular, allowing for easy customization and extension based on specific requirements and user feedback. All AI processing happens locally, ensuring privacy and security while providing powerful AI capabilities integrated throughout the system.
