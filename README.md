# TechPath

TechPath is a graph-based career and skill exploration platform that helps users understand how technical skills connect to other skills, technologies, prerequisites, and career opportunities.

Users can explore a technical skill, discover related skills, see possible career destinations, visualize the underlying skill graph, and generate a learning path toward a selected career.

---

## Overview

Traditional career-learning platforms usually present skills as isolated lists.

TechPath models the relationships between skills and careers as a graph.

For example:

```text
Python
   |
   +---- FastAPI
   |       |
   |       +---- Backend Developer
   |
   +---- Machine Learning
   |       |
   |       +---- ML Engineer
   |       |
   |       +---- AI Engineer
   |
   +---- NumPy
           |
           +---- Pandas
                   |
                   +---- Data Scientist
Architecture

TechPath follows a layered architecture.

                         React + TypeScript
                                |
                                | REST API
                                v
                         FastAPI Backend
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
                 Routes                  Services
                                            |
                                            v
                                      Repositories
                                            |
                                            v
                                       Neo4j Graph
                                      /  CognoDB
