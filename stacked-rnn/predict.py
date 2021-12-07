
from __future__ import print_function

from os import path, environ
import numpy

if __name__ == '__main__':
    environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    from twgeo.models.geomodel import Model
    from twgeo.data import twus_dataset, constants

    # x_train, y_train, x_dev, y_dev, x_test, y_test = twus_dataset.load_state_data(size='large')
    import twgeo.data.input as input
    # tweets, locations = input.read_csv_data('aarjavdata.csv', tweet_txt_column_idx=0, location_column_idx=1)
    # tweets, locations = input.read_csv_data('diptidata.csv', tweet_txt_column_idx=0, location_column_idx=1)
    tweets, locations = input.read_csv_data('diptitanmaydatatesting.csv', tweet_txt_column_idx=0, location_column_idx=1)

    x_test = tweets
    y_test = locations


    # x_train.to_csv("TRAINDATAX.CSV")
    # y_train.to_csv("TRAINDATAY.CSV")
    # x_test.to_csv("TESTDATAX.CSV")
    # # y_test.to_csv("TESTDATAY.CSV")
    # numpy.savetxt("TESTDATAX.CSV", x_test, fmt='%s', delimiter='\n')
    # numpy.savetxt("TESTDATAY.CSV", y_test, fmt='%s')

    geoModel = Model(batch_size=650)

    geoModel.load_saved_model(path.join(constants.DATACACHE_DIR, 'geomodel_full_state'))
    predictions = geoModel.predict(x_test)
    evaluation = geoModel.evaluate(x_test, y_test)
    print(evaluation)
    print(predictions)

