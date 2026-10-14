from datetime import UTC, datetime

from hindsight_api.engine.retain.fact_extraction import _infer_temporal_date


def test_infers_absolute_date_from_when_without_retain_timestamp() -> None:
    result = _infer_temporal_date(
        "Ara moved the scheduler on one date and the first run succeeded on another",
        event_date=None,
        when="The first successful run was on 2026-10-12 at 14:00 UTC",
    )

    assert result == "2026-10-12"


def test_invalid_absolute_date_falls_back_to_relative_text() -> None:
    result = _infer_temporal_date(
        "The migration completed yesterday",
        event_date=datetime(2026, 10, 13, 21, tzinfo=UTC),
        when="2026-13-40",
    )

    assert result == "2026-10-12T00:00:00+00:00"


def test_does_not_use_retain_timestamp_for_undated_event() -> None:
    result = _infer_temporal_date(
        "The migration completed successfully",
        event_date=datetime(2026, 10, 13, 21, tzinfo=UTC),
        when="N/A",
    )

    assert result is None
