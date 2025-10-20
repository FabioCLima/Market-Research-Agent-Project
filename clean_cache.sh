#!/bin/bash
# UdaPlay Project - Cache Cleanup Script
# Este script limpa todos os arquivos de cache e temporários do projeto

echo "🧹 Iniciando limpeza de cache do UdaPlay..."

# Limpar cache Python
echo "📁 Removendo __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "🐍 Removendo arquivos .pyc..."
find . -name "*.pyc" -delete 2>/dev/null || true

echo "🐍 Removendo arquivos .pyo..."
find . -name "*.pyo" -delete 2>/dev/null || true

# Limpar cache de testes
echo "🧪 Removendo cache do pytest..."
rm -rf .pytest_cache/ 2>/dev/null || true

# Limpar arquivos de build
echo "🔨 Removendo arquivos de build..."
rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true

# Limpar arquivos de cobertura
echo "📊 Removendo arquivos de cobertura..."
find . -name ".coverage" -delete 2>/dev/null || true

# Limpar logs
echo "📝 Removendo arquivos de log..."
find . -name "*.log" -delete 2>/dev/null || true

# Limpar arquivos temporários do sistema
echo "🗑️ Removendo arquivos temporários..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true

# Limpar cache do ChromaDB (opcional - descomente se necessário)
# echo "🗄️ Removendo cache do ChromaDB..."
# rm -rf chromadb_test/ 2>/dev/null || true

echo "✅ Limpeza de cache concluída!"
echo ""
echo "📋 Arquivos removidos:"
echo "   - __pycache__ directories"
echo "   - *.pyc files"
echo "   - *.pyo files"
echo "   - .pytest_cache/"
echo "   - build/, dist/, *.egg-info/"
echo "   - .coverage files"
echo "   - *.log files"
echo "   - Arquivos temporários do sistema"
echo ""
echo "💡 Para executar novamente: ./clean_cache.sh"
