from typing import TypedDict, Dict, List

class StartupState(TypedDict):

    startup_idea: str

    messages: List[str]

    chat_history: List[Dict]

    completed_tasks: List[str]

    selected_tools: List[str]

    tool_outputs: Dict

    next_action: str

    reflection: str

    final_report: str

    iteration_count: int

    tool_retry_counts: Dict


