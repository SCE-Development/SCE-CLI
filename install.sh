#!/bin/sh
set -e

REPO="SCE-Development/SCE-CLI"
INSTALL_DIR="/usr/local/bin"

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
  darwin) OS="darwin" ;;
  linux)  OS="linux" ;;
  *)
    echo "unsupported OS: $OS"
    exit 1
    ;;
esac

# Detect architecture
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  ARCH="amd64" ;;
  aarch64) ARCH="arm64" ;;
  arm64)   ARCH="arm64" ;;
  *)
    echo "unsupported architecture: $ARCH"
    exit 1
    ;;
esac

BINARY="sce-${OS}-${ARCH}"
URL="https://github.com/${REPO}/releases/latest/download/${BINARY}"

echo "downloading sce for ${OS}/${ARCH}..."
curl -sSL "$URL" -o /tmp/sce

echo "installing to ${INSTALL_DIR}/sce..."
sudo install -m 755 /tmp/sce "${INSTALL_DIR}/sce"
rm /tmp/sce

echo "sce installed successfully! run 'sce --help' to get started."
