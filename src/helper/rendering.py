import networkx as nx
import matplotlib.pyplot as plt
from ..core.path_selection import *

def render_graph(
    nodes: list[dict],
) -> None:
    graph = nx.DiGraph()
    positions = {}

    for node in nodes:
        coord = node["coord"]
        x, y = map(int, coord.split(","))

        graph.add_node(coord)
        positions[coord] = (x, y)

        for child in node["children"]:
            graph.add_edge(coord, child)

    color_map = {
        "monster": "white",
        "elite": "red",
        "restsite": "green",
        "unknown": "yellow",
        "treasure": "orange",
        "boss": "purple",
        "shop": "lightgreen",
        "ancient":"gray"
        }

    kind_by_coord = {
        node["coord"]: node["kind"]
        for node in nodes
        }

    colors = [
        color_map.get(kind_by_coord[coord], "black")
        for coord in graph.nodes
        ]

    fig, ax = plt.subplots(figsize=(10, 7))

    nx.draw_networkx(
        graph,
        pos=positions,
        ax=ax,
        with_labels=True,
        node_size=700,
        node_color=colors,
        edgecolors="#ff6a00",
        edge_color="#777777",
        arrows=True,
        arrowsize=15,
        font_size=8,
        linewidths=2,
    )

    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig, ax, graph, positions

def add_path_overlay(
    ax,
    graph: nx.DiGraph,
    positions: dict,
    path: list[str],
    color: str = "#00aaff",
    node_size: int = 1100,
    line_width: float = 3,
    draw_edges: bool = True
):
    # Draw highlighted edges on top of the existing graph
    path_edges = list(zip(path, path[1:]))

    if draw_edges:
        nx.draw_networkx_edges(
            graph,
            pos=positions,
            ax=ax,
            edgelist=path_edges,
            edge_color=color,
            width=line_width,
            arrows=True,
            arrowsize=20,
        )

    # Draw unfilled circles around highlighted nodes
    nx.draw_networkx_nodes(
        graph,
        pos=positions,
        ax=ax,
        nodelist=path,
        node_size=node_size,
        node_color="none",
        edgecolors=color,
        linewidths=3,
    )