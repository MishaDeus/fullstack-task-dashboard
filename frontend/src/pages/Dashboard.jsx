import { useState } from "react";

import TaskList from "../components/TaskList";
import TaskForm from "../components/TaskForm";
import TaskChart from "../components/TaskChart";

export default function Dashboard() {
  const [refresh, setRefresh] = useState(false);

  return (
    <div>
      <h2>Dashboard</h2>
      <TaskForm onCreated={() => setRefresh(!refresh)} />
      <TaskList key={refresh} />
      <TaskChart />
    </div>
  );
}