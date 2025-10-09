import pandas as pd
import os

# File paths
full_data_path = "C:/Users/laksh/Downloads/US_Accidents_March23.csv"
output_path = "C:/Users/laksh/Downloads/US_Accidents_March23_sampled_1M.csv"

print("🔍 Checking file path...")
print("File exists:", os.path.exists(full_data_path))

if not os.path.exists(full_data_path):
    print("❌ File not found. Check your Downloads folder and correct the name in the script.")
else:
    print("✅ File found! Loading dataset... Please wait, it may take a few seconds.")
    try:
        df = pd.read_csv(full_data_path,nrows=2000000)
        print(f"📊 Dataset loaded successfully — {len(df)} rows and {len(df.columns)} columns.")
        
        sample_size = min(1_000_000, len(df))
        df_sampled = df.sample(n=sample_size, random_state=42)
        df_sampled.reset_index(drop=True, inplace=True)
        df_sampled.to_csv(output_path, index=False)

        print(f"✅ Sampled {sample_size} rows saved to: {output_path}")
    except Exception as e:
        print("❌ Error while loading or sampling:", e)

