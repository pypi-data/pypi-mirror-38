class forecast: 
    """ Class to forecast time series using multiple naive models.

    # Arguments
        time series: a Python list containing exclusively numbers.
        frequency: a Python integer. Used to specify time series
			pattern: 
			 - 12 for monthly.
			 - 7 for weekly.
			 - 365 for daily.
        ahed: A Python integer. Used to specify number of periods
			 towards the future.
    """
	
    TRAINING_SET = [0.55 ,0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
    TEST_SET = [0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15]

    fcst = None
    fitted = None
    test = None
    err = 0
    po = 0
	
    def __init__(self, time_series, f, h):
        self.time_series = time_series
        self.f = f
        self.h = h
        self.series_len = len(self.time_series)
        n = self.__class__.__name__
        self.method_list = [func for func in dir(eval(n)) if callable(getattr(eval(n), func)) and func[0]!='__' and func!='optimizer' and func[:5] == 'model']
    		
    # Error function
    def err_predict(self, obs, est):
        # Calculates MAD
        error_pred = [a - b for a, b in zip(obs, est)]
        total_error = [abs(number) for number in error_pred]
        try:
            result = sum(total_error) / len(obs)
        except ZeroDivisionError as err:
            print('run-time error:', err)
            result = 'NA'
            del error_pred
            del total_error	
        return result
    
    # O[n-1]
    def model_naive(self):
        allow = 1
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
		
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        self.fitted = [x[-1] for i in range(x_hat)]
        result.append(self.fitted)
        
		# Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
		# Calculates forecast based on periods ahead
        self.fcst = [self.time_series[-1] for i in range(self.h)]
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[:n/n]
    def model_last_period(self):
        allow = self.f
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            x.append(x[-self.f])
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            y.append(y[-self.f])
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
		# appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

  # O[:2n/2]
    def model_mean_two_period(self):
        allow = 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = sum(x[-2:])/2
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-2:])/2
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[:3n/3]
    def model_mean_three_period(self):
        allow = 3
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = sum(x[-3:])/3
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-3:])/3
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[:6n/6] -> change formula
    def model_mean_half_period(self):
        allow = self.f / 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = sum(x[-6:])/6
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-6:])/6
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[:12n/12]
    def model_mean_full_period(self):
        allow = self.f
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = sum(x[-self.f:])/self.f
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-self.f:])/self.f
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[:24n/24]
    def model_mean_double_full_period(self):
        allow = self.f * 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        doub_freq = self.f * 2
        while i < x_hat:
            op = sum(x[-doub_freq:])/doub_freq
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-doub_freq:])/doub_freq
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2
    def model_growth_full_period(self):
        allow = self.f * 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        doub_freq = self.f * 2
        while i < x_hat:
            op = (x[-doub_freq] + x[-self.f]) / 2
            x.append(op)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = (y[-doub_freq] + y[-self.f]) / 2
            y.append(op)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2 -> change description
    def model_growth_full(self): # check
        allow = self.f * 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        doub_freq = self.f * 2
        while i < x_hat:
            op = sum(x[-doub_freq:])/ doub_freq
            ov = sum(x[-self.f:])/ self.f
            ow = ov + (ov - op)
            x.append(ow)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-doub_freq:])/ doub_freq
            ov = sum(y[-self.f:])/ self.f
            ow = ov + (ov - op)
            y.append(ow)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2 -> change description
    def model_mean_weighted(self): # check
        allow = self.f * 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        w = [0.15, 0.25, 0.6]
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = x[-1] * w[2]
            ov = x[-2] * w[1]
            ow = x[-3] * w[0]
            x.append(op + ov + ow)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = y[-1] * w[2]
            ov = y[-2] * w[1]
            ow = y[-3] * w[0]
            y.append(op + ov + ow)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2 -> change description
    def model_expo_weighted(self):
        allow = self.f * 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
		# Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = x[-self.f] * 0.4
            ov = (sum(x[-3:]) / 3 )  * 0.6
            x.append(op + ov)
            i += 1
            
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = y[-self.f] * 0.4
            ov = (sum(y[-3:]) / 3 )  * 0.6
            y.append(op + ov)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2 -> change description
    def model_mean_threefith(self):
        allow = 5
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        # Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        while i < x_hat:
            op = sum(x[-3:]) / 3
            ov = sum(x[-5:]) / 5
            ow = (op + ov) / 2
            x.append(ow)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-3:]) / 3
            ov = sum(y[-5:]) / 5
            ow = (op + ov) / 2
            y.append(ow)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    # O[12n + 24n]/ 2 -> change description
    def model_mean_fullhalf(self):
        allow = self.f / 2
        result = []
        y_hat = int(round(self.series_len * self.TRAINING_SET[self.po],0))
        x_hat = int(self.series_len - y_hat)
        
		# Calculates the trainig set
        x = self.time_series[:y_hat]
        i = 0
        half_seas = int(self.f / 2)
        while i < x_hat:
            op = sum(x[-self.f:]) / self.f
            ov = sum(x[-half_seas:]) / half_seas
            ow = (op + ov) / 2
            x.append(ow)
            i += 1
        del x[:y_hat]
        self.fitted = x   
        result.append(self.fitted)

        # Calculates the test set observed
        self.test = self.time_series[x_hat * -1:]
        
		# Calculates the total error
        self.err = self.err_predict(self.test, self.fitted)
        result.append(self.err)
        
        # Calculates forecast based on periods ahead
        i = 0
        y = self.time_series[:]
        while i < self.h:
            op = sum(y[-self.f:]) / self.f
            ov = sum(y[-half_seas:]) / half_seas
            ow = (op + ov) / 2
            y.append(ow)
            i += 1
        del y[:self.series_len]
        self.fcst = y   
        result.append(self.fcst)
        # appends true or false
        result.append(self.series_len >= allow)
        # Returns array with data
        return result

    def get_forecast(self, model):
        elem = 2
        x = eval('self.' + model + '()')
        return x[elem]

    def get_all_forecasts(self, model):
        elem = 2
        y = []
        for i in model:
            try:
                x = eval('self.' + i + '()')
                y.append(x[elem])
            except:
                pass    
        return y

    def eval_model(self, method):
        accuracy = 1
        try:
            if eval('self.' + method + '()[3]') == True:
                return eval('self.' + method + '()[' + str(accuracy) + ']')   
        except:
            pass
            #print("model {0} cannot be evaluated".format(method))
    
    def optimizer(self):
        models = {}

        for m in self.method_list:
            x = len(self.TRAINING_SET)
            y =[]
            i = 0
			
            while i < x:
                self.po = i
                y.append(self.eval_model(m))
                i += 1
            models[m] = y
        del y
        return models

    def best_model(self):
        best = {}
        model = self.optimizer()
		
        for k, v in model.items():
            try:
                best[k] = sum(v) / len(v)
            except:
                pass

        min_v = min(best.values())
        return ''.join([k for k, v in best.items() if v == min_v])
