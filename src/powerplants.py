#! /usr/bin/env python

import models

class Photovoltaic:
    def __init__( self, nominal_power
                , model = models.Photovoltaic(
                    [ "latitude", "longitude", "module_name", "azimuth"
                    , "tilt" , "parallelStrings", "seriesModules", "albedo"])
                , **attributes):
        """
        Unless you override the default model, the following attributes are
        required:

          blablab...

        Should you opt to override the default model, the model parameter
        is expected to have a property called 'required' containing a list
        of parameters required for the model to calculate the feed.
        Calculating the powerplants feed then calls into the model with the
        given parameters. """
        self.nominal_power = nominal_power
        self.model = model
        for k in attributes: setattr(self, k, attributes[k])
        for k in model.required:
            if not hasattr(self, k):
                raise AttributeError(
                    "Your model requires {k}".format(k = k) +
                    " but it's not provided as an argument."
                )

    @property
    def feedin(self):
        return list(self.model.feedin(**{k: getattr(self, k)
                                         for k in self.model.required}))

class Wind: pass

if __name__ == "__main__":

    pv_plant = Photovoltaic(0,
            latitude = 52.52437,
            longitude = 13.41053,
            module_name = 'Advent_Solar_Ventura_210___2008_',
            azimuth = 0,
            tilt = 30,
            parallelStrings = 1,
            seriesModules = 1,
            albedo = 0.2)
    

    class ConstantModell:
        def __init__(self, required = ["nominal_power", "steps"]):
          self.required = required
        def feedin(self, **ks): return [ks["nominal_power"]] * ks["steps"]
    
    pvc = Photovoltaic(nominal_power = 100000000, steps = 3, model = ConstantModell())
    pvc2 = Photovoltaic(nominal_power = 100000000, steps = 3, model = models.ConstantModell())
    # pv_plant.weather = oemof.geolib.weather(pv_plant)
    # or
    # pv_plant.get_my_weatherdata(mode = "standard_database")


    # oemof.timeseries_plot(my_pv_plant.feedin)
    # We don't have a plotter so just mock stuff by printing.
    print(pv_plant.feedin)
    print()
    print(pvc.feedin)
    print()
    print(pvc2.feedin)

