#numpy for doing math
import numpy as np

#matplotlib for plotting
import matplotlib.pyplot as plt

#scipy for more 'science' functions, in this case curve fitting
from scipy.optimize import curve_fit
from scipy import stats


#we need the following package to allow colab to access files on our computer
# from google.colab import files

def chisquare(data,model,uncertainty):
    '''
    Calculates value of chi squared for model given data and unvertainty

    Parameters
    ----------
    data : numpy array
            1D vector of data values

    model : numpy array
            1D vector of values predicted by model

    uncertainty : numpy array
            1D vector of uncertainty corresponding to data

    Returns
    -------
    x2 : float
       Returns value of chi squared for this model given data and uncertainty
    '''

    x2 = np.sum((data-model)**2/uncertainty**2)

    return x2


def mycurvefit(func,XX,YY,UNCERT,xlabel=None,ylabel=None,p0=None,title=None,plot=False):
    '''
    Fits data (XX, YY, UNCERT) to function using scipy.curvefit, and then plots data and best fit
        Parameters
    ----------
    func : user-defined function
            Model to be used to fit data

    XX : numpy array
            1D vector of data's independent variable

    YY : numpy array
            1D vector of data's dependent variable

    UNCERT : numpy array
            1D vector of uncertainty in YY

    xlabel: string
            label for plot's x-axis

    ylabel : string
            label for plot's y-axis

    Returns
    -------
    fitparams : numpy array
           1D array of best fit values of parameters

    fiterrs : numpy array
            1D array of errors on best fit parameters (taken from sqrt of diag of covariance matrix)


    '''

    ##################################################
    #                Do the curve fit                #
    ##################################################


    # To get curve_fit to use UNCERT, set absolute_sigma = True.  Otherwise sigma = 1
    fitparams,pcov = curve_fit(func,XX,YY,sigma = UNCERT,absolute_sigma=True, p0=p0)

    # Find error in each parameter.  Assumes covariance matrix is roughly diagonal.
    fiterrs = np.sqrt(np.diag(pcov))

    # print out the parameters and errors on them
    print('Best Fit Parameters:\n')
    if xlabel:
        print('\t Independent Variable: ' + xlabel)
    if ylabel:
        print('\t Dependent Variable: ' + ylabel)
    if title:
        print('\t Model: ' + title)
    i = 0
    for A,sigA in zip(fitparams, fiterrs):
        i = i +1
        mystring = '\t P' + str(i) + ' = '
        print(mystring,round(A,5),'+/-',round(sigA,5))



    ##################################################
    #                Begin Plotting                  #
    ##################################################

    if plot:

        fig,ax = plt.subplots()
        fig.set_size_inches(10,6)

        # plot the raw data
        ax.errorbar(XX,YY,UNCERT,fmt='.',label='Data', color='#3498db', zorder=1)

        # plot the fit
        XX_shade = np.linspace(min(XX),max(XX),100)
        ax.plot(XX_shade,func(XX_shade,*fitparams),label = 'Best Fit', color='#F26363', linewidth=2, linestyle='--', zorder=2)

        if xlabel == None:
            xlabel = ''
        if ylabel == None:
            ylabel = ''

        # make the plot nice
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)     
        plt.legend()

        # make x and y labels bold and size 12
        ax.xaxis.label.set_size(12)
        ax.yaxis.label.set_size(12)
        ax.xaxis.label.set_weight('bold')
        ax.yaxis.label.set_weight('bold')

        # add title
        if title:
             ax.set_title(title)

        # add a gray dashed grid in the background
        plt.grid(axis = "both", color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.gca().set_axisbelow(True)

    ##################################################
    #    Calculate and display the fit metrics       #
    ##################################################

    # calculate the number of degrees of freedom
    shape = np.shape(XX)
    dof = shape[0] - len(fitparams)

    print('\n Fit Metrics:\n')
    print('\t Degrees of freedom (N-d): ', dof)

    X2 = chisquare(YY,func(XX,*fitparams),UNCERT)
    #X2string = '\t Chi Squared = ' + str(round(X2,1))
    X2redstring = '\t Reduced Chi Squared = '+ str(round(X2/dof,3))
    #print(X2string)
    print(X2redstring + '\n')

    return fitparams,fiterrs

#to calculate a 2-tailed p-value from a s.s. value call the function pvalue_1tailed (whose input is an s.s. value)
def get_pvalue(ss_value):
    #print('p-value:', stats.norm.sf(abs(ss_value)))
    return 2*stats.norm.sf(abs(ss_value))

def gaussian_profile(x, mean, std):
  return 1/np.sqrt(2*np.pi*std**2)*np.exp(-1/2*(x-mean)**2/std**2)

def compare_data_to_model_plot(measurements, theory, theory_err):

  fig, ax = plt.subplots()
  ax.hist(measurements, density = True, color='blue', alpha = 0.5, label = 'data')
  ylimits = ax.get_ylim()
  #ax.vlines(theory, *ylimits, 'r', linestyle='--', label = 'prediction')
  #ax.axvspan(theory - theory_err, theory + theory_err, color='red', alpha= 0.5)

  ax.errorbar(theory,gaussian_profile(measurements.mean(), measurements.mean(), measurements.std()),
              xerr =theory_err, markersize = 16, fmt = '.r', capsize=8,
              label = 'prediction')


  ax.set_ylim(*ylimits)

  xlimits =ax.get_xlim()
  xplot = np.linspace(*xlimits)
  gaus_meas = gaussian_profile(xplot, measurements.mean(), measurements.std())
  ax.plot(xplot, gaus_meas, '--k', alpha=0.75, label = 'distribution of data')
  ax.errorbar(measurements.mean(), gaus_meas.max(), xerr = measurements.std()/np.sqrt(len(measurements)), markersize = 16, fmt = '.k', capsize=8)

  ax.set_xlim(*xlimits)

  ax.legend()
  return