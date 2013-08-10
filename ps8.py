# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances=resistances
        self.mutProb=mutProb

        # TODO



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]
        # TODO

    def isResistantToAll (self, drugList):
        """ Helper function that checks if virus is resistant to all the drugs
            in drugList """
        for drug in drugList:
            if not self.isResistantTo(drug):
                return False
        return True
    
    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        ##check for resistances
        ##if anything returns false raise exception
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()

        prob = random.random()
        if prob < self.maxBirthProb * (1 - popDensity):

            childResistances = {}
            for drug in self.resistances.keys():
                resistanceProb = random.random()
                if resistanceProb < self.mutProb:
                    childResistances[drug] = not self.resistances[drug]
                else:
                    childResistances[drug] = self.resistances[drug]
                    
            child = ResistantVirus(self.maxBirthProb, self.clearProb, childResistances,self.mutProb)
            return child
        else:
            raise NoChildException()

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        
        SimplePatient.__init__(self, viruses, maxPop)
        self.activeDrugs=[]
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.activeDrugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        numResistantViruses = 0
        for virus in self.viruses:
            if virus.isResistantToAll(drugResist):
                numResistantViruses += 1

        return numResistantViruses
            
                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        survivedViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                survivedViruses.append(virus)

        popDensity = float(len(survivedViruses)) / self.maxPop
        self.viruses = survivedViruses

        childViruses = []

        for virus in self.viruses:
            childViruses.append(virus)
            try:
                child = virus.reproduce(popDensity, self.activeDrugs)
                childViruses.append(child)
            except NoChildException:
                pass

        self.viruses = childViruses
        return self.getTotalPop()


#
# PROBLEM 2
#

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,mutProb, numTrials):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    totalViruses = None
    resistantViruses = None

    for i in xrange(0, numTrials):
        print 'iteration: ' + str(i)
        #print "running trial", i
        (total, resistant) = runDrugSimulation(numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb,150, 300)
        if totalViruses == None:
            totalViruses = total
            resistantViruses = resistant
        else:
            for j in xrange(0, len(total)):
                totalViruses[j] += total[j]
                resistantViruses[j] += resistant[j]
    
    for i in xrange(0, len(totalViruses)):
        totalViruses[i] /= float(numTrials)
        resistantViruses[i] /= float(numTrials)

    pylab.plot(xrange(0, len(totalViruses)), totalViruses, label = "Total")
    pylab.plot(xrange(0, len(totalViruses)), resistantViruses,label = "ResistantVirus")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc = "best")
    pylab.show()


#
# PROBLEM 3
#        
def runDrugSimulation (numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps):
    """ Helper function for doing one actual simulation run with drug applied """

    assert numStepsBeforeDrugApplied <= totalNumSteps
    
    viruses = []

    for i in xrange(0, numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances,mutProb))

    patient = Patient(viruses, maxPop)

    numVirusesEachStep = []
    numResistantVirusesEachStep = []
    for i in xrange(0, totalNumSteps):
        if i == numStepsBeforeDrugApplied:
            patient.addPrescription("guttagonol")
        numVirusesEachStep.append(patient.update())
        numResistantVirusesEachStep.append(patient.getResistPop(["guttagonol"]))
    
    return (numVirusesEachStep, numResistantVirusesEachStep)

def simulationWithDrugDelay(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps,numTrials):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    totalViruses = None
    resistantViruses = None

    for i in xrange(0, numTrials):
        print 'iteration: ' + str(i)
        #print "running trial", i
        (total, resistant) = runDrugSimulation(numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb,numStepsBeforeDrugApplied, totalNumSteps)
        
        if totalViruses == None:
            totalViruses = total
            resistantViruses = resistant
        else:
            for j in xrange(0, len(total)):
                totalViruses[j] += total[j]
                resistantViruses[j] += resistant[j]
    print 'len totalVirus: ' + str(len(totalViruses))
    for i in xrange(0, len(totalViruses)):
        totalViruses[i] /= float(numTrials)
        resistantViruses[i] /= float(numTrials)

    pylab.plot(xrange(0, len(totalViruses)), totalViruses, label = "Total")
    pylab.plot(xrange(0, len(totalViruses)), resistantViruses,label = "ResistantVirus")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc = "best")
    pylab.show()


def simulationWithDrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps,numTrials):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    virii=[]
    for i in xrange(0, numTrials):
        print 'iteration: ' + str(i)
        #print "running trial", i
        (total, resistant) = runDrugSimulation(numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb,numStepsBeforeDrugApplied, totalNumSteps)
        virii.append(total[totalNumSteps-1])
    
    return virii
    
def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, totalNumSteps,numTrials):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO
    v1_stddev=0
    v2_stddev=0
    v3_stddev=0
    v4_stddev=0
    v1=simulationWithDrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 300,totalNumSteps,numTrials)
    v2=simulationWithDrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 150,totalNumSteps,numTrials)
    v3=simulationWithDrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 75,totalNumSteps,numTrials)
    v4=simulationWithDrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 0,totalNumSteps,numTrials)
    v1_mean=float(sum(v1))/float(len(v1))
    v2_mean=float(sum(v2))/float(len(v2))
    v3_mean=float(sum(v3))/float(len(v3))
    v4_mean=float(sum(v4))/float(len(v4))
    for i in xrange(0,len(v1)):
        v1_stddev+=(v1_mean-v1[i])**2
        v2_stddev+=(v2_mean-v2[i])**2
        v3_stddev+=(v3_mean-v3[i])**2
        v4_stddev+=(v4_mean-v4[i])**2
    v1_stddev=(v1_stddev/float(len(v1)))**.5
    v2_stddev=(v2_stddev/float(len(v2)))**.5
    v3_stddev=(v3_stddev/float(len(v3)))**.5
    v4_stddev=(v4_stddev/float(len(v4)))**.5
    if v1_mean>(1e-6):
        v1_cov=v1_stddev/v1_mean
    else:
        v1_cov=None
    if v2_mean>(1e-6):
        v2_cov=v2_stddev/v2_mean
    else:
        v2_cov=None
    if v3_mean>(1e-6):
        v3_cov=v3_stddev/v3_mean
    else:
        v3_cov=None
    if v4_mean>(1e-6):
        v4_cov=v4_stddev/v4_mean
    else:
        v4_cov=None
    
    print '0 delay mean: ' + str(v4_mean)
    print '0 delay stddev: ' + str(v4_stddev)
    print '0 delay cov: ' + str(v4_cov)
    print '75 delay mean: ' + str(v3_mean)
    print '75 delay stddev: ' + str(v3_stddev)
    print '75 delay cov: ' + str(v3_cov)
    print '150 delay mean: ' + str(v2_mean)
    print '150 delay stddev: ' + str(v2_stddev)
    print '150 delay cov: ' + str(v2_cov)
    print '300 delay mean: ' + str(v1_mean)
    print '300 delay stddev: ' + str(v1_stddev)
    print '300 delay cov: ' + str(v1_cov)
   
    
    
    pylab.subplot(1,4,1)
    pylab.hist(v1,12,(0,600))
    pylab.title("Delay 300")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,2)
    pylab.hist(v2,12,(0,600))
    pylab.title("Delay 150")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,3)
    pylab.hist(v3,12,(0,600))
    pylab.title("Delay 75")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,4)
    pylab.hist(v4,12,(0,600))
    pylab.title("Delay 0")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.show()
    
#
# PROBLEM 4
#

def run2DrugSimulation (numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps):
    """ Helper function for doing one actual simulation run with drug applied """

    assert numStepsBeforeDrugApplied <= totalNumSteps
    
    viruses = []

    for i in xrange(0, numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances,mutProb))

    patient = Patient(viruses, maxPop)

    numVirusesEachStep = []
    guttagonolNumResistantVirusesEachStep = []
    grimpexNumResistantVirusesEachStep = []
    allNumResistantVirusesEachStep = []
    for i in xrange(0, totalNumSteps):
        if i == 150:
            patient.addPrescription("guttagonol")
        if i == (numStepsBeforeDrugApplied+150):
            patient.addPrescription("grimpex")
        numVirusesEachStep.append(patient.update())
        guttagonolNumResistantVirusesEachStep.append(patient.getResistPop(["guttagonol"]))
        grimpexNumResistantVirusesEachStep.append(patient.getResistPop(["grimpex"]))
        allNumResistantVirusesEachStep.append(patient.getResistPop(["guttagonol","grimpex"]))
    
    return (numVirusesEachStep, guttagonolNumResistantVirusesEachStep,grimpexNumResistantVirusesEachStep,allNumResistantVirusesEachStep)

def simulationWith2DrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps,numTrials):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    virii=[]
    for i in xrange(0, numTrials):
        print 'iteration: ' + str(i)
        #print "running trial", i
        (total, gur,grr,tr) = run2DrugSimulation(numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb,numStepsBeforeDrugApplied, totalNumSteps)
        virii.append(total[totalNumSteps-1])
    
    return virii

def simulation2DrugDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    numTrials=30
    numViruses=100
    maxPop=1000
    maxBirthProb=0.1
    clearProb=0.05
    resistances={'guttagonol':False, 'grimpex':False}
    mutProb=0.005
    # TODO
    v1_stddev=0
    v2_stddev=0
    v3_stddev=0
    v4_stddev=0
    v1=simulationWith2DrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 300,600,numTrials)
    v2=simulationWith2DrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 150,450,numTrials)
    v3=simulationWith2DrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 75,225,numTrials)
    v4=simulationWith2DrugDelayHist(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 0,300,numTrials)
    v1_mean=float(sum(v1))/float(len(v1))
    v2_mean=float(sum(v2))/float(len(v2))
    v3_mean=float(sum(v3))/float(len(v3))
    v4_mean=float(sum(v4))/float(len(v4))
    for i in xrange(0,len(v1)):
        v1_stddev+=(v1_mean-v1[i])**2
        v2_stddev+=(v2_mean-v2[i])**2
        v3_stddev+=(v3_mean-v3[i])**2
        v4_stddev+=(v4_mean-v4[i])**2
    v1_stddev=(v1_stddev/float(len(v1)))**.5
    v2_stddev=(v2_stddev/float(len(v2)))**.5
    v3_stddev=(v3_stddev/float(len(v3)))**.5
    v4_stddev=(v4_stddev/float(len(v4)))**.5
    if v1_mean>(1e-6):
        v1_cov=v1_stddev/v1_mean
    else:
        v1_cov=None
    if v2_mean>(1e-6):
        v2_cov=v2_stddev/v2_mean
    else:
        v2_cov=None
    if v3_mean>(1e-6):
        v3_cov=v3_stddev/v3_mean
    else:
        v3_cov=None
    if v4_mean>(1e-6):
        v4_cov=v4_stddev/v4_mean
    else:
        v4_cov=None
    
    print '0 delay mean: ' + str(v4_mean)
    print '0 delay stddev: ' + str(v4_stddev)
    print '0 delay cov: ' + str(v4_cov)
    print '75 delay mean: ' + str(v3_mean)
    print '75 delay stddev: ' + str(v3_stddev)
    print '75 delay cov: ' + str(v3_cov)
    print '150 delay mean: ' + str(v2_mean)
    print '150 delay stddev: ' + str(v2_stddev)
    print '150 delay cov: ' + str(v2_cov)
    print '300 delay mean: ' + str(v1_mean)
    print '300 delay stddev: ' + str(v1_stddev)
    print '300 delay cov: ' + str(v1_cov)
   
    
    
    pylab.subplot(1,4,1)
    pylab.hist(v1,12,(0,600))
    pylab.title("Delay 300")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,2)
    pylab.hist(v2,12,(0,600))
    pylab.title("Delay 150")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,3)
    pylab.hist(v3,12,(0,600))
    pylab.title("Delay 75")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.subplot(1,4,4)
    pylab.hist(v4,12,(0,600))
    pylab.title("Delay 0")
    pylab.xlabel("final virus count")
    pylab.ylabel("# viruses")
    ##pylab.legend(loc = "best")
    pylab.show()
#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO
def simulationTwoDrugsDelayedTreatment(numStepsBeforeDrugApplied):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    numTrials=30
    numViruses=100
    maxPop=1000
    maxBirthProb=0.1
    clearProb=0.05
    resistances={'guttagonol':False, 'grimpex':False}
    mutProb=0.005
    totalNumSteps=numStepsBeforeDrugApplied+300
    # TODO
    totalViruses = None
    resistantGuttangonol = None
    resistantGrimpex = None
    resistantAll = None

    for i in xrange(0, numTrials):
        print 'iteration: ' + str(i)
        #print "running trial", i
        (total, gur,grr,ar) = run2DrugSimulation(numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb,numStepsBeforeDrugApplied, totalNumSteps)
        
        if totalViruses == None:
            totalViruses = total
            resistantGuttangonol = gur
            resistantGrimpex = grr
            resistantAll = ar
        else:
            for j in xrange(0, len(total)):
                totalViruses[j] += total[j]
                resistantGuttangonol[j] += gur[j]
                resistantGrimpex[j] += grr[j]
                resistantAll[j] += ar[j]
    print 'len totalVirus: ' + str(len(totalViruses))
    for i in xrange(0, len(totalViruses)):
        totalViruses[i] /= float(numTrials)
        resistantGuttangonol[i] /= float(numTrials)
        resistantGrimpex[i] /= float(numTrials)
        resistantAll[i] /= float(numTrials)

    pylab.plot(xrange(0, len(totalViruses)), totalViruses, label = "Total")
    pylab.plot(xrange(0, len(totalViruses)), resistantGuttangonol,label = "ResistantGuttangonol")
    pylab.plot(xrange(0, len(totalViruses)), resistantGrimpex,label = "ResistantGrimpex")
    pylab.plot(xrange(0, len(totalViruses)), resistantAll,label = "ResistantAll")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc = "best")
    pylab.show()    

def simulationTwoDrugsDelayedTreatmentBatch():
    simulationTwoDrugsDelayedTreatment(300)
    simulationTwoDrugsDelayedTreatment(150)
    simulationTwoDrugsDelayedTreatment(75)
    simulationTwoDrugsDelayedTreatment(0)



