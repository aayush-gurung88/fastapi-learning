What is CORS ? 
- it stands for cross origin resource sharing 
- When frontend (browser) and backend are on different origins - browser blocks the request by default for security .

- SO CORS is needed when frontend and backend are on different origins


Origin = protocol + domain + port
http://localhost:3000  ← frontend (React/Vue)
http://localhost:8000  ← backend (FastAPI)

These are different origins --> browser blocks by default 
CORS tells the browser --> hey , allow this frontend or , this frontend is allowed to talk or share resource


NOTE : Always add CORS before other routing, authentication, and endpoint middlewares.
