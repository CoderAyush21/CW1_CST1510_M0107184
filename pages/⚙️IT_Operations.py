import streamlit as st
from app.data.db import connect_database
import plotly.express as px
import pandas as pd 
from datetime import datetime
from app.data.tickets import insert_ticket, get_all_tickets, update_ticket_status, delete_ticket
from app.services.analyticalQueries import get_avg_resolution_by_staff, get_high_priority_tickets_by_status, get_slow_resolution_tickets, get_tickets_by_priority
import time
st.set_page_config(
    page_title="IT Operations",
    layout="wide",
)

st.title("IT OPERATIONS DASHBOARD")

if st.session_state.get("logged_in") != True:
    st.error("Please Log in")
    st.stop()

conn=connect_database()
col1,col2= st.columns([0.8,0.2])
with col1:

    st.subheader("Service Desk Performance: Average Resolution Time by Staff Members")
    df_resolution_times = get_avg_resolution_by_staff(conn)

    fig = px.bar(
        df_resolution_times,
        x="assigned_to",
        y="avg_resolution_time",
        color="avg_resolution_time",
        color_continuous_scale=px.colors.sequential.Plotly3_r,
        hover_data=["assigned_to", "avg_resolution_time"],  
    )

    fig.update_layout(
        xaxis_title="Staff Member", 
        yaxis_title="Average Resolution Time (hours)",
    )

    st.plotly_chart(fig, use_container_width=True)

col1,col2= st.columns([0.8,0.2])
with col1:
    st.subheader("High Priority Tickets by Status")
    df_high_priority = get_high_priority_tickets_by_status(conn)

    fig2 = px.bar(
        df_high_priority,
        x="count",
        y="status",
        orientation='h',
        color="count",
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_data=["status", "count"],
    )

    fig2.update_layout(
        xaxis_title="Number of High Priority Tickets",
        yaxis_title="Ticket Status",
        yaxis=dict(autorange="reversed"), 
    )

    st.plotly_chart(fig2, use_container_width=True)


df_slow_resolution = get_slow_resolution_tickets(conn, min_resolution_time=24)
df_priority_level = get_tickets_by_priority(conn)
col1,col2= st.columns([0.5,0.5])
with col2:
    st.markdown("### Tickets Distribution by Priority Level")
    fig = px.pie(
        df_priority_level,
        names="priority",
        values="count",
        color="priority",
        color_discrete_map={
            "Low": "#00CC96",
            "Medium": "#FFA15A",
            "High": "#EF553B"
        }
    )
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
    )
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.markdown("### Tickets with Slow Resolution Times by Status")


    fig = px.bar(
        df_slow_resolution,
        x="status",
        y="avg_resolution",
        color="avg_resolution",
        color_continuous_scale=px.colors.sequential.Plotly3,
        hover_data=["status", "avg_resolution"],
    )

    fig.update_layout(
        xaxis_title="Ticket Status",
        yaxis_title="Average Resolution Time (hours)",
    )
    st.plotly_chart(fig, use_container_width=True)



# Get all incident ids as list for the update form
df_ticket= get_all_tickets()
ticket_all__ids= df_ticket['ticket_id'].tolist()

st.subheader("IT Tickets Management")
col1,col2= st.columns([0.8,0.2])
with col1:
    action_choice = st.selectbox("Select Action", ([" Add Ticket", " Update Ticket Status", "Delete Ticket"]), key="action_choice_ticket")


    if action_choice == " Add Ticket":
        # Add Incidents Form
        st.markdown("### Add Ticket ###") 
        with st.form("Add new ticket"):
            priority = st.selectbox("Priority", ["Low", "Medium", "High","Critical"])
            status = st.selectbox("Status", ["Open", "Closed", "In Progress","Resolved"])
            assigned_to = st.text_input("Assigned to")
            description = st.text_input("Description")
            resolution_time= st.text_input("Resolution Hours")
            submitted = st.form_submit_button("Submit")

        if submitted:
            ticket_datetime= datetime.now()
            try :
                insert_ticket(priority,description,status, assigned_to,resolution_time,ticket_datetime)
                st.success("Ticket added")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error adding incident: {e}")

    elif action_choice == " Update Ticket Status":
        st.markdown("### Update Ticket Status")
        with st.form("Update Ticket status"):
            incident_id = st.selectbox("Ticket ID", ticket_all__ids)
            new_status = st.selectbox("New Status", ["Open", "Closed", "In Progress","Resolved"])
            updated = st.form_submit_button("Update Status")
        if updated:
            try:
                success = update_ticket_status(incident_id, new_status)
                if success:
                    st.success("Ticket status updated")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Ticket ID not found")
            except Exception as e:
                st.error(f"Error updating status: {e}")

    elif action_choice == "Delete Ticket":
        st.markdown("### Delete Ticket")
        with st.form("Delete Ticket"):
            ticket_id= st.selectbox("Ticket ID to Delete", ticket_all__ids, key="delete_ticket_id")
            
            submitted= st.form_submit_button("Delete")

            if submitted:
                if st.checkbox("Confirm deletion of ticket"):                
                    deleted = delete_ticket(ticket_id)
                    if deleted:
                            st.success("Ticket deleted")
                            time.sleep(2)
                            st.rerun()
                    else:
                            st.error("Ticket ID not found")
                else:
                    st.warning("Please confirm deletion by checking the box.")

