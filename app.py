from hive import app
import os, subprocess, sys
if __name__=="__main__":
    # p = subprocess.Popen(['powershell.exe', os.path.join(app.root_path,'find_ip.ps1')], stdout=subprocess.PIPE)
    # a = str(p.stdout.read()).split('\\')[0].split('\'')[1]
    # a=str(p.stdout.read())
    # print(p, 'printp')
    # print(a, 'so')
    app.run(debug=True, host='192.168.1.111', port=5001)
    # app.run(debug=True)