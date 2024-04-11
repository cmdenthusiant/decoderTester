import subprocess
import threading
import requests
import tkinter
from tkinter import ttk
import time
import sys
import os

window = tkinter.Tk()
class menu:
    def __init__(self):
        
        window.title('decrypter Tester')
        window.minsize(800,300)

        self.decrypterTester = DecrypterTester()

        if self.decrypterTester.hasLocalSamples():
            self.decrypterTester.getAllSamples()
            self.initMenu()
        else:
            th = threading.Thread(target=self.decrypterTester.downloadOnlineSamples)
            uth = threading.Thread(target=self.updateSampleProcess)
            th.daemon = True
            uth.daemon = True
            th.start()
            uth.start()

        window.mainloop()
    def initMenu(self):
        self.mainFrame = tkinter.Frame(window)
        self.canvas = tkinter.Canvas(self.mainFrame)
        self.containerFrame = tkinter.Frame(self.canvas, width = 800, height = 600)
        window.bind_all("<Button>", lambda event: event.widget.focus_set())

        self.mainFrame.pack(fill='both',expand=1)
        self.canvas.pack(side="left",fill="both",expand=1)
        self.scrollBar = tkinter.Scrollbar(self.mainFrame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.TitleFrame = tkinter.Frame(self.containerFrame,width=790, height=120)

        self.infoLabel = tkinter.Label(self.containerFrame, text="In order to receive sample's Updates,\nSimply delete the '.sample' folder,\nand restart this app")
        self.infoLabel.place(x=530,y=10)

        self.bugInfoLabel = tkinter.Label(self.containerFrame, text="Bug Occurred?\nCheck if 'testerPreInput.txt' \nand Input/Output File are configured Correctly.")

        self.decrypterFilePathLabel = tkinter.Label(self.containerFrame, text="decrypter File:")
        self.decrypterFilePathInput = tkinter.Entry(self.containerFrame, width=20)
        self.inputFilePathLabel = tkinter.Label(self.containerFrame, text="Input File:")
        self.inputFilePathInput = tkinter.Entry(self.containerFrame, width=20)
        self.outputFilePathLabel = tkinter.Label(self.containerFrame, text="Output File:")
        self.outputFilePathInput = tkinter.Entry(self.containerFrame, width=20)

        self.decrypterFilePathInput.insert(tkinter.END, 'main.py')
        self.inputFilePathInput.insert(tkinter.END, 'Secret.txt')
        self.outputFilePathInput.insert(tkinter.END, 'Message.txt')

        self.startTestBtn = tkinter.Button(self.containerFrame,text='Start Test', width=30 ,command=self.startTest)
        

        self.TitleFrame.pack(fill='x',expand=1)
        
        self.decrypterFilePathLabel.place(x=10, y=10)
        self.decrypterFilePathInput.place(x=110, y=10)

        self.inputFilePathLabel.place(x=10, y=30)
        self.inputFilePathInput.place(x=110, y=30)

        self.outputFilePathLabel.place(x=10, y=50)
        self.outputFilePathInput.place(x=110, y=50)

        self.startTestBtn.place(x=10, y=80)

        self.difficultyFrameTitle = {
            'e':"[Easy] Long Sentences",
            'm':"[Medium] Short Sentences",
            'h':"[Hard] Extreme Cases"
        }

        self.easyCaseFrame = ToggledFrame(self.containerFrame, self.canvas, self.difficultyFrameTitle['e'], relief="raised", borderwidth=2)
        self.mediumCaseFrame = ToggledFrame(self.containerFrame, self.canvas, self.difficultyFrameTitle['m'], relief="raised", borderwidth=2)
        self.hardCaseFrame = ToggledFrame(self.containerFrame, self.canvas, self.difficultyFrameTitle['h'], relief="raised", borderwidth=2)
        self.caseFrames = {'e':self.easyCaseFrame, 'm':self.mediumCaseFrame, 'h':self.hardCaseFrame}
        self.easyCaseFrame.pack(padx=10,pady=10,fill='x')
        self.mediumCaseFrame.pack(padx=10,pady=10,fill='x')
        self.hardCaseFrame.pack(padx=10,pady=10,fill='x')

        self.allCaseFrame = []

        easyTestLabel = tkinter.Label(self.easyCaseFrame.containerFrame, text="decrypter Not Tested")
        mediumTestLabel = tkinter.Label(self.mediumCaseFrame.containerFrame, text="decrypter Not Tested")
        hardTestLabel = tkinter.Label(self.hardCaseFrame.containerFrame, text="decrypter Not Tested")

        self.testLabels = [easyTestLabel, mediumTestLabel, hardTestLabel]
        easyTestLabel.pack()
        mediumTestLabel.pack()
        hardTestLabel.pack()

        self.canvas.configure(yscrollcommand=self.scrollBar.set)

        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        def _shouldScroll():
            currFocus = self.canvas.focus_get() 
            return not (hasattr(currFocus, 'needScroll') and currFocus.needScroll == True)
        def _onMousewheel(event):
            if not _shouldScroll(): return
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _onWheelButton(isUp):
            if not _shouldScroll(): return
            self.canvas.yview_scroll((-1 if isUp else 1),'units')
        self.canvas.bind_all('<MouseWheel>', _onMousewheel)
        self.canvas.bind_all('<Button-4>', lambda e: _onWheelButton(True))
        self.canvas.bind_all('<Button-5>', lambda e: _onWheelButton(False))
        self.canvas.create_window((0,0), window=self.containerFrame, anchor='w')
    def startTest(self):
        self.startTestBtn.configure(state='disabled')
        for label in self.testLabels: label.forget()
        decrypterFile = self.decrypterFilePathInput.get()
        inputFile = self.inputFilePathInput.get()
        outputFile = self.outputFilePathInput.get()

        tth = threading.Thread(target=self.decrypterTester.startdecrypt, args=(decrypterFile,inputFile,outputFile,))
        uth = threading.Thread(target=self.updateTestProcess)
        tth.daemon = True
        uth.daemon = True
        tth.start()
        uth.start()
    def updateSampleProcess(self):
        loopAnimation = ['/','-','\\','|']
        loopAnimationIdx = 0
        waitDownloadLabel = tkinter.Label(window, text="Downloading Samples...")
        waitDownloadLabel.place(relx=.5,rely=.5, anchor='center')
        time.sleep(0.9)
        while self.decrypterTester.downloading:
            time.sleep(0.1)
            waitDownloadLabel.configure(text="Downloading Samples... "+loopAnimation[loopAnimationIdx]+" "+str(self.decrypterTester.downloadedNum))
            loopAnimationIdx += 1
            if loopAnimationIdx == 4:
                loopAnimationIdx = 0
        
        waitDownloadLabel.forget()
        self.initMenu()

    def updateTestProcess(self):
        inputFile = self.inputFilePathInput.get()
        outputFile = self.outputFilePathInput.get()
        for frame in self.allCaseFrame:
            frame.forget()
        self.allCaseFrame.clear()
        
        for diff in self.caseFrames:
            self.caseFrames[diff].titleLabel.configure(fg='#000000', text=self.difficultyFrameTitle[diff])


        time.sleep(0.5) #wait for setup
        loopAnimation = ['/','-','\\','|']
        loopAnimationIdx = 0
        totalCaseNum = str(len(self.decrypterTester.samples['e']) + len(self.decrypterTester.samples['m']) + len(self.decrypterTester.samples['h']))
        prevTestedNum = 0
        waitedCnt = 0
        while self.decrypterTester.currentDiff:
            time.sleep(0.1)
            self.decrypterTester.currentDiff
            self.startTestBtn.configure(text="Testing... "+"("+str(self.decrypterTester.testedNum)+"/"+totalCaseNum+") "+loopAnimation[loopAnimationIdx])

            if prevTestedNum == self.decrypterTester.testedNum:
                waitedCnt += 1
                if waitedCnt >= 50: #5 seconds
                    self.bugInfoLabel.place(x=300,y=70)
            else:
                self.bugInfoLabel.place_forget()
                waitedCnt = 0
                prevTestedNum = self.decrypterTester.testedNum

            loopAnimationIdx += 1
            if loopAnimationIdx == 4:
                loopAnimationIdx = 0
        
        self.bugInfoLabel.place_forget()
        self.startTestBtn.configure(state='active', text="Start Test")

        accuracyLevelsToDisc = [["#FFAA1D","Perfect"],["#29B532","Good"],["#BF7C00","Acceptable"],["#FA2C2C","Bad"]]

        for diff in self.caseFrames:
            results = self.decrypterTester.results[diff]
            areaSize = 10 if diff == 'e' else 5
            correctCaseNum = 0
            for i in range(len(results)):
                res = results[i][0]
                if res == True:
                    correctCaseNum += 1

                caseFrame = ToggledFrame(self.caseFrames[diff].containerFrame, self.canvas, "["+str(i+1)+"] Decrypt "+("Successed" if res else "Failed"),
                                         ("#29B532" if res else "#FA2C2C"))
                self.allCaseFrame.append(caseFrame)

                sampleLabel = tkinter.Label(caseFrame.containerFrame,text="Sample:")
                sampleLabel.pack(anchor='w')

                sampleText = ScrollableText(caseFrame.containerFrame, self.decrypterTester.samples[diff][i][0], areaSize)
                sampleText.pack(fill='x')

                tkinter.Label(caseFrame.containerFrame).pack() #skip line
                
                decrypterInputLabel = tkinter.Label(caseFrame.containerFrame, text="Decrypter Input("+inputFile+"):")
                decrypterInputLabel.pack(anchor='w')

                decrypterInputText = ScrollableText(caseFrame.containerFrame, self.decrypterTester.samples[diff][i][1], areaSize)
                decrypterInputText.pack(fill='x')

                tkinter.Label(caseFrame.containerFrame).pack() #skip line

                decrypterOutputLabel = tkinter.Label(caseFrame.containerFrame, text="Your Decrypter Output("+("Decrypter printed logs" if results[i][2] else outputFile)+"):")
                decrypterOutputLabel.pack(anchor='w')

                decrypterOutputText = ScrollableText(caseFrame.containerFrame, results[i][1], areaSize)
                decrypterOutputText.pack(fill='x')

                caseFrame.pack(fill='x')

            accuracy = correctCaseNum / len(results)

            totalAccuracyLevels = len(self.decrypterTester.accuracyLevel[diff])
            for i in range(totalAccuracyLevels):
                if accuracy >= self.decrypterTester.accuracyLevel[diff][i]:
                    color = accuracyLevelsToDisc[i][0]
                    discribe = accuracyLevelsToDisc[i][1]
                    self.caseFrames[diff].titleLabel.configure(fg=color, text=self.difficultyFrameTitle[diff]
                                                               +" Accuracy: "+str(round(accuracy*100))+"%, "+discribe)
                    break
                    

class ToggledFrame(tkinter.Frame):
    def __init__(self, root, canvas, text, textColor="#000000", *args, **options):
        super().__init__(root, *args, **options)
        self.root = root
        self.canvas = canvas

        self.titleFrame = tkinter.Frame(self)
        self.titleFrame.pack(fill='x', expand=1)

        self.titleLabel = tkinter.Label(self.titleFrame, text=text, fg=textColor)
        self.titleLabel.pack(side='left', fill='x', expand=1)

        self.expandLabel = tkinter.Label(self.titleFrame, text='+',width=5)
        self.expandLabel.pack(side='right')

        self.containerFrame = tkinter.Frame(self, relief="sunken",borderwidth=1)
        tkinter.Frame(self.containerFrame, height=10).pack()
        self.expanded = False

        self.titleLabel.bind('<Button-1>', self.toggle)
        self.expandLabel.bind('<Button-1>', self.toggle)
    
    def toggle(self,event):
        self.expanded = not self.expanded

        if self.expanded:
            self.containerFrame.pack(fill='x', expand=1)
            self.expandLabel.configure(text='-')
        else:
            self.containerFrame.forget()
            self.expandLabel.configure(text='+')
        window.update()
        self.canvas.event_generate('<Configure>')


class ScrollableText(tkinter.Frame):
    def __init__(self, root, text,areaSize, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root

        self.txt = tkinter.Text(self,height=areaSize)
        self.txt.insert(tkinter.END, text)
        self.txt.configure(state='disabled')
        self.txt.needScroll = True
        self.txt.pack(side='left',fill='both')

        scrollbar = ttk.Scrollbar(self, command=self.txt.yview)
        scrollbar.pack(side='right',fill='y')
        self.txt['yscrollcommand'] = scrollbar.set


class DecrypterTester:
    def __init__(self) -> None:
        self.samples = {
            'e':[],
            'm':[],
            'h':[]
            }
        self.currentDiff = None
        self.currentSample = None
        self.testedNum = 0
        self.downloading = False
        self.downloadedNum = 0
        self.results = {
            'e':[],
            'm':[],
            'h':[]
        }
        self.accuracyLevel = {
            'e':[1, .8, .6,0],
            'm':[1,.75, .4,0],
            'h':[.8, .5, .25,0]
        }
    def hasLocalSamples(self):
        return os.path.isdir('.samples')
    def getAllSamples(self):
        self.getSamples('e')
        self.getSamples('m')
        self.getSamples('h')

    def downloadOnlineSamples(self):
        self.downloading = True
        os.mkdir('.samples')
        os.mkdir('.samples/e')
        os.mkdir('.samples/m')
        os.mkdir('.samples/h')
        self.getOnlineSamples('e')
        self.getOnlineSamples('m')
        self.getOnlineSamples('h')
        self.downloading = False

    def getSamples(self,difficluty):
        i=1
        while True:
            fileName = str(i)+".txt"
            file1Name = str(i)+"e.txt"
            if not os.path.isfile('.samples/'+difficluty+'/'+fileName) or not os.path.isfile('.samples/'+difficluty+'/'+file1Name):
                break

            file = open('.samples/'+difficluty+'/'+fileName,'r',encoding='utf-8')
            file1 = open('.samples/'+difficluty+'/'+file1Name,'r',encoding='utf-8')
            sample = file.read()
            sample1 = file1.read()
            file.close()
            file1.close()

            self.samples[difficluty].append([sample,sample1])
            i += 1
    def getOnlineSamples(self, difficulty):
        i=1
        while True:
            fileName = str(i)+".txt"
            file1Name = str(i)+"e.txt"
            req = requests.get("https://raw.githubusercontent.com/cmdenthusiant/decoderTester/main/samples/"+difficulty+"/"+fileName)
            if req.status_code != requests.codes.ok:
                break
            req1 = requests.get("https://raw.githubusercontent.com/cmdenthusiant/decoderTester/main/samples/"+difficulty+"/"+file1Name)
            if req1.status_code != requests.codes.ok:
                break
            sample = req.content
            sample1 = req1.content
            self.samples[difficulty].append([sample.decode(), sample1.decode()])

            file = open('.samples/'+difficulty+'/'+fileName,'wb')
            file1 = open('.samples/'+difficulty+'/'+file1Name,'wb')

            file.write(sample)
            file1.write(sample1)

            file.close()
            file1.close()

            i += 1
            self.downloadedNum += 1
    def startdecrypt(self, decrypterFilePath, inputFilePath, outputFilePath):
        self.testedNum = 0

        preInputFile = open('testerPreInput.txt','rb')
        preInput = preInputFile.readlines()
        preInputFile.close()

        for difficulty in self.samples:
            self.currentDiff = difficulty
            self.results[difficulty].clear()
            n = len(self.samples[difficulty])
            for i in range(n):
                self.currentSample = i

                messageFile = open(outputFilePath,'w',encoding='utf-8')
                messageFile.write("")
                messageFile.close()

                secretFile = open(inputFilePath, 'w',encoding='utf-8')
                secretFile.write(self.samples[difficulty][i][1])
                secretFile.close()

                procOutput = open('decrypterOutput.txt','w')
                procOutput.write("")
                procOutput.close()

                procOutput = open('decrypterOutput.txt','w')

                proc = subprocess.Popen([sys.executable, decrypterFilePath], stdin=subprocess.PIPE, stdout=procOutput)
                for preIn in preInput:
                    if proc.stdin.closed: break
                    proc.communicate((preIn[:-1] if preIn[-1:] == b'\n' else preIn))

                proc.terminate()

                procOutput.close()
                
                messageFile = open(outputFilePath,'r',encoding='utf-8')
                message = messageFile.read()

                procOutput = open('decrypterOutput.txt','r',encoding='utf-8')
                output = procOutput.read()

                answer = ""
                correct = False
                useProcOutput = False

                if message:
                    answer = message
                    correct = message in self.samples[difficulty][i][0] or self.samples[difficulty][i][0] in message
                elif output:
                    answer = output
                    correct = self.samples[difficulty][i][0] in output
                    useProcOutput = True

                self.results[difficulty].append([correct, answer,useProcOutput])
                messageFile.close()
                procOutput.close()
                self.testedNum += 1
            time.sleep(0.5)
        self.currentDiff = None
        self.currentSample = None


menu()