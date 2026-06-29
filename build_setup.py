# build_setup.py
import os
import sys
import subprocess
import base64
import zipfile
import io
from pathlib import Path

print("Zapret Setup Builder")
print("=" * 50)

# Устанавливаем PyInstaller если нет
try:
    import PyInstaller
except ImportError:
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Папка с файлами zapret
source_dir = Path(os.path.dirname(os.path.abspath(__file__)))
print(f"Source directory: {source_dir}")

# Собираем все файлы в ZIP архив
print("\nCollecting files...")
zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    files_added = 0
    for file in source_dir.rglob('*'):
        if file.is_file():
            # Пропускаем файлы сборки
            if file.name in ['build_setup.py', 'setup.exe', 'zapret_installer.py', 'installer.py']:
                continue
            # Пропускаем папку __pycache__
            if '__pycache__' in str(file):
                continue
            # Пропускаем build и dist
            if 'build' in str(file) or 'dist' in str(file):
                continue
                
            rel_path = file.relative_to(source_dir)
            zip_file.write(file, rel_path)
            files_added += 1
            print(f"  Added: {rel_path}")
    
    zip_file.writestr('_files_count.txt', str(files_added))

print(f"\nTotal files added: {files_added}")
zip_data = base64.b64encode(zip_buffer.getvalue()).decode('ascii')
print(f"ZIP size: {len(zip_data)} bytes")

# Создаем installer.py - используем обычные строки без f-строк
print("\nCreating installer.py...")

installer_code = '''import os
import sys
import subprocess
import ctypes
import base64
import zipfile
import shutil
import io
from pathlib import Path

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

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *

EMBEDDED_ZIP = """''' + zip_data + '''"""

class Styles:
    MAIN = """
        QMainWindow { background-color: #0a0e14; }
        QWidget#centralWidget { background-color: transparent; }
        QLabel#titleLabel { font-size: 28px; font-weight: 600; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
        QLabel#subtitleLabel { font-size: 14px; color: #8b949e; font-family: 'Segoe UI', sans-serif; }
        QPushButton { background-color: #238636; color: #ffffff; border: none; border-radius: 6px; padding: 12px 28px; font-size: 15px; font-weight: 500; font-family: 'Segoe UI', sans-serif; }
        QPushButton:hover { background-color: #2ea043; }
        QPushButton:disabled { background-color: #21262d; color: #484f58; }
        QPushButton#secondaryBtn { background-color: #21262d; border: 1px solid #30363d; }
        QPushButton#secondaryBtn:hover { background-color: #30363d; }
        QGroupBox { font-weight: 600; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; margin-top: 14px; padding-top: 14px; font-family: 'Segoe UI', sans-serif; font-size: 13px; }
        QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 8px; color: #e6edf3; }
        QLineEdit { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; color: #e6edf3; font-size: 13px; }
        QLineEdit:focus { border-color: #1f6feb; }
        QProgressBar { border: none; border-radius: 4px; background-color: #21262d; height: 8px; }
        QProgressBar::chunk { background-color: #238636; border-radius: 4px; }
        QTextEdit { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #e6edf3; font-family: 'Consolas', monospace; font-size: 12px; padding: 8px; }
        QCheckBox { color: #e6edf3; font-family: 'Segoe UI', sans-serif; font-size: 13px; spacing: 8px; }
        QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 2px solid #30363d; background: #0d1117; }
        QCheckBox::indicator:checked { background: #238636; border-color: #238636; }
        QStatusBar { background: #0d1117; color: #8b949e; font-family: 'Segoe UI', sans-serif; font-size: 12px; padding: 2px 12px; border-top: 1px solid #21262d; }
        QMessageBox { background-color: #0d1117; color: #e6edf3; }
        QMessageBox QPushButton { min-width: 80px; }
    """

class ZapretSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.install_path = Path("C:/Program Files/Zapret")
        self.total_files = 0
        self.init_ui()
        
        try:
            zip_data = base64.b64decode(EMBEDDED_ZIP)
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
                self.total_files = len(zip_file.namelist()) - 1
        except:
            self.total_files = 0

    def init_ui(self):
        self.setWindowTitle("Zapret Setup")
        self.setFixedSize(800, 600)
        self.setStyleSheet(Styles.MAIN)
        self.setWindowIcon(self.create_icon())

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)

        header = QLabel("Zapret")
        header.setObjectName("titleLabel")
        main_layout.addWidget(header)

        subtitle = QLabel("DPI bypass tool for Discord, YouTube and games")
        subtitle.setObjectName("subtitleLabel")
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        content = QHBoxLayout()
        content.setSpacing(20)

        left = self.create_left_panel()
        content.addWidget(left, 3)

        right = self.create_right_panel()
        content.addWidget(right, 2)

        main_layout.addLayout(content)

        main_layout.addSpacing(10)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to install")

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

    def create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        info_group = QGroupBox("Setup Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = f"""
        <b>Files to install:</b> {self.total_files}
        <br><br>
        <b>Installation size:</b> ~20 MB
        <br><br>
        <b>Includes:</b>
        <br>• winws.exe (DPI bypass)
        <br>• All strategies (bat files)
        <br>• Service manager
        <br>• Configuration lists
        """
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #8b949e; font-size: 13px; font-family: 'Segoe UI', sans-serif;")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)

        install_group = QGroupBox("Installation")
        install_layout = QVBoxLayout(install_group)

        path_label = QLabel("Installation path:")
        path_label.setStyleSheet("color: #8b949e; font-size: 13px; font-family: 'Segoe UI', sans-serif;")
        install_layout.addWidget(path_label)

        path_row = QHBoxLayout()
        self.path_edit = QLineEdit(str(self.install_path))
        path_row.addWidget(self.path_edit)

        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.setMaximumWidth(100)
        browse_btn.clicked.connect(self.browse_path)
        path_row.addWidget(browse_btn)

        install_layout.addLayout(path_row)

        self.shortcut_cb = QCheckBox("Create desktop shortcut")
        self.shortcut_cb.setChecked(True)
        install_layout.addWidget(self.shortcut_cb)

        self.startmenu_cb = QCheckBox("Add to Start Menu")
        self.startmenu_cb.setChecked(True)
        install_layout.addWidget(self.startmenu_cb)

        install_layout.addSpacing(10)

        install_btn = QPushButton("Install")
        install_btn.clicked.connect(self.install)
        install_btn.setObjectName("successBtn")
        install_layout.addWidget(install_btn)

        layout.addWidget(install_group)
        layout.addStretch()
        return widget

    def create_right_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        log_group = QGroupBox("Installation Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.setSpacing(8)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        log_layout.addWidget(self.progress)

        self.status_label = QLabel("Ready to install")
        self.status_label.setObjectName("statusLabel")
        log_layout.addWidget(self.status_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)

        layout.addWidget(log_group)
        return widget

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Installation Directory",
            str(self.install_path),
            QFileDialog.Option.ShowDirsOnly
        )
        if path:
            self.install_path = Path(path)
            self.path_edit.setText(str(self.install_path))

    def log(self, message, color="#8b949e"):
        self.log_text.append(f'<span style="color:{color}">{message}</span>')
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

    def install(self):
        self.setWindowTitle("Zapret Setup - Installing...")
        self.log("Starting installation...", "#58a6ff")
        self.progress.setValue(5)
        
        install_path = Path(self.path_edit.text())
        
        try:
            self.log(f"Extracting files to: {install_path}", "#8b949e")
            
            zip_data = base64.b64decode(EMBEDDED_ZIP)
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
                files = zip_file.namelist()
                total = len(files)
                
                for i, filename in enumerate(files):
                    if filename == '_files_count.txt':
                        continue
                        
                    target = install_path / filename
                    target.parent.mkdir(parents=True, exist_ok=True)
                    
                    content = zip_file.read(filename)
                    with open(target, 'wb') as f:
                        f.write(content)
                    
                    progress = 10 + (i / total) * 70
                    self.progress.setValue(int(progress))
                    
                    if i % 10 == 0:
                        self.log(f"  Extracting: {filename}", "#8b949e")
                
                self.progress.setValue(85)
                self.log("All files extracted successfully!", "#3fb950")

            self.create_manager(install_path)
            self.progress.setValue(90)

            if self.shortcut_cb.isChecked():
                self.create_desktop_shortcut(install_path)
                self.log("Desktop shortcut created", "#3fb950")

            if self.startmenu_cb.isChecked():
                self.create_startmenu_shortcut(install_path)
                self.log("Start Menu shortcut created", "#3fb950")

            self.progress.setValue(100)
            self.status_label.setText("Installation Complete!")

            self.log("", "#8b949e")
            self.log("=" * 50, "#58a6ff")
            self.log("Installation completed successfully!", "#3fb950")
            self.log(f"Installed to: {install_path}", "#8b949e")
            self.log(f"Files installed: {total}", "#8b949e")
            self.log("=" * 50, "#58a6ff")
            
            self.setWindowTitle("Zapret Setup - Complete")

            reply = QMessageBox.question(
                self,
                "Installation Complete",
                f"Zapret has been installed to:\\n{install_path}\\n\\nDo you want to open the installation folder?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                os.startfile(str(install_path))

        except Exception as e:
            self.log(f"Installation failed: {e}", "#f85149")
            self.status_label.setText("Installation Failed!")
            QMessageBox.critical(self, "Error", f"Installation failed:\\n{str(e)}")
            self.setWindowTitle("Zapret Setup - Failed")

    def create_manager(self, install_path):
        content = '@echo off\\nchcp 65001 > nul\\ncd /d "' + str(install_path) + '"\\necho Starting Zapret Manager...\\ncall service.bat\\npause'
        with open(install_path / "Zapret Manager.bat", "w", encoding="utf-8") as f:
            f.write(content.replace('\\n', '\\n'))

    def create_desktop_shortcut(self, install_path):
        desktop = Path(os.path.expanduser("~/Desktop"))
        shortcut = desktop / "Zapret Manager.lnk"
        self.create_shortcut(install_path / "Zapret Manager.bat", shortcut)

    def create_startmenu_shortcut(self, install_path):
        startmenu = Path(os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"))
        if not startmenu.exists():
            startmenu = Path(os.path.expanduser("~/Start Menu/Programs"))
        if startmenu.exists():
            shortcut = startmenu / "Zapret Manager.lnk"
            self.create_shortcut(install_path / "Zapret Manager.bat", shortcut)

    def create_shortcut(self, target, shortcut_path):
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(target)
            shortcut.WorkingDirectory = str(target.parent)
            shortcut.Description = "Zapret Manager"
            shortcut.Save()
        except:
            pass

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
    
    window = ZapretSetup()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''

# Сохраняем installer.py
with open(source_dir / "installer.py", "w", encoding="utf-8") as f:
    f.write(installer_code)

print("\nInstaller.py created")

# Собираем EXE с PyInstaller
print("\nBuilding setup.exe with PyInstaller...")
print("This may take a few minutes...")

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "setup",
    "--distpath", str(source_dir),
    "--workpath", str(source_dir / "build"),
    "--specpath", str(source_dir),
    str(source_dir / "installer.py")
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n" + "=" * 50)
    print("SUCCESS! setup.exe created!")
    print(f"Location: {source_dir / 'setup.exe'}")
    print("=" * 50)
    
    # Удаляем временные файлы
    import shutil
    shutil.rmtree(source_dir / "build", ignore_errors=True)
    shutil.rmtree(source_dir / "__pycache__", ignore_errors=True)
    (source_dir / "installer.py").unlink(missing_ok=True)
    (source_dir / "setup.spec").unlink(missing_ok=True)
    
else:
    print("\n" + "=" * 50)
    print("ERROR building setup.exe:")
    print("=" * 50)
    print(result.stderr)

print("\nDone!")