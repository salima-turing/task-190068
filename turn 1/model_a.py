import time
import random
import pandas as pd
from typing import List, Dict

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

def gather_process_data(mock_client, node_ids: List[str]) -> Dict[str, List[float]]:
	data = {}

	for node_id in node_ids:
		data[node_id] = []
		for _ in range(10):  # Gather 10 data points
			value, _ = mock_client.read_node(node_id)
			data[node_id].append(value)
			time.sleep(0.5)  # Mock short delay between readings

	return data

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
			"reorder_level": mean - 2 * std_dev,  # Simple reorder level calculation
		}

	return analysis_results

if __name__ == "__main__":
	# Mocked OPC UA Server endpoint
	mock_opcua_server_endpoint = "opc.tcp://mock-server:4840"

	# PLC Node IDs for process data
	node_ids = [
		"ns=2;s=ProcessVariables.Level_Sensor_1",
		"ns=2;s=ProcessVariables.Level_Sensor_2",
	]

	try:
		# Create a mock OPC UA client
		client = MockOPCUAClient(mock_opcua_server_endpoint)

		# Gather process data
		process_data = gather_process_data(client, node_ids)

		# Analyze the data
		inventory_analysis = analyze_inventory_data(process_data)

		# Print the analysis results
		print("Inventory Analysis Results:")
		for node_id, result in inventory_analysis.items():
			print(f"Node ID: {node_id}")
			print(f"Mean: {result['mean']:.2f}")
			print(f"Standard Deviation: {result['std_dev']:.2f}")
			print(f"Reorder Level: {result['reorder_level']:.2f}")
			print("-" * 30)

	finally:
		client.close()
