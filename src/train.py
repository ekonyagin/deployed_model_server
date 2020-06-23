import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import max_error, mean_absolute_error
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    excel_file = "file_training.xlsx"
    df = pd.read_excel(excel_file)
    
    print(f"File {excel_file} read successfully!")
    
    elem = df.columns[78]

    df = df.drop(['АВТОМОБИЛЬ',
                  '20200101_0000_20200201_0000_MAN. Эффективность вождения (таблица)  (01.01.2020 - 01.02.2020) (4).xlsx',
                 'ГОС. НОМЕР',
                 'VIN',
                 'ОТ',
                 'ДО',
                 'ВОДИТЕЛИ',
                 'РАСХОД',
                 'РАСХОД НА СТОЯНКЕ',
                 'РАСХОД ДВИЖ',
                 'ОДОМЕТР НА НАЧАЛО РЕЙСА',
                 'ОДОМЕТР НА КОНЕЦ РЕЙСА',
                 'УРОВЕНЬ ДУТ Н',
                 'УРОВЕНЬ ДУТ К',
                 'ЗАПРАВКА ДУТ З',
                 'СЛИВЫ ДУТ',
                 'ВРЕМЯ С ОТБОРОМ',
                 'РАСХОД БЕЗ',
                 'РАСХОД С',
                 'РЕТАРДЕР %',
                 'РЕТАРДЕР КМ',
                 'КВ ВЫС',
                 '1650-1700',
                 '1700-1750',
                 '1750-1800',
                 '1800-1850',
                 '1850-1900',
                 '1900-2000',
                  elem,
                 '1650-1700%',
                 '1700-1750%',
                 '1750-1800%',
                 '1800-1850%',
                 '1850-1900%',
                 '1900-2000%',
                 '2000+%'], axis=1)
    df.head().to_excel('new_sample.xlsx', index=False)
    X_train, X_test, y_train, y_test = train_test_split(df.drop(['РАСХОД СР'], axis=1),
                                                        df['РАСХОД СР'],
                                                        test_size=0.2)
    print(f"Starting training a model...")
    clf = RandomForestRegressor()
    clf.fit(X_train, y_train)
    print(f"Model finished training!")
    y_pred = clf.predict(X_test)
    max_err = max_error(y_test, y_pred)
    mean_err = mean_absolute_error(y_test, y_pred)
    median_err = np.median(np.abs(np.subtract(y_test, y_pred)))

    print(f"max error: {max_err}\t mean error: {mean_err}\t median error: {median_err}")
    
    s = pickle.dumps(clf)
    fname = "model.cfg"
    with open(fname, 'wb') as fp:
        fp.write(s)
    print(f"Model saved successfully to file {fname}")
