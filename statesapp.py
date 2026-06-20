{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "265483a5-59d7-4976-b225-4185a8151d80",
   "metadata": {},
   "outputs": [],
   "source": [
    "import random\n",
    "import streamlit as st\n",
    "from streamlit_gsheets import GSheetsConnection\n",
    "\n",
    "st.title(\"4th of July - American delicacies lunch🦅\")\n",
    "st.write(\"Enter your name to claim your State *except Florida!\")\n",
    "\n",
    "# 1. Establish connection to your Google Sheet\n",
    "conn = st.connection(\"gsheets\", type=GSheetsConnection)\n",
    "\n",
    "# Read the current data from the sheet\n",
    "df = conn.read()\n",
    "\n",
    "# Clean up data formatting\n",
    "df['Name'] = df['Name'].fillna('').astype(str).str.strip()\n",
    "df['State'] = df['State'].astype(str).str.strip()\n",
    "\n",
    "# 2. User Input\n",
    "user_name = st.text_input(\"Who are you?\").strip().title()\n",
    "\n",
    "if st.button(\"Assign Me a State, Except Florida, Arkansas, Alabama, and West Virgina\"):\n",
    "    if not user_name:\n",
    "        st.error(\"What's your name!?\")\n",
    "    \n",
    "    # Check if this person already has a state assigned\n",
    "    elif user_name in df['Name'].values:\n",
    "        already_assigned = df[df['Name'] == user_name]['State'].values[0]\n",
    "        st.warning(f\"Hey {user_name}, you already got assigned to **{already_assigned}**, sucks to be you.\")\n",
    "        \n",
    "    else:\n",
    "        # Filter for rows where the Name column is still empty\n",
    "        available_rows = df[df['Name'] == \"\"]\n",
    "        \n",
    "        if available_rows.empty:\n",
    "            st.error(\"All states have been claimed somehow!\")\n",
    "        else:\n",
    "            # Pick a random row from the available ones\n",
    "            chosen_index = random.choice(available_rows.index)\n",
    "            chosen_state = df.loc[chosen_index, 'State']\n",
    "            \n",
    "            # Assign the name to that row in our local copy\n",
    "            df.loc[chosen_index, 'Name'] = user_name\n",
    "            \n",
    "            # Push the updated data back to the Google Sheet live\n",
    "            conn.update(data=df)\n",
    "            \n",
    "            st.success(f\"🎉 Congratulations {user_name}! Your assigned state is **{chosen_state}** I'm sorry if it's Florida or Alabama.\")\n",
    "\n",
    "# 3. Live Dashboard of claims\n",
    "with st.expander(\"See current claims\"):\n",
    "    claimed_df = df[df['Name'] != \"\"][['Name', 'State']]\n",
    "    if not claimed_df.empty:\n",
    "        st.dataframe(claimed_df, use_container_width=True, hide_index=True)\n",
    "    else:\n",
    "        st.write(\"No states claimed yet.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
