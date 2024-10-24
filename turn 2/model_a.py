import time
import random
import pandas as pd
from typing import List, Dict
import threading


# Mock OPC UA Client
class MockOPCUAClient:
    def __init__(self, endpoint):
        pass

    def read_node(self, node_id):
        # Mocked data generation
        value = random.randint(10, 100)
        quality = True
        return value, quality

    def close(self):
        pass


def gather_real_time_data(mock_client, node_ids: List[str], data: Dict[str, List[float]], interval=0.5):
    while True:
        for node_id in node_ids:
            value, _ = mock_client.read_node(node_id)
            data[node_id].append(value)
        time.sleep(interval)


def analyze_inventory_data(data: dict) -> dict:
    analysis_results = {}

    for node_id, readings in data.items():
        df = pd.DataFrame({'Reading': readings})

        # Basic analysis: Calculate mean and standard deviation
        mean = df['Reading'].mean()
        std_dev = df['Reading'].std()

        analysis_results[node_id] = {
            "mean": mean,
            "std_dev": std_dev,
            "reorder_level": mean - 2 * std_dev,
        }

    return analysis_results


if __name__ == "__main__":
    mock_opcua_server_endpoint = "opc.tcp://mock-server:4840"

    node_ids = [
        "ns=2;s=ProcessVariables.Level_Sensor_1",
        "ns=2;s=ProcessVariables.Level_Sensor_2",
    ]

    try:
        client = MockOPCUAClient(mock_opcua_server_endpoint)
        process_data = {node_id: [] for node_id in node_ids}

        data_collection_thread = threading.Thread(target=gather_real_time_data, args=(client, node_ids, process_data))
        data_collection_thread.daemon = True
        data_collection_thread.start()

        print("Real-time data collection started...")

        while True:
            time.sleep(5)  # Analyze data every 5 seconds

            # Analyze the data
            inventory_analysis = analyze_inventory_data(process_data)

            # Print the analysis results
            print("\nInventory Analysis Results:")
            for node_id, result in inventory_analysis.items():
                print(f"Node ID: {node_id}")
                print(f"Mean: {result['mean']:.2f}")
                print(f"Standard Deviation: {result['std_dev']:.2f}")
                print(f"Reorder Level: {result['reorder_level']:.2f}")
                print("-" * 30)

    finally:
        client.close()
