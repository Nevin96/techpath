import { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import SearchBar from "../components/SearchBar";
import SkillCard from "../components/SkillCard";

import { getSkills, getSkill } from "../services/api";

import type { Skill } from "../types";


function Home() {
  const navigate = useNavigate();

  const [skills, setSkills] = useState<Skill[]>([]);
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {

    async function loadSkills() {

      try {

        const data = await getSkills();

        setSkills(data);

      } catch (error) {

        console.error(error);

        setError(
          "Unable to connect to the TechPath server."
        );

      } finally {

        setLoading(false);

      }
    }

    loadSkills();

  }, []);


  async function handleSearch() {

    const trimmedSearch = search.trim();

    if (!trimmedSearch) {
      return;
    }

    try {

      setError(null);

      const skill = await getSkill(trimmedSearch);

      navigate(
        `/skills/${encodeURIComponent(skill.name)}`
      );

    } catch (error) {

      console.error(error);

      setError(
        `We couldn't find a skill called "${trimmedSearch}".`
      );

    }
  }


  function handleSkillClick(skill: Skill) {

    navigate(
      `/skills/${encodeURIComponent(skill.name)}`
    );

  }


  return (

    <main>

      {/* Hero */}

      <section className="px-6 pb-20 pt-24">

        <div className="mx-auto max-w-4xl text-center">

          <div className="mb-6 inline-flex items-center rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-600">
            Explore the career graph
          </div>

          <h1 className="text-5xl font-bold tracking-tight text-slate-950 md:text-6xl">

            Discover where your

            <span className="text-indigo-600">
              {" "}skills can take you.
            </span>

          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-500">

            Explore connections between skills, technologies
            and career opportunities through an interactive
            knowledge graph.

          </p>

          <div className="mt-10">

            <SearchBar
              value={search}
              onChange={setSearch}
              onSubmit={handleSearch}
            />

          </div>

          {error && (

            <p className="mt-4 text-sm text-red-500">
              {error}
            </p>

          )}

        </div>

      </section>


      {/* Skills */}

      <section className="border-t border-slate-200 bg-white px-6 py-16">

        <div className="mx-auto max-w-6xl">

          <div className="mb-8">

            <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
              Explore
            </p>

            <h2 className="mt-2 text-3xl font-bold text-slate-950">
              Popular skills
            </h2>

            <p className="mt-2 text-slate-500">
              Start exploring the relationships in our career graph.
            </p>

          </div>


          {loading ? (

            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">

              {Array.from({ length: 8 }).map((_, index) => (

                <div
                  key={index}
                  className="h-44 animate-pulse rounded-2xl bg-slate-100"
                />

              ))}

            </div>

          ) : (

            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">

              {skills.slice(0, 8).map((skill) => (

                <SkillCard
                  key={skill.name}
                  skill={skill}
                  onClick={() => handleSkillClick(skill)}
                />

              ))}

            </div>

          )}

        </div>

      </section>

    </main>

  );
}


export default Home;