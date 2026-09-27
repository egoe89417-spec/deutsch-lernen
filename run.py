import asyncio, os
from threading import Thread
import uvicorn
from dotenv import load_dotenv

load_dotenv()

def web():
    uvicorn.run("server:app",host=os.getenv("HOST","0.0.0.0"),port=int(os.getenv("PORT","8000")))

if __name__=="__main__":
    Thread(target=web,daemon=True).start()
    from bot import main
    asyncio.run(main())
