"""
=========================================
JARVIS CORE

Arquivo:
main.py

Descrição:
Ponto de entrada da aplicação.

Inicializa o Genesis Core,
controla o terminal de interação
e encaminha comandos para a Mind.

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




def format_response(response):
    """
    Normaliza respostas cognitivas.
    """


    if response is None:

        return "Sem resposta gerada."



    if hasattr(
        response,
        "summary"
    ):

        try:

            return response.summary()

        except Exception:

            pass



    if hasattr(
        response,
        "content"
    ):

        return response.content



    if hasattr(
        response,
        "message"
    ):

        return response.message



    return str(response)






def main():


    kernel = None


    try:


        kernel = Kernel()


        kernel.boot()



        print("\n" + "=" * 60)

        print(
            "          BEM-VINDO À MATRIX (JARVIS MARK III)"
        )

        print(
            "    Rafiki está sentado na árvore esperando sua diretriz..."
        )

        print("=" * 60 + "\n")



        print(
            "Digite 'sair' para encerrar com segurança.\n"
        )



        while True:


            prompt = input(
                "[Caio] > "
            ).strip()



            if not prompt:

                continue



            if prompt.lower() in [

                "sair",

                "exit",

                "shutdown"

            ]:

                break




            if not kernel.mind:


                print(
                    "\n[ERRO] Mind indisponível.\n"
                )

                continue





            try:


                response = kernel.mind.think(
                    prompt
                )


                print(
                    "\n[Resposta]"
                )


                print(
                    format_response(response)
                )


                print()



            except Exception as error:


                print(
                    "\n[FALHA COGNITIVA]:",
                    error,
                    "\n"
                )




    except KeyboardInterrupt:


        print(
            "\n\n[SIGINT] Encerramento solicitado."
        )



    except Exception as fatal_error:


        print(
            "\n[FALHA CRÍTICA NO RUNTIME]:",
            fatal_error
        )



    finally:


        if kernel:


            kernel.shutdown()



        print(
            "Processo finalizado com sucesso. Até logo, Senhor."
        )



        sys.exit(0)






if __name__ == "__main__":

    main()