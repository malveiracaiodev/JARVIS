"""
=========================================
GENESIS CORE - INTERACTIVE TERMINAL

Arquivo:
main.py

Descrição:
Ponto de entrada principal via terminal.

Responsável por:
- Inicializar Kernel
- Acessar serviços do Genesis
- Comunicação com AIService
- Interface terminal

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import sys

from core.kernel.kernel import Kernel
from core.models.thought import Thought



def format_response(response):
    """
    Normaliza respostas da IA.
    Compatível com:
    - AIResponse
    - Thought
    - texto bruto
    - dicionários
    """


    if response is None:
        return (
            "Sem resposta gerada pelo "
            "sistema cognitivo."
        )


    if isinstance(response, str):
        return response



    if hasattr(response, "content"):

        return str(
            response.content
        )



    if hasattr(response, "result"):

        return str(
            response.result
        )



    if hasattr(response, "to_dict"):

        data = response.to_dict()

        if isinstance(data, dict):

            return str(
                data.get("response")
                or data.get("output")
                or data.get("result")
                or data
            )



    return str(response)




def resolve_ai_service(kernel):
    """
    Localiza o AIService dentro do Genesis.

    Mantém compatibilidade com futuras
    mudanças no Kernel.
    """


    # Tentativa 1:
    # Kernel possui get()

    if hasattr(kernel, "get"):

        service = kernel.get(
            "ai_service"
        )

        if service:
            return service



    # Tentativa 2:
    # Kernel possui bootstrap

    if hasattr(kernel, "bootstrap"):

        bootstrap = kernel.bootstrap


        if hasattr(
            bootstrap,
            "get"
        ):

            service = bootstrap.get(
                "ai_service"
            )

            if service:
                return service



    # Tentativa 3:
    # Kernel possui registry

    if hasattr(kernel, "registry"):

        registry = kernel.registry


        if hasattr(
            registry,
            "get"
        ):

            service = registry.get(
                "ai_service"
            )

            if service:
                return service



    return None




def main():

    kernel = None


    try:

        print(
            "[BOOT] Inicializando Genesis Core..."
        )


        kernel = Kernel()

        kernel.boot()



        print(
            "\n"
            + "=" * 60
        )

        print(
            "          BEM-VINDO À MATRIX"
        )

        print(
            "          JARV.IS MARK V - EVOLUTION"
        )

        print(
            "          Camada IA desacoplada."
        )

        print(
            "=" * 60
            + "\n"
        )


        ai_service = resolve_ai_service(
            kernel
        )



        if ai_service:

            print(
                "[ONLINE] AIService conectado."
            )

        else:

            print(
                "[WARNING] AIService não encontrado."
            )



        print()

        print(
            "Digite 'sair', 'exit' ou "
            "'shutdown' para encerrar."
        )


        while True:


            prompt = input(
                "\n[Caio] > "
            ).strip()



            if not prompt:

                continue



            if prompt.lower() in [
                "sair",
                "exit",
                "shutdown"
            ]:

                break



            try:


                print(
                    "\n[Processando...]\n"
                )



                if not ai_service:

                    print(
                        "[JARV.IS]"
                    )

                    print(
                        "Serviço de IA offline."
                    )

                    continue



                response = ai_service.ask(
                    prompt
                )


                print(
                    "[JARV.IS]"
                )


                print(
                    format_response(
                        response
                    )
                )


            except Exception as error:


                print(
                    "\n[FALHA IA]:",
                    error
                )



    except KeyboardInterrupt:


        print(
            "\n[SIGINT] Encerramento solicitado."
        )



    except Exception as error:


        print(
            "\n[FALHA CRÍTICA]:",
            error
        )



    finally:


        if kernel:

            kernel.shutdown()



        print(
            "\nGenesis Core desligado."
        )


        sys.exit(0)




if __name__ == "__main__":

    main()