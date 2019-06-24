const {app, BrowserWindow} = require('electron')
const {PythonShell} = require('python-shell')


//makes an instance of BrowserWindow and loads the index.html
function createWindow () {
    window = new BrowserWindow({width: 800, height: 400});
    window.loadFile('electron.html');
  
    PythonShell.run('start.py', null,(err, res) => {
        if(err) throw err
        else
        console.log("ERROR")
    
    });


}

//When the application is ready, run the createWindow() method:
app.on('ready', createWindow)


//
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })
