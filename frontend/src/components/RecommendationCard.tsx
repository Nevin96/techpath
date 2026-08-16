import type { SkillRecommendation } from "../types";

interface RecommendationCardProps {
  recommendation: SkillRecommendation;
  onClick: () => void;
}

function RecommendationCard({
  recommendation,
  onClick,
}: RecommendationCardProps) {
  return (
    <button
      onClick={onClick}
      className="group w-full rounded-2xl border border-slate-200 bg-white p-6 text-left transition hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg"
    >
      <div className="flex items-start justify-between">

        <div>
          <h3 className="font-semibold text-slate-900 transition group-hover:text-indigo-600">
            {recommendation.skill}
          </h3>

          {recommendation.difficulty && (
            <span className="mt-2 inline-block rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-600">
              {recommendation.difficulty}
            </span>
          )}
        </div>

        <span className="text-slate-400 transition group-hover:translate-x-1">
          →
        </span>

      </div>

      {recommendation.description && (
        <p className="mt-4 text-sm leading-6 text-slate-500">
          {recommendation.description}
        </p>
      )}

      {recommendation.careers.length > 0 && (
        <div className="mt-5 border-t border-slate-100 pt-4">

          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Career paths
          </p>

          <div className="mt-2 flex flex-wrap gap-2">
            {recommendation.careers.map((career) => (
              <span
                key={career}
                className="rounded-lg bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700"
              >
                {career}
              </span>
            ))}
          </div>

        </div>
      )}

    </button>
  );
}

export default RecommendationCard;