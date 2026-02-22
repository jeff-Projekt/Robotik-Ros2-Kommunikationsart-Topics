#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from v2_service_interface.srv import SetScanFrequency

class ScanFrequencyClientNode(Node):
    def __init__(self):
        super().__init__('set_scan_frequency_client')
        #service client erzeugen
        self.client=self.create_client(SetScanFrequency,'set_scan_frequency') #Nachrichtentyp und Service-Name
        #warten bis der service verfügbar ist
        
    def call_set_scan_frequency(self,value):
             #prüfen ,ob der Service verfügbar ist
        while not self.client.wait_for_service(1.0):
             self.get_logger().warn("Waiting for a service...")

             # Request -objekt erzeugen
        request= SetScanFrequency.Request()
        #request mit gewünschter Scan-Frequenz füllen
        request.scan_frequency =value
        #Service asynchron aufrufen
        future = self.client.call_async(request)
        future.add_done_callback(self.callback_set_scan_frequency_response)   

    def callback_set_scan_frequency_response(self,future):
        #Antwort des Service-servers auslesen
        response= future.result()
        #überprüfen ob der Server die Scan_Frequenz akzeptiert hat
        if response.success:
            self.get_logger().info(f"Scan frequency set erfolgreich:{response.message}.")
        else:
             self.get_logger().warn(f"set scan frequency abgelehnt:{response.message}")     
                 

def main(args=None):
        rclpy.init(args=args)
        node = ScanFrequencyClientNode()
        # schritt 7:Service-Aufruf durchführen
        node.call_set_scan_frequency(5)
        rclpy.spin(node)
        rclpy.shutdown()
if __name__ == '__main__':
   main()