import uvicorn
import asyncio



def main():
    uvicorn.run("app.main:app", port=3000, log_level="info", reload=True)


if __name__ == "__main__":
    asyncio.run(main())
