import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import NodeDetails from "../components/NodeDetails";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  MarkerType,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import dagre from "@dagrejs/dagre";

import { getGraph } from "../services/api";

import type { GraphResponse,
    GraphNode,
 } from "../types";


function GraphPage() {
  const { skillName } = useParams<{
    skillName: string;
  }>();

  const [graph, setGraph] =
    useState<GraphResponse | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [selectedNode, setSelectedNode] =
  useState<GraphNode | null>(null);
  const connectedNodeIds = useMemo(() => {
      if (!selectedNode || !graph) {
        return new Set<string>();
      }

      const connected = new Set<string>();
      const queue: string[] = [selectedNode.id];

      connected.add(selectedNode.id);

      while (queue.length > 0) {
        const current = queue.shift()!;

        graph.edges.forEach((edge) => {
          let nextNode: string | null = null;

          // Follow the graph in both directions
          if (edge.source === current) {
            nextNode = edge.target;
          } else if (edge.target === current) {
            nextNode = edge.source;
          }

          if (
            nextNode &&
            !connected.has(nextNode)
          ) {
            connected.add(nextNode);
            queue.push(nextNode);
          }
        });
      }

      return connected;
    }, [selectedNode, graph]);

  /*
   * Load graph from FastAPI
   */

  useEffect(() => {

    async function loadGraph() {

      if (!skillName) {
        return;
      }

      try {

        setLoading(true);
        setError(null);

        const data = await getGraph(skillName);

        setGraph(data);

      } catch (error) {

        console.error(error);

        setError(
          "Unable to load the career graph."
        );

      } finally {

        setLoading(false);

      }
    }

    loadGraph();

  }, [skillName]);


  /*
   * Convert backend graph
   * into React Flow graph
   */

  const { nodes, edges } = useMemo(() => {

    if (!graph) {

      return {
        nodes: [],
        edges: [],
      };

    }


    /*
     * Create nodes
     */

    const flowNodes: Node[] =
      graph.nodes.map((node) => {

        const isJob =
    node.type === "job";

        const isSelected =
        selectedNode?.id === node.id;

        const isConnected =
        connectedNodeIds.has(node.id);

        const isDimmed =
        selectedNode !== null &&
        !isConnected;

        return {

          id: node.id,

          position: {
            x: 0,
            y: 0,
          },

          data: {

            label: (

              <div className="min-w-[160px] text-center">

                <div className="font-semibold text-slate-900">
                  {node.id}
                </div>

                <div
                  className={
                    isJob
                      ? "mt-1 text-xs font-semibold text-emerald-600"
                      : "mt-1 text-xs font-semibold text-indigo-600"
                  }
                >
                  {isJob
                    ? "JOB"
                    : "SKILL"}
                </div>

              </div>

            ),

          },

          style: {

                padding: "14px 20px",

                borderRadius: "14px",

                border: isSelected
                    ? "3px solid #4f46e5"
                    : isJob
                    ? "2px solid #86efac"
                    : "2px solid #a5b4fc",

                background: isJob
                    ? "#f0fdf4"
                    : "#eef2ff",

                fontWeight: 600,

                opacity: isDimmed
                    ? 0.25
                    : 1,

                boxShadow: isSelected
                    ? "0 0 0 6px rgba(99,102,241,0.15)"
                    : "0 4px 12px rgba(0,0,0,0.06)",

                transition:
                    "opacity 200ms ease, box-shadow 200ms ease",

                },

        };

      });


    /*
     * Create edges
     */

    const flowEdges: Edge[] =
  graph.edges.map(
    (edge, index) => {

      const isConnected =
        !selectedNode ||
        edge.source === selectedNode.id ||
        edge.target === selectedNode.id;

      return {

        id:
          `${edge.source}-${edge.target}-${index}`,

        source: edge.source,

        target: edge.target,

        type: "smoothstep",

        label:
          edge.relationship.replaceAll(
            "_",
            " "
          ),

        markerEnd: {
          type: MarkerType.ArrowClosed,
        },

        style: {
          opacity: isConnected
            ? 1
            : 0.15,

          strokeWidth:
            isConnected
              ? 2
              : 1,

        },

        labelStyle: {

          fontSize: 10,

          fontWeight: 600,

          fill: "#475569",

          opacity:
            isConnected
              ? 1
              : 0.15,

        },

        labelBgStyle: {
          fill: "#ffffff",
        },

        labelBgPadding: [
          6,
          4,
        ],

        labelBgBorderRadius: 6,

      };
    }
  );


    /*
     * Dagre layout
     */

    const layoutGraph =
      new dagre.graphlib.Graph();


    layoutGraph.setDefaultEdgeLabel(
      () => ({})
    );


    layoutGraph.setGraph({

      rankdir: "LR",

      nodesep: 100,

      ranksep: 220,

      marginx: 50,

      marginy: 50,

    });


    /*
     * Register nodes
     */

    flowNodes.forEach(
      (node) => {

        layoutGraph.setNode(
          node.id,
          {
            width: 210,
            height: 80,
          }
        );

      }
    );


    /*
     * Register edges
     */

    flowEdges.forEach(
      (edge) => {

        layoutGraph.setEdge(
          edge.source,
          edge.target
        );

      }
    );


    /*
     * Calculate layout
     */

    dagre.layout(layoutGraph);


    /*
     * Apply positions
     */

    const positionedNodes =
      flowNodes.map((node) => {

        const position =
          layoutGraph.node(node.id);


        return {

          ...node,

          position: {

            x:
              position.x - 105,

            y:
              position.y - 40,

          },

        };

      });


    return {

      nodes: positionedNodes,

      edges: flowEdges,

    };

  }, [graph,
    selectedNode,
  connectedNodeIds,
  ]);


  /*
   * Loading
   */

  if (loading) {

    return (

      <main className="mx-auto max-w-6xl px-6 py-16">

        <div className="h-[600px] animate-pulse rounded-3xl bg-slate-100" />

      </main>

    );

  }


  /*
   * Error
   */

  if (error) {

    return (

      <main className="mx-auto max-w-6xl px-6 py-16">

        <Link
          to={`/skills/${encodeURIComponent(
            skillName ?? ""
          )}`}
          className="text-sm font-medium text-indigo-600"
        >
          ← Back to skill
        </Link>


        <div className="mt-10 rounded-2xl border border-red-100 bg-red-50 p-8">

          <h1 className="text-xl font-semibold text-red-900">
            Something went wrong
          </h1>

          <p className="mt-2 text-red-700">
            {error}
          </p>

        </div>

      </main>

    );

  }


  /*
   * Empty graph
   */

  if (
    !graph ||
    graph.nodes.length === 0
  ) {

    return (

      <main className="mx-auto max-w-6xl px-6 py-16">

        <Link
          to={`/skills/${encodeURIComponent(
            skillName ?? ""
          )}`}
          className="text-sm font-medium text-indigo-600"
        >
          ← Back to skill
        </Link>


        <div className="mt-10 rounded-2xl border border-slate-200 bg-white p-10 text-center">

          <h1 className="text-2xl font-bold text-slate-950">
            No graph data found
          </h1>

          <p className="mt-2 text-slate-500">
            There aren't any connected career paths for this skill yet.
          </p>

        </div>

      </main>

    );

  }


  /*
   * Main graph
   */

  return (

    <main className="flex h-[calc(100vh-73px)] flex-col bg-slate-50">


      {/* Header */}

      <div className="border-b border-slate-200 bg-white px-6 py-4">

        <div className="mx-auto flex max-w-7xl items-center justify-between">

          <div>

            <Link
              to={`/skills/${encodeURIComponent(
                skillName ?? ""
              )}`}
              className="text-sm font-medium text-slate-500 hover:text-indigo-600"
            >
              ← Back to {skillName}
            </Link>


            <h1 className="mt-1 text-2xl font-bold text-slate-950">
              Career Graph
            </h1>

          </div>


          <div className="flex items-center gap-3">

            <div className="rounded-full bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-600">
              {graph.nodes.length} nodes
            </div>

            <div className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600">
              {graph.edges.length} connections
            </div>

          </div>

        </div>

      </div>


      {/* Legend */}

      <div className="absolute z-10 ml-6 mt-24 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">

        <p className="mb-3 text-xs font-bold uppercase tracking-wider text-slate-500">
          Legend
        </p>


        <div className="flex items-center gap-2 text-sm text-slate-700">

          <span className="h-3 w-3 rounded-full bg-indigo-400" />

          Skill

        </div>


        <div className="mt-2 flex items-center gap-2 text-sm text-slate-700">

          <span className="h-3 w-3 rounded-full bg-emerald-400" />

          Job

        </div>

      </div>


      {/* Graph */}

      <div className="relative min-h-0 flex-1">

                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    fitView
                    nodesDraggable
                    nodesConnectable={false}
                    elementsSelectable

                    onNodeClick={(_, node) => {

                    const selected = graph?.nodes.find(
                        (item) => item.id === node.id
                    );

                    if (selected) {
                        setSelectedNode(selected);
                    }

                    }}
                >

                    <Background />

                    <Controls />

                    <MiniMap />

                </ReactFlow>


                {selectedNode && (

                    <NodeDetails
                    node={selectedNode}
                    onClose={() => setSelectedNode(null)}
                    />

                )}

                </div>

                    </main>

                );
                }


export default GraphPage;