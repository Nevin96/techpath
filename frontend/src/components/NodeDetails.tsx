import type { GraphNode } from "../types";

interface NodeDetailsProps {
  node: GraphNode;
  onClose: () => void;
}

function NodeDetails({
  node,
  onClose,
}: NodeDetailsProps) {
  const isJob = node.type === "job";

  return (
    <div className="absolute right-6 top-6 z-20 w-80 rounded-2xl border border-slate-200 bg-white p-6 shadow-xl">

      <div className="flex items-start justify-between">

        <div>

          <span
            className={
              isJob
                ? "rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-600"
                : "rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-600"
            }
          >
            {isJob ? "JOB" : "SKILL"}
          </span>

          <h2 className="mt-4 text-xl font-bold text-slate-950">
            {node.id}
          </h2>

        </div>

        <button
          onClick={onClose}
          className="rounded-lg px-2 py-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
        >
          ✕
        </button>

      </div>


      {node.description && (

        <p className="mt-4 text-sm leading-6 text-slate-500">
          {node.description}
        </p>

      )}


      {node.difficulty && (

        <div className="mt-6 border-t border-slate-100 pt-5">

          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Difficulty
          </p>

          <p className="mt-1 font-medium text-slate-800">
            {node.difficulty}
          </p>

        </div>

      )}

    </div>
  );
}

export default NodeDetails;