"""
=========================================
GENESIS CORE

Arquivo:
test_ia.py

Descrição:
Teste completo da arquitetura de IA.

Valida:

- AIManager
- ProviderFactory
- ProviderRegistry
- MockProvider
- AIRequest
- AIResponse
- ProviderState

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.managers.ai_manager import AIManager


def separator():

    print("=" * 60)



def main():

    separator()

    print(
        "TESTE AI MANAGER - GENESIS CORE"
    )

    separator()


    # =====================================
    # Criando Manager
    # =====================================

    print("\n[1] Inicializando AIManager...")


    manager = AIManager()


    manager.initialize(
        "mock"
    )


    print(
        "[OK] AIManager online"
    )


    # =====================================
    # Status
    # =====================================

    print("\n[2] Status da IA:")


    status = manager.status()


    for key, value in status.items():

        print(
            f"{key}: {value}"
        )


    # =====================================
    # Pergunta
    # =====================================

    print("\n[3] Enviando pergunta...")


    response = manager.ask(
        "O que é uma IA?"
    )


    print(
        "\nResposta:"
    )


    print(
        response.content
    )


    # =====================================
    # Dados resposta
    # =====================================

    print("\n[4] Dados da resposta:")


    print(
        f"Sucesso: {response.success}"
    )


    print(
        f"Provider: {response.provider}"
    )


    print(
        f"Modelo: {response.model}"
    )


    print(
        f"Tempo: {response.latency:.6f}s"
    )


    # =====================================
    # Estado final
    # =====================================

    print("\n[5] Estado final:")


    status = manager.status()


    for key, value in status.items():

        print(
            f"{key}: {value}"
        )


    # =====================================
    # Encerramento
    # =====================================

    print("\n[6] Encerrando...")


    manager.shutdown()


    print(
        "[OK] Genesis AI desligado"
    )


    separator()

    print(
        "TESTE FINALIZADO"
    )

    separator()



if __name__ == "__main__":

    main()