"""Shared camera convention for generated pose and roadmap plots."""

from __future__ import annotations

import math


# Shared orthographic isometric view.  It projects the calculation frame with
# +X down-left (downhill), +Y down-right, and +Z vertically upward.
POSE_VIEW_ELEVATION_DEG = math.degrees(math.asin(1.0 / math.sqrt(3.0)))
POSE_VIEW_AZIMUTH_DEG = 45.0
POSE_VIEW_ROLL_DEG = 0.0

_SCREEN_AXIS_DIRECTIONS = {
    "X": (-math.sqrt(3.0) / 2.0, -0.5, "#d62728"),
    "Y": (math.sqrt(3.0) / 2.0, -0.5, "#2ca02c"),
    "Z": (0.0, 1.0, "#1f77b4"),
}


def apply_pose_view(axis) -> None:
    """Apply the common GUI-compatible orthographic pose camera."""

    axis.set_proj_type("ortho")
    axis.view_init(
        elev=POSE_VIEW_ELEVATION_DEG,
        azim=POSE_VIEW_AZIMUTH_DEG,
        roll=POSE_VIEW_ROLL_DEG,
    )


def draw_coordinate_axes(
    axis,
    *,
    origin: tuple[float, float] = (0.80, 0.80),
    length: float = 0.16,
) -> None:
    """Draw the calculation-frame X/Y/Z triad using the shared camera."""

    for label, (direction_x, direction_y, color) in _SCREEN_AXIS_DIRECTIONS.items():
        endpoint = (
            origin[0] + length * direction_x,
            origin[1] + length * direction_y,
        )
        axis.annotate(
            "",
            xy=endpoint,
            xytext=origin,
            xycoords="axes fraction",
            arrowprops={
                "arrowstyle": "-|>",
                "color": color,
                "linewidth": 1.25,
                "mutation_scale": 8,
            },
            annotation_clip=False,
        )
        axis.text2D(
            endpoint[0] + 0.008,
            endpoint[1],
            label,
            transform=axis.transAxes,
            color=color,
            fontsize=6,
            weight="bold",
            ha="left",
            va="center",
            clip_on=False,
        )
