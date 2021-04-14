
from modules import *
from s_viz_2 import *

def pred():
    print("pred 1 ...")
    class NeuralNetModel:

        def __init__(self, model_name):
            self.__model_name = model_name
            self.__model = None

        def train(self, x, y, hidden_layer_sizes=[10,], learning_rate=0.001, max_iter=2000):
            self.__model = MLPRegressor(solver="adam", activation="relu", alpha=1e-5, random_state=0, 
                                        hidden_layer_sizes=hidden_layer_sizes, verbose=False, tol=1e-5, 
                                        learning_rate_init=learning_rate, max_iter=max_iter)
            self.__model.fit(x, y)

        def get_predictions(self, x):
            return np.round(self.__model.predict(x), 0).astype(np.int32)

    class PolynomialRegressionModel:

        def __init__(self, model_name, polynomial_degree):
            self.__model_name = model_name
            self.__polynomial_degree = polynomial_degree
            self.__model = None

        def train(self, x, y):
            polynomial_features = PolynomialFeatures(degree=self.__polynomial_degree)
            x_poly = polynomial_features.fit_transform(x)
            self.__model = LinearRegression()
            self.__model.fit(x_poly, y)

        def get_predictions(self, x):
            polynomial_features = PolynomialFeatures(degree=self.__polynomial_degree)
            x_poly = polynomial_features.fit_transform(x)
            return np.round(self.__model.predict(x_poly), 0).astype(np.int32)

        def get_model_polynomial_str(self):
            coef = self.__model.coef_
            intercept = self.__model.intercept_
            poly = "{0:.3f}".format(intercept)

            for i in range(1, len(coef)):
                if coef[i] >= 0:
                    poly += " + "
                else:
                    poly += " - "
                poly += "{0:.3f}".format(coef[i]).replace("-", "") + "X^" + str(i)

            return poly

    def plot_graph(model_name, x, y, y_pred, name):

        plt.scatter(x, y, s=10)
        sort_axis = operator.itemgetter(0)
        sorted_zip = sorted(zip(x, y_pred), key=sort_axis)
        x, y_pred = zip(*sorted_zip)

        plt.plot(x, y_pred, color='m')
        plt.title("Amount of " + model_name + " in each day")
        plt.xlabel("Day")
        plt.ylabel(model_name)
        plt.savefig("img/" + name)


    def print_forecast(model_name, model, beginning_day=0, limit=10):

        next_days_x = np.array(range(beginning_day, beginning_day + limit)).reshape(-1, 1)
        next_days_pred = model.get_predictions(next_days_x)

        print("The forecast for " + model_name + " in the following " + str(limit) + " days is:")
        for i in range(0, limit):
            print("Day " + str(i + 1) + ": " + str(next_days_pred[i]))



    world_confirmed_ts_df = pd.read_csv(world_confirmed_ts_url, header=0, escapechar='\\')
    world_deaths_ts_df = pd.read_csv(world_deaths_ts_url, header=0, escapechar='\\')
    usa_ts_df = pd.read_csv(usa_ts_url, header=0, escapechar='\\')
    date_list = usa_ts_df.columns.tolist()[11:]

    usa_overall_confirmed_ts_df = world_confirmed_ts_df[world_confirmed_ts_df["Country/Region"] == "US"]
    new_usa_confirmed_df = usa_overall_confirmed_ts_df[date_list].T
    new_usa_confirmed_df.columns = ["confirmed"]
    new_usa_confirmed_df = new_usa_confirmed_df.assign(days=[1 + 
                                                   i for i in range(len(new_usa_confirmed_df))])[['days'] + 
                                                   new_usa_confirmed_df.columns.tolist()]

    #print(new_usa_confirmed_df)

    usa_overall_deaths_ts_df = world_deaths_ts_df[world_deaths_ts_df["Country/Region"] == "US"]
    new_usa_deaths_df = usa_overall_deaths_ts_df[date_list].T
    new_usa_deaths_df.columns = ["deaths"]
    new_usa_deaths_df = new_usa_deaths_df.assign(days=[1 +
                                                       i for i in range(len(new_usa_deaths_df))])[['days'] + 
                                                       new_usa_deaths_df.columns.tolist()]




    training_set = new_usa_confirmed_df
    x = np.array(training_set["days"]).reshape(-1, 1)
    y = training_set["confirmed"]

    training_set_deaths = new_usa_deaths_df
    x_deaths = np.array(training_set_deaths["days"]).reshape(-1, 1)
    y_deaths = training_set_deaths["deaths"]


    regression_model = PolynomialRegressionModel("Cases using Polynomial Regression", 2)
    regression_model.train(x, y)
    y_pred = regression_model.get_predictions(x)
    print_forecast("Cases using Polynomial Regression", regression_model, 
                   beginning_day=len(x), 
                   limit=10)
    plot_graph("Cases using Polynomial Regression", x, y, y_pred, "US_Cases_using_Polynomial_Regression.png")
