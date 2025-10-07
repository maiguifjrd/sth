#!/bin/bash

APP_NAME="Steam Translator Helper"
SCRIPT_NAME="sth.py"
ICON_NAME="sth.png"
DESKTOP_NAME="sth.desktop"

BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.icons"
DESKTOP_DIR="$HOME/.local/share/applications"

# --- Função para checar comando ---
check_command() {
    command -v "$1" >/dev/null 2>&1
}

echo "🚀 Instalando $APP_NAME..."

# --- 1. Verifica Python 3 ---
if ! check_command python3; then
    echo "❌ Python 3 não encontrado! Instale antes de continuar."
    exit 1
fi

# --- 2. Verifica PySide6 ---
python3 - <<EOF
try:
    import PySide6
except ImportError:
    import sys
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ PySide6 não encontrado! Instale via 'pip install PySide6'"
    exit 1
fi

# --- 3. Cria pastas necessárias ---
mkdir -p "$BIN_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$DESKTOP_DIR"

# --- 4. Copia o script e torna executável ---
cp "$SCRIPT_NAME" "$BIN_DIR/"
chmod +x "$BIN_DIR/$SCRIPT_NAME"

# --- 5. Copia ícone ---
cp "assets/$ICON_NAME" "$ICON_DIR/"

# --- 6. Copia .desktop ---
cp "$DESKTOP_NAME" "$DESKTOP_DIR/"

# --- 7. Atualiza database de aplicativos ---
update-desktop-database "$DESKTOP_DIR"

# --- 8. Adiciona ~/.local/bin ao PATH se necessário ---
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH=$HOME/.local/bin:$PATH' >> "$HOME/.bashrc"
    echo "⚠️ ~/.local/bin adicionado ao PATH. Execute 'source ~/.bashrc' para aplicar."
fi

echo "✅ $APP_NAME instalado com sucesso!"

