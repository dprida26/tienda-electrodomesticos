#!/usr/bin/env python3
"""
Script para actualizar variables de entorno en .env
Uso: python update_env.py TELEGRAM_CHAT_ID <valor>
"""

import sys
import os

def update_env(key, value):
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

    if not os.path.exists(env_path):
        print(f"❌ No se encontró .env en {env_path}")
        sys.exit(1)

    # Leer el archivo
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Buscar y actualizar
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    # Si no existe, agregarlo
    if not updated:
        lines.append(f"{key}={value}\n")

    # Escribir
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ {key}={value} actualizado en .env")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python update_env.py <KEY> <VALUE>")
        print("Ej:  python update_env.py TELEGRAM_CHAT_ID -1001234567890")
        sys.exit(1)

    key = sys.argv[1]
    value = sys.argv[2]
    update_env(key, value)
