import networkx as nx
import matplotlib.pyplot as plt

def render_graph(
    nodes: list[dict],
    node_colors: dict[str, str] | None = None,
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

    # Default color, overridden by individual node colors
    colors = [
        (node_colors or {}).get(coord, "#f2f2f2")
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
    plt.show()