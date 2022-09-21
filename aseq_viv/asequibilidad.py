import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def subclasificacion_estrato(ref, lim_inf, lim_sup, n):
    '''
    Clasifica estratos de ingresos.

    Args
    ----
    ref (int): precio de referencia
    lim_inf (int): monto de limite inferior
    lim_sup (int): monto del limite superior
    n (int): cantidad de cortes
    ...
    Returns
    dict: limite superior del rango y porcentaje que representa
          sobre el valor de referencia
    '''
    r = np.array_split(range(lim_inf,lim_sup), n)
    lims = []
    for i in range(len(r)):
        lim_sup = r[i][-1]
        lims.append(lim_sup)

    out = {}
    for l in lims:
        out[l] = round(l/ref,2)
    return out

def auc_asequible(estrato_bajo, estrato_medio, estrato_alto, ylabel='Monto alquiler (1 amb)'):
    '''
    Calcula el área de cobertura/asequibilidad para distintos estratos de ingresos.

    Args
    ----
    estrato_bajo (dict): punto de corte y porcentaje que representan sobre un precio de referencia
    estrato_medio (dict): punto de corte y porcentaje que representan sobre un precio de referencia
    estrato_alto (dict): punto de corte y porcentaje que representan sobre un precio de referencia
                         (e.g. {50,000: 0.3}
    ylabel (str): nombre del eje y
    ...
    Returns
    dict: limite superior del rango y porcentaje que representa
          sobre el valor de referencia.
    '''
    estrato_bajo_qcut = list(estrato_bajo.keys())
    estrato_medio_qcut = list(estrato_medio.keys())
    estrato_alto_qcut = list(estrato_alto.keys())

    alquiler = [0]
    ingresos = [0]

    for e in (estrato_bajo, estrato_medio, estrato_alto):
        for k,v in e.items():
            ingresos.append(k)
            alquiler.append(v)

    f, ax = plt.subplots(figsize=(12,4))
    alquiler_pct = [int(i*100) for i in alquiler]
    ax.fill_between(ingresos,#alquiler_pct,
                    alquiler_pct,#ingresos,
                    color='lightgray', alpha=0.4)

    for pos in ['left', 'right', 'top', 'bottom']:
        ax.spines[pos].set_visible(False)

    # axis label
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Ingresos ($ARS)')

    # axis ticks format
    x_value=['$'+'{:,.0f}'.format(x) for x in ax.get_xticks()]
    ax.set_xticklabels(x_value)
    y_value=['{:,.0f}'.format(x) + '%' for x in ax.get_yticks()]
    ax.set_yticklabels(y_value)

    # references
    props = dict(boxstyle='round', facecolor='#4e2c76', alpha=0.8)
    ax.axvline(estrato_bajo_qcut[-1], color="#07cdd8", linewidth=0.5)
    ax.annotate('Bajos (≤ 1 CBT)', xy=(estrato_bajo_qcut[-1]/2, 275), xycoords='data', bbox=props, color='white', ha='right')

    ax.axvline(estrato_medio_qcut[-1], color='#fed547', linewidth=0.5)
    estrato_medio_pos = np.median(range(estrato_bajo_qcut[-1], estrato_medio_qcut[-1]))
    ax.annotate('Medios (1 - 3,5 CBT)', xy=(estrato_medio_pos, 275), xycoords='data', bbox=props, color='white', ha='center')

    estrato_alto_pos = np.median(range(estrato_medio_qcut[-1], estrato_alto_qcut[-1]))
    ax.annotate('Altos (> 3,5 CBT)', xy=(estrato_alto_pos, 275), xycoords='data', bbox=props, color='white', ha='center')

    ax.axhline(100, color='black', linestyle='--', linewidth=0.75)
    ax.yaxis.labelpad = 20
    ax.xaxis.labelpad = 20

def pct_asequible(estrato_bajo, estrato_medio, estrato_alto, ref, tipologia, ylabel):
    '''
    Calcula el el porcentaje que representa un precio de referencia para los
    distintos estratos de ingresos.

    Args
    ----
    estrato_bajo (dict): punto de corte y porcentaje que representan sobre un precio de referencia
    estrato_medio (dict): punto de corte y porcentaje que representan sobre un precio de referencia
    estrato_alto (dict): punto de corte y porcentaje que representan sobre un precio de referencia
                         (e.g. {50,000: 0.3}
    ref(int): precio de referencia
    tipologia(str): nombre de la tipologia del precio de referencia
    ylabel (str): nombre del eje y
    ...
    Returns
    dict: limite superior del rango y porcentaje que representa
          sobre el valor de referencia.
    '''
    # valores
    bajo = [list(estrato_bajo.keys())[-1]]
    medio = list(estrato_medio.keys())
    alto = [list(estrato_alto.keys())[-1]]
    x = bajo + medio + alto
    y = list(np.repeat(ref, len(x)))

    # etiquetas eje x
    ingresos = ['I1']
    c = 1
    for e in list(estrato_medio.keys()):
        c+=1
        ingresos.append('I{}'.format(c))
    ingresos.append('I{}'.format(c+1))

    # ingreso restante despues de pagar alquiler
    ing_res = [round((ref/i)*100,1) for i in x]
    ind = np.arange(len(x))

    fig, ax = plt.subplots(figsize=(12,4))
    ax.bar(x=ind, height=x, width=0.55, color='#07cdd8', align='center')
    ax.bar(x=ind, height=y, width=0.55/2,  color='#fed547', align='center')

    # anotaciones
    props = dict(boxstyle='round', facecolor='#4e2c76', alpha=0.8)
    for i in range(len(ing_res)):
        ax.annotate('{}%'.format(ing_res[i]), xy=(i, ref/2), xycoords='data', bbox=props, color='white', ha='center')
        label = round(100-ing_res[i],1)
        if label < 0:
            pos = ref
        else:
            pos = x[i] - x[i]*0.15
        ax.annotate('{}%'.format(label), xy=(i, pos), xycoords='data', bbox=props, color='white', ha='center')

    ax.annotate('{}'.format(tipologia),
                xy=(-0.3, ref+(ref*0.01)),
                xycoords='data',
                xytext =  (-0.4, ref+(ref*0.5)),
                textcoords='data',
                arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))

    # ejes
    for pos in ['right', 'top']:
        ax.spines[pos].set_visible(False)

    ax.yaxis.labelpad = 20
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Ingresos ($ARS)')
    ax.xaxis.labelpad = 20

    x_value=[l+' - (${:,})'.format(x[idx]) for idx,l in enumerate(ingresos)]
    plt.xticks(ind, x_value)
    y_value=['$'+'{:,.0f}'.format(x) for x in ax.get_yticks()]
    ax.set_yticklabels(y_value)

    # referencias
    ax.axhline(ref, color='black', linestyle='--', linewidth=0.75)

    dis = [i-ref for i in x]
    for idx,d in enumerate(dis):
        if d < 0:
            ax.vlines(x=[idx + .2], ymin=x[idx], ymax=ref, colors='r', ls=':', lw=2, label='vline_single - full height')
        else:
            ax.vlines(x=[idx + .2], ymin=ref, ymax=x[idx], colors='w', ls=':', lw=2, label='vline_single - full height')
