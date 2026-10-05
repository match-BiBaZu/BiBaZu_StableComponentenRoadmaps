"""Render the supplied observations with the bundled chute camera and geometry."""
from __future__ import annotations

import base64
from collections import defaultdict
from io import BytesIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import networkx as nx
import numpy as np

from ._engine.visualization import _draw_pose
from .roadmap import BuiltRoadmap


def pose_figure(built: BuiltRoadmap, number: int, *, thumbnail=False):
    figure = plt.figure(figsize=(2.4, 1.8) if thumbnail else (5, 4.5), dpi=100 if thumbnail else 160)
    axis = figure.add_subplot(111, projection="3d", computed_zorder=False)
    mesh = built.mesh
    vertices = np.asarray(mesh.vertices) - np.asarray(mesh.center_mass)
    pose = next(pose for pose, node_id in built.numbered if node_id == number)
    title = f"Pose {number} · {pose.source_id}\nObserved frequency: {pose.frequency_percent:g}%"
    _draw_pose(axis, built.contacts[number], vertices, np.asarray(mesh.faces),
               pose_label=title, show_title=not thumbnail)
    if thumbnail:
        figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    else:
        figure.suptitle(built.source.workpiece + " · observed simulation pose", fontsize=13)
        figure.tight_layout(rect=(0, 0, 1, .95))
    return figure


def thumbnails(built: BuiltRoadmap, check_cancel=lambda: None) -> dict[int, np.ndarray]:
    images = {}
    for pose, number in built.numbered:
        check_cancel()
        figure = pose_figure(built, number, thumbnail=True)
        figure.canvas.draw()
        images[number] = np.asarray(figure.canvas.buffer_rgba()).copy()
        plt.close(figure)
    return images


def embed_thumbnails(document: dict, images: dict[int, np.ndarray]):
    for node in document["nodes"]:
        buffer = BytesIO()
        plt.imsave(buffer, images[node["node_id"]], format="png")
        node["thumbnail_png_base64"] = base64.b64encode(buffer.getvalue()).decode("ascii")


def render_roadmap(built: BuiltRoadmap, path: Path, formats: tuple[str, ...], images):
    graph = nx.Graph()
    graph.add_nodes_from(number for _, number in built.numbered)
    graph.add_edges_from((edge["source"], edge["target"]) for edge in built.document["edges"])
    count = len(graph)
    # Spring layouts can cluster connected nodes and hide their pose images.
    # A circle keeps every observation visible, including disconnected nodes.
    positions = nx.circular_layout(graph, scale=1)
    if count == 1:
        positions[next(iter(graph))] = np.array([0., 0.])
    separation = min((np.max(np.abs(positions[a] - positions[b]))
                      for index, a in enumerate(graph) for b in list(graph)[index + 1:]), default=2)
    required_height = max(7, 7.6 / separation)
    height = min(24, required_height)
    image_scale = height / required_height
    figure, axis = plt.subplots(figsize=(max(10, height * 1.35), height), dpi=180)
    axis.set_xlim(-1.6, 1.6)
    axis.set_ylim(-1.6, 1.6)
    axis.set_aspect("equal")
    axis.axis("off")
    colors = {"x": "#e63946", "y": "#2ca02c", "z": "#277da1"}
    pairs = defaultdict(list)
    for edge in built.document["edges"]:
        pairs[tuple(sorted((edge["source"], edge["target"])))].append(edge)
    for pair, edges in pairs.items():
        for index, edge in enumerate(edges):
            start, end = positions[edge["source"]], positions[edge["target"]]
            radius = (index - (len(edges) - 1) / 2) * .18
            direction = 1 if edge["source"] == pair[0] else -1
            radius *= direction
            action_axis = "x" if "main_" in edge["actuation"] else edge["actuation"][-1]
            color = colors[action_axis]
            axis.annotate("", xy=end, xytext=start,
                          arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.8,
                                      "shrinkA": 45 * image_scale, "shrinkB": 45 * image_scale, "connectionstyle": f"arc3,rad={radius}"}, zorder=2)
            delta = end - start
            normal = np.array([delta[1], -delta[0]])
            label = (start + end) / 2 + normal * radius / 2
            axis.text(*label, f"{edge['signed_angle_deg']:+.1f}°", color=color, fontsize=7,
                      ha="center", va="center", bbox={"facecolor": "white", "alpha": .85, "edgecolor": "none", "pad": .5}, zorder=4)
    for pose, number in built.numbered:
        position = positions[number]
        box = AnnotationBbox(OffsetImage(images[number], zoom=.47 * image_scale), position, frameon=True,
                             bboxprops={"edgecolor": "#084081", "lw": 1.8, "facecolor": "white"}, zorder=5)
        axis.add_artist(box)
        axis.annotate(f"Pose {number}\n{pose.source_id} · {pose.frequency_percent:g}%", position,
                      xytext=(0, 56 * image_scale), textcoords="offset points", ha="center", va="bottom", fontsize=9 * image_scale, weight="bold", zorder=6)
    cutoff = built.document["generation"]["minimum_frequency_percent"]
    mode = "frequency numbering" if built.document["generation"]["renumber_by_frequency"] else "source numbering"
    axis.set_title(f"{built.source.workpiece}: observed stable-pose roadmap\n{count} poses · {len(built.document['edges'])} direct connections · minimum {cutoff:g}% · {mode}", fontsize=14, pad=20)
    figure.legend(handles=[Line2D([0], [0], color=color, label=f"{name.upper()} rotation") for name, color in colors.items()],
                  loc="lower center", bbox_to_anchor=(.5, .045), ncol=3, fontsize=8)
    figure.text(.5, .015, "Observed simulation poses; connections are geometric candidates and remain untested. No analytical stability classification.", ha="center", fontsize=8)
    for fmt in formats:
        figure.savefig(path.with_suffix("." + fmt), bbox_inches="tight")
    plt.close(figure)


def render_pose_sheets(built: BuiltRoadmap, folder: Path, formats: tuple[str, ...], check_cancel=lambda: None):
    folder.mkdir(parents=True, exist_ok=True)
    for pose, number in built.numbered:
        check_cancel()
        figure = pose_figure(built, number)
        for fmt in formats:
            figure.savefig(folder / f"{built.source.workpiece}_pose-{number:04d}.{fmt}", bbox_inches="tight")
        plt.close(figure)
