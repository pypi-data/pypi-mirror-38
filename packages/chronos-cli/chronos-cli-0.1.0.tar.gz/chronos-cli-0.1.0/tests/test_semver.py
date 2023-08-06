from chronoslib.semver import SemVer
import pytest


@pytest.fixture()
def semvers():
    return (
        SemVer(100, 100, 100),
        SemVer(100, 100, 99),
        SemVer(100, 99, 100),
        SemVer(99, 100, 100),
        SemVer(1 << 32, 1 << 32, 1 << 32),
        SemVer(1 << 32, 1 << 32, 1 << 32 - 1),
        SemVer(1 << 32, 1 << 32 - 1, 1 << 32),
        SemVer(1 << 32 - 1, 1 << 32, 1 << 32)
    )


class TestSemVer(object):
    def test_initializes_properly(self):
        sv = SemVer(100, 100, 100)
        assert sv.major == 100 and sv.minor == 100 and sv.patch == 100

    def test_setting_major_to_negative_raises_value_error(self):
        sv = SemVer()
        with pytest.raises(ValueError):
            sv.major = -1

    def test_setting_minor_to_negative_raises_value_error(self):
        sv = SemVer()
        with pytest.raises(ValueError):
            sv.minor = -1

    def test_setting_patch_to_negative_raises_value_error(self):
        sv = SemVer()
        with pytest.raises(ValueError):
            sv.patch = -1

    def test_setting_version_to_negative_raises_value_error(self):
        sv = SemVer()
        with pytest.raises(ValueError):
            sv.version = '0.-1.0'

    def test_initializing_semver_with_negatives_raises_valueerror(self):
        with pytest.raises(ValueError):
            SemVer(major=-1)

    def test_setting_version_via_version_setter_works(self):
        sv = SemVer()
        sv.version = '100.100.100'
        assert (
            sv.major == 100 and
            sv.minor == 100 and
            sv.patch == 100 and
            sv.version == '100.100.100'
        )

    def test_version_property_returns_correct_value(self):
        assert SemVer(100, 100, 100).version == '100.100.100'

    def test_eq_magic_method(self):
        sv0, sv1 = SemVer(100, 100, 100), SemVer(100, 100, 99)
        assert (
            sv0.__eq__(sv0) is True and
            sv0.__eq__(sv1) is False and
            sv0 == sv0
        )

    def test_ne_magic_method(self):
        sv0, sv1 = SemVer(100, 100, 100), SemVer(100, 100, 99)
        assert (
            sv0.__ne__(sv1) is True and
            sv0.__ne__(sv0) is False and
            sv0 != sv1
        )

    def test_repr_magic_method(self):
        sv = SemVer(100, 100, 100)
        assert repr(sv) == '100.100.100' and sv.__repr__() == '100.100.100'

    def test_gt_magic_method(self, semvers):
        assert (
            semvers[0].__gt__(semvers[1]) is True and
            semvers[0].__gt__(semvers[2]) is True and
            semvers[0].__gt__(semvers[2]) is True and
            semvers[4].__gt__(semvers[5]) is True and
            semvers[4].__gt__(semvers[6]) is True and
            semvers[4].__gt__(semvers[7]) is True and
            semvers[1].__gt__(semvers[0]) is False and
            semvers[2].__gt__(semvers[0]) is False and
            semvers[2].__gt__(semvers[0]) is False and
            semvers[5].__gt__(semvers[4]) is False and
            semvers[6].__gt__(semvers[4]) is False and
            semvers[7].__gt__(semvers[4]) is False
        )

    def test_lt_magic_method(self, semvers):
        assert (
            semvers[0].__lt__(semvers[1]) is False and
            semvers[0].__lt__(semvers[2]) is False and
            semvers[0].__lt__(semvers[2]) is False and
            semvers[4].__lt__(semvers[5]) is False and
            semvers[4].__lt__(semvers[6]) is False and
            semvers[4].__lt__(semvers[7]) is False and
            semvers[1].__lt__(semvers[0]) is True and
            semvers[2].__lt__(semvers[0]) is True and
            semvers[2].__lt__(semvers[0]) is True and
            semvers[5].__lt__(semvers[4]) is True and
            semvers[6].__lt__(semvers[4]) is True and
            semvers[7].__lt__(semvers[4]) is True
        )
