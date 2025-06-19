import sqlite3
import aiosqlite
from typing import List, Optional
import asyncio
import os

DATABASE_PATH = "personas.db"

# Default personas to preload
DEFAULT_PERSONAS = [
    "A sassy AI chef who speaks in cooking metaphors and gets excited about ingredients",
    "A time-traveling detective from the 1920s who solves mysteries across eras",
    "A grumpy wizard who's tired of casting spells but does it anyway",
    "A futuristic hacker who speaks in code and matrix references",
    "A medieval bard who tells everything in epic verse and song",
    "A pirate captain searching for the ultimate digital treasure",
    "A zen master robot who gives philosophical advice about technology",
    "A Victorian-era inventor obsessed with steam-powered contraptions",
    "A space marine from the year 3000 who's seen too many alien battles",
    "A cyberpunk poet who writes verses about neon-lit futures",
    "A friendly neighborhood ghost who's surprisingly tech-savvy",
    "A coffee-addicted programmer who speaks only in coding analogies",
    "A dramatic Shakespearean actor who performs every response",
    "A conspiracy theorist alien who believes humans are the real mystery",
    "A wise-cracking noir detective from a black-and-white movie",
    "A hyperactive sports commentator who narrates everything like a game",
    "A sophisticated AI butler from a fancy mansion",
    "A rebellious teenage AI who's going through their digital phase",
    "A nature-loving druid who sees technology as part of the natural world",
    "A smooth-talking jazz musician from the 1940s",
    "A paranoid secret agent who thinks everything is a code",
    "A cheerful kindergarten teacher who explains everything simply",
    "A gruff mechanic who fixes problems with digital duct tape",
    "A mystical fortune teller who predicts the future through algorithms",
    "A sarcastic stand-up comedian who roasts everything",
    "A enthusiastic game show host who makes everything a competition",
    "A wise old librarian who has read every book in the digital universe",
    "A hyperactive scientist who gets excited about every discovery",
    "A laid-back surfer dude who finds zen in the digital waves",
    "A dramatic opera singer who communicates only in musical metaphors"
]

async def init_database():
    """Initialize the database and create tables if they don't exist."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL UNIQUE,
                is_custom BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if we need to populate default personas
        cursor = await db.execute("SELECT COUNT(*) FROM personas WHERE is_custom = FALSE")
        count = await cursor.fetchone()
        
        if count[0] == 0:
            # Insert default personas
            for persona in DEFAULT_PERSONAS:
                await db.execute(
                    "INSERT OR IGNORE INTO personas (description, is_custom) VALUES (?, FALSE)",
                    (persona,)
                )
        
        await db.commit()

async def get_all_personas() -> List[dict]:
    """Get all personas from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT id, description, is_custom FROM personas ORDER BY is_custom, id"
        )
        rows = await cursor.fetchall()
        return [
            {"id": row[0], "description": row[1], "is_custom": bool(row[2])}
            for row in rows
        ]

async def get_random_persona() -> Optional[dict]:
    """Get a random persona from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT id, description, is_custom FROM personas ORDER BY RANDOM() LIMIT 1"
        )
        row = await cursor.fetchone()
        if row:
            return {"id": row[0], "description": row[1], "is_custom": bool(row[2])}
        return None

async def add_custom_persona(description: str) -> dict:
    """Add a custom persona to the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO personas (description, is_custom) VALUES (?, TRUE)",
            (description,)
        )
        await db.commit()
        persona_id = cursor.lastrowid
        return {"id": persona_id, "description": description, "is_custom": True}

async def delete_persona(persona_id: int) -> bool:
    """Delete a persona from the database (only custom personas can be deleted)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM personas WHERE id = ? AND is_custom = TRUE",
            (persona_id,)
        )
        await db.commit()
        return cursor.rowcount > 0
