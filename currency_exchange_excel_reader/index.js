const { app, BrowserWindow, Menu } = require("electron");

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 1000,
    title: "Kurs Walut",
    icon: "./static/money.png",
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile("index.html");
};

const menuTemplate = [
  {
    label: "Narzedzia",
    submenu: [
      { role: "reload" },
      { role: "togglefullscreen" },
      { role: "zoomIn" },
      { role: "zoomOut" },
      { type: "separator" },
      { role: "toggleDevTools" },
      {
        role: "help",
        click() {
          openHelpWindow();
        },
      },
    ],
  },
];

let helpWindow;

const openHelpWindow = () => {
  if (helpWindow) {
    helpWindow.focus();
    return;
  }

  helpWindow = new BrowserWindow({
    height: 600,
    resizable: true,
    width: 1200,
    title: "Pomoc",
    icon: "./static/money.png",
  });

  helpWindow.setMenu(null);

  helpWindow.loadFile("./help.html");

  helpWindow.on("closed", () => {
    helpWindow = null;
  });
};

const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);
app.commandLine.appendSwitch("ignore-certificate-errors");
app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
