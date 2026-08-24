# Practice Task

# Make POST /register/{email}:

# Returns {"message": "Registration successful"} immediately
# In background → writes to registrations.txt:
#   New registration: email@example.com

# Run it → check the file appears after the response.


from fastapi import FastAPI , BackgroundTasks

app = FastAPI()

# this is called helper function 
# def send_successful_email(email: str, name: str):
#     print(f"Sending email to {name} at {email}")


def writetofile(email:str):
    print(f"THis is the email {email}")
    with open("registrations.txt","a") as file:
        file.write(f"New registration: {email}")

@app.post("/register/{email}")
async def add_email(email:str, background_tasks: BackgroundTasks):

    background_tasks.add_task(writetofile, email )

    return{
        "message": "Registration Successful"
    }