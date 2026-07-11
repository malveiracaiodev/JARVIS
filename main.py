"""
=========================================
JARVIS CORE

Arquivo:
main.py

Genesis Core
Mark II

Autor:
Caio Vitor Malveira
=========================================
"""


import time


from core.kernel.kernel import Kernel





def main():


    kernel = Kernel()


    kernel.boot()



    print()


    print(
        "JARVIS ONLINE"
    )


    print()



    print(
        "SYSTEM HEALTH:"
    )


    print(
        kernel.health()
    )



    print()



    print(
        "REGISTRY:"
    )


    print(
        kernel.registry.diagnostics()
    )



    print()



    while True:


        time.sleep(1)







if __name__ == "__main__":


    main()