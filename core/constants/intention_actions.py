"""
=========================================
GENESIS CORE

Arquivo:
core/constants/intention_actions.py

Descrição:
Taxonomia de intenções cognitivas
suportadas pelo Genesis Core.

Representa ações abstratas que podem
ser produzidas por voz, texto, agentes
ou modelos de IA.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from enum import Enum



class IntentionAction(
    str,
    Enum
):


    """
    Vocabulário cognitivo do Genesis.
    """



    # ==================================================
    # BASE
    # ==================================================

    UNKNOWN = "unknown"



    # ==================================================
    # CONVERSAÇÃO
    # ==================================================

    CHAT = "chat"

    ASK = "ask"

    ANSWER = "answer"

    EXPLAIN = "explain"

    GREETING = "greeting"

    GOODBYE = "goodbye"

    THANK = "thank"



    # ==================================================
    # COGNIÇÃO
    # ==================================================

    THINK = "think"

    ANALYZE = "analyze"

    COMPARE = "compare"

    SUMMARIZE = "summarize"

    REFLECT = "reflect"

    LEARN = "learn"



    # ==================================================
    # MEMÓRIA
    # ==================================================

    REMEMBER = "remember"

    FORGET = "forget"

    SAVE_MEMORY = "save_memory"

    LOAD_MEMORY = "load_memory"

    SEARCH_MEMORY = "search_memory"



    # ==================================================
    # CONHECIMENTO
    # ==================================================

    SEARCH_KNOWLEDGE = "search_knowledge"

    SEARCH_WEB = "search_web"

    GET_INFORMATION = "get_information"



    # ==================================================
    # PLANEJAMENTO
    # ==================================================

    CREATE_PLAN = "create_plan"

    UPDATE_PLAN = "update_plan"

    CANCEL_PLAN = "cancel_plan"

    EXECUTE_PLAN = "execute_plan"



    # ==================================================
    # TAREFAS
    # ==================================================

    CREATE_TASK = "create_task"

    EXECUTE_TASK = "execute_task"

    PAUSE_TASK = "pause_task"

    RESUME_TASK = "resume_task"

    CANCEL_TASK = "cancel_task"



    # ==================================================
    # SISTEMA
    # ==================================================

    GET_STATUS = "get_status"

    DIAGNOSTIC = "diagnostic"

    RESTART_SYSTEM = "restart_system"

    SHUTDOWN_SYSTEM = "shutdown_system"



    # ==================================================
    # APLICAÇÕES
    # ==================================================

    OPEN_APPLICATION = "open_application"

    CLOSE_APPLICATION = "close_application"

    RESTART_APPLICATION = "restart_application"



    # ==================================================
    # ARQUIVOS
    # ==================================================

    OPEN_FILE = "open_file"

    CREATE_FILE = "create_file"

    SAVE_FILE = "save_file"

    DELETE_FILE = "delete_file"

    COPY_FILE = "copy_file"

    MOVE_FILE = "move_file"



    # ==================================================
    # INTERNET
    # ==================================================

    OPEN_WEBSITE = "open_website"

    DOWNLOAD_FILE = "download_file"

    SEND_REQUEST = "send_request"



    # ==================================================
    # AUTOMAÇÃO
    # ==================================================

    RUN_COMMAND = "run_command"

    RUN_SCRIPT = "run_script"

    RUN_WORKFLOW = "run_workflow"



    # ==================================================
    # DESENVOLVIMENTO
    # ==================================================

    WRITE_CODE = "write_code"

    READ_CODE = "read_code"

    DEBUG_CODE = "debug_code"

    TEST_CODE = "test_code"

    REFACTOR_CODE = "refactor_code"



    # ==================================================
    # MULTIMÍDIA
    # ==================================================

    PLAY_MEDIA = "play_media"

    PAUSE_MEDIA = "pause_media"

    STOP_MEDIA = "stop_media"

    SET_VOLUME = "set_volume"



    # ==================================================
    # IA
    # ==================================================

    GENERATE_TEXT = "generate_text"

    GENERATE_IMAGE = "generate_image"

    ANALYZE_IMAGE = "analyze_image"

    TRANSCRIBE_AUDIO = "transcribe_audio"

    SYNTHESIZE_SPEECH = "synthesize_speech"



    # ==================================================
    # VOZ
    # ==================================================

    LISTEN = "listen"

    SPEAK = "speak"

    WAKE_WORD = "wake_word"



    # ==================================================
    # AGENTES
    # ==================================================

    CREATE_AGENT = "create_agent"

    START_AGENT = "start_agent"

    STOP_AGENT = "stop_agent"

    SWITCH_PERSONALITY = "switch_personality"



    # ==================================================
    # AUTONOMIA
    # ==================================================

    OBSERVE = "observe"

    MONITOR = "monitor"

    OPTIMIZE = "optimize"

    SELF_DIAGNOSTIC = "self_diagnostic"



    # ==================================================
    # BOOT
    # ==================================================

    LOAD_MODULE = "load_module"

    UNLOAD_MODULE = "unload_module"

    RELOAD_MODULE = "reload_module"