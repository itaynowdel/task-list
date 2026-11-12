from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    
    priority = task.get("priority") #יצירת משתנה חדש בשם priority שמקבל את הערך של המפתח "priority" מהמשימה שהתקבלה. אם המפתח לא קיים, הערך יהיה None.
    if priority == None: #בודק אם לא קיבל ערך נותן לו 2 כברירת מחדל
        priority = 2
    if type(priority) != int: #בודק שמדובר בINT אחרת מחזיר שגיאה
        raise HTTPException(status_code=400, detail="Priority must be an integer") 
    if priority < 1 or priority > 3: #בודק את הטווח
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 3")
      
        
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority #הוספת שדה
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
