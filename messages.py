from PySide6.QtWidgets import QMessageBox

def send_error(text, title="Ошибка", informative="", parent=None):
    """Сообщение об ошибке пользователя или системы."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    if informative:
        msg.setInformativeText(informative)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec()

def send_forbidden(text, title="Действие запрещено", informative="У вас нет прав для этого действия.", parent=None):
    """Сообщение о запрещённом действии (нет прав)."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setInformativeText(informative)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec()

def send_warning(text, title="Предупреждение", informative="Подтвердите действие.", parent=None):
    """Предупреждение с выбором Да/Нет (удаление, изменение)."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(title)
    if informative:
        msg.setInformativeText(informative)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)
    return msg.exec()

def send_info(text, title="Информация", informative="", parent=None):
    """Уведомление об успешном действии."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle(title)
    if informative:
        msg.setInformativeText(informative)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec()


