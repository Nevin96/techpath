export interface Skill {
  name: string;
  description: string;
  difficulty: string;
}


export interface Job {
  title: string;
  description: string;
}


export interface CareerPath {
  job: string;
  path: string[];
  distance: number;
}


export interface CareerPathResponse {
  skill: string;
  paths: CareerPath[];
}


// Graph types

export interface GraphNode {
  id: string;
  type: "skill" | "job";
  description?: string;
  difficulty?: string | null;
}


export interface GraphEdge {
  source: string;
  target: string;
  relationship: string;
}


export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
}


// Recommendation types

export interface SkillRecommendation {
  skill: string;
  difficulty?: string | null;
  description?: string | null;
  careers: string[];
}


export interface RecommendationResponse {
  skill: string;
  recommendations: SkillRecommendation[];
}
export interface LearningPathNode {
  name: string;
  type: "skill" | "job";
  description?: string | null;
  difficulty?: string | null;
}


export interface CareerLearningPathResponse {
  skill: string;
  job: string;
  path: LearningPathNode[];
  distance: number;
}