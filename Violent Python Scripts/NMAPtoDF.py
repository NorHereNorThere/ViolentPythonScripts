import nmap
import pandas as pd
from io import StringIO

nmScanObj = nmap.PortScanner()
nmScanObj.scan(hosts='192.168.0.0/24', ports='1-8000', arguments='-T5 -sV')

textStream = StringIO(initial_value=nmScanObj.csv(), newline='\r\n')
textStream.seek(0)
dataFrame = pd.read_table(filepath_or_buffer=textStream, sep=';', skip_blank_lines=True)

