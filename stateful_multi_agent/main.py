import asyncio

# Import the main customer service agent
from customer_service_agent.agent import customer_service_agent
from config import AppConfig, DatabaseConfig
from database_utils import CustomerServiceDatabase
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import add_user_query_to_history, call_agent_async
from auth import authenticate_prompt  # import auth demo

load_dotenv()

# ===== PART 1: User Authentication =====
# Prompt user to authenticate
USER_ID = authenticate_prompt()

# ===== PART 2: Initialize Persistent Session Service =====
# Using SQLite database for persistent storage
db_url = DatabaseConfig.get_db_url()
session_service = DatabaseSessionService(db_url=db_url)
db_utils = CustomerServiceDatabase(db_url)


async def main_async():
    # Setup constants
    APP_NAME = AppConfig.get_app_name()
    # Define initial state using authenticated user
    initial_state = AppConfig.get_initial_state(user_name=USER_ID)

    print(f"🚀 Starting Customer Service System")
    print(f"📊 Database: {db_url}")
    print(f"👤 User: {USER_ID}")
    print(f"🏢 App: {APP_NAME}\n")

    # ===== PART 3: Session Management - Find or Create =====
    # Check for existing sessions for this user
    try:
        existing_sessions = await session_service.list_sessions(
            app_name=APP_NAME,
            user_id=USER_ID,
        )

        # If there's an existing session, use it, otherwise create a new one
        if existing_sessions and len(existing_sessions.sessions) > 0:
            # Use the most recent session
            SESSION_ID = existing_sessions.sessions[0].id
            print(f"📂 Continuing existing session: {SESSION_ID}")

            # Display user summary
            summary = await db_utils.get_user_interaction_summary(APP_NAME, USER_ID)
            print(f"📈 Session Summary:")
            print(f"   • Total sessions: {summary['total_sessions']}")
            print(f"   • Total interactions: {summary['total_interactions']}")
            print(
                f"   • Agents used: {', '.join(summary['agents_used']) if summary['agents_used'] else 'None'}"
            )
        else:
            # Create a new session with initial state
            new_session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                state=initial_state,
            )
            SESSION_ID = new_session.id
            print(f"🆕 Created new session: {SESSION_ID}")

    except Exception as e:
        print(f"❌ Error with session management: {e}")
        # If there's an error, try to create a new session with a different approach
        print("🔄 Attempting to create a fresh session...")
        try:
            new_session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                state=initial_state,
            )
            SESSION_ID = new_session.id
            print(f"✅ Created new session: {SESSION_ID}")
        except Exception as create_error:
            print(f"❌ Failed to create session: {create_error}")
            return

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the main customer service agent
    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Customer Service Chat!")
    print("Your conversation history and course information will be saved.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break

        # Update interaction history with the user's query
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== PART 6: State Examination =====
    # Show final session state
    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
