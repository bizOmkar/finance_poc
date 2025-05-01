import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.patches as mpatches

# 3. 📈 Waterfall Chart Plotting Function
def plot_ebitda_walk(df_row):
    labels = [
        "EBITDA_From_Quarter", "Sales", "LME", "Strategic Hedging", "Premium", 
         "Alumina", "Power", "Other Hot Metal", "Conversion & Other", "EBITDA_To_Quarter"
    ]
    values = [df_row[label] for label in labels]

    fig, ax = plt.subplots(figsize=(12, 5))  # Slightly taller figure to prevent touching

    # Waterfall base calculation
    cum_values = [values[0]]
    for v in values[1:-1]:
        cum_values.append(cum_values[-1] + v)
    cum_values.append(values[-1])

    colors = ['navy'] + ['limegreen' if v >= 0 else 'red' for v in values[1:-1]] + ['navy']

    # Plot bars
    prev = 0
    bar_width = 0.6  # Slightly thinner bars
    for i in range(len(values)):
        if i == 0 or i == len(values) - 1:
            ax.bar(i, values[i], color=colors[i], width=bar_width)
            height = values[i]
            y = 0
        else:
            height = values[i]
            y = prev
            ax.bar(i, height, bottom=y, color=colors[i], width=bar_width)
        prev = y + height

    # X-ticks
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")

    # Title and grid
    ax.set_title("EBITDA Walk (Mn$)")
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Compute y-limits manually to leave space
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax * 1.2)  # 20% extra headroom

    # Add value labels neatly
    for i, (labels, value) in enumerate(zip(labels, values)):
        if i == 0 or i == len(labels) - 1:
            ypos = value + (0.05 * ymax) if value >= 0 else value - (0.05 * ymax)
            ax.text(i, ypos, f"{int(value)}", ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ypos = cum_values[i-1] + (value/2)
            ax.text(i, ypos, f"{int(value)}", ha='center', va='center', fontsize=8)

    # Add legend manually, move it lower
    increase_patch = mpatches.Patch(color='limegreen', label='Increase')
    decrease_patch = mpatches.Patch(color='red', label='Decrease')
    total_patch = mpatches.Patch(color='navy', label='Total')
    ax.legend(handles=[increase_patch, decrease_patch, total_patch], loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=3)

    plt.tight_layout()
    return fig

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_ebitda_walk_from_quarters(df_ebitda_walk_impact, source_quarter, target_quarter):
    expected_period = f"EW_{source_quarter}_{target_quarter}"
    row_match = df_ebitda_walk_impact[df_ebitda_walk_impact['Period'] == expected_period]
    print("*********************************************************")
    print("Row Successfully got if Dataframe")
    
    if row_match.empty:
        return None  # Handle not found case

    selected_row = row_match.iloc[0]
    fig = plot_ebitda_walk(selected_row)
    print("*********************************************************")
    print("Plotting EBITDA WALK")
    return fig