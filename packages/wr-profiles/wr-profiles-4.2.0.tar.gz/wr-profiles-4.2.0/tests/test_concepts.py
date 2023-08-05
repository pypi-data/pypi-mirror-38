from tests.warehouse_profile import WarehouseProfile


def test_default_profile_is_active_and_live():
    profile = WarehouseProfile()
    assert profile.profile_name is None
    assert profile.profile_is_active
    assert profile.profile_is_live


def test_custom_profile_is_frozen_but_could_be_active(monkeypatch):
    monkeypatch.setenv("WAREHOUSE_PROFILE", "staging")

    profile = WarehouseProfile.load("staging")
    assert profile.profile_name == "staging"
    assert profile.profile_is_active

    monkeypatch.setenv("WAREHOUSE_PROFILE", "")
    assert not profile.profile_is_active

    monkeypatch.setenv("WAREHOUSE_PROFILE", "staging")
    assert profile.profile_is_active
