import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: addProgramDialog
    title: "Add New Program"
    modal: true
    width: 400
    height: 250
    standardButtons: Dialog.Ok | Dialog.Cancel

    signal addProgram(string name, string path, string iconUrl)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        Label { text: "Name:" }
        TextField {
            id: nameField
            Layout.fillWidth: true
        }

        RowLayout { // Используем RowLayout для Path и Browse Button
            Layout.fillWidth: true
            Label { text: "Path:"; Layout.alignment: Qt.AlignVCenter }
            TextField {
                id: pathField
                Layout.fillWidth: true
            }
            Button {
                text: "Browse"
                onClicked: fileDialog.open()
                Layout.alignment: Qt.AlignVCenter
            }
        }

        Label { text: "Icon URL:" }
        TextField {
            id: iconUrlField
            Layout.fillWidth: true
        }
    }

    onAccepted: {
        addProgram(nameField.text, pathField.text, iconUrlField.text);
        nameField.text = "";
        pathField.text = "";
        iconUrlField.text = "";
        addProgramDialog.close();
    }

    onRejected: {
        nameField.text = "";
        pathField.text = "";
        iconUrlField.text = "";
        addProgramDialog.close();
    }

    onAccepted: {
        addProgram(nameField.text, pathField.text, iconUrlField.text);
        nameField.text = "";
        pathField.text = "";
        iconUrlField.text = "";
        addProgramDialog.close();
    }

    onRejected: {
        nameField.text = "";
        pathField.text = "";
        iconUrlField.text = "";
        addProgramDialog.close();
    }
    FileDialog {
        id: fileDialog
        title: "Choose Program"
        nameFilters: ["Executable files (*.exe *.app)"] // Фильтр для исполняемых файлов
        onAccepted: {
            pathField.text = fileDialog.fileUrl.toString().replace("file:///", ""); // Получаем путь и убираем "file:///"
            if (nameField.text === "") {
                // Автоматически заполняем имя, если оно пустое
                let fileName = fileDialog.fileUrl.toString().split("/").pop();
                nameField.text = fileName.substring(0, fileName.lastIndexOf(".")); // Убираем расширение файла
            }
        }
        onRejected: {
            console.log("Canceled");
        }
    }
}
