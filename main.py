"""
=========================================
GENESIS CORE - INTERACTIVE TERMINAL

Arquivo:
main.py

Descrição:
Ponto de entrada principal via terminal.
Inicializa o Genesis Core Mark IV, gerencia a 
interação do usuário e orquestra a Thought Engine.

Arquitetura:
Genesis Core
Mark:
IV - Thought Engine
=========================================
"""

import sys
from core.kernel.kernel import Kernel
from core.models.thought import Thought


def format_response(thought_obj):
    """
    Normaliza e extrai o resultado do ciclo cognitivo Mark IV.
    """
    if thought_obj is None:
        return "Sem resposta gerada pelo sistema cognitivo."

    # Se o processamento retornou um objeto Thought estruturado
    if hasattr(thought_obj, "result") and thought_obj.result:
        return thought_obj.result

    if hasattr(thought_obj, "to_dict"):
        data = thought_obj.to_dict()
        return data.get("result", str(data))

    return str(thought_obj)


def main():
    kernel = None
    try:
        # Inicialização do ecossistema unificado Mark IV
        kernel = Kernel()
        kernel.boot()

        print("\n" + "=" * 60)
        print("          BEM-VINDO À MATRIX (JARVIS MARK IV)")
        print("          Rafiki está sentado na árvore esperando sua diretriz...")
        print("=" * 60 + "\n")

        print("Digite 'sair', 'exit' ou 'shutdown' para encerrar com segurança.\n")

        while True:
            prompt = input("[Caio] > ").strip()

            if not prompt:
                continue

            if prompt.lower() in ["sair", "exit", "shutdown"]:
                break

            # Verificação de integridade da mente do sistema
            if not hasattr(kernel, "mind") or not kernel.mind:
                print("\n[ERRO] Estrutura 'Mind' indisponível no Kernel.\n")
                continue

            try:
                # No Mark IV, o fluxo passa pela Thought Engine / Pipeline
                print("\n[Pensando...]")

                # Executa o pensamento usando a infraestrutura do cérebro
                if hasattr(kernel.mind, "think"):
                    response = kernel.mind.think(prompt)
                else:
                    response = kernel.mind.brain.process(prompt)

                print("\n[Resposta]")
                print(format_response(response))
                print()

            except Exception as error:
                print(f"\n[FALHA COGNITIVA]: {error}\n")

    except KeyboardInterrupt:
        print("\n\n[SIGINT] Encerramento solicitado pelo usuário.")

    except Exception as fatal_error:
        print(f"\n[FALHA CRÍTICA NO RUNTIME]: {fatal_error}")

    finally:
        if kernel:
            kernel.shutdown()
        print("Processo finalizado com sucesso. Até logo, Senhor.")
        sys.exit(0)


if __name__ == "__main__":
    main()