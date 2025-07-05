"""Database utilities for the customer service multiagent system."""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from google.adk.sessions import DatabaseSessionService
from pydantic import BaseModel


class SessionInfo(BaseModel):
    """Pydantic model for session information."""
    session_id: str
    user_id: str
    app_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    state: Dict


class CustomerServiceDatabase:
    """Database management utilities for customer service system."""
    
    def __init__(self, db_url: str = "sqlite:///./customer_service_data.db"):
        """Initialize the database service.
        
        Args:
            db_url: SQLite database URL
        """
        self.db_url = db_url
        self.session_service = DatabaseSessionService(db_url=db_url)
    
    async def get_user_sessions(self, app_name: str, user_id: str) -> List[SessionInfo]:
        """Get all sessions for a specific user.
        
        Args:
            app_name: The application name
            user_id: The user ID
            
        Returns:
            List of session information
        """
        try:
            sessions_response = await self.session_service.list_sessions(
                app_name=app_name,
                user_id=user_id,
            )
            
            session_infos = []
            for session in sessions_response.sessions:
                # Try to extract timestamps from state if available, else set to None
                created_at = session.state.get("created_at")
                updated_at = session.state.get("updated_at")
                # Convert to datetime if present and not None
                if created_at:
                    created_at = datetime.fromisoformat(created_at)
                else:
                    created_at = None
                if updated_at:
                    updated_at = datetime.fromisoformat(updated_at)
                else:
                    updated_at = None
                session_info = SessionInfo(
                    session_id=session.id,
                    user_id=session.user_id,
                    app_name=session.app_name,
                    created_at=created_at,
                    updated_at=updated_at,
                    state=session.state
                )
                session_infos.append(session_info)
            
            return session_infos
        except Exception as e:
            print(f"Error retrieving user sessions: {e}")
            return []
    
    async def get_user_course_history(self, app_name: str, user_id: str) -> List[Dict]:
        """Get all purchased courses across all sessions for a user.
        
        Args:
            app_name: The application name
            user_id: The user ID
            
        Returns:
            List of all purchased courses
        """
        sessions = await self.get_user_sessions(app_name, user_id)
        all_courses = []
        
        for session in sessions:
            courses = session.state.get("purchased_courses", [])
            for course in courses:
                if isinstance(course, dict):
                    course_info = course.copy()
                    course_info["session_id"] = session.session_id
                    all_courses.append(course_info)
        
        return all_courses
    
    async def get_user_interaction_summary(self, app_name: str, user_id: str) -> Dict:
        """Get a summary of user interactions across all sessions.
        
        Args:
            app_name: The application name
            user_id: The user ID
            
        Returns:
            Summary dictionary with interaction statistics
        """
        sessions = await self.get_user_sessions(app_name, user_id)
        
        total_interactions = 0
        query_count = 0
        response_count = 0
        agents_used = set()
        
        for session in sessions:
            interactions = session.state.get("interaction_history", [])
            total_interactions += len(interactions)
            
            for interaction in interactions:
                if isinstance(interaction, dict):
                    action = interaction.get("action", "")
                    if action == "user_query":
                        query_count += 1
                    elif action == "agent_response":
                        response_count += 1
                        agent = interaction.get("agent", "")
                        if agent:
                            agents_used.add(agent)
        
        return {
            "total_sessions": len(sessions),
            "total_interactions": total_interactions,
            "user_queries": query_count,
            "agent_responses": response_count,
            "agents_used": list(agents_used),
            "latest_session": sessions[0].session_id if sessions else None,
        }
    
    async def cleanup_old_sessions(
        self, 
        app_name: str, 
        user_id: str, 
        keep_latest: int = 5
    ) -> int:
        """Clean up old sessions, keeping only the most recent ones.
        
        Args:
            app_name: The application name
            user_id: The user ID
            keep_latest: Number of latest sessions to keep
            
        Returns:
            Number of sessions deleted
        """
        sessions = await self.get_user_sessions(app_name, user_id)
        
        if len(sessions) <= keep_latest:
            return 0
        
        # Sort by updated_at descending (most recent first)
        sessions.sort(key=lambda x: x.updated_at, reverse=True)
        sessions_to_delete = sessions[keep_latest:]
        
        deleted_count = 0
        for session in sessions_to_delete:
            try:
                # Note: DatabaseSessionService doesn't have a delete method in the current API
                # This is a placeholder for when the API supports session deletion
                print(f"Would delete session: {session.session_id}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting session {session.session_id}: {e}")
        
        return deleted_count
    
    async def export_user_data(self, app_name: str, user_id: str) -> Dict:
        """Export all user data for backup or analysis.
        
        Args:
            app_name: The application name
            user_id: The user ID
            
        Returns:
            Complete user data export
        """
        sessions = await self.get_user_sessions(app_name, user_id)
        courses = await self.get_user_course_history(app_name, user_id)
        summary = await self.get_user_interaction_summary(app_name, user_id)
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "app_name": app_name,
            "summary": summary,
            "courses": courses,
            "sessions": [session.dict() for session in sessions],
        }


async def main():
    """Example usage of the database utilities."""
    db = CustomerServiceDatabase()
    
    # Example operations
    app_name = "Customer Support"
    user_id = "aiwithantony"
    
    print("=== Customer Service Database Utilities ===\n")
    
    # Get user sessions
    sessions = await db.get_user_sessions(app_name, user_id)
    print(f"Found {len(sessions)} sessions for user {user_id}")
    
    # Get course history
    courses = await db.get_user_course_history(app_name, user_id)
    print(f"Found {len(courses)} courses purchased")
    
    # Get interaction summary
    summary = await db.get_user_interaction_summary(app_name, user_id)
    print("Interaction Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Export user data
    export_data = await db.export_user_data(app_name, user_id)
    print(f"\nExported {len(export_data)} data categories")


if __name__ == "__main__":
    asyncio.run(main())
