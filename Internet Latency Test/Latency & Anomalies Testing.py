import subprocess
import time
import speedtest
import numpy as np
import subprocess

def ping(host='8.8.8.8'):
    command = ['ping', '-c', '4', host]  # -c 4 sends 4 packets
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        output = result.stdout
        # Extract latency from ping output (example for Linux)
        latencies = [float(line.split('time=')[1].split(' ms')[0]) for line in output.splitlines() if 'time=' in line]
        return latencies
    else:
        print(f"Ping failed to {host}. Return error: {result.returncode}")
        return None

def check_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping
    return download_speed, upload_speed, ping

def detect_anomalies(latencies):
    if latencies:
        mean = np.mean(latencies)
        std_dev = np.std(latencies)
        
        # Define thresholds for anomaly detection (e.g., 2 standard deviations away from mean)
        anomaly_threshold = 2
        anomalies = [latency for latency in latencies if abs(latency - mean) > anomaly_threshold * std_dev]
        
        if anomalies:
            print(f"Anomalies detected: {anomalies}")
        else:
            print("No anomalies detected")
    else:
        print("No latency data to check for anomalies")

if False:
    
    def monitor_connection():
        while True:
            latencies = ping()
        if latencies:
            detect_anomalies(latencies)
        time.sleep(60)  # Check every minute

#monitor_connection()

latencies = ping()
if latencies:
    print(f"Latencies: {latencies} ms")
else:
    print("No latency data")

download_speed, upload_speed, ping = check_speed()
print(f"Download speed: {download_speed:.2f} Mbps")
print(f"Upload speed: {upload_speed:.2f} Mbps")
print(f"Ping: {ping} ms")

detect_anomalies(latencies)
