import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
import logging

# --- Logging configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("fundranking.log"),
        logging.StreamHandler()
    ]
)

# Load and clean data
def load_data(file_path):
    df = pd.read_excel(file_path)
    numerical_columns = ['Net Asset Value', 'Monthly Total Return', 'Benchmark Return', 'Expense Ratio', 'Fund Size']
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Rename columns to match script expectations
    df = df.rename(columns={
        'Fund Name': 'Fund_Name',
        'Fund Category': 'Fund_Category',
        'Monthly Total Return': 'Monthly_Total_Return',
        'Benchmark Return': 'Benchmark_Return',
        'Expense Ratio': 'Expense_Ratio',
        'Fund Size': 'Fund_Size_₦',
        'Net Asset Value (₦)': 'NAV_₦'
    })
    
    logging.info("Loaded and cleaned data from %s", file_path)
    return df

# Morningstar-style scoring
def assign_morningstar_score(percentile):
    if percentile >= 90:
        return 5
    elif percentile >= 67.5:
        return 4
    elif percentile >= 32.5:
        return 3
    elif percentile >= 10:
        return 2
    else:
        return 1

# Calculate MMF effective annualized yield
def calculate_mmf_yield(df, years=None):
    if years:
        df = df[df['Year'].isin(years)]
    
    grouped = df.groupby('Fund_Name')
    yields = []
    
    for fund, group in grouped:
        monthly_returns = group['Monthly_Total_Return'].dropna()
        T = len(monthly_returns)
        if T == 0:
            effective_yield = 0
        else:
            product = np.prod(1 + monthly_returns)
            effective_yield = (product ** (12 / T) - 1)
        yields.append({'Fund_Name': fund, 'Effective_Yield': effective_yield})
    
    return pd.DataFrame(yields)

# Calculate non-MMF metrics (R, RAR, Risk)
def calculate_nonmmf_metrics(df, years=None):
    if years:
        df = df[df['Year'].isin(years)]
    
    grouped = df.groupby(['Fund_Name', 'Fund_Category'])
    metrics = []
    
    for (fund, category), group in grouped:
        monthly_returns = group['Monthly_Total_Return'].dropna()
        benchmark_returns = group['Benchmark_Return'].dropna()
        T = len(monthly_returns)
        
        # NEED-Ensure benchmark returns are aligned with monthly returns
        # if T == 0 or len(benchmark_returns) != T:
        #     metrics.append({
        #         'Fund_Name': fund,
        #         'Fund_Category': category,
        #         'Annualized_Return': 0,
        #         'RAR': 0,
        #         'Risk': 0
        #     })
        #     continue

        excess_returns = monthly_returns - benchmark_returns
        product = np.prod(1 + excess_returns)
        if product > 0 and T > 0:
            R = (product ** (12 / T) - 1)
        else:
            R = np.nan  # or R = 0
        RAR = np.mean(excess_returns)
        risk = R - RAR
        
        metrics.append({
            'Fund_Name': fund,
            'Fund_Category': category,
            'Annualized_Return': R,
            'RAR': RAR,
            'Risk': risk
        })
    logging.info("Non-MMF Metrics calculated: %d records", len(metrics))
    logging.debug("Non-MMF Metrics DataFrame:\n%s", pd.DataFrame(metrics))
    return pd.DataFrame(metrics)

# Calculate MMF ratings
def calculate_mmf_rating(df, years=None, period_name=''):
    df_mmf = df[df['Fund_Category'] == 'Cash/Money Market Fund']
    if df_mmf.empty:
        logging.warning("No MMF funds found for period: %s", period_name)
        return pd.DataFrame()
    
    yield_data = calculate_mmf_yield(df_mmf, years)
    expense_data = df_mmf.groupby('Fund_Name')['Expense_Ratio'].mean().reset_index(name='Average_Expense_Ratio')
    nav_data = df_mmf.groupby('Fund_Name')['Fund_Size_₦'].mean().reset_index(name='Average_NAV_₦')
    
    results = yield_data.merge(expense_data, on='Fund_Name').merge(nav_data, on='Fund_Name')
    results['Fund_Category'] = 'Cash/Money Market Fund'
    
    results['Yield_Percentile'] = results['Effective_Yield'].apply(
        lambda x: percentileofscore(results['Effective_Yield'].dropna(), x, kind='rank')
    )
    results['Yield_Score'] = results['Yield_Percentile'].apply(assign_morningstar_score)
    
    results['Expense_Percentile'] = results['Average_Expense_Ratio'].apply(
        lambda x: 100 - percentileofscore(results['Average_Expense_Ratio'].dropna(), x, kind='rank')
    )
    results['Expense_Ratio_Score'] = results['Expense_Percentile'].apply(assign_morningstar_score)
    
    results['NAV_Percentile'] = results['Average_NAV_₦'].apply(
        lambda x: percentileofscore(results['Average_NAV_₦'].dropna(), x, kind='rank')
    )
    results['Fund_Size_Score'] = results['NAV_Percentile'].apply(assign_morningstar_score)
    
    results['MMF_Score'] = (
        0.60 * results['Yield_Score'] +
        0.25 * results['Expense_Ratio_Score'] +
        0.15 * results['Fund_Size_Score']
    )
    results['Star_Rating'] = results['MMF_Score'].round().astype(int)
    results['Period'] = period_name
    results['Category_Rank'] = results['MMF_Score'].rank(ascending=False, method='min').astype(int)
    
    output_columns = [
        'Fund_Name', 'Fund_Category', 'Period', 'Effective_Yield', 'Yield_Score',
        'Average_Expense_Ratio', 'Expense_Ratio_Score', 'Average_NAV_₦', 'Fund_Size_Score',
        'MMF_Score', 'Star_Rating', 'Category_Rank'
    ]
    logging.info("Final MMF Ratings for period %s:\n%s", period_name, results[output_columns])
    return results[output_columns]

# Calculate non-MMF ratings with sub-category ranking
def calculate_nonmmf_rating(df, years=None, period_name=''):
    df_nonmmf = df[df['Fund_Category'] != 'Cash/Money Market Fund']
    if df_nonmmf.empty:
        logging.warning("No non-MMF funds found for period: %s", period_name)
        return pd.DataFrame()
    
    metrics = calculate_nonmmf_metrics(df_nonmmf, years)
    
    # Calculate percentiles and scores within each Fund_Category
    results = []
    for category in metrics['Fund_Category'].unique():
        cat_metrics = metrics[metrics['Fund_Category'] == category].copy()
        if len(cat_metrics) < 3:  # Handle categories with fewer than 3 funds
            cat_metrics['RAR_Percentile'] = 50
            cat_metrics['RAR_Score'] = 3
            cat_metrics['Risk_Percentile'] = 50
            cat_metrics['Risk_Score'] = 3
            cat_metrics['Overall_Score'] = 3
            cat_metrics['Star_Rating'] = 3
            cat_metrics['Category_Rank'] = 1
            cat_metrics['Period'] = period_name
            results.append(cat_metrics)
            continue
        
        cat_metrics['RAR_Percentile'] = cat_metrics['RAR'].apply(
            lambda x: percentileofscore(cat_metrics['RAR'].dropna(), x, kind='rank')
        )
        cat_metrics['RAR_Score'] = cat_metrics['RAR_Percentile'].apply(assign_morningstar_score)
        
        cat_metrics['Risk_Percentile'] = cat_metrics['Risk'].apply(
            lambda x: 100 - percentileofscore(cat_metrics['Risk'].dropna(), x, kind='rank')
        )
        cat_metrics['Risk_Score'] = cat_metrics['Risk_Percentile'].apply(assign_morningstar_score)
        
        cat_metrics['Overall_Score'] = (0.5 * cat_metrics['RAR_Score'] + 0.5 * cat_metrics['Risk_Score'])
        cat_metrics['Star_Rating'] = cat_metrics['Overall_Score'].apply(
            lambda x: 5 if x >= 4.5 else 4 if x >= 3.5 else 3 if x >= 2.5 else 2 if x >= 1.5 else 1
        )
        cat_metrics['Category_Rank'] = cat_metrics['Overall_Score'].rank(ascending=False, method='min').astype(int)
        cat_metrics['Period'] = period_name
        results.append(cat_metrics)
    
    if not results:
        return pd.DataFrame()
    
    results_df = pd.concat(results, ignore_index=True)
    
    output_columns = [
        'Fund_Name', 'Fund_Category', 'Period', 'Annualized_Return', 'RAR', 'RAR_Score',
        'Risk', 'Risk_Score', 'Overall_Score', 'Star_Rating', 'Category_Rank'
    ]
    logging.info("Non-MMF Ratings before rating across periods for period %s:\n%s", period_name, results_df[output_columns])
    return results_df[output_columns]

#NOT USED IN NON-MMF RATING
# This function combines non-MMF ratings across different periods, applying weights to each period's score
def calculate_combined_nonmmf_rating(df, periods):
    combined_results = []
    
    for period_name, years in periods.items():
        result = calculate_nonmmf_rating(df, years, period_name)
        if not result.empty:
            combined_results.append(result)
    
    if not combined_results:
        logging.warning("No combined non-MMF results found.")
        return pd.DataFrame()

    weights = {'1-year': 1.0, '2-years': 0.5, '3-years': 0.3,'5-years': 0.2,'6-years': 0.1}  # Only 1-year period available
    combined_df = pd.concat(combined_results)
    
    pivot_scores = combined_df.pivot(index=['Fund_Name', 'Fund_Category'], columns='Period', values='Overall_Score')
    
    final_scores = []
    for (fund, category) in pivot_scores.index:
        weighted_score = 0
        for period_name in periods.keys():
            if period_name in pivot_scores.columns:
                score = pivot_scores[period_name].loc[(fund, category)]
                if not pd.isna(score):
                    weighted_score += weights[period_name] * score
        star_rating = 5 if weighted_score >= 4.5 else 4 if weighted_score >= 3.5 else 3 if weighted_score >= 2.5 else 2 if weighted_score >= 1.5 else 1
        final_scores.append({
            'Fund_Name': fund,
            'Fund_Category': category,
            'Weighted_Score': weighted_score,
            'Weighted_Star_Rating': star_rating
        })
    
    final_df = pd.DataFrame(final_scores)
    logging.info("FINAL Non-MMF Ratings:\n%s", final_df)
    return final_df.sort_values('Weighted_Score', ascending=False)

# Combine all ratings
def combine_ratings(mmf_results, nonmmf_results, periods):
    """
    Combine MMF and non-MMF rating results into a unified DataFrame,
    standardize score columns, and compute consistent star-based rankings.
    """
    # Columns we expect across both MMF and non-MMF results
    standard_columns = [
        'Fund_Name', 'Fund_Category', 'Period',
        'Overall_Score', 'Star_Rating'
    ]

    # --- Normalize MMF results ---
    if not mmf_results.empty:
        mmf_results = mmf_results.copy()
        mmf_results['Overall_Score'] = pd.to_numeric(mmf_results.get('MMF_Score', np.nan), errors='coerce')
        mmf_results['Star_Rating'] = pd.to_numeric(mmf_results.get('Star_Rating', np.nan), errors='coerce')
        mmf_results = mmf_results[standard_columns].copy()
    else:
        mmf_results = pd.DataFrame(columns=standard_columns)

    # --- Normalize non-MMF results ---
    if not nonmmf_results.empty:
        nonmmf_results = nonmmf_results.copy()
        nonmmf_results['Overall_Score'] = pd.to_numeric(nonmmf_results.get('Overall_Score', np.nan), errors='coerce')
        nonmmf_results['Star_Rating'] = pd.to_numeric(nonmmf_results.get('Star_Rating', np.nan), errors='coerce')
        nonmmf_results = nonmmf_results[standard_columns].copy()
    else:
        nonmmf_results = pd.DataFrame(columns=standard_columns)

    # --- Merge both datasets ---
    combined_df = pd.concat([mmf_results, nonmmf_results], ignore_index=True)

    # Handle empty case
    if combined_df.empty:
        logging.warning("Combined results are empty.")
        return pd.DataFrame()

    # Ensure correct types
    combined_df['Overall_Score'] = pd.to_numeric(combined_df['Overall_Score'], errors='coerce')
    combined_df['Star_Rating'] = pd.to_numeric(combined_df['Star_Rating'], errors='coerce')

    # --- Ranking ---
    if 'Period' in combined_df.columns and combined_df['Period'].notna().any():
        combined_df['Overall_Rank'] = combined_df.groupby('Period')['Star_Rating'].rank(
            method='min', ascending=False
        )
    else:
        # fallback in case 'Period' is missing or empty
        combined_df['Overall_Rank'] = combined_df['Star_Rating'].rank(method='min', ascending=False)

    # Sort for presentation
    combined_df = combined_df.sort_values(by=['Period', 'Overall_Rank'], ascending=[True, True])

    logging.info("Combined ratings DataFrame:\n%s", combined_df)
    return combined_df

# Main function
def main():
    file_path = 'funds/management/csv_data/final_doccy_for_etom(1).xlsx'
    periods = {
        # '1-year': [2018],
        # '3-years': [2018, 2019, 2020],
        # '5-years': [2018, 2019, 2020, 2021, 2022],
        '6-years': [2018, 2019, 2020, 2021, 2022, 2023],
    }

    df = load_data(file_path)
    mmf_results = []
    nonmmf_results = []
    
    for period_name, years in periods.items():
        mmf_result = calculate_mmf_rating(df, years, period_name)
        nonmmf_result = calculate_nonmmf_rating(df, years, period_name)
        if not mmf_result.empty:
            mmf_results.append(mmf_result)
        if not nonmmf_result.empty:
            nonmmf_results.append(nonmmf_result)
    
    # Concatenate results
    mmf_results = pd.concat(mmf_results, ignore_index=True) if mmf_results else pd.DataFrame()
    nonmmf_results = pd.concat(nonmmf_results, ignore_index=True) if nonmmf_results else pd.DataFrame()
    
    # Combine ratings
    combined_df = combine_ratings(mmf_results, nonmmf_results, periods.keys())
    if not combined_df.empty:
        combined_df.to_csv('funds/management/csv_data/fund_rankings.csv', index=False)
        logging.info("Results saved to 'funds/management/csv_data/fund_rankings.csv'")
    else:
        logging.error("No results to save.")

if __name__ == '__main__':
    main()