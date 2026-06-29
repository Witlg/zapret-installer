import os
import sys
import subprocess
import ctypes
import re
import json
import tempfile
import shutil
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    try:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        return True
    except:
        return False

if not is_admin():
    print("Requesting administrator privileges...")
    if run_as_admin():
        sys.exit(0)
    else:
        print("Failed to get administrator privileges.")
        input("Press Enter to exit...")
        sys.exit(1)

class Config:
    VERSION = "1.0.0"
    APP_NAME = "Zapret Manager"
    STRATEGY_FILES = [
        "general.bat",
        "general (ALT).bat",
        "general (ALT2).bat",
        "general (ALT3).bat",
        "general (ALT4).bat",
        "general (ALT5).bat",
        "general (ALT6).bat",
        "general (ALT7).bat",
        "general (ALT8).bat",
        "general (ALT9).bat",
        "general (ALT10).bat",
        "general (ALT11).bat",
        "general (ALT12).bat",
        "general (SIMPLE FAKE).bat",
        "general (SIMPLE FAKE ALT).bat",
        "general (SIMPLE FAKE ALT2).bat",
        "general (FAKE TLS AUTO).bat",
        "general (FAKE TLS AUTO ALT).bat",
        "general (FAKE TLS AUTO ALT2).bat",
        "general (FAKE TLS AUTO ALT3).bat",
    ]

class Lang:
    EN = {
        "app_title": "Zapret Manager",
        "app_subtitle": "DPI bypass management for Discord, YouTube and games",
        "status_running_service": "Service running",
        "status_running_bat": "Running (bat)",
        "status_stopped": "Stopped",
        "status_checking": "Checking...",
        "admin": "Administrator",
        "strategy": "Strategy",
        "install_service": "Install as Service",
        "run_bat": "Run (bat)",
        "service_control": "Service Control",
        "stop_service": "Stop Service",
        "restart_service": "Restart Service",
        "remove_service": "Remove Service",
        "diagnostics": "Diagnostics",
        "update_lists": "Update Lists",
        "settings": "Settings",
        "game_mode": "Game Mode (all ports)",
        "tcp_udp": "TCP and UDP",
        "tcp_only": "TCP only",
        "udp_only": "UDP only",
        "check_updates": "Check updates on startup",
        "console": "Console",
        "clear": "Clear",
        "system_info": "System Info",
        "strategy_label": "Strategy",
        "status_label": "Status",
        "path_label": "Path",
        "not_installed": "Not installed",
        "unknown": "Unknown",
        "ready": "Ready",
        "error": "Error",
        "success": "Success",
        "confirm": "Confirm",
        "continue_question": "This will stop and then reinstall the service. Continue?",
        "remove_question": "Are you sure you want to remove the zapret service?",
        "yes": "Yes",
        "no": "No",
        "no_strategy": "No strategy files found",
        "winws_not_found": "winws.exe not found",
        "install_failed": "Failed to parse strategy arguments",
        "install_service_action": "Installing service",
        "stop_service_action": "Stopping service",
        "remove_service_action": "Removing service",
        "diagnostics_action": "Running diagnostics",
        "update_lists_action": "Updating lists",
        "starting_strategy": "Running strategy",
        "strategy_started": "Strategy started in new window",
        "game_mode_enabled": "Game mode enabled (TCP and UDP)",
        "game_mode_disabled": "Game mode disabled",
        "filter_mode": "Filter mode",
        "update_check_enabled": "Update check enabled",
        "update_check_disabled": "Update check disabled",
        "language": "Language",
        "english": "English",
        "russian": "Russian",
        "stopping_service": "Stopping zapret service",
        "removing_service": "Removing service",
        "removing_windivert": "Removing WinDivert",
        "killing_processes": "Terminating processes",
        "installing_service": "Installing service",
        "creating_service": "Creating service",
        "saving_strategy": "Saving strategy name",
        "starting_service": "Starting service",
        "operation_completed": "Operation completed",
        "operation_failed": "Operation failed"
    }

    RU = {
        "app_title": "Zapret Manager",
        "app_subtitle": "Управление обходом DPI для Discord, YouTube и игр",
        "status_running_service": "Служба запущена",
        "status_running_bat": "Запущен (bat)",
        "status_stopped": "Остановлен",
        "status_checking": "Проверка...",
        "admin": "Администратор",
        "strategy": "Стратегия",
        "install_service": "Установить службу",
        "run_bat": "Запустить (bat)",
        "service_control": "Управление службой",
        "stop_service": "Остановить",
        "restart_service": "Перезапустить",
        "remove_service": "Удалить службу",
        "diagnostics": "Диагностика",
        "update_lists": "Обновить списки",
        "settings": "Настройки",
        "game_mode": "Игровой режим (все порты)",
        "tcp_udp": "TCP и UDP",
        "tcp_only": "Только TCP",
        "udp_only": "Только UDP",
        "check_updates": "Проверять обновления при запуске",
        "console": "Консоль",
        "clear": "Очистить",
        "system_info": "Информация о системе",
        "strategy_label": "Стратегия",
        "status_label": "Состояние",
        "path_label": "Путь",
        "not_installed": "Не установлена",
        "unknown": "Неизвестно",
        "ready": "Готов",
        "error": "Ошибка",
        "success": "Успех",
        "confirm": "Подтверждение",
        "continue_question": "Это остановит и переустановит службу. Продолжить?",
        "remove_question": "Вы уверены, что хотите удалить службу zapret?",
        "yes": "Да",
        "no": "Нет",
        "no_strategy": "Файлы стратегий не найдены",
        "winws_not_found": "winws.exe не найден",
        "install_failed": "Не удалось разобрать аргументы стратегии",
        "install_service_action": "Установка службы",
        "stop_service_action": "Остановка службы",
        "remove_service_action": "Удаление службы",
        "diagnostics_action": "Запуск диагностики",
        "update_lists_action": "Обновление списков",
        "starting_strategy": "Запуск стратегии",
        "strategy_started": "Стратегия запущена в новом окне",
        "game_mode_enabled": "Игровой режим включен (TCP и UDP)",
        "game_mode_disabled": "Игровой режим выключен",
        "filter_mode": "Режим фильтрации",
        "update_check_enabled": "Проверка обновлений включена",
        "update_check_disabled": "Проверка обновлений выключена",
        "language": "Язык",
        "english": "Английский",
        "russian": "Русский",
        "stopping_service": "Остановка службы zapret",
        "removing_service": "Удаление службы",
        "removing_windivert": "Удаление WinDivert",
        "killing_processes": "Завершение процессов",
        "installing_service": "Установка службы",
        "creating_service": "Создание службы",
        "saving_strategy": "Сохранение имени стратегии",
        "starting_service": "Запуск службы",
        "operation_completed": "Операция выполнена",
        "operation_failed": "Операция не удалась"
    }

class Styles:
    MAIN = """
        QMainWindow { background-color: #0a0e14; }
        QWidget#centralWidget { background-color: transparent; }
        QLabel#titleLabel { font-size: 24px; font-weight: 600; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
        QLabel#subtitleLabel { font-size: 13px; color: #8b949e; font-family: 'Segoe UI', sans-serif; }
        QPushButton { background-color: #238636; color: #ffffff; border: none; border-radius: 6px; padding: 9px 18px; font-size: 13px; font-weight: 500; font-family: 'Segoe UI', sans-serif; min-height: 20px; }
        QPushButton:hover { background-color: #2ea043; }
        QPushButton:pressed { background-color: #196c2e; }
        QPushButton:disabled { background-color: #21262d; color: #484f58; }
        QPushButton#dangerBtn { background-color: #da3633; }
        QPushButton#dangerBtn:hover { background-color: #f85149; }
        QPushButton#secondaryBtn { background-color: #21262d; border: 1px solid #30363d; }
        QPushButton#secondaryBtn:hover { background-color: #30363d; border-color: #8b949e; }
        QPushButton#successBtn { background-color: #1f6feb; }
        QPushButton#successBtn:hover { background-color: #388bfd; }
        QGroupBox { font-weight: 600; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; margin-top: 14px; padding-top: 14px; font-family: 'Segoe UI', sans-serif; font-size: 13px; }
        QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 8px; color: #e6edf3; }
        QLabel#statusRunning { background-color: rgba(35,134,54,0.15); color: #3fb950; border: 1px solid rgba(63,185,80,0.2); border-radius: 6px; padding: 4px 14px; font-size: 13px; font-weight: 500; }
        QLabel#statusStopped { background-color: rgba(218,54,51,0.15); color: #f85149; border: 1px solid rgba(248,81,73,0.2); border-radius: 6px; padding: 4px 14px; font-size: 13px; font-weight: 500; }
        QLabel#statusWarning { background-color: rgba(187,128,9,0.15); color: #d29922; border: 1px solid rgba(210,153,34,0.2); border-radius: 6px; padding: 4px 14px; font-size: 13px; font-weight: 500; }
        QLabel#statusInfo { background-color: rgba(31,111,235,0.15); color: #58a6ff; border: 1px solid rgba(88,166,255,0.2); border-radius: 6px; padding: 4px 14px; font-size: 13px; font-weight: 500; }
        QTextEdit { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #e6edf3; font-family: 'Consolas', monospace; font-size: 12px; padding: 8px; }
        QComboBox { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 7px 12px; color: #e6edf3; font-size: 13px; font-family: 'Segoe UI', sans-serif; min-height: 20px; }
        QCheckBox { color: #e6edf3; font-family: 'Segoe UI', sans-serif; font-size: 13px; spacing: 8px; }
        QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #30363d; background: #0d1117; }
        QCheckBox::indicator:checked { background: #238636; border-color: #238636; }
        QStatusBar { background: #0d1117; color: #8b949e; font-family: 'Segoe UI', sans-serif; font-size: 12px; padding: 2px 12px; border-top: 1px solid #21262d; }
        QLabel#adminBadge { color: #3fb950; font-size: 12px; font-weight: 500; background: rgba(35,134,54,0.15); padding: 2px 12px; border-radius: 4px; }
        QProgressBar { border: none; border-radius: 4px; background-color: #21262d; height: 3px; }
        QProgressBar::chunk { background-color: #238636; border-radius: 4px; }
        QLabel#langLabel { color: #8b949e; font-size: 13px; font-weight: 500; font-family: 'Segoe UI', sans-serif; }
    """

class CommandWorker(QThread):
    output_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal(bool, str)
    status_update = pyqtSignal()

    def __init__(self, command, cwd, description="Executing"):
        super().__init__()
        self.command = command
        self.cwd = cwd
        self.description = description

    def run(self):
        try:
            self.output_signal.emit(f"{self.description}...", "blue")
            
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.cwd,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                encoding='cp866',
                errors='replace'
            )
            
            stdout, stderr = process.communicate()
            
            if stdout:
                for line in stdout.splitlines():
                    if line.strip():
                        self.output_signal.emit(f"  {line.strip()}", "gray")
            
            if stderr:
                for line in stderr.splitlines():
                    if line.strip():
                        self.output_signal.emit(f"  {line.strip()}", "yellow")
            
            if process.returncode == 0:
                self.output_signal.emit(f"{self.description} completed", "green")
                self.finished_signal.emit(True, "Success")
            else:
                self.output_signal.emit(f"{self.description} failed (code: {process.returncode})", "red")
                self.finished_signal.emit(False, f"Failed with code {process.returncode}")

        except Exception as e:
            self.output_signal.emit(f"Error: {e}", "red")
            self.finished_signal.emit(False, str(e))
        finally:
            self.status_update.emit()

class ZapretManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_path = Path(os.path.dirname(os.path.abspath(__file__)))
        self.bin_path = self.base_path / "bin"
        self.workers = []
        self.current_lang = "EN"
        self.lang = Lang.EN
        
        self.lang_file = self.base_path / "lang.json"
        self.load_language()
        
        self.init_ui()
        self.refresh_status()

    def load_language(self):
        if self.lang_file.exists():
            try:
                data = json.loads(self.lang_file.read_text(encoding='utf-8'))
                self.current_lang = data.get("lang", "EN")
                self.lang = Lang.EN if self.current_lang == "EN" else Lang.RU
            except:
                pass

    def save_language(self):
        try:
            self.lang_file.write_text(json.dumps({"lang": self.current_lang}), encoding='utf-8')
        except:
            pass

    def tr(self, key):
        return self.lang.get(key, key)

    def init_ui(self):
        self.setWindowTitle(f"{self.tr('app_title')} v{Config.VERSION}")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(Styles.MAIN)
        self.setWindowIcon(self.create_icon())

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 25, 30, 25)

        header = self.create_header()
        main_layout.addWidget(header)

        content = QHBoxLayout()
        content.setSpacing(25)

        left_panel = self.create_left_panel()
        content.addWidget(left_panel, 3)

        right_panel = self.create_right_panel()
        content.addWidget(right_panel, 2)

        main_layout.addLayout(content)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.tr('ready'))

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(3000)

        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.setMaximumHeight(16)
        self.progress.setTextVisible(False)
        self.progress.hide()
        self.status_bar.addPermanentWidget(self.progress)

    def create_icon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#238636"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(6, 6, 52, 52, 10, 10)
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Z")
        painter.end()
        icon = QIcon()
        icon.addPixmap(pixmap)
        return icon

    def create_header(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(2)

        top_row = QHBoxLayout()
        title = QLabel(self.tr('app_title'))
        title.setObjectName("titleLabel")
        top_row.addWidget(title)
        top_row.addStretch()
        
        lang_label = QLabel(self.tr('language') + ":")
        lang_label.setObjectName("langLabel")
        top_row.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([self.tr('english'), self.tr('russian')])
        self.lang_combo.setCurrentIndex(0 if self.current_lang == "EN" else 1)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.lang_combo.setMaximumWidth(120)
        top_row.addWidget(self.lang_combo)
        
        self.status_label = QLabel(self.tr('status_checking'))
        self.status_label.setObjectName("statusInfo")
        top_row.addWidget(self.status_label)
        
        admin_label = QLabel(self.tr('admin'))
        admin_label.setObjectName("adminBadge")
        top_row.addWidget(admin_label)
        
        layout.addLayout(top_row)

        subtitle = QLabel(self.tr('app_subtitle'))
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)

        return widget

    def create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        strategy_group = QGroupBox(self.tr('strategy'))
        strategy_layout = QVBoxLayout(strategy_group)
        strategy_layout.setSpacing(10)

        self.strategy_combo = QComboBox()
        strategy_files = self.get_strategy_files()
        self.strategy_combo.addItems(strategy_files)
        if strategy_files:
            self.strategy_combo.setCurrentIndex(0)
        strategy_layout.addWidget(self.strategy_combo)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        self.install_btn = QPushButton(self.tr('install_service'))
        self.install_btn.clicked.connect(self.install_service)
        self.install_btn.setObjectName("successBtn")
        btn_row.addWidget(self.install_btn)

        self.run_btn = QPushButton(self.tr('run_bat'))
        self.run_btn.clicked.connect(self.run_strategy)
        self.run_btn.setObjectName("secondaryBtn")
        btn_row.addWidget(self.run_btn)

        strategy_layout.addLayout(btn_row)
        layout.addWidget(strategy_group)

        service_group = QGroupBox(self.tr('service_control'))
        service_layout = QVBoxLayout(service_group)
        service_layout.setSpacing(8)

        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)

        self.stop_btn = QPushButton(self.tr('stop_service'))
        self.stop_btn.clicked.connect(self.stop_service)
        self.stop_btn.setObjectName("dangerBtn")
        btn_grid.addWidget(self.stop_btn, 0, 0)

        self.restart_btn = QPushButton(self.tr('restart_service'))
        self.restart_btn.clicked.connect(self.restart_service)
        self.restart_btn.setObjectName("secondaryBtn")
        btn_grid.addWidget(self.restart_btn, 0, 1)

        self.remove_btn = QPushButton(self.tr('remove_service'))
        self.remove_btn.clicked.connect(self.remove_service)
        self.remove_btn.setObjectName("dangerBtn")
        btn_grid.addWidget(self.remove_btn, 1, 0)

        self.diag_btn = QPushButton(self.tr('diagnostics'))
        self.diag_btn.clicked.connect(self.run_diagnostics)
        self.diag_btn.setObjectName("secondaryBtn")
        btn_grid.addWidget(self.diag_btn, 1, 1)

        service_layout.addLayout(btn_grid)
        layout.addWidget(service_group)

        settings_group = QGroupBox(self.tr('settings'))
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(8)

        self.game_filter_cb = QCheckBox(self.tr('game_mode'))
        self.game_filter_cb.stateChanged.connect(self.toggle_game_filter)
        settings_layout.addWidget(self.game_filter_cb)

        self.game_filter_mode = QComboBox()
        self.game_filter_mode.addItems([self.tr('tcp_udp'), self.tr('tcp_only'), self.tr('udp_only')])
        self.game_filter_mode.setEnabled(False)
        self.game_filter_mode.currentTextChanged.connect(self.change_game_mode)
        settings_layout.addWidget(self.game_filter_mode)

        self.update_check_cb = QCheckBox(self.tr('check_updates'))
        self.update_check_cb.stateChanged.connect(self.toggle_update_check)
        settings_layout.addWidget(self.update_check_cb)

        layout.addWidget(settings_group)
        layout.addStretch()
        return widget

    def create_right_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        log_group = QGroupBox(self.tr('console'))
        log_layout = QVBoxLayout(log_group)
        log_layout.setSpacing(8)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(300)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        log_layout.addWidget(self.log_text)

        clear_btn = QPushButton(self.tr('clear'))
        clear_btn.clicked.connect(lambda: self.log_text.clear())
        clear_btn.setObjectName("secondaryBtn")
        clear_btn.setMaximumWidth(100)
        log_layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(log_group)

        info_group = QGroupBox(self.tr('system_info'))
        info_layout = QVBoxLayout(info_group)
        info_layout.setSpacing(4)

        self.info_labels = {}
        info_items = [
            (self.tr('strategy_label'), self.tr('not_installed')),
            (self.tr('status_label'), self.tr('unknown')),
            (self.tr('path_label'), str(self.base_path)),
        ]
        for key, value in info_items:
            label = QLabel(f"{key}: {value}")
            label.setStyleSheet("color: #8b949e; font-size: 13px; font-family: 'Segoe UI', sans-serif;")
            self.info_labels[key] = label
            info_layout.addWidget(label)

        layout.addWidget(info_group)
        return widget

    def change_language(self, index):
        self.current_lang = "EN" if index == 0 else "RU"
        self.lang = Lang.EN if self.current_lang == "EN" else Lang.RU
        self.save_language()
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(f"{self.tr('app_title')} v{Config.VERSION}")
        
        self.findChild(QLabel, "titleLabel").setText(self.tr('app_title'))
        self.findChild(QLabel, "subtitleLabel").setText(self.tr('app_subtitle'))
        
        for child in self.findChildren(QGroupBox):
            if child.title() in [Lang.EN["strategy"], Lang.RU["strategy"]]:
                child.setTitle(self.tr('strategy'))
            elif child.title() in [Lang.EN["service_control"], Lang.RU["service_control"]]:
                child.setTitle(self.tr('service_control'))
            elif child.title() in [Lang.EN["settings"], Lang.RU["settings"]]:
                child.setTitle(self.tr('settings'))
            elif child.title() in [Lang.EN["console"], Lang.RU["console"]]:
                child.setTitle(self.tr('console'))
            elif child.title() in [Lang.EN["system_info"], Lang.RU["system_info"]]:
                child.setTitle(self.tr('system_info'))
        
        self.install_btn.setText(self.tr('install_service'))
        self.run_btn.setText(self.tr('run_bat'))
        self.stop_btn.setText(self.tr('stop_service'))
        self.restart_btn.setText(self.tr('restart_service'))
        self.remove_btn.setText(self.tr('remove_service'))
        self.diag_btn.setText(self.tr('diagnostics'))
        self.game_filter_cb.setText(self.tr('game_mode'))
        self.update_check_cb.setText(self.tr('check_updates'))
        
        self.game_filter_mode.setItemText(0, self.tr('tcp_udp'))
        self.game_filter_mode.setItemText(1, self.tr('tcp_only'))
        self.game_filter_mode.setItemText(2, self.tr('udp_only'))
        
        self.status_bar.showMessage(self.tr('ready'))
        self.refresh_status()

    def get_strategy_files(self):
        files = []
        for f in Config.STRATEGY_FILES:
            path = self.base_path / f
            if path.exists():
                files.append(f)
        if not files:
            files = [self.tr('no_strategy')]
        return files

    def log(self, message, color=None):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        colors = {
            "green": "#3fb950",
            "red": "#f85149",
            "yellow": "#d29922",
            "blue": "#58a6ff",
            "gray": "#8b949e",
        }
        color_code = colors.get(color, "#e6edf3")
        self.log_text.append(
            f'<span style="color:#484f58;">[{timestamp}]</span> '
            f'<span style="color:{color_code};">{message}</span>'
        )
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def refresh_status(self):
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq winws.exe"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            is_running = "winws.exe" in result.stdout

            result = subprocess.run(
                ["sc", "query", "zapret"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            is_service = "RUNNING" in result.stdout

            try:
                result = subprocess.run(
                    ["reg", "query", "HKLM\\System\\CurrentControlSet\\Services\\zapret", "/v", "zapret-discord-youtube"],
                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        if "zapret-discord-youtube" in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                self.running_strategy = parts[2]
                                break
            except:
                pass

            if is_service:
                self.status_label.setText(self.tr('status_running_service'))
                self.status_label.setObjectName("statusRunning")
                self.info_labels[self.tr('status_label')].setText(f"{self.tr('status_label')}: {self.tr('status_running_service')}")
                self.info_labels[self.tr('status_label')].setStyleSheet("color: #3fb950; font-size: 13px;")
            elif is_running:
                self.status_label.setText(self.tr('status_running_bat'))
                self.status_label.setObjectName("statusWarning")
                self.info_labels[self.tr('status_label')].setText(f"{self.tr('status_label')}: {self.tr('status_running_bat')}")
                self.info_labels[self.tr('status_label')].setStyleSheet("color: #d29922; font-size: 13px;")
            else:
                self.status_label.setText(self.tr('status_stopped'))
                self.status_label.setObjectName("statusStopped")
                self.info_labels[self.tr('status_label')].setText(f"{self.tr('status_label')}: {self.tr('status_stopped')}")
                self.info_labels[self.tr('status_label')].setStyleSheet("color: #f85149; font-size: 13px;")

            if hasattr(self, 'running_strategy') and self.running_strategy:
                self.info_labels[self.tr('strategy_label')].setText(f"{self.tr('strategy_label')}: {self.running_strategy}")
                self.info_labels[self.tr('strategy_label')].setStyleSheet("color: #58a6ff; font-size: 13px;")

            game_file = self.base_path / "utils" / "game_filter.enabled"
            if game_file.exists():
                try:
                    mode = game_file.read_text().strip()
                    mode_map = {"all": self.tr('tcp_udp'), "tcp": self.tr('tcp_only'), "udp": self.tr('udp_only')}
                    self.game_filter_cb.setChecked(True)
                    self.game_filter_mode.setEnabled(True)
                    self.game_filter_mode.setCurrentText(mode_map.get(mode, self.tr('tcp_udp')))
                except:
                    pass
            else:
                self.game_filter_cb.setChecked(False)
                self.game_filter_mode.setEnabled(False)

            update_file = self.base_path / "utils" / "check_updates.enabled"
            self.update_check_cb.setChecked(update_file.exists())

        except Exception as e:
            pass

    def run_command_thread(self, command, description):
        self.set_buttons_enabled(False)
        self.progress.show()
        self.progress.setRange(0, 0)
        
        worker = CommandWorker(command, str(self.base_path), description)
        worker.output_signal.connect(self.log)
        worker.finished_signal.connect(lambda success, msg: self.on_command_finished(success, msg))
        worker.status_update.connect(self.refresh_status)
        worker.finished.connect(lambda: self.cleanup_worker(worker))
        
        self.workers.append(worker)
        worker.start()

    def on_command_finished(self, success, message):
        self.progress.hide()
        self.set_buttons_enabled(True)
        if not success:
            QMessageBox.warning(self, self.tr('error'), f"{self.tr('operation_failed')}: {message}")

    def cleanup_worker(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)

    def set_buttons_enabled(self, enabled):
        for btn in [self.install_btn, self.stop_btn, self.restart_btn, 
                    self.remove_btn, self.diag_btn]:
            btn.setEnabled(enabled)
        self.run_btn.setEnabled(enabled)

    def parse_strategy_args(self, strategy_file):
        args = []
        try:
            with open(self.base_path / strategy_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.splitlines():
                    if 'winws.exe' in line and not line.strip().startswith('::'):
                        parts = line.split('winws.exe')
                        if len(parts) > 1:
                            args_str = parts[1].strip()
                            args = []
                            current = ''
                            in_quotes = False
                            for char in args_str:
                                if char == '"' and not in_quotes:
                                    in_quotes = True
                                    current += char
                                elif char == '"' and in_quotes:
                                    in_quotes = False
                                    current += char
                                elif char == ' ' and not in_quotes:
                                    if current:
                                        args.append(current)
                                        current = ''
                                else:
                                    current += char
                            if current:
                                args.append(current)
                            break
        except Exception as e:
            self.log(f"Error parsing strategy: {e}", "red")
        return args

    def install_service(self):
        strategy = self.strategy_combo.currentText()
        if strategy == self.tr('no_strategy'):
            QMessageBox.warning(self, self.tr('error'), self.tr('no_strategy'))
            return

        self.log(self.tr('installing_service'), "blue")

        winws_path = self.bin_path / "winws.exe"
        if not winws_path.exists():
            QMessageBox.warning(self, self.tr('error'), f"{self.tr('winws_not_found')} in {self.bin_path}")
            return

        args = self.parse_strategy_args(strategy)
        if not args:
            QMessageBox.warning(self, self.tr('error'), self.tr('install_failed'))
            return

        install_script = self.base_path / "install_service_temp.bat"
        winws_path_str = str(winws_path)
        bin_path_with_args = f'"{winws_path_str}" {" ".join(args)}'
        
        script_content = f'''@echo off
chcp 65001 > nul
cd /d "{self.base_path}"

net stop zapret 2>nul
sc delete zapret 2>nul

sc create zapret binPath= "{bin_path_with_args}" DisplayName= "zapret" start= auto

if %errorlevel% equ 0 (
    reg add "HKLM\\System\\CurrentControlSet\\Services\\zapret" /v zapret-discord-youtube /t REG_SZ /d "{strategy}" /f
    sc start zapret
)
'''
        
        with open(install_script, "w", encoding="utf-8", newline='\r\n') as f:
            f.write(script_content)
        
        self.run_command_thread([str(install_script)], self.tr('installing_service'))
        QTimer.singleShot(10000, lambda: install_script.unlink(missing_ok=True))

    def run_strategy(self):
        strategy = self.strategy_combo.currentText()
        if strategy == self.tr('no_strategy'):
            QMessageBox.warning(self, self.tr('error'), self.tr('no_strategy'))
            return

        self.log(f"{self.tr('starting_strategy')}: {strategy}", "blue")
        try:
            subprocess.Popen(
                ["cmd", "/c", "start", "", strategy],
                cwd=str(self.base_path),
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.log(self.tr('strategy_started'), "green")
            self.refresh_status()
        except Exception as e:
            self.log(f"Run error: {e}", "red")

    def stop_service(self):
        self.log(self.tr('stop_service_action'), "blue")
        
        stop_script = self.base_path / "stop_service_temp.bat"
        script_content = f'''@echo off
chcp 65001 > nul
cd /d "{self.base_path}"

net stop zapret
taskkill /IM winws.exe /F 2>nul
'''
        with open(stop_script, "w", encoding="utf-8", newline='\r\n') as f:
            f.write(script_content)
        
        self.run_command_thread([str(stop_script)], self.tr('stop_service_action'))
        QTimer.singleShot(5000, lambda: stop_script.unlink(missing_ok=True))

    def restart_service(self):
        reply = QMessageBox.question(
            self, self.tr('confirm'),
            self.tr('continue_question'),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.log(self.tr('restart_service'), "blue")
        self.stop_service()
        QTimer.singleShot(4000, self.install_service)

    def remove_service(self):
        reply = QMessageBox.question(
            self, self.tr('confirm'),
            self.tr('remove_question'),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.log(self.tr('remove_service_action'), "blue")
            
            remove_script = self.base_path / "remove_service_temp.bat"
            script_content = f'''@echo off
chcp 65001 > nul
cd /d "{self.base_path}"

net stop zapret 2>nul
sc delete zapret
sc delete WinDivert 2>nul
taskkill /IM winws.exe /F 2>nul
'''
            with open(remove_script, "w", encoding="utf-8", newline='\r\n') as f:
                f.write(script_content)
            
            self.run_command_thread([str(remove_script)], self.tr('remove_service_action'))
            QTimer.singleShot(5000, lambda: remove_script.unlink(missing_ok=True))

    def run_diagnostics(self):
        self.log(self.tr('diagnostics_action'), "blue")
        
        diag_script = self.base_path / "diag_temp.bat"
        script_content = f'''@echo off
chcp 65001 > nul
cd /d "{self.base_path}"

echo === ZAPRET DIAGNOSTICS ===
echo.
echo Checking zapret service...
sc query zapret
echo.
echo Checking WinDivert service...
sc query WinDivert
echo.
echo Checking running processes...
tasklist /FI "IMAGENAME eq winws.exe"
echo.
echo Checking WinDivert driver...
dir "{self.bin_path}\\*.sys" 2>nul
'''
        with open(diag_script, "w", encoding="utf-8", newline='\r\n') as f:
            f.write(script_content)
        
        self.run_command_thread([str(diag_script)], self.tr('diagnostics_action'))
        QTimer.singleShot(10000, lambda: diag_script.unlink(missing_ok=True))

    def toggle_game_filter(self, state):
        game_file = self.base_path / "utils" / "game_filter.enabled"
        if state == Qt.CheckState.Checked.value:
            game_file.parent.mkdir(exist_ok=True)
            game_file.write_text("all")
            self.game_filter_mode.setEnabled(True)
            self.log(self.tr('game_mode_enabled'), "green")
        else:
            if game_file.exists():
                game_file.unlink()
            self.game_filter_mode.setEnabled(False)
            self.log(self.tr('game_mode_disabled'), "yellow")
        self.refresh_status()

    def change_game_mode(self, mode):
        if not self.game_filter_cb.isChecked():
            return
        mode_map = {
            self.tr('tcp_udp'): "all",
            self.tr('tcp_only'): "tcp",
            self.tr('udp_only'): "udp"
        }
        game_file = self.base_path / "utils" / "game_filter.enabled"
        game_file.parent.mkdir(exist_ok=True)
        game_file.write_text(mode_map.get(mode, "all"))
        self.log(f"{self.tr('filter_mode')}: {mode}", "blue")

    def toggle_update_check(self, state):
        update_file = self.base_path / "utils" / "check_updates.enabled"
        if state == Qt.CheckState.Checked.value:
            update_file.parent.mkdir(exist_ok=True)
            update_file.write_text("ENABLED")
            self.log(self.tr('update_check_enabled'), "green")
        else:
            if update_file.exists():
                update_file.unlink()
            self.log(self.tr('update_check_disabled'), "yellow")

    def closeEvent(self, event):
        for worker in self.workers:
            worker.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0a0e14"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#e6edf3"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#0d1117"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#161b22"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#e6edf3"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#0a0e14"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#e6edf3"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#e6edf3"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#f85149"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = ZapretManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
