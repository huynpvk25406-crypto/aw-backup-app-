"""Giao dien quan tri: xem du lieu + backup thu cong + danh sach file backup."""
import os
import pandas as pd
import pyodbc
import streamlit as st
from backup_manager import backup, BACKUP_DIR, CONN, DB

st.set_page_config(page_title="AdventureWorks Backup Console", layout="wide")
st.title("Quan tri AdventureWorks + Backup")

c1, c2, c3 = st.columns(3)
for col, kind in zip((c1, c2, c3), ("FULL", "DIFF", "LOG")):
    if col.button(f"Backup {kind}"):
        st.success(f"Backup {kind} thanh cong") if backup(kind) else st.error("That bai - xem backup.log")

st.subheader("Danh sach file backup")
rows = []
for f in sorted(os.listdir(BACKUP_DIR), reverse=True):
    p = os.path.join(BACKUP_DIR, f)
    if f.endswith((".bak", ".trn")):
        rows.append({"File": f, "MB": round(os.path.getsize(p) / 1048576, 2)})
st.dataframe(pd.DataFrame(rows), use_container_width=True)

st.subheader("Nhat ky (backup.log)")
log = os.path.join(BACKUP_DIR, "backup.log")
if os.path.exists(log):
    st.code("".join(open(log, encoding="utf-8").readlines()[-15:]))

st.subheader("Xem nhanh du lieu: Sales.SalesOrderHeader")
cn = pyodbc.connect(CONN.replace("DATABASE=master", f"DATABASE={DB}"))
st.dataframe(pd.read_sql("SELECT TOP 20 * FROM Sales.SalesOrderHeader", cn), use_container_width=True)
