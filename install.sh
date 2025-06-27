#!/bin/bash
# dashtrash installation script
# Usage: curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash

set -e

echo "🗑️  Installing dashtrash - Terminal Dashboard"
echo "============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. You have $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Install dashtrash using virtual environment
echo "📦 Installing dashtrash..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

if command -v git &> /dev/null; then
    echo "📥 Cloning dashtrash repository..."
    git clone https://github.com/turancannb02/dashtrash.git
    cd dashtrash
    
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "🔧 Installing dashtrash..."
    pip install --upgrade pip
    pip install .
    
    # Create a global launcher script in a permanent location
    INSTALL_DIR="$HOME/.local/bin"
    VENV_DIR="$HOME/.dashtrash-venv"
    mkdir -p "$INSTALL_DIR"
    
    # Move the virtual environment to a permanent location
    cp -r venv "$VENV_DIR"
    
    # Create wrapper script
    cat > "$INSTALL_DIR/dashtrash" << EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
exec python -m dashtrash "\$@"
EOF
    
    chmod +x "$INSTALL_DIR/dashtrash"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "🔧 Adding $INSTALL_DIR to PATH..."
        if [[ "$SHELL" == *"zsh"* ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        else
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        fi
    fi
    
    echo "✅ dashtrash installed successfully!"
else
    echo "❌ git is required but not installed."
    echo "Please install git and try again."
    exit 1
fi

echo ""
echo "🎉 dashtrash is ready to use!"
echo ""
echo "📋 Quick Start:"
echo "  dashtrash --create-config    # Create default configuration"
echo "  dashtrash                    # Run dashboard"
echo "  dashtrash --help             # Show help"

echo ""
echo "🔧 Configuration:"
echo "  Edit dashboard.yml to customize panels and settings"
echo ""
echo "📚 Documentation:"
echo "  https://github.com/turancannb02/dashtrash"

# Test if dashtrash is in PATH
if command -v dashtrash &> /dev/null; then
    echo "✅ dashtrash is ready to use!"
else
    echo "⚠️  dashtrash may not be in your PATH."
    echo "   Try adding ~/.local/bin to your PATH:"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
fi

echo ""
echo "🗑️✨ Real-time dashboards. Questionable aesthetics." 