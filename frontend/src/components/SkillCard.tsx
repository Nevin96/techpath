import type { Skill } from "../types";

interface SkillCardProps {
  skill: Skill;
  onClick: () => void;
}

function SkillCard({
  skill,
  onClick,
}: SkillCardProps) {
  return (
    <button
      onClick={onClick}
      className="group rounded-2xl border border-slate-200 bg-white p-5 text-left transition hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg"
    >
      <div className="mb-4 flex items-center justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 font-semibold text-indigo-600">
          {skill.name.charAt(0)}
        </div>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
          {skill.difficulty}
        </span>
      </div>

      <h3 className="font-semibold text-slate-900 group-hover:text-indigo-600">
        {skill.name}
      </h3>

      <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-500">
        {skill.description}
      </p>
    </button>
  );
}

export default SkillCard;