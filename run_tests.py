#!/usr/bin/env python3
"""Script para executar todos os testes e validar a instalação."""

import subprocess
import sys


def run_command(cmd, description):
    """Executa um comando e mostra o resultado."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERRO: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Executa todos os testes."""
    print("=== PyVyOS Test Suite ===\n")

    steps = [
        ("uv sync", "1. Sincronizando dependências"),
        ("uv run python test_quick.py", "2. Verificação rápida de imports"),
        ("uv run pytest tests/test_shims.py -v", "3. Testes de shims"),
        ("uv run pytest tests/utils/ -v", "4. Testes de utils"),
        ("uv run pytest tests/test_exceptions.py -v", "5. Testes de exceptions"),
        (
            "uv run pytest tests/modules/test_vy_device.py::test_shim_compatibility -v",
            "6. Teste de compatibilidade",
        ),
        ("uv run pytest tests/ -v --tb=short", "7. TODOS os testes"),
    ]

    results = []
    for cmd, desc in steps:
        success = run_command(cmd, desc)
        results.append((desc, success))
        if not success:
            print(f"\n❌ Falha em: {desc}")
            sys.exit(1)

    print(f"\n{'='*60}")
    print("✅ TODOS OS TESTES PASSARAM!")
    print(f"{'='*60}\n")

    for desc, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {desc}")


if __name__ == "__main__":
    main()

