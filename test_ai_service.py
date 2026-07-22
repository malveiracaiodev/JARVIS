"""
=========================================
GENESIS CORE

Arquivo:
test_ai_service.py

Descrição:
Teste do serviço de Inteligência Artificial.

Valida:

- AIService
- AIManager
- MockProvider
- Ciclo de vida do serviço

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.services.ai_service import AIService


def separator():

    print("=" * 60)



def main():

    separator()

    print(
        "TESTE AI SERVICE - GENESIS CORE"
    )

    separator()


    # =====================================
    # Criar serviço
    # =====================================

    print("\n[1] Criando AIService...")


    service = AIService()


    print(
        "[OK] Serviço criado"
    )


    # =====================================
    # Inicializar
    # =====================================

    print("\n[2] Inicializando...")


    started = service.initialize()


    print(
        f"Status inicialização: {started}"
    )


    # =====================================
    # Status
    # =====================================

    print("\n[3] Status:")


    status = service.ai_status()


    for key, value in status.items():

        print(
            f"{key}: {value}"
        )


    # =====================================
    # Pergunta
    # =====================================

    print("\n[4] Perguntando para IA...")


    response = service.ask(
        "O que é uma inteligência artificial?"
    )


    print("\nResposta:")

    print(
        response.content
    )


    # =====================================
    # Encerramento
    # =====================================

    print("\n[5] Encerrando...")


    service.shutdown()


    print(
        "[OK] AIService desligado"
    )


    separator()

    print(
        "TESTE FINALIZADO"
    )

    separator()



if __name__ == "__main__":

    main()