import pyaudio
import wave

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

    print("Đang ghi âm...")

    # Khởi tạo danh sách khung mẫu rỗng để lưu trữ dữ liệu ghi âm
    frames = []

    # Ghi âm theo từng khung mẫu và lưu vào danh sách khung mẫu
    for i in range(0, int(tan_so_mau / kich_thuoc_bo_dem * thoi_gian_ghi)):
        data = stream.read(kich_thuoc_bo_dem)
        frames.append(data)

    print("Ghi âm hoàn tất.")

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

# Gọi hàm ghi âm
ghi_am("code_31", 3, 44100, 1024, 0)