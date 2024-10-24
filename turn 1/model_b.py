import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Modbus TCP Server Configuration
PLC_IP = '127.0.0.1'  # Use the actual PLC IP address here if connecting to a physical PLC
PLC_PORT = 502

# Modbus Address Range for Inventory Data
ITEM_COUNT_REGISTER_ADDRESS = 0x00  # Address 0 holds the item count
TANK_LEVEL_REGISTER_ADDRESS = 0x01  # Address 1 holds the tank level


def mock_plc_client():
    # For demonstration purposes, we will mock the PLC client using a TcpClient to a Modbus Slave.
    client = ModbusTcpClient(PLC_IP, PLC_PORT)
    return client


def read_process_data(client):
    try:
        # Read item count from PLC
        item_count = client.read_holding_registers(ITEM_COUNT_REGISTER_ADDRESS, 1).registers[0]
        # Read tank level from PLC
        tank_level = client.read_holding_registers(TANK_LEVEL_REGISTER_ADDRESS, 1).registers[0]
        return item_count, tank_level
    except ModbusException as e:
        print(f"Error reading process data: {e}")
        return None, None


def main():
    client = mock_plc_client()

    # Assuming we have set some initial values for the PLC registers during testing
    # Mock data: Item Count = 100, Tank Level = 60
    item_count_threshold = 80  # Set your desired threshold value
    reorder_level = 20  # Set your desired reorder level

    while True:
        item_count, tank_level = read_process_data(client)

        if item_count is not None and tank_level is not None:
            print(f"Current Inventory: {item_count} units")
            print(f"Current Tank Level: {tank_level} units")

            if item_count < item_count_threshold:
                print("Inventory level is low. Consider reordering!")
            if tank_level < reorder_level:
                print("Tank level is low. Please refill!")
        time.sleep(5)  # Simulate continuous data collection every 5 seconds

    client.close()


if __name__ == "__main__":
    main()
