import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
import aioserial
from contextlib import asynccontextmanager
import codecs

# Task in parallel: Read from serial
@asynccontextmanager
async def lifespan(app: FastAPI):
	asyncio.create_task(task_read_serial())
	yield

size = 3
# Constructor
aioserial_instance: aioserial.AioSerial = aioserial.AioSerial('COM12', 9600)
    # ... same with what can be passed to serial.Serial ...,

last_message_recieved = ''
event = asyncio.Event()

async def task_read_serial():
	global last_message_recieved
	while True:
		last_message_recieved = await aioserial_instance.read_async(size)
		print(last_message_recieved)
		event.set()
		event.clear()

# Create the instance of the app
app = FastAPI(lifespan=lifespan)

# Task in parallel: request the server 
@app.get('/stream')
async def message_stream(request: Request):
	async def event_generator():
		while True:
			await event.wait()
			yield str(last_message_recieved)

	return EventSourceResponse(event_generator())

app.mount("/", StaticFiles(directory="./", html=True), name="site")
uvicorn.run(app, host="0.0.0.0", port=8000)