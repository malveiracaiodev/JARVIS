"""
=========================================
JARVIS CORE

Arquivo:
main.py

Descrição:
Ponto de entrada da aplicação. Inicializa a arquitetura e provê terminal de interação.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import sys
from core.kernel.kernel import Kernel


def main():
    kernel = None
    try:
        kernel = Kernel()
        kernel.boot()

        print("\n" + "="*60)
        print("          BEM-VINDO À MATRIX (JARVIS MARK III)")
        print("    Rafiki está sentado na árvore esperando sua diretriz...")
        print("="*60 + "\n")

        print("Pressione Ctrl+C ou digite 'sair' para encerrar com segurança.\n")

        # Loop de interação com o terminal cognitivo
        while True:
            prompt = input("[Caio] > ").strip()
            
            if not prompt:
                continue
                
            if prompt.lower() in ["sair", "exit", "shutdown"]:
                break
            
            # Chama o cérebro integrado
            if kernel.mind:
                response = kernel.mind.think(prompt)
                print(f"\n[Resposta] {response}\n")
            else:
                print("\n[Erro] Sistema cognitivo inacessível.\n")

    except KeyboardInterrupt:
        print("\n\n[SIGINT] Interrupção detectada pelo usuário.")
    except Exception as fatal_error:
        print(f"\n[FALHA CRÍTICA NO RUNTIME]: {fatal_error}")
    finally:
        if kernel:
            kernel.shutdown()
        print("Processo finalizado com sucesso. Até logo, Senhor.")
        sys.exit(0)


if __name__ == "__main__":
    main()