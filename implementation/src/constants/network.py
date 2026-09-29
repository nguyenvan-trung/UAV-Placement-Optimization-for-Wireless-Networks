"""Thông số cố định mặc định của mạng không dây và mô hình A2G 5G/6G."""

# Kích thước không gian
DEFAULT_AREA_WIDTH_M = 1000.0
DEFAULT_AREA_HEIGHT_M = 1000.0
DEFAULT_MIN_ALTITUDE_M = 50.0
DEFAULT_MAX_ALTITUDE_M = 300.0

# Số lượng UAV mặc định
DEFAULT_NUM_UAVS = 4

# Tham số vô tuyến (5G Sub-6 GHz)
CARRIER_FREQUENCY_HZ = 3.5e9  # 3.5 GHz
SPEED_OF_LIGHT = 3.0e8        # 3e8 m/s

# Tham số môi trường đô thị dày đặc (Urban Dense - Al-Hourani)
ENV_A = 9.61
ENV_B = 0.16
ETA_LOS = 1.0    # dB (Thêm suy hao khi có LoS)
ETA_NLOS = 20.0  # dB (Thêm suy hao khi bị chắn NLoS)

# Công suất và ngưỡng kết nối
TRANSMIT_POWER_DBM = 30.0     # 30 dBm (1.0 W)
NOISE_POWER_DBM = -104.0      # dBm
SNR_THRESHOLD_DB = 18.0       # 18.0 dB (Chuẩn QoS 5G để tạo độ phân biệt vùng phủ sóng)
DEFAULT_COVERAGE_THRESHOLD_DBM = -90.0

# Năng lượng tiêu thụ (Hovering + Transmit)
DEFAULT_P_HOVER_BASE_W = 100.0
DEFAULT_P_TRANSMIT_W = 1.0

# Trọng số hàm mục tiêu đa tiêu chí (w1*f1 - w2*f2 - w3*f3)
WEIGHT_COVERAGE = 0.6       # w1
WEIGHT_ENERGY = 0.2         # w2
WEIGHT_INTERFERENCE = 0.2   # w3
