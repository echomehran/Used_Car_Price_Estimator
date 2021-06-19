from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import pandas as pd
import numpy as np
from collections import defaultdict


df = pd.read_csv()


encoder = defaultdict(LabelEncoder)


cols = ['exterior_color', 'interior_color', 'location', 'make', 'model', 'mileage', 'style', 'year', 'engine', 'accidentCount',
        'accidentCount', 'ownerCount', 'isCleanTitle', 'isFrameDamaged', 'isLemon', 'isSalvage', 'isTheftRecovered', 'price']


df[cols] = df[cols].apply(lambda x: encoder[x.name].fit_transform(x))


exclude_price = df[df.columns.difference(['price'])]


clf = tree.DecisionTreeClassifier()
clf = clf.fit(exclude_price, df.price)

my_data = ['Night Black', 'Unknown', 'Patchogue, NY', 'Audi', 'Q7', '5000', 'S-line 3.0T quattro',
           '2015', '2.0L Inline-4 Gas Turbocharged', '0', '5.0', '1', '1', '0', '0', '1']

new_data = LabelEncoder().fit_transform(my_data)

answer = clf.predict([new_data])
decoded = encoder['price'].inverse_transform(answer)[0]

print(f"Car's price has been predicted as ${decoded:.2f}")
