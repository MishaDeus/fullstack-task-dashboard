import { useEffect, useState } from "react";
import API from "../api/client";
import { PieChart, Pie, Cell } from "recharts";

export default function TaskChart() {
  const [data, setData] = useState([]);

  const fetchStats = async () => {
    const res = await API.get("/tasks/stats");

    const chartData = [
      { name: "Todo", value: res.data.todo },
      { name: "In Progress", value: res.data.in_progress },
      { name: "Done", value: res.data.done },
    ];

    setData(chartData);
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div>
      <h3>Task Stats</h3>
      <PieChart width={300} height={300}>
        <Pie data={data} dataKey="value" outerRadius={100} label>
          {data.map((entry, index) => (
            <Cell key={index} />
          ))}
        </Pie>
      </PieChart>
    </div>
  );
}