import { useState } from "react";
import API from "../api/client";

export default function TaskForm({ onCreated }) {
  const [title, setTitle] = useState("");

  const createTask = async () => {
    await API.post("/tasks", { title });
    setTitle("");
    onCreated();
  };




  return (
    <div>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button onClick={createTask}>Add</button>
    </div>
  );
}