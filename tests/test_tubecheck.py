import pytest

from tubecheck import TubeResult, evaluate, inch
from tubecheck.nest import nest


def test_size_a_example_round_1x095() -> None:
    result = evaluate("round", inch(1.0), inch(0.095))
    assert result.sizes["A"]["pass"] is True
    assert result.area_mm2 >= 173
    assert result.inertia_mm4 >= 11320


def test_size_b_example_round_1x065() -> None:
    result = evaluate("round", inch(1.0), inch(0.065))
    assert result.sizes["A"]["pass"] is False
    assert result.sizes["B"]["pass"] is True
    assert result.sizes["C"]["pass"] is True


def test_size_c_example_round_1x049() -> None:
    result = evaluate("round", inch(1.0), inch(0.049))
    assert result.sizes["B"]["pass"] is False
    assert result.sizes["C"]["pass"] is True
    assert result.wall_mm + 1e-6 >= 1.2


def test_size_d_needs_larger_od() -> None:
    one_inch = evaluate("round", inch(1.0), inch(0.120))
    metric = evaluate("round", 35.0, inch(0.049))
    published_example = evaluate("round", inch(1.375), inch(0.049))
    assert one_inch.sizes["D"]["od"] is False
    assert metric.sizes["D"]["od"] is True
    # 1.375 in = 34.925 mm, 0.075 mm under the 35.0 mm table minimum.
    assert published_example.od_mm < 35.0
    assert 35.0 - published_example.od_mm < 0.08


def test_min_od_and_wall_is_not_enough() -> None:
    # 25 mm x 2.0 mm round meets A wall+OD but not I/area — the rules warning.
    result = evaluate("round", 25.0, 2.0)
    assert result.min_od_wall_warning is True
    assert result.sizes["A"]["od"] is True
    assert result.sizes["A"]["wall"] is True
    assert result.sizes["A"]["pass"] is False


def test_square_area_and_inertia() -> None:
    result = evaluate("square", inch(1.0), inch(0.065))
    assert isinstance(result, TubeResult)
    assert result.shape == "square"
    assert result.area_mm2 > 0
    assert result.inertia_mm4 > 0


def test_nest_counts_sticks() -> None:
    plan = nest([20, 20, 15, 10], stock=72, kerf=0.06, end_trim=0.25)
    assert plan["stick_count"] >= 1
    assert plan["total_cut"] == 65
    assert all(sum(stick) <= plan["usable"] + 1e-6 for stick in plan["sticks"])


def test_nest_rejects_non_positive_lengths() -> None:
    with pytest.raises(ValueError, match="positive"):
        nest([-5, 10], stock=72)
    with pytest.raises(ValueError, match="positive"):
        nest([0, 10], stock=72)
