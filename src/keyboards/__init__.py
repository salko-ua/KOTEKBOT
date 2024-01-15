from keyboards.admin_kb import AdminKeyboards
from keyboards.back_kb import BackKeyboards
from keyboards.menu_kb import MenuKeyboards
from keyboards.reg_kb import RegKeyboards
from keyboards.settings_kb import SettingsKeyboards
from keyboards.stats_kb import StatsKeyboards
from keyboards.student_kb import StusentKeyboards
from keyboards.super_admin_kb import SuperAdminKeyboards
from keyboards.url_kb import UrlKeyboards


class Keyboards(
    AdminKeyboards,
    BackKeyboards,
    MenuKeyboards,
    RegKeyboards,
    SettingsKeyboards,
    StatsKeyboards,
    StusentKeyboards,
    SuperAdminKeyboards,
    UrlKeyboards,
):
    """
    main class for keyboards
    """
