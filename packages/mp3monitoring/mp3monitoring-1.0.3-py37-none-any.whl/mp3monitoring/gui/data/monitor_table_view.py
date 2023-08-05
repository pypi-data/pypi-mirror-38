from PyQt5.QtWidgets import QMenu


def context_menu(table_view, position):
    menu = QMenu()
    remove_selected_item = menu.addAction('Delete monitoring job')
    action = menu.exec(table_view.mapToGlobal(position))
    if action == remove_selected_item:
        rows = sorted(set(index.row() for index in table_view.selectedIndexes()))
        table_view.model().removeRows(min(rows), max(rows))
