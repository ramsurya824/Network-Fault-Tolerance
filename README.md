# 🛠️ Network Fault Tolerance and Critical Component Analysis

This Python program simulates a computer network and performs fault tolerance and critical component analysis using the NetworkX library. It models a system with one Application Server (AS), multiple Storage Servers (SS), and several Routers.

## 📌 Features

- ✅ **Simulate Failures**
  - Remove one or more router nodes or network links and check network connectivity.
  
- 📊 **Fault Tolerance Analysis**
  - Determine the **maximum number of routers or links that can fail** while still keeping all SS nodes connected to the AS.
  - Compute the **minimum number of nodes and edges required** to maintain network functionality.

- ⚠️ **Critical Component Identification**
  - Identify **critical nodes** and **critical edges** whose failure would break connectivity.

## 🧠 How It Works

1. **Graph Construction**:
   - Nodes are labeled with types: `"Application Server"`, `"Storage Server"`, or `"Router"`.
   - Edges represent network links between these nodes.

2. **Connectivity Check**:
   - Uses **Breadth-First Search (BFS)** to verify if all SS nodes can reach the AS node.

3. **Fault Tolerance Calculation**:
   - Iteratively removes combinations of router nodes or edges to determine:
     - Maximum nodes/edges that can fail without disconnecting the network.
     - Minimum infrastructure needed to keep the network functional.

4. **Critical Nodes & Edges**:
   - A node or edge is **critical** if its removal disconnects any storage server from the application server.

## 📦 Requirements

- Python 3.x
- [networkx](https://networkx.org/)
- [matplotlib](https://matplotlib.org/) (optional, for visualization)

Install dependencies using pip:

```bash
pip install networkx matplotlib
