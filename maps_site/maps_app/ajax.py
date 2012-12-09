from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def request_points(request):
    dajax = Dajax()
    points = [
        {'lat':37.41444798751896, 'lng':-122.0916223526001, 'text':'Some Site #1'},
        {'lat':37.412061929307924, 'lng':-122.08582878112793, 'text':'Other Site #2'},
        {'lat':37.41301636171327, 'lng':-122.0780611038208, 'text':'Other Site #3'}]

    dajax.add_data(points, 'example_draw_points')
    dajax.assign('#example_log', 'value', "it works")
    return dajax.json()


@dajaxice_register
def move_point(request, lat, lng):
    dajax = Dajax()
    message = "Saved new location at, %s, %s" % (lat, lng)
    dajax.assign('#example_log', 'value', message)
    return dajax.json()
