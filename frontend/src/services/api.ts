import axios from "axios";

import type {
  Skill,
  Job,
  CareerPathResponse,
  GraphResponse,
  RecommendationResponse,
} from "../types";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});


export async function getSkills(): Promise<Skill[]> {
  const response = await api.get<Skill[]>("/api/skills");

  return response.data;
}


export async function getSkill(
  skillName: string
): Promise<Skill> {
  const response = await api.get<Skill>(
    `/api/skills/${encodeURIComponent(skillName)}`
  );

  return response.data;
}


export async function getRelatedSkills(
  skillName: string
): Promise<Skill[]> {
  const response = await api.get<Skill[]>(
    `/api/skills/${encodeURIComponent(skillName)}/related`
  );

  return response.data;
}


export async function getJobsForSkill(
  skillName: string
): Promise<Job[]> {
  const response = await api.get<Job[]>(
    `/api/skills/${encodeURIComponent(skillName)}/jobs`
  );

  return response.data;
}


export async function getCareerPaths(
  skillName: string
): Promise<CareerPathResponse> {
  const response = await api.get<CareerPathResponse>(
    `/api/skills/${encodeURIComponent(skillName)}/career-paths`
  );

  return response.data;
}
export async function getGraph(
  skillName: string
): Promise<GraphResponse> {

  const response = await api.get<GraphResponse>(
    `/api/skills/${encodeURIComponent(skillName)}/graph`
  );

  return response.data;
}
export async function getRecommendations(
  skillName: string
): Promise<RecommendationResponse> {
  const response = await api.get<RecommendationResponse>(
    `/api/skills/${encodeURIComponent(skillName)}/recommendations`
  );

  return response.data;
}