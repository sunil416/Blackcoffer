import pandas as pd


class InputReader:
    def __init__(self, path) -> None:
        try:
            self.data=pd.read_excel(path)
        except Exception as e:
            print(f"Exception in INput Reader {e}")
    
    


    