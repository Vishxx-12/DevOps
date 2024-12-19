# Real-Time Delivery Monitoring Pipeline

## **Objective**
You are a DevOps engineer in ZIPPTO managing a fast-paced delivery service that needs real-time insights into operational efficiency and delivery performance.
You task is to create monitoring application top provide insights on performance of the delivery service.

## **Approach**
Using Python, Prometheus, Grafana and Jenkins, create a pipeline that simulates delivery metrics, visualizes them on dashboards and sets up automated alerts to ensure smooth operations and quick problem detection.

---

## **1. Prerequisites**
Ensure the following tools are installed:
- **Docker**: For containerizing and running services.
- **Python**: Version 3.10 or higher.
- **Jenkins**: For pipeline automation.
- **Prometheus**: For metrics scraping.
- **Grafana**: For data visualization.

---

## **2a. Install Packages**

```
pip3 install prometheus-client
```

## **2. Code Directory Structure**

```
delivery_monitoring/
├── delivery_metrics.py   # Python script to simulate metrics
├── prometheus.yml        # Prometheus configuration
├── Jenkinsfile           # Jenkins pipeline script

Steps:
mkdir delivery_monitoring
cd delivery_monitoring
```
Create above files under 'delivery_monitoring' directory

---

## **3. Steps to Set Up and Simulate**

### **Step 1: Write the Python Application**
Create a file named `delivery_metrics.py`:

```
from prometheus_client import start_http_server, Summary, Gauge
import random
import time

# Metrics
total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge("pending_deliveries", "Number of pending deliveries")
on_the_way_deliveries = Gauge("on_the_way_deliveries", "Number of deliveries on the way")
average_delivery_time = Summary("average_delivery_time", "Average delivery time in seconds")

# Simulate delivery statuses
def simulate_delivery():
    pending = random.randint(10, 50)
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    avg_time = random.uniform(15, 45)

    total = pending + on_the_way + delivered

    print(f"[DEBUG] Total deliveries: {total}")
    print(f"[DEBUG] Pending deliveries: {pending}")
    print(f"[DEBUG] On-the-way deliveries: {on_the_way}")
    print(f"[DEBUG] Average delivery time: {avg_time:.2f} seconds")

    total_deliveries.set(total)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(avg_time)

if __name__ == "__main__":
    print("[INFO] Starting the HTTP server on port 8000...")
    start_http_server(8000)
    print("[INFO] HTTP server started. Simulating deliveries...")
    while True:
        simulate_delivery()
        print("[INFO] Sleeping for 5 seconds...")
        time.sleep(5)
```

Run the script:
```
python3 delivery_metrics.py

[INFO] Starting the HTTP server on port 8000...
[INFO] HTTP server started. Simulating deliveries...
[DEBUG] Total deliveries: 68
[DEBUG] Pending deliveries: 23
[DEBUG] On-the-way deliveries: 5
[DEBUG] Average delivery time: 28.81 seconds
[INFO] Sleeping for 5 seconds...
[DEBUG] Total deliveries: 96
[DEBUG] Pending deliveries: 30
[DEBUG] On-the-way deliveries: 10
[DEBUG] Average delivery time: 18.65 seconds
[INFO] Sleeping for 5 seconds...
[DEBUG] Total deliveries: 104
[DEBUG] Pending deliveries: 24
[DEBUG] On-the-way deliveries: 20
[DEBUG] Average delivery time: 23.19 seconds
[INFO] Sleeping for 5 seconds...
```
Access metrics at [http://localhost:8000/metrics](http://localhost:8000/metrics).

---

### **Step 2: Configure Prometheus**

Create a file named `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "delivery_service"
    static_configs:
      - targets: ["host.docker.internal:8000"]
```

Run Prometheus:
```bash
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

Output
```
docker run -d --name prometheus -p 9090:9090   -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
754702408add8b672f0328e265e73b8bcf1d832317438d05d167349a83673f39
```

Access Prometheus at [http://localhost:9090](http://localhost:9090).

---

### **Step 3: Set Up Grafana**

Run Grafana:
```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

Output
```
docker run -d --name grafana -p 3000:3000 grafana/grafana
d15b35389cd54e91aa9451f3093a6701934968d022ddd20e8fb382cb1f05736f
```

Note IP address of your machine
```
ip addr show docker0
```

Output
```
ip addr show docker0
4: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:11:26:95:13 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:11ff:fe26:9513/64 scope link
       valid_lft forever preferred_lft forever
```
Note the IP address (for example, here IP address is): 172.17.0.1


#### Step 3a: Access Grafana
Open Grafana in your browser at http://localhost:3000.

#### Step 3b: Log in with the default credentials:
Username: admin
Password: admin.

#### Step 3c: Add Prometheus as a Data Source
In the left-hand menu, Goto: Home -> Connections -> Data sources ->prometheus

#### Step 3d: Configure Prometheus
In the list of data sources, select Prometheus.
Enter the following details:
URL: http://host.docker.internal:9090.
Leave other fields as default 
Click the Save & Test button to verify the connection.

2. Create a new dashboard with the following panels:
   - **Panel 1**: Query `total_deliveries`.
   - **Panel 2**: Query `pending_deliveries` and `on_the_way_deliveries`.
   - **Panel 3**: Query `average_delivery_time`.

---

### **Step 4: Automate Alerts in Prometheus**

Update `prometheus.yml`:

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ["localhost:9093"]

alerts:
  - alert: HighPendingDeliveries
    expr: pending_deliveries > 40
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High Pending Deliveries"
      description: "Pending deliveries exceeded threshold: {{ $value }}."
```

Restart Prometheus:
```bash
docker restart prometheus
```
Verify alerts in the Prometheus UI under the "Alerts" tab.

---

### **Step 5: Create the Jenkins Pipeline**

Create a file named `Jenkinsfile`:

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/your-repo/delivery_monitoring.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t delivery_metrics .'
            }
        }
        stage('Run Application') {
            steps {
                sh 'docker run -d -p 8000:8000 --name delivery_metrics delivery_metrics'
            }
        }
        stage('Run Prometheus & Grafana') {
            steps {
                sh '''
                docker run -d --name prometheus -p 9090:9090 \
                  -v $WORKSPACE/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
                docker run -d --name grafana -p 3000:3000 grafana/grafana
                '''
            }
        }
    }
}
```

Run Jenkins:
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

Access Jenkins at [http://localhost:8080](http://localhost:8080) and create a pipeline job using the `Jenkinsfile`.

---

### **Step 6: Simulate Alerts**

Modify `delivery_metrics.py` to increase `pending_deliveries` values:

```python
pending = random.randint(50, 100)  # Increase range to exceed alert threshold
```

Restart the Python script and Prometheus. Verify alerts in the Prometheus UI and Grafana.

---

## **Expected Outputs**
1. **Metrics Endpoint:** [http://localhost:8000/metrics](http://localhost:8000/metrics).
2. **Prometheus Query:** Graphs for `total_deliveries`, `pending_deliveries`, and `average_delivery_time`.
3. **Grafana Dashboard:** Visualizations for delivery metrics and trends.
4. **Jenkins Logs:** Successful pipeline build with logs for Docker commands.
5. **Prometheus Alerts:** Critical alerts for high pending deliveries.

---

Feel free to reach out for further assistance!
