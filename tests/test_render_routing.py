import numpy as np
import pytest

from bibazu_stable_roadmaps.render import transition_path


@pytest.mark.parametrize('target', [
    (300,0,500,150), (0,300,200,450), (300,300,500,450),
    (600,250,800,400), (250,600,450,750), (-600,250,-400,400),
    (-600,-350,-400,-200), (250,-600,450,-450),
])
@pytest.mark.parametrize('lane', [-.8, 0, .8])
def test_routes_attach_to_borders_using_distinct_angle_families(target, lane):
    source = (0,0,100,80)
    points = transition_path(source, target, lane)
    def on_border(point, bounds):
        x,y = point
        x0,y0,x1,y1 = bounds
        return (x0-1e-6 <= x <= x1+1e-6 and y0-1e-6 <= y <= y1+1e-6
            and min(abs(x-x0),abs(x-x1),abs(y-y0),abs(y-y1)) < 1e-6)
    assert on_border(points[0], source)
    assert on_border(points[-1], target)
    for dx,dy in np.diff(points,axis=0):
        assert min(abs(dx),abs(dy),abs(abs(dx)-abs(dy))) < 1e-6
        assert np.hypot(dx,dy) > 0


def test_axis_alignment_is_preferred_and_attachments_can_spread():
    source, target = (0,0,100,80), (300,-20,500,150)
    first = transition_path(source,target,-.8)
    second = transition_path(source,target,.8)
    assert first.shape == second.shape == (2,2)
    assert first[0,1] == first[1,1]
    assert second[0,1] == second[1,1]
    assert first[0,1] != second[0,1]
