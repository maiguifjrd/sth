#!/bin/bash

APP_NAME="Steam Translator Helper"
SCRIPT_NAME="steam-translator-helper.py"
ICON_NAME="sth.png"
DESKTOP_NAME="sth.desktop"

BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.icons"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "🧹 Desinstalando $APP_NAME..."

# --- Remove script ---
if [ -f "$BIN_DIR/$SCRIPT_NAME" ]; then
    rm -f "$BIN_DIR/$SCRIPT_NAME"
    echo "🗑️ Removido: $BIN_DIR/$SCRIPT_NAME"
else
    echo "⚠️ Script não encontrado em $BIN_DIR."
fi

# --- Remove ícone ---
if [ -f "$ICON_DIR/$ICON_NAME" ]; then
    rm -f "$ICON_DIR/$ICON_NAME"
    echo "🗑️ Removido: $ICON_DIR/$ICON_NAME"
else
    echo "⚠️ Ícone não encontrado em $ICON_DIR."
fi

# --- Remove arquivo .desktop ---
if [ -f "$DESKTOP_DIR/$DESKTOP_NAME" ]; then
    rm -f "$DESKTOP_DIR/$DESKTOP_NAME"
    echo "🗑️ Removido: $DESKTOP_DIR/$DESKTOP_NAME"
else
    echo "⚠️ Arquivo .desktop não encontrado em $DESKTOP_DIR."
fi

# --- Atualiza banco de dados de aplicativos ---
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR"
    echo "🔄 Banco de dados de aplicativos atualizado."
fi

echo "✅ $APP_NAME removido com sucesso!"

