import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('./dsk_winrates_by_turn.csv')

# Filter out lands
lands = ['Sawmp', 'Forest', 'Island', 'Mountain', 'Plains']
df = df[~df['Card Name'].isin(lands)]

# Calculate average win rate by turn
avg_win_rate = df.groupby('Turn').agg({'Win Rate': 'mean'})

# Streamlit app
st.title("Win Rate by Turn: Random Card Viewer")

# Add explainer
st.markdown(
    """
    ### About This Tool
    Data comes from [17lands](https://www.17lands.com).
    
    This tool expands on 17lands winrate data by analyzing when a permanent is in play and calculating the winrate for any specific turn. 
    For example, if a permanent is in play on turn 4, this tool estimates the probability that the player will win the game.
    
    The **red dashed line** represents the baseline winrate of any card on any specific turn, while the plot shows the winrate for a randomly selected card.

    **Note**: The only data included at the moment is from the **Duskmourn set**.

    Check out my website for more Magic-related content: [jackjosephwright.github.io](https://jackjosephwright.github.io/mtg_main_page/)
    """
)

# Button to refresh
if st.button("Show Random Card"):
    # Pick a random card
    unique_card_names = df['Card Name'].unique()
    random_card_name = np.random.choice(unique_card_names)
    card_df = df[df['Card Name'] == random_card_name].copy()

    # Prepare data for plotting
    card_df['Turn'] = card_df['Turn'].astype(int)
    card_df.sort_values('Turn', inplace=True)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(card_df['Turn'], card_df['Win Rate'], marker='o', label=random_card_name)
    ax.plot(avg_win_rate, color='red', linestyle='dashed', label="Average Win Rate")
    ax.set_xticks(np.arange(0, max(card_df['Turn']) + 1, 1))
    ax.set_xlabel('Turn')
    ax.set_ylabel('Win Rate')
    ax.set_ylim(0.4, 0.7)
    ax.set_title(f"Win Rate of {random_card_name} Over Turns")
    ax.legend()
    
    st.pyplot(fig)
else:
    st.write("Click the button to view a random card's win rate!")
