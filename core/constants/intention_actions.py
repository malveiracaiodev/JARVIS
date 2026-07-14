"""
=========================================
JARVIS CORE

Arquivo:
core/mind/constants/intention_actions.py

Descrição:
Enumeração das ações cognitivas suportadas
pelo sistema de intenções do JARVIS.

Representa ações de alto nível que podem
ser geradas pelos parsers de linguagem,
LLMs ou comandos de voz.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from enum import Enum


class IntentionAction(str, Enum):
    """
    Ações cognitivas conhecidas pelo JARVIS.
    """

    # =====================================================
    # Genéricas
    # =====================================================

    UNKNOWN = "unknown"

    # =====================================================
    # Conversação
    # =====================================================

    CHAT = "chat"

    ASK = "ask"

    ANSWER = "answer"

    EXPLAIN = "explain"

    GREETING = "greeting"

    GOODBYE = "goodbye"

    THANK = "thank"

    # =====================================================
    # Cognição
    # =====================================================

    THINK = "think"

    LEARN = "learn"

    REMEMBER = "remember"

    FORGET = "forget"

    SEARCH_MEMORY = "search_memory"

    SEARCH_KNOWLEDGE = "search_knowledge"

    REFLECT = "reflect"

    SUMMARIZE = "summarize"

    ANALYZE = "analyze"

    COMPARE = "compare"

    # =====================================================
    # Planejamento
    # =====================================================

    CREATE_PLAN = "create_plan"

    UPDATE_PLAN = "update_plan"

    CANCEL_PLAN = "cancel_plan"

    EXECUTE_PLAN = "execute_plan"

    EXECUTE_TASK = "execute_task"

    PAUSE_TASK = "pause_task"

    RESUME_TASK = "resume_task"

    CANCEL_TASK = "cancel_task"

    # =====================================================
    # Aplicações
    # =====================================================

    OPEN_APPLICATION = "open_application"

    CLOSE_APPLICATION = "close_application"

    MINIMIZE_APPLICATION = "minimize_application"

    MAXIMIZE_APPLICATION = "maximize_application"

    RESTART_APPLICATION = "restart_application"

    # =====================================================
    # Arquivos
    # =====================================================

    OPEN_FILE = "open_file"

    CREATE_FILE = "create_file"

    SAVE_FILE = "save_file"

    DELETE_FILE = "delete_file"

    COPY_FILE = "copy_file"

    MOVE_FILE = "move_file"

    RENAME_FILE = "rename_file"

    # =====================================================
    # Diretórios
    # =====================================================

    CREATE_FOLDER = "create_folder"

    DELETE_FOLDER = "delete_folder"

    OPEN_FOLDER = "open_folder"

    # =====================================================
    # Internet
    # =====================================================

    SEARCH_WEB = "search_web"

    OPEN_WEBSITE = "open_website"

    DOWNLOAD_FILE = "download_file"

    SEND_REQUEST = "send_request"

    # =====================================================
    # Sistema Operacional
    # =====================================================

    SHUTDOWN_SYSTEM = "shutdown_system"

    RESTART_SYSTEM = "restart_system"

    LOCK_SYSTEM = "lock_system"

    LOGOUT = "logout"

    OPEN_SETTINGS = "open_settings"

    # =====================================================
    # Serviços
    # =====================================================

    START_SERVICE = "start_service"

    STOP_SERVICE = "stop_service"

    RESTART_SERVICE = "restart_service"

    # =====================================================
    # Dispositivos
    # =====================================================

    CONNECT_DEVICE = "connect_device"

    DISCONNECT_DEVICE = "disconnect_device"

    SCAN_DEVICES = "scan_devices"

    # =====================================================
    # Comunicação
    # =====================================================

    SEND_MESSAGE = "send_message"

    SEND_EMAIL = "send_email"

    MAKE_CALL = "make_call"

    # =====================================================
    # Automação
    # =====================================================

    RUN_WORKFLOW = "run_workflow"

    RUN_SCRIPT = "run_script"

    RUN_COMMAND = "run_command"

    # =====================================================
    # Desenvolvimento
    # =====================================================

    WRITE_CODE = "write_code"

    READ_CODE = "read_code"

    REFACTOR_CODE = "refactor_code"

    DEBUG_CODE = "debug_code"

    TEST_CODE = "test_code"

    BUILD_PROJECT = "build_project"

    # =====================================================
    # Mídia
    # =====================================================

    PLAY_MEDIA = "play_media"

    PAUSE_MEDIA = "pause_media"

    STOP_MEDIA = "stop_media"

    NEXT_MEDIA = "next_media"

    PREVIOUS_MEDIA = "previous_media"

    SET_VOLUME = "set_volume"

    # =====================================================
    # Inteligência Artificial
    # =====================================================

    GENERATE_TEXT = "generate_text"

    GENERATE_IMAGE = "generate_image"

    ANALYZE_IMAGE = "analyze_image"

    TRANSCRIBE_AUDIO = "transcribe_audio"

    SYNTHESIZE_SPEECH = "synthesize_speech"

    # =====================================================
    # Administração
    # =====================================================

    LOAD_MODULE = "load_module"

    UNLOAD_MODULE = "unload_module"

    RELOAD_MODULE = "reload_module"

    GET_STATUS = "get_status"

    GET_INFORMATION = "get_information"

    DIAGNOSTIC = "diagnostic"