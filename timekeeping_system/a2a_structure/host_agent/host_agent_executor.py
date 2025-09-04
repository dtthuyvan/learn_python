import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, TextPart, Part
from a2a.utils import new_agent_text_message, new_task

# Giả sử bạn có HostAgent cơ bản
try:
    from .agent_host import HostAgent
except ImportError:
    from agent_host import HostAgent

from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types

class HostAgentExecutor(AgentExecutor):
    def __init__(self):
        self.host_agent = HostAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = context.current_task

        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        try:
            # 1. Tạo router agent (LLM)
            agent = self.host_agent.create_agent()
            runner = Runner(
                app_name=agent.name,
                agent=agent,
                artifact_service=InMemoryArtifactService(),
                session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService(),
            )
            session = await runner.session_service.create_session(
                app_name=agent.name,
                user_id="llm_router",
                state={},
                session_id=task.context_id,
            )

            # 2. Đóng gói query vào Content
            content = types.Content(role="user", parts=[types.Part.from_text(text=query)])

            response_text = "No response"
            async for event in runner.run_async(
                user_id="llm_router", session_id=session.id, new_message=content
            ):
                if event.is_final_response():
                    # 3. Kiểm tra function_call
                    for p in event.content.parts:
                        if hasattr(p, "function_call") and p.function_call:
                            agent_name = p.function_call.args.get("agent_name")
                            message = p.function_call.args.get("message")

                            # Forward tới agent đích
                            result = await self.host_agent.send_message(agent_name, message, tool_context=None)
                            response_text = str(result)
                        elif hasattr(p, "text") and p.text:
                            response_text = p.text

            # 4. Gửi kết quả về cho client
            await updater.add_artifact([Part(root=TextPart(text=response_text))], name="response")
            await updater.complete()

        except Exception as e:
            print(f"HostAgentExecutor error: {e}")
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Error: {str(e)}", task.context_id, task.id),
                final=True,
            )
            
    async def cancel(self, request: RequestContext, event_queue: EventQueue):
        # Chưa cần implement cancel
        return None