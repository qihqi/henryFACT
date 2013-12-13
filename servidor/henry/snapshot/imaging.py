
from snapshot.models import *
from snapshot.heavylifter import *
from django.http import HttpResponse, HttpResponseRedirect, Http404

class holder:
    pass
def plot_date_cant(dates, cants, desde, hasta):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    
    except ImportError as x:
        print x, type(x)
        y = holder()
        y.savefig = lambda self, x, y : None
        return y 
        

    fmt = mdates.DateFormatter("%Y-%m-%d")
    locator = mdates.DayLocator(interval=7)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, cants, "ro-")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    ax.set_xlim(desde, hasta)
    ax.format_xdata = fmt
    ax.grid(True)
    fig.autofmt_xdate()
    return fig


def prod_date_sale(request, codigo, bodega, desde, hasta, row, row2='fecha_float'):
    desde = parse_date(desde)
    hasta = parse_date(hasta)

    todos = Snapshot.objects.filter(prod_id=codigo,
                                    bodega_id=int(bodega),
                                    fecha__range=(desde, hasta))
    dates = []
    cants = []
    print todos.count()
    for x in todos:
        dates.append(getattr(x, row2))
        cants.append(getattr(x,row))
        print x.fecha, x.cant

    fig = plot_date_cant(dates, cants, desde, hasta)

    response = HttpResponse(mimetype='image/png')
    fig.savefig(response, format='png')
    return response


