import type {
  CareerLearningPathResponse,
} from "../types";


interface LearningPathProps {
  learningPath: CareerLearningPathResponse;
  completedSkills: Set<string>;
  onToggleSkill: (skillName: string) => void;
}


function LearningPath({
  learningPath,
  completedSkills,
  onToggleSkill,
}: LearningPathProps) { 

  return (
    <div className="mt-10">

      <div className="space-y-0">

        {learningPath.path.map(
          (node, index) => {

            const isFirst = index === 0;

            const isLast =
              index === learningPath.path.length - 1;

            const isJob = node.type === "job";
            const isCompleted = node.type === "skill" && completedSkills.has(node.name);

            return (
              <div
                key={`${node.name}-${index}`}
                className="relative flex gap-5"
              >

                {/* Timeline */}

                <div className="flex flex-col items-center">

                  <div
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-bold ${
                      isFirst
                        ? "bg-indigo-500 text-white"
                        : isJob
                          ? "bg-emerald-500 text-white"
                          : "bg-white/10 text-slate-200"
                    }`}
                  >
                    {isCompleted ? "✓" : index + 1}
                  </div>

                  {!isLast && (
                    <div className="w-px flex-1 bg-white/20" />
                  )}

                </div>


                {/* Node */}

                <div className="mb-8 flex-1">

                  <button
                        type="button"
                        disabled={isJob}
                        onClick={() => {
                            if (!isJob) {
                            onToggleSkill(node.name);
                            }
                        }}
                        className={`w-full rounded-2xl border p-6 text-left transition ${
                            isCompleted
                            ? "border-emerald-500/30 bg-emerald-500/10"
                            : "border-white/10 bg-white/5"
                        } ${
                            !isJob
                            ? "cursor-pointer hover:bg-white/10"
                            : "cursor-default"
                        }`}
                    >

                    <div className="flex flex-wrap items-center gap-3">

                      <h3 className="text-lg font-semibold text-white">
                        {node.name}
                      </h3>


                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          isJob
                            ? "bg-emerald-500/20 text-emerald-300"
                            : "bg-indigo-500/20 text-indigo-300"
                        }`}
                      >
                        {isJob ? "CAREER" : "SKILL"}
                      </span>


                      {!isJob &&
                        node.difficulty && (

                          <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-300">
                            {node.difficulty}
                          </span>

                        )}
                        {isCompleted && (
                        <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-300">
                            ✓ COMPLETED
                        </span>
                        )}
                    </div>
                    </button>

                    {node.description && (

                      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
                        {node.description}
                      </p>

                    )}

                  </div>

                </div>
            );
          }
        )}

      </div>

    </div>
  );
}


export default LearningPath;