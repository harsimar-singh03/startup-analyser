import streamlit as st
from graph import graph
from nodes.chat_node import chat_node
from utils.report_generator import generate_report
from utils.tool_names import TOOL_DISPLAY_NAMES
from utils.db import (
    init_db,
    save_message,
    load_history,
    get_all_threads,
    new_thread_id,
    save_research,
    load_research,
)

# -----------------------------------
# INIT DB
# -----------------------------------

init_db()

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Startup Intelligence Agent",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>
    /* Sidebar thread buttons */
    div[data-testid="stSidebar"] .stButton button {
        text-align: left;
        background: transparent;
        border: 1px solid transparent;
        color: var(--text-color);
        font-size: 13px;
        padding: 6px 10px;
        border-radius: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    div[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.15);
    }
    /* Active thread highlight */
    div[data-testid="stSidebar"] .active-thread button {
        background: rgba(99,102,241,0.15) !important;
        border-color: rgba(99,102,241,0.4) !important;
    }
    /* New chat button */
    div[data-testid="stSidebar"] .new-chat-btn button {
        background: #6366f1 !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
    }
    div[data-testid="stSidebar"] .new-chat-btn button:hover {
        background: #4f46e5 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# THREAD ID — persisted via URL params
# -----------------------------------

params = st.query_params

if "thread" in params:
    st.session_state["thread_id"] = params["thread"]
elif "thread_id" not in st.session_state:
    st.session_state["thread_id"] = new_thread_id()

thread_id = st.session_state["thread_id"]
st.query_params["thread"] = thread_id

# -----------------------------------
# RESTORE RESULT FROM DB ON REFRESH
# -----------------------------------

if "result" not in st.session_state:
    saved = load_research(thread_id)
    if saved:
        st.session_state["result"] = {
            "startup_idea": saved["startup_idea"],
            "tool_outputs": saved["tool_outputs"],
            "chat_history": [],
            "messages": [],
            "completed_tasks": list(saved["tool_outputs"].keys()),
            "selected_tools": [],
            "next_action": "FINISHED",
            "reflection": "",
            "final_report": "",
            "iteration_count": 0,
            "tool_retry_counts": {}
        }

# -----------------------------------
# SIDEBAR — thread list
# -----------------------------------

with st.sidebar:
    st.markdown("## 💬 Chats")

    with st.container():
        st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
        if st.button("+ New Chat", use_container_width=True):
            new_tid = new_thread_id()
            st.session_state["thread_id"] = new_tid
            st.session_state.pop("result", None)
            st.session_state.pop("report_file", None)
            st.query_params["thread"] = new_tid
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    threads = get_all_threads()

    if not threads:
        st.caption("No chats yet. Start a new one!")
    else:
        for t in threads:
            label = f"🔍 {t['title']}" if t["title"] else "Untitled chat"
            is_active = t["thread_id"] == thread_id

            if is_active:
                st.markdown('<div class="active-thread">', unsafe_allow_html=True)

            if st.button(label, key=f"thread_{t['thread_id']}", use_container_width=True):
                st.session_state["thread_id"] = t["thread_id"]
                st.session_state.pop("result", None)
                st.session_state.pop("report_file", None)
                st.query_params["thread"] = t["thread_id"]
                st.rerun()

            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# MAIN TITLE
# -----------------------------------

st.title("Startup Intelligence Agent")

# -----------------------------------
# RESEARCH SECTION
# -----------------------------------

# Show input only if no research done for this thread
if "result" not in st.session_state:

    startup_idea = st.text_area(
        "Enter your startup idea",
        placeholder="e.g. start a business of ...."
    )

    if st.button("Run Research") and startup_idea.strip():

        status_box = st.empty()
        progress_container = st.container()

        initial_state = {
            "startup_idea": startup_idea,
            "messages": [],
            "chat_history": [],
            "completed_tasks": [],
            "selected_tools": [],
            "tool_outputs": {},
            "next_action": "",
            "reflection": "",
            "final_report": "",
            "iteration_count": 0,
            "tool_retry_counts": {}
        }

        status_box.info("Supervisor Agent Started")
        final_state = None

        for step in graph.stream(initial_state):
            for node_name, node_output in step.items():

                if node_name == "supervisor":
                    selected_tools = node_output.get("selected_tools", [])
                    if selected_tools:
                        names = [
                            TOOL_DISPLAY_NAMES.get(t, t)
                            for t in selected_tools
                        ]
                        status_box.info(
                            f"Supervisor Selected: {', '.join(names)}"
                        )

                elif node_name == "tool_executor":
                    with progress_container:
                        for tool in node_output.get("completed_tasks", []):
                            st.success(
                                f"{TOOL_DISPLAY_NAMES.get(tool, tool)} Completed"
                            )

                elif node_name == "reflection":
                    status_box.info(
                        f"Reflection: {node_output.get('reflection', '')}"
                    )

                if final_state is None:
                    final_state = initial_state.copy()
                final_state.update(node_output)

        # Save to session + DB
        st.session_state["result"] = final_state

        save_research(
            thread_id,
            startup_idea,
            final_state["tool_outputs"]
        )

        report_file = generate_report(final_state)
        st.session_state["report_file"] = report_file

        status_box.success("Research Completed Successfully!")
        st.rerun()

# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------

if "result" in st.session_state:

    result = st.session_state["result"]

    # Show startup idea as context
    st.caption(f"**Startup Idea:** {result.get('startup_idea', '')}")

    st.header("Research Results")

    for tool, output in result["tool_outputs"].items():
        display_name = TOOL_DISPLAY_NAMES.get(tool, tool)
        with st.expander(display_name):
            st.write(output.get("summary", "No summary available"))

    # -----------------------------------
    # PDF DOWNLOAD
    # -----------------------------------

    # Generate report if not already done
    if "report_file" not in st.session_state:
        report_file = generate_report(result)
        st.session_state["report_file"] = report_file

    with open(st.session_state["report_file"], "rb") as pdf_file:
        st.download_button(
            label="Download Startup Report PDF",
            data=pdf_file,
            file_name="startup_report.pdf",
            mime="application/pdf"
        )

    # -----------------------------------
    # CHAT SECTION
    # -----------------------------------

    st.header("Startup Advisor Chat")

    # Load full chat history from DB
    history = load_history(thread_id)

    # Display existing messages
    for chat in history:
        with st.chat_message(chat["role"]):
            st.write(chat["message"])

    # New message input
    user_question = st.chat_input(
        "Ask anything about your startup..."
    )

    if user_question:

        # Save + show user message
        save_message(thread_id, "user", user_question)

        with st.chat_message("user"):
            st.write(user_question)

        # Generate + save assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = chat_node(
                    result,
                    user_question,
                    history
                )
                st.write(answer)

        save_message(thread_id, "assistant", answer)

        st.rerun()