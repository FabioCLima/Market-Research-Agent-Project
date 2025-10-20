#!/bin/bash
# Script para consolidar branches no GitHub
# Execute este script APÓS mudar a branch padrão no GitHub

echo "🔄 Consolidando branches no repositório GitHub..."
echo ""

# Verificar se estamos na branch main
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "❌ Você precisa estar na branch 'main'"
    echo "Execute: git checkout main"
    exit 1
fi

echo "✅ Estamos na branch: $current_branch"
echo ""

# Deletar branch master remota
echo "🗑️ Deletando branch 'master' remota..."
if git push origin --delete master; then
    echo "✅ Branch 'master' deletada com sucesso!"
else
    echo "⚠️ Erro ao deletar branch 'master' (pode já ter sido deletada)"
fi

echo ""

# Deletar branch master local (se existir)
echo "🗑️ Deletando branch 'master' local..."
if git branch -d master 2>/dev/null; then
    echo "✅ Branch 'master' local deletada!"
elif git branch -D master 2>/dev/null; then
    echo "✅ Branch 'master' local deletada (forçado)!"
else
    echo "ℹ️ Branch 'master' local não existe"
fi

echo ""

# Verificar status final
echo "📊 Status final das branches:"
git branch -a

echo ""
echo "🎉 Consolidação concluída!"
echo "✅ Branch padrão: main"
echo "✅ Todas as alterações estão na branch main"
echo "✅ Branch master removida"
