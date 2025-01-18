from gui.gui import Gui
import config_data

gui = Gui(
    config_data.config.btns.btn_reg,
    config_data.config.btns.btn_start_quiz,
    config_data.config.btns.btn_show_score,
    config_data.config.btns.btn_show_participants
)