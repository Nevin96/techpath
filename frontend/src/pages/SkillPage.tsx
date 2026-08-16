import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import RecommendationCard from "../components/RecommendationCard";

import {
  getSkill,
  getRelatedSkills,
  getJobsForSkill,
  getRecommendations,
} from "../services/api";

import type {
  RecommendationResponse,
} from "../types";
import type { Skill, Job } from "../types";


function SkillPage() {
  const { skillName } = useParams<{ skillName: string }>();

  const [skill, setSkill] = useState<Skill | null>(null);
  const [relatedSkills, setRelatedSkills] = useState<Skill[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);

  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    async function loadSkill() {
      if (!skillName) {
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const [skillData, relatedData, jobsData,recommendationData] =
          await Promise.all([
            getSkill(skillName),
            getRelatedSkills(skillName),
            getJobsForSkill(skillName),
            getRecommendations(skillName),
          ]);

        setSkill(skillData);
        setRelatedSkills(relatedData);
        setJobs(jobsData);
        setRecommendations(recommendationData);

      } catch (error) {
        console.error(error);

        setError(
          "Unable to load this skill."
        );

      } finally {
        setLoading(false);
      }
    }

    loadSkill();
  }, [skillName]);


  if (loading) {
    return (
      <main className="mx-auto max-w-6xl px-6 py-16">

        <div className="animate-pulse">

          <div className="h-5 w-24 rounded bg-slate-200" />

          <div className="mt-6 h-12 w-72 rounded bg-slate-200" />

          <div className="mt-4 h-5 w-96 max-w-full rounded bg-slate-200" />

        </div>

      </main>
    );
  }


  if (error || !skill) {
    return (
      <main className="mx-auto max-w-6xl px-6 py-16">

        <Link
          to="/"
          className="text-sm font-medium text-indigo-600"
        >
          ← Back to Explore
        </Link>

        <div className="mt-12 rounded-2xl border border-red-100 bg-red-50 p-8">

          <h1 className="text-xl font-semibold text-red-900">
            Skill not found
          </h1>

          <p className="mt-2 text-red-700">
            We couldn't find the requested skill.
          </p>

        </div>

      </main>
    );
  }


  return (
    <main className="mx-auto max-w-6xl px-6 py-12">

      {/* Back */}

      <Link
        to="/"
        className="text-sm font-medium text-slate-500 transition hover:text-indigo-600"
      >
        ← Back to Explore
      </Link>


      {/* Header */}

      <section className="mt-10">

        <div className="flex flex-wrap items-center gap-3">

          <span className="rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-600">
            {skill.difficulty}
          </span>

        </div>

        <h1 className="mt-4 text-5xl font-bold tracking-tight text-slate-950">
          {skill.name}
        </h1>

        <p className="mt-4 max-w-2xl text-lg leading-8 text-slate-500">
          {skill.description}
        </p>

      </section>


      {/* Related Skills */}

      <section className="mt-16">

        <div className="mb-6">

          <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
            Connections
          </p>

          <h2 className="mt-2 text-2xl font-bold text-slate-950">
            Related skills
          </h2>

        </div>


        {relatedSkills.length === 0 ? (

          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-slate-500">
            No related skills found.
          </div>

        ) : (

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            {relatedSkills.map((relatedSkill) => (

              <Link
                key={relatedSkill.name}
                to={`/skills/${encodeURIComponent(relatedSkill.name)}`}
                className="rounded-2xl border border-slate-200 bg-white p-5 transition hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg"
              >

                <div className="flex items-center justify-between">

                  <span className="font-semibold text-slate-900">
                    {relatedSkill.name}
                  </span>

                  <span className="text-slate-400">
                    →
                  </span>

                </div>

                <p className="mt-2 text-sm text-slate-500">
                  {relatedSkill.difficulty}
                </p>

              </Link>

            ))}

          </div>

        )}

      </section>
      <section className="mt-16">

  <div className="mb-6">
    <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
      Learning path
    </p>

    <h2 className="mt-2 text-2xl font-bold text-slate-950">
      What should you learn next?
    </h2>

    <p className="mt-2 max-w-2xl text-slate-500">
      Skills directly connected to {skill?.name} in the TechPath graph.
    </p>
  </div>

  {recommendations &&
  recommendations.recommendations.length > 0 ? (

    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">

      {recommendations.recommendations.map(
        (recommendation) => (

          <RecommendationCard
            key={recommendation.skill}
            recommendation={recommendation}
            onClick={() => {
              window.location.href =
                `/skills/${encodeURIComponent(
                  recommendation.skill
                )}`;
            }}
          />

        )
      )}

    </div>

  ) : (

    <div className="rounded-2xl border border-slate-200 bg-white p-8 text-slate-500">
      No recommendations available yet.
    </div>

  )}

</section>

      {/* Career Opportunities */}

      <section className="mt-16">

        <div className="mb-6">

          <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
            Career
          </p>

          <h2 className="mt-2 text-2xl font-bold text-slate-950">
            Career opportunities
          </h2>

        </div>


        {jobs.length === 0 ? (

          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-slate-500">
            No career opportunities found.
          </div>

        ) : (

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

            {jobs.map((job) => (

              <div
                key={job.title}
                className="rounded-2xl border border-slate-200 bg-white p-6"
              >

                <h3 className="font-semibold text-slate-900">
                  {job.title}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  {job.description}
                </p>

              </div>

            ))}

          </div>

        )}

      </section>


      {/* Career Path CTA */}

      <section className="mt-16 rounded-3xl bg-slate-950 p-8 text-white md:p-12">

        <div className="max-w-2xl">

          <p className="text-sm font-semibold uppercase tracking-wider text-indigo-300">
            Graph exploration
          </p>

          <h2 className="mt-3 text-3xl font-bold">
            Where can {skill.name} take you?
          </h2>

          <p className="mt-4 leading-7 text-slate-300">
            Explore the paths connecting this skill to different
            career opportunities through the TechPath graph.
          </p>

          <Link
            to={`/skills/${encodeURIComponent(skill.name)}/graph`}
            className="mt-7 inline-flex rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-slate-200"
          >
            Explore career paths →
          </Link>

        </div>

      </section>

    </main>
  );
}


export default SkillPage;