import React, { useEffect, useState } from "react";
import { getAllTasks } from "../api/tasks.api";
import { TaskCard } from "./TaskCard";

export function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [tasksPerPage] = useState(6); // Número de tareas por página

  useEffect(() => {
    async function loadTasks() {
      const res = await getAllTasks();
      setTasks(res.data);
    }
    loadTasks();
  }, []);

  // Calcular índices de las tareas a mostrar en la página actual
  const indexOfLastTask = currentPage * tasksPerPage;
  const indexOfFirstTask = indexOfLastTask - tasksPerPage;
  const currentTasks = tasks.slice(indexOfFirstTask, indexOfLastTask);

  // Cambiar de página
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div>
      <div className="grid grid-cols-3 gap-3">
        {currentTasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
      <div className="pagination">
        <div className="pagination-button-left">
          <button
            onClick={() => paginate(currentPage - 1)}
            disabled={currentPage === 1}
            className="pagination-button"
          >
            &#8592;
          </button>
        </div>
        <div className="pagination-button-right">
          <button
            onClick={() => paginate(currentPage + 1)}
            disabled={indexOfLastTask >= tasks.length}
            className="pagination-button"
          >
            &#8594;
          </button>
        </div>
      </div>
    </div>
  );
}
