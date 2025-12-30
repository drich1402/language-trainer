"""
Seed database with vocabulary data from vocabulary.json
"""
import asyncio
import json
from pathlib import Path
from sqlalchemy import select
from models.database import AsyncSessionLocal, engine
from models.models import Vocabulary

async def seed_vocabulary():
    """Load vocabulary from JSON file into database."""
    vocab_file = Path(__file__).parent / "vocabulary.json"
    
    if not vocab_file.exists():
        print("❌ vocabulary.json not found. Run scripts/scrape_vocab.py first.")
        return
    
    with open(vocab_file, "r", encoding="utf-8") as f:
        vocabulary_data = json.load(f)
    
    async with AsyncSessionLocal() as session:
        # Check if vocabulary already exists
        result = await session.execute(select(Vocabulary))
        existing = result.scalars().all()
        
        if existing:
            print(f"⚠️  Database already contains {len(existing)} vocabulary entries.")
            response = input("Do you want to clear and re-seed? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed.")
                return
            
            # Clear existing vocabulary
            for vocab in existing:
                await session.delete(vocab)
            await session.commit()
            print("✅ Cleared existing vocabulary.")
        
        # Insert new vocabulary
        for item in vocabulary_data:
            vocab = Vocabulary(
                german=item["german"],
                spanish=item["spanish"],
                word_class=item.get("word_class"),
                frequency_rank=item.get("frequency_rank"),
                example_de=item.get("example_de"),
                example_es=item.get("example_es"),
                difficulty=item.get("difficulty", 1)
            )
            session.add(vocab)
        
        await session.commit()
        print(f"✅ Seeded {len(vocabulary_data)} vocabulary entries into database.")

if __name__ == "__main__":
    asyncio.run(seed_vocabulary())
