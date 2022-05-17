# 인터페이스 주요 기능을 위한 모듈
import tkinter as tk
from tkinter import *
from tkinter import filedialog       # 파일 대화창에서 파일 불러오기
from keras.models import load_model  # 모델 로드
import librosa                       # 음성 인식을 위한 라이브러리
import numpy as np                   # 모델에 넣을 수 있도록 음성 추출을 위한 모듈
import pygame                        # 인터페이스내에서 음성 파일이 재생될 수 있도록 함
from scipy.io import wavfile         # specgram 그래프 파라미터를 가져오기 위해 필요한 모듈
import soundfile                     # 파이썬에서 읽을 수 없는 wav 파일을 읽을 수 있도록 변환시켜주는 모듈
from tkinter import messagebox       # 그래프 저장시 성공 메시지 출력을 위한 모듈
from tkinter.filedialog import asksaveasfile # 그래프를 저장할 수 있도록 경로와 파일명을 지정하는 모듈

# 그래프를 그리기 위한 모듈
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # tk 인터페이스 내에 그래프를 넣을 수 있도록 함
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import librosa.display
sns.set_style("darkgrid")

class main_interface:
    def __init__(self, root):
        # tk 인터페이스 기본 설정
        self.root = root
        self.root.attributes('-topmost',True) # # tk 창이 화면 제일 위로 오도록함
        self.root.title("Sound Classification GUI")
        self.root.geometry('1000x1000+10+10')
        self.root.configure(background='#DFE6E6')
        self.root.resizable(False, False)

        # 모델 불러오기 
        self.model = load_model("base_model.h5")
        
        # 제목 
        self.heading = Label(self.root, text="Classifying the sounds of birds, cats, and dogs", pady=20, font=('Arial',20,'bold'))
        self.heading.configure(background='#DFE6E6', foreground='#364156')
        self.heading.pack(pady=10, padx=10)
        
        pygame.mixer.init() # mixer 모듈 초기화
        self.main_buttons() # main_buttons 함수 호출
        
        # 그래프가 그려질 빈 그래프 생성
        self.f = Figure(figsize=(8,7), dpi=100, constrained_layout=True)  # 그래프가 그려질 창을 생성
        self.a1 = self.f.add_subplot(311)                   # 창에 빈 그래프를 생성 - a1
        self.a2 = self.f.add_subplot(312)                   # 창에 빈 그래프를 생성 - a2
        self.a3 = self.f.add_subplot(313)
        self.canvas = FigureCanvasTkAgg(self.f, self.root)  # tk 안에 그려질 영역 생성 (영역 안에 창을 넣기)
        self.canvas.get_tk_widget().place(x=100, y=200)        
        
        # tkinter 창을 닫으면 음악이 재생되지 않도록 함
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def main_buttons(self):
        # 파일 업로드 버튼
        self.upload_button = Button(self.root, text='Upload', command=self.upload_audio, width=15, height=1)
        self.upload_button.configure(background='#364156', foreground='white', font=('Arial',12,'bold'))
        self.upload_button.place(x=80, y=120)
        
        # 음성 파일 재생 버튼 (시각화, 모델 예측 결과 반환)
        self.play_button = Button(self.root, text='Play', command=self.play, width=15, height=1)
        self.play_button.configure(background='#92B1B6', foreground='white', font=('Arial',12,'bold'))
        self.play_button.place(x=310, y=120)
        
        # 음성 일시정지 버튼
        self.pause_button = Button(self.root, text='Pause', command=self.pause, width=15, height=1)
        self.pause_button.configure(background='#dce2e8', font=('Arial',12,'bold'))
        self.pause_button.place(x=540, y=120)
        
        # 음성 파일 정지 버튼
        self.stop_button = Button(self.root, text='Stop', command=self.stop, width=15, height=1)
        self.stop_button.configure(background='#dce2e8', font=('Arial',12,'bold'))
        self.stop_button.place(x=770, y=120)
            
    def upload_audio(self):
        try:    
            path = filedialog.askopenfilename() # 대화상자를 만들고 파일을 선택할 수 있도록 함, 파일 경로가 변수에 담김 
            if path != '':                      # 새로운 경로가 변수에 들어왔다면
                self.file_path = path           # file_path 변수에 경로를 담기
                self.load_audio()
                self.destroy()                  # destroy 함수 호출
                self.cnt_play_event = True
                self.save_button.place_forget() 
        except:
            pass
        
    def load_audio(self):
        try:
            pygame.mixer.music.load(self.file_path)
        except:
            data, samplerate = soundfile.read(self.file_path)
            soundfile.write(self.file_path, data, samplerate, subtype='PCM_16') # wav 파일을 읽을 수 있도록 변환
            pygame.mixer.music.load(self.file_path)
            
    def destroy(self):
        try:
            self.label.destroy()    # 모델 예측 결과 출력 초기화
            self.a1.clear()         # 그래프 초기화
            self.a2.clear()
            self.a3.clear()
            self.spec_colorbar.remove()  # colorbar 초기화
            self.mfccs_colorbar.remove()
            self.canvas.draw_idle()      # 없을 시 새로운 file_path 경로가 들어왔을 때 그래프 초기화가 되지 않는다.
        except:
            pass
                
    def play(self):
        try:
            pygame.mixer.music.play() # 로드한 오디오 파일 재생
        
            # file_path에 그려지는 그래프와 모델 분류는 한번만 하고 유지되도록 함
            if self.cnt_play_event:
                try:
                    self.classify()       # classify 함수 호출
                    self.set_plot()       # set_plot 함수 호출

                    # 그래프 파일 저장 버튼
                    self.save_button = Button(self.root, text='Save Graph', command=self.save_graph, width=15, height=1)
                    self.save_button.configure(background='#E6DFDF', font=('Arial',12,'bold'))
                    self.save_button.place(x=770, y=930)
                except:
                    pass
                finally:
                    self.cnt_play_event = False # play를 누를 때마다 그래프와 예측 결과가 텍스트가 새로 나타나지 않도록 함(겹치지 않게)
        except:
            pass
      
    def pause(self):
        if pygame.mixer.music.get_busy(): # 음악이 재생 중인지 확인
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
                
    def stop(self):
        try:
            pygame.mixer.music.stop() # 재생중인 오디오 파일을 정지
        except:
            pass
       
    
    # 샘플 파일을 집어넣으면 음성의 특징을 추출하는 함수(불러온 모델에 넣어 예측할 수 있도록 변형)
    def extract_features(self):
        self.sample, self.sr = librosa.load(self.file_path) # 불러온 오디오 파일의 진폭을 담기
        extracted_features = np.empty((0, 61, ))            # 61개의 값을 받을 비어있는 리스트 생성
        zero_cross_feat = librosa.feature.zero_crossing_rate(self.sample).mean()     
        self.mfccs = librosa.feature.mfcc(y=self.sample, sr=self.sr, n_mfcc=60) 
        mfccsscaled = np.mean(self.mfccs.T, axis=0) 
        mfccsscaled = np.append(mfccsscaled, zero_cross_feat)
        mfccsscaled = mfccsscaled.reshape(1, 61, )
        self.test_sample = np.vstack((extracted_features, mfccsscaled))
    
    # 모델 예측
    def classify(self):
        self.extract_features()  # extract_features 함수 호출
        pred = self.model.predict(self.test_sample.reshape(1, 61,))  
        answer = np.argmax(pred)
        result_pred = str(pred[0][answer]*100)[:6]
        if answer == 0:
            self.sign='Bird : ' + result_pred + '%' # 소수점 셋째 자리까지 나타내어 퍼센트로 출력
        elif answer == 1:
            self.sign='Cat : ' + result_pred + '%' 
        else:
            self.sign='Dog : ' + result_pred + '%' 
            
        # 모델 예측 결과 출력    
        self.label = Label(self.root, background='#DFE6E6', font=('Arial', 20, 'bold'))
        self.label.configure(foreground='#364156', text=self.sign)
        self.label.pack(side="bottom", pady=50)
    
    # 그래프 그리기
    def set_plot(self):
        # 진폭 plot 그리기
        time = np.linspace(0, len(self.sample)/self.sr, len(self.sample)) # x축 범위 지정
        self.a1.plot(time, self.sample)                    # 불러온 파일의 진폭을 그래프로 표현
        self.split_index = self.file_path.rfind('/') + 1   # 그래프 제목에 파일명을 넣기 위함
        self.a1.set_title('\''+ self.file_path[self.split_index:] + '\' Audio Graph') # 그래프 제목
        self.a1.set_xlabel("Time [s]")
        self.a1.set_ylabel("Amplitude")

        # specgram 그리기
        sf, sd = wavfile.read(self.file_path)
        try:
            pxx,  freq, t, cax = self.a2.specgram(sd, Fs=sf)
            self.spec_colorbar = self.f.colorbar(cax, format="%+2.f dB", ax=self.a2)
            self.a2.set_xlabel("Time [s]")
            self.a2.set_ylabel("Frequency")
            self.a2.grid(False)
        except:
            pxx,  freq, t, cax = self.a2.specgram(sd[:,0], Fs=sf)
            self.spec_colorbar = self.f.colorbar(cax, format="%+2.f dB", ax=self.a2)
            self.a2.set_xlabel("Time [s]")
            self.a2.set_ylabel("Frequency")
            self.a2.grid(False)
            
        # MFCC 그리기
        mfccs_graph = librosa.display.specshow(self.mfccs, sr=self.sr, x_axis='time', ax=self.a3)
        self.a3.set_ylabel("MFCC coefficients")
        self.mfccs_colorbar = self.f.colorbar(mfccs_graph, ax=self.a3)
       
        self.canvas.draw()
    
    # 그래프를 저장하는 함수
    def save_graph(self):
        try:
            files = [('PNG', '.png'), ('JPEG', '.jpg'), ("All Files", ".*")]  # 저장할 수 있는 파일 형식 목록
            save_file = filedialog.asksaveasfilename(initialdir="/", 
                                                     title="Select Folder", 
                                                     filetypes=files,
                                                     defaultextension='.png')
            if save_file:
                self.f.savefig(save_file) 
                messagebox.showinfo("Success!", "Save pictures successfully") # 파일이 저장될 때만 알림창이 나타나도록 함
        except:
            pass
        
    # tkinter 창을 닫으면 실행되는 함수, 창을 닫으면 재생중인 음악이 정지
    def on_closing(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()
        
# class 실행 함수
def main():
    root = tk.Tk()
    main_interface(root)
    root.mainloop()