from tests.warehouse_profile import WarehouseProfile


def test_ultimate_live_profile():
    profile = WarehouseProfile()
    assert profile.profile_root == "warehouse"

    assert profile._const_name is None
    assert profile._const_parent_name is None
    assert profile.profile_is_live is True

    assert not profile.profile_name
    assert not profile._profile_parent_name
    assert not profile._profile_parent

    assert profile.profile_is_active


def test_concrete_frozen_profile(monkeypatch):
    monkeypatch.setenv("WAREHOUSE_PROFILE", "something_else")  # ignored
    monkeypatch.setenv("WAREHOUSE_STAGING_PARENT_PROFILE", "not_production")  # ignored
    monkeypatch.setenv("WAREHOUSE_STAGING_USERNAME", "staging-username")
    monkeypatch.setenv("WAREHOUSE_PRODUCTION_PASSWORD", "production-password")

    live = WarehouseProfile(name="staging", parent_name="production", profile_is_live=True)
    frozen = WarehouseProfile(name="staging", parent_name="production", profile_is_live=False)

    assert live.username == "staging-username"
    assert frozen.username is None

    assert live.password == "production-password"
    assert frozen.password is None

    assert live.host == "localhost"
    assert frozen.host == "localhost"

    frozen._do_load()

    assert live.host == frozen.host
    assert live.username == frozen.username
    assert live.password == frozen.password
