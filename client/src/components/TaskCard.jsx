import { useNavigate } from "react-router-dom";



export function TaskCard({ task }) {
  const navigate = useNavigate();

  return (
<div
  className="bg-zinc-800 p-3 hover:bg-zinc-700 hover:cursor-pointer flex items-center"
  onClick={() => {
    navigate(`/placas/${task.id}`);
  }}
>
  <div className="image-container">
    <img src={task.imagen} alt="Imagen" />
  </div>
  <div className="ml-4">
    <h1 className="text-white font-bold uppercase rounded-lg">Placa generada</h1>
    <p className="text-slate-400">{task.texto_generado}</p>
    <h1 className="text-white font-bold uppercase rounded-lg">Placa correcta</h1>
    <p className="text-slate-400">{task.texto_ingresado}</p>
    <h1 className="text-white font-bold uppercase rounded-lg">Precision</h1>
    <p className="text-slate-400">{task.precision}</p>
  </div>
</div>


  );
}


