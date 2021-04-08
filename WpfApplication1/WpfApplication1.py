import clr

#dll import
clr.AddReferenceToFileAndPath("IronPython.Wpf.dll")
clr.AddReferenceToFileAndPath("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath("wpf")
clr.AddReferenceToFileAndPath("json")
clr.AddReferenceToFileAndPath("struct")
clr.AddReferenceToFileAndPath("os")
clr.AddReferenceToFileAndPath("ntpath")
clr.AddReferenceToFileAndPath("stat")
clr.AddReferenceToFileAndPath("genericpath")
clr.AddReferenceToFileAndPath("warnings")
clr.AddReferenceToFileAndPath("linecache")
clr.AddReferenceToFileAndPath("types")
clr.AddReferenceToFileAndPath("UserDict")
clr.AddReferenceToFileAndPath("_abcoll")
clr.AddReferenceToFileAndPath("abc")
clr.AddReferenceToFileAndPath("_weakrefset")

#python import
import wpf
import time
import sys
import json
import os

#modulos form import
from System import *
from System.Windows import *
from System.Windows.Markup import *
from System.Windows.Media import *
from System.Windows.Input import *
from System.Windows.Threading import *
from System.Windows import Application, Window
from System.ComponentModel import BackgroundWorker

from System.Net import HttpWebRequest
from System.IO import StreamReader



#Cria o wpf(form) do windows
class MyWindow(Window):    
    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplication1.xaml')
        self.cont = 0
        self.timer = DispatcherTimer()
        self.timer2 = DispatcherTimer()
        self.filial = sys.argv[1]
        self.segBar = 20
        self.default_msg = "" 
        while not self.Load_config():
            time.sleep(10)
        self.timer.Interval = TimeSpan(0, 0, self.seg)          #( 0 , Minutos, Segundos ) update
        self.timer2.Interval = TimeSpan(0, 0, 1)                #( 0 , Minutos, Segundos ) barra 
        self.timer.Tick += self.Update
        self.timer2.Tick += self.Bar
        self.timer.Start()
        

    #Evento chamado a cada update da form
    def Update(self, a, b):
            self.Msg.Text = ""
            self.Quantidade.Content = ""
            try:
                time.sleep(5)
                produto = request_get(uri=("http://robot.nisseilabs.com.br/aviso/loja/pedido/2AD6D5EEDAB05C29968CDAC90161CC43D7CBAB48FF625E418C9468E2AE857A07/"+sys.argv[1]))
                #produto = request_get(uri="http://127.0.0.1:8000/teste")
                if produto['status']:
                    self.seg = int(produto['tempo'])
                    self.segBar = int(produto['tempo_fechar'])
                    self.link = produto['link_botao']                    
                    self.Quantidade.Content = produto['qtd_pedidos']
                    if produto['msg'] is not None:
                        self.Msg.Text = produto['msg'].replace(",",'\n')
                    self.Show()
                    self.Bt_Close.IsEnabled = False
                    self.timer.Interval = TimeSpan(0, 0, self.seg)
                    self.timer2.Start()
                else:
                    self.Msg.Text = ""
                print(produto)
            except Exception as e:
                print(e)
            

    #Controlador da Barra e do Timer
    def Bar(self, a, b):
        self.cont += 1
        self.Barra.Maximum = self.segBar
        self.Barra.Value = self.cont
        if self.cont >= self.segBar:
            self.cont = 0
            self.Bt_Close.IsEnabled = True
            self.timer2.Stop()
            

    #Evento chamado quando o usuario clica no botao close da form
    def Closing_form(sender, e, a):
        a.Cancel = True
        if sender.Bt_Close.IsEnabled == True:
            sender.Hide()

    #Carrega a config atravez de requests
    def Load_config(self):
        try:
            config = request_get(uri=("http://robot.nisseilabs.com.br/aviso/loja/pedido/2AD6D5EEDAB05C29968CDAC90161CC43D7CBAB48FF625E418C9468E2AE857A07/"+sys.argv[1]))        
            #config = request_get(uri="http://127.0.0.1:8000/teste")
            print(config)
            self.seg = int(config['tempo'])
            self.link = config['link_botao']
            self.segBar = int(config['tempo_fechar'])
            return True
        except Exception as e:
            print(e)
            return False
    
    #botao fechar
    def Bt_Close_Click(self, sender, e):
        self.Hide()
        self.Bt_Close.IsEnabled = False
        
    def TextBox_Click(self, sender, e):
        os.system("start "+self.link)
        pass
                        


#inicializa a thread form 
def run_form():
    Application().Run(MyWindow())
    time.sleep(1)


#funcao para fazer um request get
def request_get(uri):
    webRequest = HttpWebRequest.Create(uri)
    webRequest.Method = 'GET'
    webRequest.ContentType = 'application/json'
    webRequest.ContentLength = 0
    response = webRequest.GetResponse()
    streamReader = StreamReader(response.GetResponseStream())
    jsonData = json.loads(streamReader.ReadToEnd())
    response.Close()
    return jsonData

if __name__ == '__main__':
    if len(sys.argv)>2 or len(sys.argv)<2:
        print("Argumentos invalidos")
        sys.exit()
    print("Filial: "+sys.argv[1])
    run_form()
    time.sleep(5)