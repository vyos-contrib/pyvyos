#!/bin/bash
set -e

echo "=== PyVyOS Test Suite ==="
echo ""

echo "1. Sincronizando dependências..."
uv sync

echo ""
echo "2. Verificação rápida de imports..."
uv run python test_quick.py

echo ""
echo "3. Executando testes de shims..."
uv run pytest tests/test_shims.py -v

echo ""
echo "4. Executando testes de utils..."
uv run pytest tests/utils/ -v

echo ""
echo "5. Executando testes de exceptions..."
uv run pytest tests/test_exceptions.py -v

echo ""
echo "6. Executando teste de compatibilidade..."
uv run pytest tests/modules/test_vy_device.py::test_shim_compatibility -v

echo ""
echo "7. Executando TODOS os testes..."
uv run pytest tests/ -v --tb=short

echo ""
echo "✅ Todos os testes concluídos!"

