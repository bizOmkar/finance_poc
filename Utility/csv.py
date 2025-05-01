# # import pandas as pd

# # CSV_EBITDA_WALK = "../Input_data/ebitda_walk.csv"
# # CSV_YTD = "../Input_data/data_walk.csv"

# import os
# import pandas as pd

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CSV_EBITDA_WALK = os.path.join(BASE_DIR, "Input_data", "ebitda_walk.csv")
# CSV_YTD = os.path.join(BASE_DIR, "Input_data", "data_walk.csv")
# # df_ebitda_walk_impact = pd.read_csv(CSV_EBITDA_WALK)


# # df_ebitda_walk_impact = pd.read_csv(r"C:\Users\OmkarK\OneDrive - bizmetric.com\GENAI\copy_vedanta\data\ebitda_walk.csv")
# # df_ytd = pd.read_csv(r"C:\Users\OmkarK\OneDrive - bizmetric.com\GENAI\copy_vedanta\data\data_ytd.csv")

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_EBITDA_WALK = BASE_DIR / "Input_data" / "ebitda_walk.csv"
CSV_YTD = BASE_DIR / "Input_data" / "data_ytd.csv"
