import executor
import json
import librosa
import pyaudio
import wave
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical


# ghi âm tạm thời vào 1 file
def ghi_am(filename, thoi_gian_ghi, tan_so_mau, kich_thuoc_bo_dem, thiet_bi_mau):
    # Khởi tạo PyAudio
    p = pyaudio.PyAudio()

    # Cài đặt các thông số ghi âm
    thoi_gian_ghi = thoi_gian_ghi  # Thời gian ghi âm (giây)
    tan_so_mau = tan_so_mau  # Tần số mẫu (số mẫu/giây)
    kich_thuoc_bo_dem = kich_thuoc_bo_dem  # Kích thước bộ đệm (số khung mẫu)
    thiet_bi_mau = thiet_bi_mau  # Thiết bị mẫu âm thanh đầu vào

    # Mở kết nối đến thiết bị âm thanh đầu vào
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=tan_so_mau,
                    input=True,
                    frames_per_buffer=kich_thuoc_bo_dem,
                    input_device_index=thiet_bi_mau)

    print("Say something...")

    # Khởi tạo danh sách khung mẫu rỗng để lưu trữ dữ liệu ghi âm
    frames = []

    # Ghi âm theo từng khung mẫu và lưu vào danh sách khung mẫu
    for i in range(0, int(tan_so_mau / kich_thuoc_bo_dem * thoi_gian_ghi)):
        data = stream.read(kich_thuoc_bo_dem)
        frames.append(data)

    print("Processing...")

    # Dừng kết nối và đóng stream
    stream.stop_stream()
    stream.close()

    # Đóng kết nối PyAudio
    p.terminate()

    # Lưu trữ dữ liệu ghi âm vào file WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(tan_so_mau)
    wf.writeframes(b''.join(frames))
    wf.close()

# xử lý file ghi âm tạm
def process_record():
    y, sr = librosa.load("record.wav", sr = 8000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=16)
    new_mfcc = process_mfcc(mfcc)
    last_mfcc = new_mfcc.reshape((1,16,50))
    #load model
    model = keras.models.load_model("my_model.h5")
    predictions = model.predict(last_mfcc)
    return predictions

# điều chỉnh đầu vào phù hợp để đưa vô mô hình
def process_mfcc(mfcc):
    desired_num_features = 50
    if mfcc.shape[1] > desired_num_features:
        mfcc = mfcc[:, :desired_num_features]
    elif mfcc.shape[1] < desired_num_features:
        num_missing_features = desired_num_features - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, num_missing_features)), mode='constant')
    return mfcc

file_path = "Commander.json"

# đọc file json 
def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        return data    
a = load_json(file_path)  


# trợ lý ảo xử lý thông tin của người và trả về kết quả
def response(command, json):

    reponse = None
    code = None

    for item in json["commander"]:
        if command == item["command"]:
            #
            reponse = item["response"]
            code = item["code"]
            break    
        else: # there's no item in dict
            reponse = "I can't understand what you just say!!"
    return reponse, code


# running assistant

label_list = ['bye','code','date','game','hello','music','time']
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(label_list)

one_hot_labels  = to_categorical(encoded_labels)

label_arr = np.asarray(encoded_labels)
ghi_am("record.wav", 3, 44100, 1024, 0)
predictions = process_record()
predicted_labels = np.argmax(predictions, axis=1)
#print(predicted_labels)
decoded_labels = label_encoder.inverse_transform(predicted_labels)
user_input = decoded_labels[0]
print(user_input)
x, y = response(user_input, a)
print("Assistant: "), 
print(x)
if y != None:
    exec(y)
