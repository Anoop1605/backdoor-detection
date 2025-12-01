import time
from ipaddress import ip_address, ip_network

class SteppingStoneDetector:
    def __init__(self, local_network="192.168.0.0/16", time_threshold=2.0, byte_threshold_pct=0.1):
        self.inbound_flows = []
        self.local_network = ip_network(local_network)
        self.threshold_time = time_threshold
        self.byte_threshold_pct = byte_threshold_pct
        
    def is_local_ip(self, ip_str):
        try:
            return ip_address(ip_str) in self.local_network
        except ValueError:
            return False
        
    def check_relay(self, event):
        # Validate event structure
        required_fields = ['src_ip', 'dest_ip', 'timestamp']
        if not all(field in event for field in required_fields):
            return None
            
        src_ip = event['src_ip']
        dest_ip = event['dest_ip']
        timestamp = float(event['timestamp'])  # Use actual event timestamp
        bytes_sent = event.get('flow', {}).get('bytes_toserver', 0)
        
        # INBOUND: External -> Local
        if not self.is_local_ip(src_ip) and self.is_local_ip(dest_ip):
            self.inbound_flows.append({
                "time": timestamp, 
                "bytes": bytes_sent,
                "src": src_ip,
                "dest": dest_ip
            })
            
        # OUTBOUND: Local -> External
        elif self.is_local_ip(src_ip) and not self.is_local_ip(dest_ip):
            alerts = []
            for flow in self.inbound_flows:
                time_diff = abs(timestamp - flow["time"])
                byte_diff = abs(bytes_sent - flow["bytes"])
                byte_threshold = flow["bytes"] * self.byte_threshold_pct
                
                if time_diff < self.threshold_time and byte_diff < byte_threshold:
                    alerts.append(
                        f"[ALERT] Stepping Stone: {flow['src']} -> {flow['dest']} -> {dest_ip} "
                        f"(Δt={time_diff:.2f}s, Δbytes={byte_diff})"
                    )
            
            if alerts:
                return "; ".join(alerts)
                    
        # Cleanup old flows (use event timestamp, not current time)
        self.inbound_flows = [f for f in self.inbound_flows 
                              if (timestamp - f["time"]) < 5]
        return None