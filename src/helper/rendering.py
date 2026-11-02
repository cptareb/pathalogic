import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
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
    icon_map = {
        "monster": "combat.png",
        "elite": "elite.png",
        "restsite": "restsite.png",
        "unknown": "event.png",
        "treasure": "treasure.png",
        "boss": "boss.png",
        "shop": "merchant.png",
        "ancient":"event.png" #placeholder
    }

    kind_by_coord = {
        node["coord"]: node["kind"]
        for node in nodes
        }

    colors = [
        color_map.get(kind_by_coord[coord], "black")
        for coord in graph.nodes
        ]

    icons = [
        color_map.get(kind_by_coord[coord], "event.png")
        for coord in graph.nodes
    ]

    fig, ax = plt.subplots(figsize=(16, 10))

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
        linewidths=1,
    )

    add_node_icons(
            ax=ax,
            nodes=nodes,
            positions=positions,
            icon_map = icon_map
    
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
    line_width: float = 2,
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
            arrowsize=10,
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
        linewidths=2,
    )

def add_node_icons(
    ax,
    nodes: list[dict],
    positions: dict,
    icon_map: dict,
    icon_dir: str | Path = "icons",
    zoom: float = 0.12,
):
    icon_dir = Path(icon_dir)

    image_cache = {}

    for node in nodes:
        coord = node["coord"]
        kind = node["kind"]

        filename = icon_map.get(kind)
        if filename is None:
            continue

        image_path = icon_dir / filename

        if not image_path.exists():
            print(f"Missing icon: {image_path}")
            continue

        if filename not in image_cache:
            image_cache[filename] = Image.open(image_path).convert("RGBA")

        image = image_cache[filename]

        image_box = AnnotationBbox(
            OffsetImage(image, zoom=zoom),
            positions[coord],
            frameon=False,
            pad=0,
            zorder=10,
        )

        ax.add_artist(image_box)