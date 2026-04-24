import { useEffect, useState } from "react";
import API from "../api/client";

export default function TaskList() {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    const res = await API.get("/tasks");
    setTasks(res.data);
  };

  const deleteTask = async (id) => {
    await API.delete(`/tasks/${id}`);
    fetchTasks();
  };

  const markDone = async (id) => {
    await API.put(`/tasks/${id}`, { status: "done" });
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div>
      <h3>Tasks</h3>
      {tasks.map((t) => (
        <div key={t.id}>
          {t.title} - {t.status}
          <button onClick={() => deleteTask(t.id)}>Delete</button>
          <button onClick={() => markDone(t.id)}>Done</button>
        </div>
      ))}
      
    </div>
  );
}