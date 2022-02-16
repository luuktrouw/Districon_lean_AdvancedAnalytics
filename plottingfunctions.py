import plotly.express as px


def plotworkstates_fractions_staalbuigen(work_state_times):
    workstates_staalbuigen = []
    values_staalbuigen = []
    totalvaluesstaalbuigen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalbuigen.append(i)
        values_staalbuigen.append(work_state_times[i]/totalvaluesstaalbuigen)
    fig1 = px.bar(dict(workstates_staalbuigen = workstates_staalbuigen, values_staalbuigen =values_staalbuigen), x='workstates_staalbuigen', y='values_staalbuigen')
    fig1.show()

def plotworkstates_fractions_staalkoppelen(work_state_times):
    workstates_staalkoppelen = []
    values_staalkoppelen = []
    totalvaluesstaalkoppelen = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_staalkoppelen.append(i)
        values_staalkoppelen.append(work_state_times[i]/totalvaluesstaalkoppelen)
    fig2 = px.bar(dict(workstates_staalkoppelen = workstates_staalkoppelen, values_staalkoppelen =values_staalkoppelen), x='workstates_staalkoppelen', y='values_staalkoppelen')
    fig2.show()

def plotworkstates_fractions_omhulselmaken(work_state_times):
    workstates_omhulselmaken = []
    values_omhulselmaken = []
    totalvaluesomhulselmaken = sum(work_state_times.values())
    for i in work_state_times.keys():
        workstates_omhulselmaken.append(i)
        values_omhulselmaken.append(work_state_times[i]/totalvaluesomhulselmaken)
    fig3 = px.bar(dict(workstates_omhulselmaken = workstates_omhulselmaken, values_omhulselmaken =values_omhulselmaken), x='workstates_omhulselmaken', y='values_omhulselmaken')
    fig3.show()

def wachttijd_voor_staal_buigen(finishedorders):
    wachttijd_lijst = []
    for i in range(len(finishedorders)):
        wachttijd_lijst.append(finishedorders[i]['tijd inventory staal buigen'])
    fig4 = px.histogram(dict(wachttijd_lijst = wachttijd_lijst), x = 'wachttijd_lijst')
    fig4.show()

