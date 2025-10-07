#!/usr/bin/env python3
import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QTextEdit, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt

class TraductorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam/Proton Translator Helper")
        self.setMinimumSize(600, 400)
        self.steam_path = os.path.expanduser("~/.local/share/Steam")
        self.proton_dir = os.path.join(self.steam_path, "compatibilitytools.d")
        self.proton_bin = None
        self.setup_ui()
        self.check_environment()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # --- Seção: Seleção da Tradução ---
        trad_layout = QHBoxLayout()
        trad_label = QLabel("Arquivo da tradução (.exe):")
        self.trad_path_label = QLabel("<nenhum selecionado>")
        self.trad_path_label.setStyleSheet("color: gray;")
        trad_button = QPushButton("Selecionar")
        trad_button.clicked.connect(self.select_translation)
        trad_layout.addWidget(trad_label)
        trad_layout.addWidget(self.trad_path_label, 1)
        trad_layout.addWidget(trad_button)
        main_layout.addLayout(trad_layout)

        # --- Seção: Execução ---
        exec_layout = QHBoxLayout()
        self.install_button = QPushButton("Iniciar Instalação")
        self.install_button.clicked.connect(self.install_translation)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        exec_layout.addWidget(self.install_button)
        exec_layout.addWidget(self.progress_bar)
        main_layout.addLayout(exec_layout)

        # --- Seção: Logs ---
        log_label = QLabel("Logs:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_text, 1)

        self.setLayout(main_layout)

    def log(self, message: str):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def check_environment(self):
        # Verifica Steam
        if not os.path.exists(self.steam_path):
            QMessageBox.critical(self, "Erro", "Steam não encontrada!\nInstale a Steam antes de usar este programa.")
            self.log("❌ Steam não encontrada em ~/.local/share/Steam")
            self.install_button.setEnabled(False)
            return

        # Verifica Proton/Proton-GE
        if not os.path.exists(self.proton_dir):
            QMessageBox.critical(self, "Erro", "Compatibilidade Proton não encontrada!\nInstale ao menos uma versão do Proton/Proton-GE.")
            self.log(f"❌ Pasta {self.proton_dir} não encontrada")
            self.install_button.setEnabled(False)
            return

        proton_versions = [d for d in os.listdir(self.proton_dir) if "Proton" in d]
        if not proton_versions:
            QMessageBox.critical(self, "Erro", "Nenhuma versão de Proton/Proton-GE encontrada!\nInstale ao menos uma versão do Proton na Steam.")
            self.log("❌ Nenhuma versão do Proton/Proton-GE encontrada em compatibilitytools.d")
            self.install_button.setEnabled(False)
            return

        # Seleciona a primeira versão disponível por padrão
        self.proton_bin = os.path.join(self.proton_dir, proton_versions[0], "files/bin/wine")
        self.log(f"✅ Proton detectado: {proton_versions[0]}")

    def select_translation(self):
        file_dialog = QFileDialog(self, "Selecione a tradução (.exe)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Arquivos (*.exe);;Todos os arquivos (*)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.trad_path_label.setText(selected_file)
            self.trad_path_label.setStyleSheet("color: black;")
            self.log(f"Tradução selecionada: {selected_file}")

    def install_translation(self):
        trad_path = self.trad_path_label.text()
        if trad_path == "<nenhum selecionado>":
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo de tradução antes de iniciar a instalação.")
            return

        if not self.proton_bin or not os.path.exists(self.proton_bin):
            QMessageBox.critical(self, "Erro", "Não foi possível localizar o binário do Proton.")
            return

        self.log(f"Iniciando instalador: {trad_path}")
        self.progress_bar.setValue(10)

        try:
            # Executa o instalador via Proton e captura saída
            process = subprocess.Popen(
                [self.proton_bin, trad_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Atualiza o log enquanto o processo roda
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.log(line.strip())

            process.wait()
            if process.returncode == 0:
                self.log("✅ Instalação concluída!")
                QMessageBox.information(self, "Sucesso", "Instalação concluída com sucesso!")
            else:
                self.log(f"❌ Instalador retornou código {process.returncode}")
                QMessageBox.warning(self, "Erro", "O instalador terminou com erro. Verifique os logs.")
        except Exception as e:
            self.log(f"❌ Erro ao executar instalador: {e}")
            QMessageBox.critical(self, "Erro", f"Falha ao iniciar o instalador:\n{e}")

        self.progress_bar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TraductorGUI()
    window.show()
    sys.exit(app.exec())

