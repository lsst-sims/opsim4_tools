from lsst.sims.ocs.configuration import ObservingSite
from ts_scheduler.observatoryModel import ObservatoryLocation

location = ObservatoryLocation()
location.configure({"obs_site": ObservingSite().toDict()})
