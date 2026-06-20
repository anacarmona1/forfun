import random
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🦅 4th of July - American Delicacies Lunch")
st.write("Enter your name to claim your State *except Florida!")

# 1. Establish connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the current data from the sheet
df = conn.read()

# Clean up data formatting
df['Name'] = df['Name'].fillna('').astype(str).str.strip()
df['State'] = df['State'].astype(str).str.strip()

# 2. User Input
user_name = st.text_input("Who are you?").strip().title()

if st.button("Assign Me a State, Except Florida, Arkansas, Alabama, and West Virginia"):
    if not user_name:
        st.error("What's your name!?")
    
    # Check if this person already has a state assigned
    elif user_name in df['Name'].values:
        already_assigned = df[df['Name'] == user_name]['State'].values[0]
        st.warning(f"Hey {user_name}, you already got assigned to **{already_assigned}**, sucks to be you.")
        
    else:
        # Filter for rows where the Name column is still empty
        available_rows = df[df['Name'] == ""]
        
        if available_rows.empty:
            st.error("All states have been claimed somehow!")
        else:
            # Pick a random row from the available ones
            chosen_index = random.choice(available_rows.index)
            chosen_state = df.loc[chosen_index, 'State']
            
            # Assign the name to that row in our local copy
            df.loc[chosen_index, 'Name'] = user_name
            
            # Push the updated data back to the Google Sheet live
            conn.update(data=df)
            
            st.success(f"🎉 Congratulations {user_name}! Your assigned state is **{chosen_state}** I'm sorry if it's Florida or Alabama.")

# 3. Live Dashboard of claims
with st.expander("See current claims"):
    claimed_df = df[df['Name'] != ""][['Name', 'State']]
    if not claimed_df.empty:
        st.dataframe(claimed_df, use_container_width=True, hide_index=True)
    else:
        st.write("No states claimed yet.")
