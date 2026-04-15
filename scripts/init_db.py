#!/usr/bin/env python3
"""
Database initialization script.
"""
import asyncio
import asyncpg
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


async def init_database():
    """Initialize the database with required tables."""
    database_url = os.getenv("DATABASE_URL", "postgresql://agency:agency_pass@localhost:5432/agency_db")
    
    print(f"Connecting to database: {database_url[:30]}...")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("Connected to database successfully!")
        
        # Create tables
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created users table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                key_hash VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(100),
                is_active BOOLEAN DEFAULT true,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP
            );
        """)
        print("Created api_keys table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                config JSONB,
                is_active BOOLEAN DEFAULT true,
                created_by INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created workflows table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                assigned_agent VARCHAR(100),
                status VARCHAR(50) DEFAULT 'pending',
                priority INTEGER DEFAULT 1,
                input_data JSONB,
                output_data JSONB,
                error_message TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created tasks table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_interactions (
                id SERIAL PRIMARY KEY,
                source_agent VARCHAR(100) NOT NULL,
                target_agent VARCHAR(100),
                event_type VARCHAR(100),
                message TEXT,
                data JSONB,
                correlation_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created agent_interactions table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                content TEXT,
                content_hash VARCHAR(64),
                metadata JSONB,
                tags TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created knowledge_base table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_memories (
                id SERIAL PRIMARY KEY,
                agent_name VARCHAR(100) NOT NULL,
                session_id VARCHAR(100),
                memory_type VARCHAR(50) DEFAULT 'short_term',
                key VARCHAR(200),
                value JSONB,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created agent_memories table")
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id SERIAL PRIMARY KEY,
                metric_name VARCHAR(100) NOT NULL,
                metric_value FLOAT NOT NULL,
                labels JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Created system_metrics table")
        
        # Create indexes
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_workflow_id ON tasks(workflow_id);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent_interactions_correlation_id 
            ON agent_interactions(correlation_id);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_base_tags ON knowledge_base USING gin(tags);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent_memories_agent_session 
            ON agent_memories(agent_name, session_id);
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_system_metrics_name_timestamp 
            ON system_metrics(metric_name, timestamp);
        """)
        
        print("Created indexes")
        
        # Insert default admin user (password: admin123)
        # In production, use proper password hashing
        await conn.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES ('admin', 'admin@agency.local', 'admin123')
            ON CONFLICT (username) DO NOTHING;
        """)
        print("Created default admin user")
        
        # Insert sample workflows
        sample_workflows = [
            {
                "name": "Content Creation Pipeline",
                "description": "Automated content creation from idea to publication",
                "config": {
                    "steps": [
                        {"agent": "content_manager", "action": "generate_ideas"},
                        {"agent": "seo_copywriter", "action": "write_content"},
                        {"agent": "seo_specialist", "action": "optimize"},
                        {"agent": "social_media_manager", "action": "schedule_posts"}
                    ]
                }
            },
            {
                "name": "SEO Audit Workflow",
                "description": "Comprehensive SEO analysis and recommendations",
                "config": {
                    "steps": [
                        {"agent": "seo_specialist", "action": "technical_audit"},
                        {"agent": "data_analyst", "action": "analyze_performance"},
                        {"agent": "marketing_strategist", "action": "create_recommendations"}
                    ]
                }
            },
            {
                "name": "Marketing Campaign Setup",
                "description": "End-to-end campaign creation and deployment",
                "config": {
                    "steps": [
                        {"agent": "marketing_strategist", "action": "define_strategy"},
                        {"agent": "content_manager", "action": "create_assets"},
                        {"agent": "ppc_specialist", "action": "setup_ads"},
                        {"agent": "email_marketing_manager", "action": "setup_emails"}
                    ]
                }
            }
        ]
        
        for workflow in sample_workflows:
            await conn.execute("""
                INSERT INTO workflows (name, description, config)
                VALUES ($1, $2, $3)
                ON CONFLICT DO NOTHING;
            """, workflow["name"], workflow["description"], workflow["config"])
        
        print("Created sample workflows")
        
        await conn.close()
        print("\nDatabase initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_database())