import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

import VirtScreen.Backend 1.0
import VirtScreen.Network 1.0

ColumnLayout {
    // virtscreen.py Network interfaces backend.
    Network {
        id: network
    }

    GroupBox {
        title: "VNC Server"
        Layout.fillWidth: true
        enabled: backend.vncState == Backend.OFF ? true : false
        ColumnLayout {
            anchors.left: parent.left
            anchors.right: parent.right
            RowLayout {
                Label { text: "Port"; Layout.fillWidth: true }
                SpinBox {
                    value: settings.vnc.port
                    from: 1
                    to: 65535
                    stepSize: 1
                    editable: true
                    onValueModified: {
                        settings.vnc.port = value;
                    }
                    textFromValue: function(value, locale) { return value; }
                }
            }
            RowLayout {
                Label { text: "Password"; Layout.fillWidth: true }
                Button {
                    text: "Delete"
                    font.capitalization: Font.MixedCase
                    highlighted: false
                    enabled: backend.vncUsePassword
                    onClicked: backend.deleteVNCPassword()
                }
                Button {
                    text: "New"
                    font.capitalization: Font.MixedCase
                    highlighted: true
                    enabled: !backend.vncUsePassword
                    onClicked: passwordDialog.open()
                }
            }
            RowLayout {
                Layout.alignment: Qt.AlignRight
                Button {
                    text: "Advanced"
                    font.capitalization: Font.MixedCase
                    onClicked: vncOptionsLoader.active = true;
                    background.opacity : 0
                    onHoveredChanged: hovered ? background.opacity = 0.4
                                               :background.opacity = 0;
                }
            }
        }
    }
    RowLayout {
        Layout.fillWidth: true
        Layout.margins: margin / 2
        Button {
            id: vncButton
            Layout.fillWidth: true
            text: vncAction.text
            highlighted: true
            enabled: vncAction.enabled
            onClicked: vncAction.onTriggered()
        }
        CheckBox {
            checked: autostart
            onToggled: {
                autostart = checked;
                if ((checked == true) && (backend.vncState == Backend.OFF) && 
                        backend.virtScreenCreated) {
                    startVNC();
                }
            }
        }
        Label { text: "Auto"; }
    }
    GroupBox {
        title: "Available IP addresses"
        Layout.fillWidth: true
        Layout.fillHeight: true
        implicitHeight: 145
        ListView {
            id: ipListView
            anchors.fill: parent
            clip: true
            ScrollBar.vertical: ScrollBar {
                parent: ipListView.parent
                anchors.top: ipListView.top
                anchors.right: ipListView.right
                anchors.bottom: ipListView.bottom
                policy: ScrollBar.AlwaysOn
            }
            model: network.ipAddresses
            delegate: TextEdit {
                text: modelData
                readOnly: true
                selectByMouse: true
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 14
            }
        }
    }
    RowLayout {
        // Empty layout
        Layout.fillHeight: true
    }
}