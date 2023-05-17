import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { createTask, deleteTask, getTask, updateTask } from "../api/tasks.api";
import { toast } from "react-hot-toast";
import axios from "axios";

export function TaskFormPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm();
  const navigate = useNavigate();
  const params = useParams();

  const sendDataToBackend = async (formData) => {
    try {
      await axios.post("/api/tu-ruta-en-django/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      toast.success("Data sent to backend", {
        position: "bottom-right",
        style: {
          background: "#101010",
          color: "#fff",
        },
      });
    } catch (error) {
      toast.error("Error sending data to backend", {
        position: "bottom-right",
        style: {
          background: "#101010",
          color: "#fff",
        },
      });
    }
  };
  
  const onSubmit = handleSubmit(async (data) => {
    try {
      const formData = new FormData();
      formData.append("imagen", data.imagen[0]);
      formData.append("texto_ingresado", data.texto_ingresado);
  
      if (params.id) {
        await updateTask(params.id, formData);
      } else {
        await createTask(formData);
      }
  
      await axios.post("/api/tu-ruta-en-django/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      toast.success("Data sent to backend", {
        position: "bottom-right",
        style: {
          background: "#101010",
          color: "#fff",
        },
      });
    } catch (error) {
      toast.error("Error sending data to backend", {
        position: "bottom-right",
        style: {
          background: "#101010",
          color: "#fff",
        },
      });
    }
  
    navigate("/tasks");
  });
  

  return (
    <div className="max-w-xl mx-auto">
      <form onSubmit={onSubmit} className="bg-zinc-800 p-10 rounded-lg mt-2">
        <input
          type="text"
          placeholder="texto_ingresado"
          {...register("texto_ingresado", { required: true })}
          className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
        />
        {errors.texto_ingresado && <span>Este campo es requerido.</span>}

        <input
          type="file"
          {...register("imagen", { required: true })}
          className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
        />
        {errors.imagen && <span>Este campo es requerido.</span>}

        <button className="bg-indigo-500 p-3 rounded-lg block w-full mt-3">
          Guardar
        </button>
      </form>

      {params.id && (
        <div className="flex justify-end">
          <button
            className="bg-red-500 p-3 rounded-lg w-48 mt-3"
            onClick={async () => {
              const accepted = window.confirm("Are you sure?");
              if (accepted) {
                await deleteTask(params.id);
                toast.success("Task Removed", {
                  position: "bottom-right",
                  style: {
                    background: "#101010",
                    color: "#fff",
                  },
                });
                navigate("/tasks");
              }
            }}
          >
            delete
          </button>
        </div>
      )}
    </div>
  );
}
