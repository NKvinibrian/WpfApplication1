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
#import base64
from System import Uri

#modulos Windows Form import
from System import *
from System.Windows import *
from System.Windows.Markup import *
from System.Windows.Media import *
from System.Windows.Input import *
from System.Windows.Threading import *
from System.Windows import Application, Window
from System.ComponentModel import BackgroundWorker
from System.Windows.Media.Imaging import BitmapImage
from System.Net import HttpWebRequest
from System.IO import StreamReader



class MyWindow(Window):    
    '''
    Nome: MyWindows
    Funcao: Cria a classe WPF form
    Retorna:
    Autor: Vinicius Maestrelli Wiggers 14/04/2021
    '''


    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplication1.xaml')
        self.cont = 0
        
        self.timer = DispatcherTimer()
        self.timer2 = DispatcherTimer()
        

        self.filial = sys.argv[1]
        self.segBar = 20
        self.default_msg = "" 
        
        #Entra no loop caso as configuracoes nao forem carregadas
        while not self.Load_config():
            time.sleep(10)
        
        #define o tempo de chamada da funcao
        self.timer.Interval = TimeSpan(0, 0, self.seg)          #( 0 , Minutos, Segundos ) Update
        self.timer2.Interval = TimeSpan(0, 0, 1)                #( 0 , Minutos, Segundos ) Barra 
        
        self.timer.Tick += self.Update
        self.timer2.Tick += self.Bar
        self.timer.Start()
        

    def Update(self, a, b):
            '''
            Nome: Update
            Funcao: Busca dados atravez do requests GET, Funcao chamada a cada update da form
            Retorna:
            Autor: Vinicius Maestrelli Wiggers 14/04/2021
            '''
            self.Msg.Text = ""
            self.Quantidade.Content = ""
            try:
                time.sleep(5)
                produto = request_get(uri=("http://robot.nisseilabs.com.br/aviso/loja/pedido/2AD6D5EEDAB05C29968CDAC90161CC43D7CBAB48FF625E418C9468E2AE857A07/"+sys.argv[1]))
                #produto = request_get(uri="http://127.0.0.1:8000/teste")               
                if produto['status']:
                    
                    #carrega os dados do requests
                    self.seg = int(produto['tempo'])
                    self.segBar = int(produto['tempo_fechar'])
                    self.link = produto['link_botao']
                    self.Quantidade.Content = produto['qtd_pedidos']
                    if produto['msg'] is not None:
                        self.Msg.Text = produto['msg']

                    #Mostra a form para o usuario
                    self.Show()


                    self.Bt_Close.IsEnabled = False
                    
                    #Configura e chama o timer da barra 
                    self.timer.Interval = TimeSpan(0, 0, self.seg)                    
                    self.timer2.Start()

                else:
                    self.Msg.Text = ""
                print(produto)
            except Exception as e:
                print(e)
            

    def Bar(self, a, b):
        '''
        Nome: Bar
        Funcao: Controla o time da barra e o botao fechar
        Retorna:
        Autor: Vinicius Maestrelli Wiggers 14/04/2021
        '''
        self.cont += 1
        self.Barra.Maximum = self.segBar
        self.Barra.Value = self.cont
        if self.cont >= self.segBar:
            self.cont = 0
            self.Bt_Close.IsEnabled = True
            self.timer2.Stop()
            

    def Closing_form(sender, e, a):
        '''
        Nome: Closing_form
        Funcao: Cancela o evento fechar e esconde a form
        Retorna:
        Autor: Vinicius Maestrelli Wiggers 14/04/2021
        '''
        a.Cancel = True
        if sender.Bt_Close.IsEnabled == True:
            sender.Hide()


    def Load_config(self):
        '''
        Nome: Load_config
        Funcao: Carrega a configuracao atrvez do requests ( Cor de fundo, tempo, tempo da barra e imagem-logo) 
        Retorna: True se for carregado com sucesso, False caso o servidor esteja offline ou alguma key errada
        Autor: Vinicius Maestrelli Wiggers 14/04/2021
        '''
        try:
            config = request_get(uri=("http://robot.nisseilabs.com.br/aviso/loja/pedido/2AD6D5EEDAB05C29968CDAC90161CC43D7CBAB48FF625E418C9468E2AE857A07/"+sys.argv[1]))        
            #config = request_get(uri="http://127.0.0.1:8000/teste")
            print(config)
            self.seg = int(config['tempo'])
            self.link = config['link_botao']
            self.segBar = int(config['tempo_fechar'])

            uri = Uri(os.path.dirname(os.path.abspath(__file__))+"\\Images\\Logo_Venda.png")
            self.Logo.Source = BitmapImage(uri)

            #Cor de fundo
            #color = ColorConverter.ConvertFromString(config['cor_background'])                       
            #self.Back.Fill = SolidColorBrush(color)
            #self.Sino_borda.Stroke = SolidColorBrush(color)
            #self.Sino.Foreground = SolidColorBrush(color)
            #self.Barra.BorderBrush = SolidColorBrush(color)
            #self.Barra.Foreground = SolidColorBrush(color)
            
            #Carrega imagem em base64 e salva no diretorio Images
            #with open(os.path.dirname(os.path.abspath(__file__))+"\\Images\\Logo_Venda.png", "wb") as f:                
            #    f.write(base64.b64decode(config['imagem']))
            #uri = Uri(os.path.dirname(os.path.abspath(__file__))+"\\Images\\Logo_Venda.png")
            #self.Logo.Source = BitmapImage(uri)

            return True
        except Exception as e:
            print(e)
            return False
    

    def Bt_Close_Click(self, sender, e):
        '''
        Nome: Bt_Close_Click
        Funcao: Evento botao fechar
        Retorna:
        Autor: Vinicius Maestrelli Wiggers 14/04/2021
        '''
        self.Hide()
        self.Bt_Close.IsEnabled = False
        

    def TextBox_Click(self, sender, e):
        '''
        Nome: TextBox_Click
        Funcao: Evento clicar no link
        Retorna:
        Autor: Vinicius Maestrelli Wiggers 14/04/2021
        '''
        os.system("start "+self.link)
        self.Hide()
        self.Bt_Close.IsEnabled = False                        


def run_form():
    '''
    Nome: run_form
    Funcao: Cria a main thread-ui e inicia a form
    Retorna:
    Autor: Vinicius Maestrelli Wiggers 14/04/2021
    '''
    Application().Run(MyWindow())
    time.sleep(1)


def request_get(uri):
    '''
    Nome: request_get
    Funcao: Faz a requisicao GET
    Retorna: Retorna dados em json
    Autor: Vinicius Maestrelli Wiggers 14/04/2021
    '''
    webRequest = HttpWebRequest.Create(uri)
    webRequest.Method = 'GET'
    webRequest.ContentType = 'application/json'
    webRequest.ContentLength = 0
    response = webRequest.GetResponse()
    streamReader = StreamReader(response.GetResponseStream())
    jsonData = json.loads(streamReader.ReadToEnd())
    response.Close()
    return jsonData


#valida a variavel argv
if __name__ == '__main__':
    if len(sys.argv)>2 or len(sys.argv)<2:
        print("Argumentos invalidos")
        sys.exit()
    print("Filial: "+sys.argv[1])
    run_form()
    time.sleep(5)