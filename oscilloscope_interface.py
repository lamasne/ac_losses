import pyvisa as visa

rm = visa.ResourceManager()
print(f"list of resources:\n {rm.list_resources()}\n")

# Create a resource object representing the oscilloscope 
try:
    oscilloscope = rm.open_resource('GPIB0::7::INSTR')
except Exception as e:
    print(f"Could not find the instrument. Maybe try to switch off and on the oscilloscope.\n{str(e)}")

try:
    print(f"Info from oscillo:\n{oscilloscope.query('*IDN?')}\n")
    print(f"Info from curve:\n{oscilloscope.query_ascii_values('CURV?', converter='f')}\n")

except Exception as e:
    oscilloscope.close()
    print(f"Session closed with error:\n{str(e)}")

# Potentially useful commands
# oscilloscope.timeout = 5000
# print(oscilloscope.query("ACQuire:MODe?"))
# print(oscilloscope.query("ACQuire:STATE?"))
# print(oscilloscope.query('CURSor?'))



# values = oscilloscope.query('WAVFrm?')
# print(values)

# print(oscilloscope.query("CURSor:SPLit:SOURCE2?"))



# oscilloscope.query_binary_values()

# oscilloscope.read()





# while True:
#     print(oscilloscope.read_bytes(1))



