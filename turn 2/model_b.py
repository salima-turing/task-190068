import time
import random
import pandas as pd
from typing import List, Dict


# Mock OPC UA Client
class MockOPCUAClient:
    def __init__(self, endpoint):
        pass

    def read_node(self, node_id):
        value = random.randint(10, 100)
        quality = True
        return value, quality

    def close(self):
        pass


def gather_process_data_realtime(mock_client, node_ids: List[str], sample_time=0.5, num_samples=None) -> Dict[
    str, List[float]]:
    data = {}
    for node_id in node_ids:
        data[node_id] = []

    try:
        print("Starting real-time data gathering...")
        while True:
            for node_id in node_ids:
                value, _ = mock_client.read_node(node_id)
                data[node_id].append(value)
                if num_samples and len(data[node_id]) >= num_samples:
                    return data
            time.sleep(sample_time)

    except KeyboardInterrupt:
        print("\nReal-time data gathering stopped by user.")
        return data


def analyze_inventory_data(data: dict) -> dict:
    # Analysis function remains the same
    pass


if __name__ == "__main__":
    mock_opcua_server_endpoint = "opc.tcp://mock-server:4840"
    node_ids = [
        "ns=2;s=ProcessVariables.Level_Sensor_1",
        "ns=2;s=ProcessVariables.Level_Sensor_2",
    ]

    try:
        client = MockOPCUAClient(mock_opcua_server_endpoint)

        # Gather real-time data for 60 seconds (10 minutes)
        realtime_data = gather_process_data_realtime(client, node_ids, sample_time=0.5, num_samples=120)

        inventory_analysis = analyze_inventory_data(realtime_data)

        print("Inventory Analysis Results:")
        for node_id, result in inventory_analysis.items():
            print(f"Node ID: {node_id}")
            print(f"Mean: {result['mean']:.2f}")
            print(f"Standard Deviation: {result['std_dev']:.2f}")
            print(f"Reorder Level: {result['reorder_level']:.2f}")
            print("-" * 30)

    finally:
        client.close()
