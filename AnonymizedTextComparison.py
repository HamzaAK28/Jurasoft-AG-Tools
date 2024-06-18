import sys
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton, QFileDialog, QApplication, qApp, QAction
from AnonTester import process_folders, compare_patterns as comText


class AnonymizedTextComparison(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_file_label = QtWidgets.QLabel()  # Add a label to display the current file name
        self.manual_text_folder_label = QtWidgets.QLabel()
        self.trained_text_folder_label = QtWidgets.QLabel()
        # Initialize missing patterns variables as empty strings
        self.missing_patterns_manual_text = ""
        self.missing_patterns_trained_text = ""

    def init_ui(self):
        # Set the window title
        self.manual_text_folder = ''
        self.trained_text_folder = ''
        self.manual_results = []
        self.trained_results = []
        self.missing_in_trained = []
        # Create a QLabel for the header
        header_label = QtWidgets.QLabel("<h1>Anonymer Tester</h1>")
        header_label.setAlignment(Qt.AlignCenter)  # Center align the header

        self.setWindowTitle('Anonymized Text Comparison(Testing Tool)')
        self.note_label1 = QtWidgets.QLabel(
            "<font color='red'>Note 1: Begin by choosing the 'Manually_anonymized_control_files' (Folder 1), followed by the selection of the 'Anonymized_by_Anonymer' (Folder 2).</font>")
        self.note_label2 = QtWidgets.QLabel(
            "<font color='red'>Note 2: In the event of comparing the outcomes of the Old Model and New Model results, please opt for the Old Model Folder first and subsequently select the New Model Folder.</font>")
        self.summary_label = QtWidgets.QLabel("Summary of above results are:")
        self.missing_patterns_label1 = QtWidgets.QLabel("Manual patterns absent from Trained Files:")
        self.missing_patterns_label2 = QtWidgets.QLabel("Trained patterns absent from Manual Files:")
        self.Summary_label = QtWidgets.QLabel("Summary:")
        self.folder_select_button = QtWidgets.QPushButton('Select Folders')
        self.compare_button = QtWidgets.QPushButton('Compare Texts')

        # Create a layout for the widgets
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(header_label)
        main_layout.addWidget(self.note_label1)
        main_layout.addWidget(self.note_label2)

        # Create a sub-layout for the labels and text areas
        results_layout = QtWidgets.QVBoxLayout()

        # Create two text areas for the results with labels
        self.manual_results_label = QtWidgets.QLabel(
            "Manual Text Results / Old Trained Text Results(Old Model Data):")
        self.manual_results_text = QtWidgets.QTextEdit()
        self.add_copy_button_to_textarea(self.manual_results_text)  # Add copy button

        self.trained_results_label = QtWidgets.QLabel(
            "Trained Text Results / New Trained Text Results(Current Model Data):")
        self.trained_results_text = QtWidgets.QTextEdit()
        self.add_copy_button_to_textarea(self.trained_results_text)  # Add copy button

        # Create text areas for missing patterns
        self.missing_patterns_manual_text_area = QtWidgets.QTextEdit()
        self.add_copy_button_to_textarea(self.missing_patterns_manual_text_area)  # add copy button

        self.missing_patterns_trained_text_area = QtWidgets.QTextEdit()
        self.add_copy_button_to_textarea(self.missing_patterns_trained_text_area)  # add copy button

        # Add the labels and text areas to the results layout
        results_layout.addWidget(self.manual_results_label)
        results_layout.addWidget(self.manual_results_text)
        results_layout.addWidget(self.trained_results_label)
        results_layout.addWidget(self.trained_results_text)

        results_layout.addWidget(self.missing_patterns_label1)
        results_layout.addWidget(self.missing_patterns_manual_text_area)

        results_layout.addWidget(self.missing_patterns_label2)
        results_layout.addWidget(self.missing_patterns_trained_text_area)

        results_layout.addWidget(self.Summary_label)
        # Create a text area for the summary
        self.summary_text = QtWidgets.QTextEdit()
        results_layout.addWidget(self.summary_text)

        # Add the sub-layout with labels and text areas to the main layout
        main_layout.addLayout(results_layout)

        # Add the buttons to the main layout
        main_layout.addWidget(self.folder_select_button)
        main_layout.addWidget(self.compare_button)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        # Set the application icon
        self.setWindowIcon(QIcon('images//difference_FILL0_wght400_GRAD0_opsz24.png'))

        # Add the logo
        self.set_logo()

        self.folder_select_button.clicked.connect(self.select_folders)
        self.compare_button.clicked.connect(self.compare_texts)

        # Add copying action
        self.add_copy_action()

        # Add text areas for all_manual_texts and all_trained_texts
        side_by_side_layout = QtWidgets.QHBoxLayout()
        self.all_manual_texts_label = QtWidgets.QLabel("All Manual Texts:")
        self.all_trained_texts_label = QtWidgets.QLabel("All Trained Texts:")
        self.all_manual_texts_area = QtWidgets.QTextEdit()
        self.all_trained_texts_area = QtWidgets.QTextEdit()

        side_by_side_layout.addWidget(self.all_manual_texts_label)
        side_by_side_layout.addWidget(self.all_manual_texts_area)
        side_by_side_layout.addWidget(self.all_trained_texts_label)
        side_by_side_layout.addWidget(self.all_trained_texts_area)

        main_layout.addLayout(side_by_side_layout)

    def add_copy_button_to_textarea(self, text_area):
        copy_button = QToolButton()
        copy_button.setIcon(QIcon('images//content_copy_FILL0_wght400_GRAD0_opsz24.png'))
        copy_button.setToolTip('Copy')
        copy_button.clicked.connect(lambda: self.copy_text_from_textarea(text_area))

        layout = QtWidgets.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(copy_button)

        text_area.setLayout(layout)

    def copy_text_from_textarea(self, text_area):
        text_area.selectAll()
        selected_text = text_area.textCursor().selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    def select_folders(self):
        self.manual_text_folder = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                             'Select Manually anonymized control files')
        self.trained_text_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Anonimized by Anonymer files')

        # Update the folder labels with the selected paths
        self.manual_text_folder_label.setText(f"Manual Text Folder: {self.manual_text_folder}")
        self.trained_text_folder_label.setText(f"Trained Text Folder: {self.trained_text_folder}")

        self.layout().insertWidget(5, self.manual_text_folder_label)
        self.layout().insertWidget(6, self.trained_text_folder_label)

    def set_logo(self):
        # Load the logo image
        logo_path = 'images//difference_FILL0_wght400_GRAD0_opsz24.png'
        copyingIcon = 'images//content_copy_FILL0_wght400_GRAD0_opsz24.png'
        pixmap = QPixmap(logo_path)

        # Create a QLabel to display the logo
        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Add the logo label to your layout
        self.layout().addWidget(logo_label)

    def compare_texts(self):
        if not self.manual_text_folder or not self.trained_text_folder:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select both folders')
            return

        # Call the process_folders function to execute the code
        manual_results, trained_results, summary_text, missing_patterns_dict, all_manual_texts, all_trained_texts = process_folders(
            self.manual_text_folder, self.trained_text_folder, self.missing_patterns_manual_text, self.missing_patterns_trained_text)

        # Display results in the respective text areas
        manual_text = '\n'.join(manual_results)
        trained_text = '\n'.join(trained_results)

        self.manual_results_text.setPlainText(manual_text)
        self.trained_results_text.setPlainText(trained_text)

        if manual_text != trained_text:
            self.manual_results_text.setStyleSheet("background-color: light red")
            self.trained_results_text.setStyleSheet("background-color: light red")
        else:
            self.manual_results_text.setStyleSheet("background-color: light green")
            self.trained_results_text.setStyleSheet("background-color: light green")

        missing_in_trained_Text, missing_in_manual_Text = comText(manual_results, trained_results)
        # Fill missing patterns in trained files text area
        missing_patterns_trained_text = ""
        missing_in_trained = missing_in_trained_Text
        if missing_in_trained:
            missing_patterns_trained_text = '\n'.join(missing_in_trained)
        self.missing_patterns_trained_text_area.setPlainText(missing_patterns_trained_text)

        # Fill missing patterns in manual files text area
        missing_patterns_manual_text = ""
        missing_in_manual = missing_in_manual_Text
        if missing_in_manual:
            missing_patterns_manual_text = '\n'.join(missing_in_manual)
        self.missing_patterns_manual_text_area.setPlainText(missing_patterns_manual_text)

        # Create a summary of file names and their counts
        manual_summary = self.create_summary(manual_results)
        trained_summary = self.create_summary(trained_results)
        summary_text = '\n'.join(summary_text)

        # Set the summary text
        self.summary_text.setPlainText(
            f"Summary of above results are:\nManual Results:\n{manual_summary}\n\nTrained Results:\n{trained_summary}\n\n{summary_text}")

        # Set the all_manual_texts and all_trained_texts in the respective text areas
        self.all_manual_texts_area.setPlainText(all_manual_texts)
        self.all_trained_texts_area.setPlainText(all_trained_texts)

    def create_summary(self, results):
        summary = ""
        current_file = None
        file_count = 0

        for line in results:
            if line.startswith("File "):
                if current_file:
                    summary += f"{current_file}, Count: {file_count}\n"
                current_file = line
                file_count = 0
            elif line.startswith("Count of Generic Patterns: "):
                file_count = int(line.split(":")[1].strip())

        if current_file:
            summary += f"{current_file}, Count: {file_count}\n"

        return summary

    def create_summary_missing_patterns(self, missing_patterns_dict):
        summary = ""
        for file_type, missing_patterns in missing_patterns_dict.items():
            summary += f"Missing patterns in {file_type} files:\n"
            for pattern in missing_patterns:
                summary += pattern + '\n'
            summary += '\n'
        return summary

    def add_copy_action(self):
        copy_action = QAction(QIcon('images//content_copy_FILL0_wght400_GRAD0_opsz24.png'), 'Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_text_from_focused_textarea)
        self.addAction(copy_action)

    def copy_text_from_focused_textarea(self):
        focus_widget = QApplication.focusWidget()
        if isinstance(focus_widget, QtWidgets.QTextEdit):
            selected_text = focus_widget.textCursor().selectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = AnonymizedTextComparison()
    ex.setWindowTitle('Anonymized Text Comparison(Testing Tool)')
    ex.setGeometry(100, 100, 800, 600)  # Increased the width and height to accommodate new text areas
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
