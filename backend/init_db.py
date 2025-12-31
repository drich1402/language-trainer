"""
Initialize database with vocabulary on startup if empty.
"""
import asyncio
import json
from pathlib import Path
from sqlalchemy import select, func
from models.database import AsyncSessionLocal, engine
from models.models import Base, Vocabulary

async def init_database():
    """Create tables and seed vocabulary if needed."""
    print("🔧 Initializing database...")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")
    
    # Check if vocabulary exists
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(Vocabulary.id)))
        vocab_count = result.scalar()
        
        if vocab_count > 0:
            print(f"✅ Database already has {vocab_count} vocabulary entries")
            return
        
        print("📚 Seeding vocabulary...")
        
        # Load vocabulary from JSON
        vocab_file = Path(__file__).parent / "seeds" / "vocabulary.json"
        if not vocab_file.exists():
            print(f"⚠️  Vocabulary file not found: {vocab_file}")
            return
        
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        # Insert vocabulary
        for item in vocab_data:
            vocab = Vocabulary(
                german=item['german'],
                spanish=item['spanish'],
                word_class=item.get('word_class'),
                difficulty=item.get('difficulty'),
                frequency_rank=item.get('frequency_rank')
            )
            session.add(vocab)
        
        await session.commit()
        
        # Verify
        result = await session.execute(select(func.count(Vocabulary.id)))
        final_count = result.scalar()
        print(f"✅ Seeded {final_count} vocabulary entries")

if __name__ == "__main__":
    asyncio.run(init_database())
