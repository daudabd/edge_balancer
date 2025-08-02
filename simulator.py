class Node:
    def __init__(self, cpu, mem, battery):
        self.cpu = cpu
        self.mem = mem
        self.battery = battery

class Task:
    def __init__(self, cpu_req, mem_req, energy_req):
        self.cpu_req  = cpu_req
        self.mem_req  = mem_req
        self.energy_req = energy_req
