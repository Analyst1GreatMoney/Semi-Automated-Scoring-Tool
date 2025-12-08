from graphviz import Digraph

dot = Digraph("FiveC_Flow", format="svg")  # 改成 svg

dot.attr(rankdir="LR")

dot.node("A", "Borrower Submits Application")
dot.node("B", "System Extracts Data\n(Application Forms + CNA)")
dot.node("C", "Automated Scoring: Each C")
dot.node("D", "Score < Threshold?", shape="diamond")
dot.node("E", "Manual Review (Override)")
dot.node("F", "Override Approved?", shape="diamond")
dot.node("G", "Proceed to Next C")
dot.node("H", "Final Lending Outcome")
dot.node("I", "Reject Application")

dot.edge("A", "B")
dot.edge("B", "C")
dot.edge("C", "D")
dot.edge("D", "E", label="Yes")
dot.edge("D", "G", label="No")
dot.edge("E", "F")
dot.edge("F", "G", label="Approve")
dot.edge("F", "I", label="Reject")
dot.edge("G", "H")

dot.render("fivec_flowchart", view=True)
