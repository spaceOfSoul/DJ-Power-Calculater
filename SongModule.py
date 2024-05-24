import pandas as pd

def load_dataframe(path, sheet_name='KR 곡 이름순'):
    df = pd.read_excel(path, sheet_name=sheet_name, header=[3, 4])
    
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
    df = df.drop([0, 1, 2, 3]).reset_index(drop=True)
    
    return df

def filter_songs(df, button_type, difficulty, is_sc):
    if is_sc:
        column_name = f'{button_type} BUTTONS_SC'
        filtered_songs = df[df[column_name] == difficulty]
    else:
        column_names = [f'{button_type} BUTTONS_NORMAL', f'{button_type} BUTTONS_HARD', f'{button_type} BUTTONS_MAXIMUM']
        filtered_songs = df[df[column_names].eq(difficulty).any(axis=1)]
    
    filtered_songs = filtered_songs[['DLC_Unnamed: 1_level_1', '곡명_Unnamed: 2_level_1']]
    return filtered_songs

if __name__ == "__main__":
    df = load_dataframe('PatternData.xlsx')
    # print(df)
    for i in filter_songs(df,4,15,False).iterrows():
        print(i[1])