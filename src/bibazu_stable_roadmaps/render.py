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
    if 'pose_groups' in built.document:
        return render_individual_groups(built, path, formats, images)
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
    render_edges = built.document["edges"] + built.document.get("composite_transfers", [])
    group_overview = "group_transfers" in built.document
    member_overview = bool(built.document.get('member_states')) and not group_overview
    if group_overview:
        preferred = {}
        for transfer in built.document["group_transfers"]:
            preferred.setdefault((transfer["source"], transfer["target"]), transfer)
        render_edges = [dict(t, transition_kind="group_overview", caption=t["display_name"]) for t in preferred.values()]
    if member_overview:
        grouped = defaultdict(list)
        for transfer in built.document['member_transfers']:
            if transfer['source'] != transfer['target']:
                grouped[transfer['source'], transfer['target']].append(transfer)
        render_edges = []
        for (a,b), transfers in sorted(grouped.items()):
            preferred = min(transfers, key=lambda t: (len(t['commands']),
                sum(abs(c['signed_angle_deg']) for c in t['commands']), t['edge_id']))
            caption = ' → '.join(f"{c['axis'].upper()} {c['signed_angle_deg']:+.8g}°" for c in preferred['commands']) or 'No rotation'
            render_edges.append(dict(source=a, target=b, actuation='member', transition_kind='member_overview',
                                     caption=caption, fallback_only=False))
    for edge in render_edges:
        pairs[tuple(sorted((edge["source"], edge["target"])))].append(edge)
    for pair, edges in pairs.items():
        for index, edge in enumerate(edges):
            start, end = positions[edge["source"]], positions[edge["target"]]
            radius = (index - (len(edges) - 1) / 2) * .18
            direction = 1 if edge["source"] == pair[0] else -1
            radius *= direction
            composite = edge.get("transition_kind") == "composite_candidate"
            member_edge = edge.get('transition_kind') in {'member_overview', 'group_overview'}
            action_axis = "x" if "main_" in edge.get("actuation", "") else edge.get("actuation", "z")[-1]
            color = colors[edge['commands'][0]['axis']] if group_overview and edge.get('commands') else '#0e827b' if member_edge else "#8a4baf" if composite else colors[action_axis]
            axis.annotate("", xy=end, xytext=start,
                          arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.8, "linestyle": "--" if composite or edge.get('fallback_only') else "-",
                                      "shrinkA": 45 * image_scale, "shrinkB": 45 * image_scale, "connectionstyle": f"arc3,rad={radius}"}, zorder=2)
            delta = end - start
            normal = np.array([delta[1], -delta[0]])
            label = (start * .58 + end * .42 if group_overview else (start + end) / 2) + normal * radius / 2
            text = edge['caption'] if member_edge else (' → '.join(
                f"{c['axis'].upper()} {c['signed_angle_deg']:+.8g}°" for c in edge['commands'])
                if composite else f"{action_axis.upper()} {edge['signed_angle_deg']:+.8g}°")
            axis.text(*label, text, color=color, fontsize=7,
                      ha="center", va="center", bbox={"facecolor": "white", "alpha": .85, "edgecolor": "none", "pad": .5}, zorder=4)
    for pose, number in built.numbered:
        position = positions[number]
        box = AnnotationBbox(OffsetImage(images[number], zoom=.34 * image_scale), position, frameon=True,
                             bboxprops={"edgecolor": "#084081", "lw": 1.8, "facecolor": "white"}, zorder=5)
        axis.add_artist(box)
        axis.annotate(f"{'Group' if group_overview else 'Pose'} {number}\n{pose.source_id} · {pose.frequency_percent:g}%", position,
                      xytext=(0, 43 * image_scale), textcoords="offset points", ha="center", va="bottom", fontsize=9 * image_scale, weight="bold", zorder=6)
    cutoff = built.document["generation"]["minimum_frequency_percent"]
    mode = "frequency numbering" if built.document["generation"]["renumber_by_frequency"] else "source numbering"
    axis.set_title(f"{built.source.workpiece}: observed stable-pose roadmap\n{count} poses · {len(built.document['edges'])} direct connections · minimum {cutoff:g}% · {mode}", fontsize=14, pad=20)
    reachability = built.document.get("connectivity")
    if reachability and "direct" in reachability and "with_candidates" in reachability:
        direct, augmented = reachability['direct'], reachability['with_candidates']
        axis.set_title(axis.get_title() + f"\nReachable pairs: {direct['reachable_pair_count']} direct graph / "
                       f"{augmented['reachable_pair_count']} with candidates / {direct['total_pair_count']} total", fontsize=12)
    if member_overview:
        info = reachability['members']
        axis.set_title(f"{built.source.workpiece}: member-conditioned group roadmap\n"
                       f"{info['known_member_inter_group_action_count']} known-member inter-group actions · representative images unchanged", fontsize=12)
    if group_overview:
        stats = reachability['groups']
        axis.set_title(f"{built.source.workpiece}: whole-group roadmap\n{count} groups · "
            f"Cartesian routes {stats['cartesian']['reachable_pair_count']}/{stats['cartesian']['total_pair_count']} · "
            f"all routes {stats['all_candidates']['reachable_pair_count']}/{stats['all_candidates']['total_pair_count']}", fontsize=12)
    handles = ([Line2D([0],[0],color='#0e827b',label='Member candidates · source conditions apply')] if member_overview else
               [Line2D([0], [0], color=color, label=f"{name.upper()} rotation") for name, color in colors.items()]
               + ([Line2D([0], [0], color='#8a4baf', linestyle='--', label='Multiple rotations' if group_overview else 'Composite · geometry only')] if reachability else []))
    figure.legend(handles=handles,
                  loc="lower center", bbox_to_anchor=(.5, .045), ncol=4 if reachability else 3, fontsize=8)
    figure.text(.5, .015, "Groups contain all members; routes assume member interchangeability. Group calibration required." if group_overview else "Group arrows summarize conditional candidates; member continuity and calibrated source coverage are required." if member_overview else "Observed simulation poses; connections are geometric candidates and remain untested. No analytical stability classification.", ha="center", fontsize=8)
    for fmt in formats:
        figure.savefig(path.with_suffix("." + fmt), bbox_inches="tight")
    plt.close(figure)


def group_label(index: int) -> str:
    """Alphabetical display labels, continuing with AA after Z."""
    label = ''
    number = index + 1
    while number:
        number, remainder = divmod(number - 1, 26)
        label = chr(ord('A') + remainder) + label
    return label


def render_individual_groups(built, path, formats, images):
    """Numbered pose tiles in lettered groups on a grid with straight arrows."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    groups = sorted(built.document['pose_groups'], key=lambda g:(min(g['pose_ids']),g['group_key']))
    columns = min(4, max(1, int(np.ceil(np.sqrt(len(groups))))))
    rows = int(np.ceil(len(groups)/columns))
    max_members = max(len(g['pose_ids']) for g in groups)
    tile_rows = int(np.ceil(max_members/3))
    panel_h = max(4.6, tile_rows*2.3+1.4)
    cell_w, cell_h = 9.5, panel_h + 2.
    width, height = max(12, columns*5.4), max(8, rows*cell_h*.62+2.)
    fig, ax = plt.subplots(figsize=(width, height), dpi=160)
    ax.set_xlim(-4.1, (columns-1)*cell_w+4.1)
    ax.set_ylim(-(rows-1)*cell_h-panel_h/2-.4, panel_h/2+.4)
    ax.axis('off')
    positions = {}; pose_positions = {}; pose_boxes = {}
    nodes={n['node_id']:n for n in built.document['nodes']}
    palette=plt.get_cmap('tab20')
    for index,group in enumerate(groups):
        x,y=(index%columns)*cell_w,-(index//columns)*cell_h
        positions[group['group_id']]=(x,y)
        color=palette(group['group_id']%20)
        ax.add_patch(FancyBboxPatch((x-3.5,y-panel_h/2+.3),7,panel_h-.6,
            boxstyle='round,pad=.06',facecolor=(*color[:3],.13),edgecolor=color,lw=1.5,zorder=1))
        ax.text(x,y+panel_h/2-.7,f"Group {group_label(index)} · total {group['observed_frequency_percent']:g}%",
            ha='center',fontsize=10,weight='bold',zorder=6,
            bbox=dict(facecolor='white',edgecolor='none',alpha=.95,pad=2))
        ids=group['pose_ids']; ncols=min(3,len(ids))
        for j,number in enumerate(ids):
            px=x+(j%ncols-(ncols-1)/2)*2.2
            py=y+(tile_rows-1)*1.05-(j//ncols)*2.3-.15
            box=AnnotationBbox(OffsetImage(images[number],zoom=.43),(px,py),frameon=False,zorder=5)
            ax.add_artist(box)
            pose_positions[number] = np.array([px, py])
            pose_boxes[number] = box
            node=nodes[number]
            ax.annotate(f"Pose {number} · {node['observed_frequency_percent']:g}%\n{node['source_pose_ids'][0]}",
                (px,py),xytext=(0,39),textcoords='offset points',ha='center',fontsize=8,weight='bold',zorder=6,
                bbox=dict(facecolor='white',edgecolor='none',alpha=.95,pad=.6))
    pose_to_group = built.document.get('planning_semantics') == 'pose_to_group'
    preferred={}
    transfers = built.document.get('pose_group_transfers', []) if pose_to_group else built.document['group_transfers']
    for t in sorted(transfers, key=lambda t:(t['preference_cost'],t['edge_id'])):
        preferred.setdefault((t['source'],t['target_group_id'] if pose_to_group else t['target']),t)
    fig.subplots_adjust(top=1-1.2/height,bottom=.85/height,left=.03,right=.97)
    fig.canvas.draw()
    colors={'x':'#c73646','y':'#248738','z':'#237898'}
    labels=[]
    for (a,b),transfer in preferred.items():
        start = pose_positions[a] if pose_to_group else np.asarray(positions[a])
        end = np.asarray(positions[b]); delta=end-start
        end_clip=min(3.6/max(abs(delta[0]),1e-12),(panel_h/2-.2)/max(abs(delta[1]),1e-12))
        if pose_to_group:
            bounds = pose_boxes[a].get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted())
            start_clip=min((bounds.width/2+.08)/max(abs(delta[0]),1e-12),
                           (bounds.height/2+.08)/max(abs(delta[1]),1e-12))
        else:
            start_clip=end_clip
        s=start+delta*start_clip; e=end-delta*end_clip
        normal=np.array([-delta[1],delta[0]])/np.linalg.norm(delta)
        # Parallel lanes separate opposing arrows without bending their shafts.
        s=s+normal*.10; e=e+normal*.10
        color=colors[transfer['commands'][0]['axis']]
        ax.add_patch(FancyArrowPatch(s,e,arrowstyle='-|>',mutation_scale=10,lw=1.1,
            connectionstyle='arc3,rad=0',color=color,zorder=2))
        label=(s+e)/2+normal*.25
        for fraction in (.3,.7,.4,.6,.2,.8,.5):
            candidate=s*(1-fraction)+e*fraction+normal*.3
            if any(abs(candidate[0]-p[0])<3.6 and abs(candidate[1]-p[1])<panel_h/2 for p in positions.values()):
                continue
            if any(abs(candidate[0]-p[0])<1.1 and abs(candidate[1]-p[1])<.3 for p in labels):
                continue
            label=candidate;break
        labels.append(label)
        ax.text(*label,transfer['display_name'],ha='center',va='center',fontsize=6,color=color,
            bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=.6),zorder=4)
    stats=built.document['connectivity']['groups']; all_routes=stats['all_candidates']; cart=stats['cartesian']
    heading = 'exact source pose → destination group' if pose_to_group else 'individual poses, shared group actions'
    fig.suptitle(f"{built.source.workpiece}: {heading}\n"
        f"{len(nodes)} poses · {len(groups)} groups · cutoff {built.document.get('filtering',{}).get('minimum_frequency_percent',0):g}%\n"
        f"Reachable group pairs: Cartesian {cart['reachable_pair_count']}/{cart['total_pair_count']} · "
        f"all {all_routes['reachable_pair_count']}/{all_routes['total_pair_count']} · no composite bridges",fontsize=13)
    footer = ('Arrows start at the exact pose and accept any destination-group member. Commands use that source pose’s witnesses.\n'
              'No actions are inherited from other source members. Same-group targets require no motion. Calibration required.') if pose_to_group else 'Outgoing actions apply to every displayed group member. Same-group targets require no motion. Calibration required.'
    if pose_to_group:
        info = built.document['connectivity']['pose_to_group']
        fig.suptitle(f"{built.source.workpiece}: {heading}\n{len(nodes)} poses · {len(groups)} groups · cutoff {built.document['filtering']['minimum_frequency_percent']:g}%\n"
            f"{len(preferred)} direct pose-to-group connections · {info['reachable_pair_count']}/{info['total_pair_count']} reachable with exported routes · no composite bridges",fontsize=13)
    fig.text(.5,.02,footer,
        ha='center',fontsize=9)
    for fmt in formats: fig.savefig(path.with_suffix('.'+fmt),bbox_inches='tight')
    plt.close(fig)


def render_pose_sheets(built: BuiltRoadmap, folder: Path, formats: tuple[str, ...], check_cancel=lambda: None):
    folder.mkdir(parents=True, exist_ok=True)
    for pose, number in built.numbered:
        check_cancel()
        figure = pose_figure(built, number)
        for fmt in formats:
            figure.savefig(folder / f"{built.source.workpiece}_pose-{number:04d}.{fmt}", bbox_inches="tight")
        plt.close(figure)
