"""
=========================================
GENESIS CORE

Arquivo:
test_genesis.py

Descrição:
Teste geral de integridade do Genesis Core.

Verifica:
- Estrutura
- Imports
- Estado cognitivo
- Pipeline
- Ferramentas
- Componentes principais

Mark:
III - Matrix
=========================================
"""


import traceback



def separator(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)



errors = []



def test(name, function):

    try:

        result = function()

        print(
            f"[OK] {name}"
        )

        return result


    except Exception as error:

        print(
            f"[ERRO] {name}"
        )

        print(
            error
        )


        errors.append(
            {
                "teste": name,
                "erro": str(error),
                "trace": traceback.format_exc()
            }
        )

        return None



# ==================================================
# IMPORTS
# ==================================================


separator(
    "TESTE DE IMPORTS"
)


test(
    "Module Base",
    lambda:
        __import__(
            "core.base.module"
        )
)



test(
    "Brain",
    lambda:
        __import__(
            "core.mind.brain"
        )
)



test(
    "Mind",
    lambda:
        __import__(
            "core.mind.mind"
        )
)



test(
    "Pipeline",
    lambda:
        __import__(
            "core.pipeline.cognitive_pipeline"
        )
)



test(
    "Reasoner",
    lambda:
        __import__(
            "core.cognitive.reasoner"
        )
)



# ==================================================
# ESTADO MENTAL
# ==================================================


separator(
    "TESTE BRAIN STATE"
)


def create_brain_state():


    from core.mind.brain_state import BrainState


    state = BrainState()


    state.initialize()


    return state



state = test(
    "Criar BrainState",
    create_brain_state
)



if state:


    print(
        "Snapshot:"
    )


    print(
        state.snapshot()
    )



# ==================================================
# MEMORIA
# ==================================================


separator(
    "TESTE MEMORIA"
)


def test_memory():


    from core.mind.memory import Memory


    memory = Memory()


    memory.initialize()


    entry = memory.store(
        {
            "teste":
            "Genesis funcionando"
        }
    )


    return entry



test(
    "Memory Store",
    test_memory
)



# ==================================================
# KNOWLEDGE
# ==================================================


separator(
    "TESTE KNOWLEDGE"
)



def test_knowledge():


    from core.mind.knowledge import Knowledge


    knowledge = Knowledge()


    knowledge.initialize()


    return knowledge.add(
        "teste",
        "Genesis funcionando"
    )



test(
    "Knowledge Add",
    test_knowledge
)



# ==================================================
# TOOL MANAGER
# ==================================================


separator(
    "TESTE TOOL MANAGER"
)



def test_tools():


    from core.managers.tool_manager import ToolManager


    manager = ToolManager()


    manager.initialize()


    return manager



tool_manager = test(
    "ToolManager",
    test_tools
)



# ==================================================
# PIPELINE
# ==================================================


separator(
    "TESTE PIPELINE"
)



def build_pipeline():


    from core.pipeline.pipeline_initializer import (
        PipelineInitializer
    )


    pipeline = PipelineInitializer(
        tool_manager=tool_manager
    ).build()


    return pipeline



pipeline = test(
    "Construir Pipeline",
    build_pipeline
)



if pipeline:


    print(
        "\nETAPAS:"
    )


    print(
        pipeline.list_steps()
    )



# ==================================================
# TESTE COGNITIVO COMPLETO
# ==================================================


separator(
    "TESTE COGNITIVO COMPLETO"
)



def run_pipeline():


    result = pipeline.process(
        "Jarvis teste seu sistema cognitivo"
    )


    return result



context = None


if pipeline:

    context = test(
        "Executar Pipeline",
        run_pipeline
    )



if context:


    print(
        "\nRESUMO:"
    )


    print(
        context.summary()
    )



    print(
        "\nDADOS:"
    )


    for key, value in context.data.items():

        print(
            "\n---",
            key,
            "---"
        )

        print(
            value
        )



# ==================================================
# RESULTADO FINAL
# ==================================================


separator(
    "RESULTADO FINAL"
)



if errors:


    print(
        f"[FALHAS] {len(errors)} erro(s)"
    )


    for error in errors:


        print(
            "\nTeste:",
            error["teste"]
        )


        print(
            error["erro"]
        )



else:


    print(
        "[SUCESSO] Genesis Core passou em todos os testes."
    )