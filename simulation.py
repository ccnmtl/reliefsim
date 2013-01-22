#!/usr/bin/python
# ReliefSim Prototype programmed by Eric Mattes
# October 2006
version = "1.1"

import string
import time
import os
import os.path
import copy
from random import Random

g = Random()


class UI:
    """the user interface to the game."""
    def __init__(self, sim):
        self.shortcut = {
            "ap": AssessRefugeePopulation,
            "aw": AssessCampWaterSupplyDemand,
            "aq": AssessCampWaterQuality,
            "af": AssessRefugeeFoodSupplyDemand,
            "adm": AssessRefugeeMeasles,
            "adf": AssessRefugeeMalnourished,
            "adc": AssessRefugeeCholera,
            "add": AssessRefugeeDiarrhea,
            "ade": AssessRefugeeMeningitis,
            "ada": AssessRefugeeMalaria,
            "as": AssessCampLatrines,
            "iw": AddCampWaterQuantity,
            "iq": AddCampWaterQuality,
            "id": AddCampLatrineDefTrench,
            "ic": AddCampLatrineCommPit,
            "itf": SetUpSuppFeedingCenter,
            "if": AddCampFoodQuantity,
            "ad": AssessRefugeeMedicalProfile,
            "itm": TreatMeasles,
            "itc": TreatCholeraAndDiarrhea,
            "ite": TreatMeningitis,
            "ita": TreatMalaria,
            "ivm": VaccinateMeasles,
            "ivc": VaccinateCholera,
            "ive": VaccinateMeningitis
        }

        self.specialShortcut = {"endTurn": "endTurn", "unAssign": "unassign"}
        self.population = ""
        self.flag = "false"
        self.gaintHighlightedItems = ""
        self.systemTime = time.strftime("%m/%d")
        self.sim = sim
        self.messages = []  # a list of messages for the user to see
        self.known = {}  # dictionary for known info
        self.bd = {}  # dictionary for known info about population breakdown
        # 'gauges' and 'bdGauges' are for formatting classifications
        # and for putting '?' in for unknowns
        self.gauges = [
            "refugees.nutritionalDemand", "refugees.waterDemand",
            "camp.waterQuality", "camp.waterQuantity",
            "camp.solidWaste", "camp.latrinesDefTrench",
            "camp.foodQuantity", "camp.suppFeedingCenters",
            "camp.latrinesCommPit", "refugees.immMeasles",
            "refugees.immCholera", "refugees.immMeningitis"
        ]  # internal names for gauges/keys
        self.bdGauges = [
            "population", "cholera", "diarrhea", "measles", "malnourished",
            "meningitis", "malaria", "dead"
        ]  # population breakdown
        self.assembleMenuString()

    def assembleMenuString(self):
        """assembles the menu by filling in the gauges, team members,
        and message information"""
        self.newMenu = ""
        self.newStatus = ""
        self.newMessage = "Message: "

        # format the data from infoStore and store it into a 'local' dictionary
        for refcamp in ("refugees", "camp"):
            for k in getattr(self.sim.action.infoStore, refcamp).keys():
                temp = getattr(self.sim.action.infoStore, refcamp)[k]
                if (refcamp + "." + k) in self.gauges:
                    # the normal gauges
                    if type(temp) == float:
                        if float(temp) % 1000.0 == 0.0 and temp != 0:
                            temp = ("%(temp).0f" % vars())[:-3] + "k"
                        else:
                            temp = ("%(temp).2f") % vars()
                    elif type(temp) == int:
                        if float(temp) % 1000.0 == 0.0 and temp != 0:
                            temp = str(temp)[:-3] + "k"
                        else:
                            temp = str(temp)
                    self.known[refcamp + "." + k] = string.rjust(temp, 7)
                else:
                    # the population breakdown gauges
                    self.bd[k] = copy.deepcopy(temp)
                    for i in range(len(self.bd[k])):
                        self.bd[k][i] = string.rjust(str(self.bd[k][i]), 6)

        for k in self.gauges:
            # fill in unknown info with a '?'
            if k not in self.known.keys():
                self.known[k] = "?"
        for k in self.bdGauges:
            # fill in unknown info with a '?'
            if k not in self.bd.keys():
                self.bd[k] = ["?", "?", "?", "?"]
        self.infoGauge = (
            "foodQuantity:: " + self.known["camp.foodQuantity"]
            + "$$" + "waterQuantity:: "
            + self.known["camp.waterQuantity"]
            + "$$" + "nutritionalDemand:: "
            + self.known["refugees.nutritionalDemand"]
            + "$$" + "waterDemand:: "
            + self.known["refugees.waterDemand"]
            + "$$" + "solidWaste:: "
            + self.known["camp.solidWaste"]
            + "$$" + "waterQuality:: "
            + self.known["camp.waterQuality"]
            + "$$" + "latrinesCommPit:: "
            + self.known["camp.latrinesCommPit"]
            + "$$" + "suppFeedingCenters:: "
            + self.known["camp.suppFeedingCenters"]
            + "$$" + "latrinesDefTrench:: "
            + self.known["camp.latrinesDefTrench"])
        for bdName in ["population", "dead", "malnourished",
                       "cholera", "diarrhea", "malaria",
                       "measles", "meningitis"]:
            x = self.bd[bdName]
            self.newMenu += (bdName + ":: " + x[0] + "@@" + x[1] + "@@"
                             + x[2] + "@@" + x[3] + "$$")
        if(self.flag == "true"):
            self.population = (self.population + "$$"
                               + self.bd["population"][0]
                               + "@@" + self.bd["population"][1]
                               + "@@" + self.bd["population"][2]
                               + "@@" + self.bd["population"][3])
            self.tempTime = time.strptime(time.strftime("%Y-%m-%d %H:%M:%S"),
                                          "%Y-%m-%d %H:%M:%S")
            self.tempSysTime = time.mktime(self.tempTime)
            self.tempSysTime = (self.tempSysTime
                                + (3 * 24 * 60 * 60)
                                * (self.sim.probability.turn - 1))
            self.tempSysTime = time.strftime(
                "%m/%d",
                time.localtime(self.tempSysTime))
            self.systemTime = self.systemTime + "$$" + self.tempSysTime
        self.flag = "false"
        i = 1

        for x in self.sim.action.resource.personnel:
            temp = x.name + ':'
            self.newStatus += temp
            if x.getDaysBusy() != 0:
                self.newStatus += ("Busy " + x.task.statusText
                                   + " for " + str(x.getDaysBusy())
                                   + " more turn")
                if x.getDaysBusy() > 1:
                    self.newStatus += "s"
                self.newStatus += ": " + x.taskId
            else:
                self.newStatus += "available"
            self.newStatus += "@@"
            i += 1
        self.isPersonnelFree = "true"
        for x in self.sim.action.resource.personnel:
            if x.getDaysBusy() != 0:
                self.isPersonnelFree = "false"
            else:
                self.isPersonnelFree = "true"
                break
        if(self.isPersonnelFree == "false"):
            self.sim.action.infoStore.messages.append(self.isPersonnelFree)
        for x in self.sim.action.infoStore.messages:
            self.messages.append(x)
        for x in self.messages:
            self.newMessage += x + "\n"
        self.sim.action.infoStore.messages = []  # clear the infostore messages
        self.messages = []  # clear the interface messages
        self.newMenu += ("##" + self.newStatus + "##"
                         + self.newMessage + "##"
                         + self.infoGauge + "##"
                         + str(self.sim.probability.turn)
                         + "##" + self.population
                         + "##" + self.systemTime
                         + "##" + self.gaintHighlightedItems)

    def process(self, input):
        """ process the input by translating the keyboard
        shortcut into the corresponding command"""
        inputValue = (input).split("split")
        inputCommond = inputValue[0]
        userId = inputValue[1]
        self.processRequest(inputCommond, userId)

    def processRequest(self, inputCommond, userId):
        if inputCommond in self.specialShortcut.keys():
            if inputCommond.endswith("endTurn"):
                # execute the input command
                getattr(self.sim.action,
                        self.specialShortcut[inputCommond])()
                self.gaintHighlightedItems = (self.gaintHighlightedItems
                                              + "$$" + userId)
                self.sim.action.infoStore.messages.append(
                    "Your team members have performed their tasks and are "
                    "ready for new assignments. Be sure to check your "
                    "information gauges for new data, if necessary.")
                self.flag = "true"
            else:
                self.sim.action.unassign(userId)
        else:
            # assign a task to somebody in your personnel
            endAfterCommand = 0
            if inputCommond.endswith("endTurn"):
                endAfterCommand = 1
                inputCommond = inputCommond[:-1]  # cut off the '.'
            if inputCommond not in self.shortcut.keys():
                self.messages.append("Unrecognized command. Try again.")
            else:
                self.sim.action.assignTask(
                    self.shortcut[inputCommond], userId, inputCommond)
                if endAfterCommand == 1:
                    self.sim.action.endTurn()

    def exportHistory(self):
        """write the history data to a file"""
        # format:
        #  [ [[titles],[breakdownTitles],[personnelNames]], \
        #  ([data],[[bd1,bd2],...],[tasks]), ... ]
        t = time.localtime()
        hist = self.sim.action.infoStore.history
        fileName = "rs_hist%02u%02u%02u%02u%02u.txt" % (
            t[0], t[1], t[2], t[3], t[4])
        try:
            if not os.path.exists('history/'):
                os.mkdir('history')
            f = open('history/' + fileName, 'w+')
            # loop thru names of stat categories
            f.write("\t")
            (titles, bd, pn) = hist[0]
            for t in titles:
                f.write("%s\t" % (t))
            for cat in bd:
                f.write(
                    "Total %s\t%s Ages < 5\t%s Ages 5-14\t%s Ages 15+\t" % (
                        cat, cat, cat, cat))
            for p in pn:
                f.write("%s\t" % (p))
            f.write("\n")
            # write the data
            for turn in range(1, len(hist)):
                f.write("Turn %d\t" % (turn))
                (data, bd, tasks) = hist[turn]
                for stat in data:
                    if type(stat) == float:
                        f.write("%.2f\t" % (stat))
                    else:
                        f.write("%s\t" % (stat))
                for stat in bd:
                    for i in range(len(stat)):
                        temp = stat[i]
                        if type(temp) == float:
                            f.write("%.2f" % (temp))
                        else:
                            f.write("%s\t" % (temp))
                for task in tasks:
                    f.write("%s\t" % (task))
                f.write("\n")
            f.close()
        except OSError:
            print ("An error occurred. The history log "
                   "file could not be written.")

    def doEndGame(self):
        """do whatever needs to be done after the game ends"""
        self.exportHistory()
        print self.style(9)
        if self.sim.probability.gameOver == 1:
            print "Sorry, all of your refugees have died! Game over!\n"
        else:
            print "Thanks for playing!\n"
        print self.style(0)  # reset colors


class WebUI(UI):
    """ override some of the UI functionality for the web interface """
    def style(self, arg):
        return ""

    def doEndGame(self):
        data = self.exportHistory()
        dead = self.sim.probability.gameOver == 1
        return (dead, data)

    def exportHistory(self):
        # TODO: use actual csv module
        # format: [ [[titles],[breakdownTitles],[personnelNames]],
        #  ([data],[[bd1, bd2],...],[tasks]), ... ]
        t = time.localtime()
        hist = self.sim.action.infoStore.history
        from cStringIO import StringIO
        f = StringIO()
        # loop thru names of stat categories
        f.write(", ")
        (titles, bd, pn) = hist[0]
        for t in titles:
            f.write("%s," % (t))
        for cat in bd:
            f.write("Total %s,%s Ages < 5,%s Ages 5-14,%s Ages 15+, " % (
                    cat, cat, cat, cat))
        for p in pn:
            f.write("%s," % (p))
        f.write("\n")
        # write the data
        for turn in range(1, len(hist)):
            f.write("Turn %d," % (turn))
            (data, bd, tasks) = hist[turn]
            for stat in data:
                if type(stat) == float:
                    f.write("%.2f," % (stat))
                else:
                    f.write("%s," % (stat))
            for stat in bd:
                for i in range(len(stat)):
                    temp = stat[i]
                    if type(temp) == float:
                        f.write("%.2f" % (temp))
                    else:
                        f.write("%s," % (temp))
            for task in tasks:
                f.write("%s," % (task))
            f.write("\n")
        return f.getvalue()

######### END PRESENTATION/INTERFACE; BEGIN SIMULATION CODE ##########


class Simulation:
    """the mother-class for the simulation.
    Seperate from the presentation/interface."""
    def __init__(self):
        self.refugees = Refugees(self)
        self.camp = Camp(self)
        self.probability = Probability(self)
        self.action = Action(self)
        self.scenario = Scenario(self.action)


class Action:
    """contains the 'API' for interacting with the simulation"""
    def __init__(self, sim):
        self.resource = Resource()
        self.infoStore = InfoStore()
        self.sim = sim
        self.probability = self.sim.probability
        self.camp = self.sim.camp
        self.refugees = self.sim.refugees
        # auto-updating data is stuff that the user is entitled
        # to know every turn without assessing for it
        self.autoUpdating = [
            "camp.suppFeedingCenters",
            "refugees.immMeasles",
            "refugees.immCholera",
            "refugees.immMeningitis"]
        # hints are only given once, after which they turn into a 1
        self.hints = {"cholera": 0}

    def assignTask(self, task, userId, taskId):
        """try to assign a task to somebody on your personnel"""
        personnelObj = self.sim.action.resource.personnel

        userId = int(userId)
        if personnelObj[userId].task is None:
            # assign a new instance of the task
            personnelObj[userId].assign(task(self.sim))
            personnelObj[userId].taskId = taskId
        else:
            self.infoStore.messages.append(
                "No personnel are available to perform that task")

    def initHistory(self):
        """initialize the history data structure"""
        personnel = []
        for p in self.sim.action.resource.personnel:
            personnel.append(p.name)
        titles = [
            "General Health (avg)",
            "Nutritional Health (avg)",
            "Disease Health (avg)",
            "Symptomatic", "Sick",
            "Food Supply", "Avg Food Demand", "Supp. Feeding Centers",
            "Water Quality",
            "Water Supply", "Avg Water Demand", "Refugees w/o Latrines",
            "Defecation Trenches", "Community Pits"]
        bdTitles = [
            "Population", "Dead*", "Cholera", "Diarrhea", "Malaria",
            "Measles", "Meningitis", "Malnourished",
            "Died with Cholera*", "Died with Diarrhea*",
            "Died with both Cholera and Diarrhea*"]
        self.infoStore.history.append([titles, bdTitles, personnel])

    def storeHistory(self, camp, refugees):
        """load the current gamestate into the history list"""
        # THIS DOES NOT INCLUDE SPECIFIC ILLNESS DATA
        # AND SHOULD NOT BE USED TO SAVE THE GAMESTATE
        c = self.camp.data
        r = self.refugees.data
        data = []
        bd = []
        taskSelection = []
        for p in self.sim.action.resource.personnel:
            if p.task is None:
                taskSelection.append("None")
            else:
                taskSelection.append(p.task.statusText)
        for itemName in ("population", "dead", "cholera", "diarrhea",
                         "malaria", "measles", "meningitis",
                         "malnourished", "diedWithCholera",
                         "diedWithDiarrhea", "diedWithBothCDD"):
            item = r[itemName]
            bd.append([item[0], item[1], item[2], item[3]])
        data.extend([r["generalHealth"], r["nutritionalHealth"],
                     r["diseaseHealth"]])
        data.extend([r["symptomatic"], r["sick"]])
        data.extend([c["foodQuantity"], r["nutritionalDemand"],
                     c["suppFeedingCenters"]])
        data.extend([c["waterQuality"], c["waterQuantity"], r["waterDemand"]])
        data.extend([c["solidWaste"], c["latrinesDefTrench"],
                     c["latrinesCommPit"]])
        self.infoStore.history.append((data, bd, taskSelection))

    def updateInfoStore(self):
        """auto-update the infoStore to contain data the
        user is always supposed to know"""
        for i in self.autoUpdating:
            (c, a) = i.split(".")
            if c == "refugees":
                self.infoStore.refugees[a] = self.probability.getRefugees(a)
            elif c == "camp":
                self.infoStore.camp[a] = self.probability.getCamp(a)

############ BEGIN NON-TASK 'SPECIAL' COMMANDS ############

    def endTurn(self):
        """ends the turn"""
        self.probability.endTurn()

    def unassign(self, userId):
        """frees up a worker and cancels the task s/he was working on"""
        userId = int(userId)
        personnelObject = self.sim.action.resource.personnel
        # free up the person and 'cancel' the task
        personnelObject[userId].task = None

############### BEGIN TASK-HELPER COMMANDS ###########

    def choleraHint(self):
        """if there is cholera present, display a hint"""
        if (self.sim.refugees.data["cholera"][3] > 0
                and self.hints["cholera"] == 0):
            self.sim.action.infoStore.messages.append(
                "A 22-year-old man has died of dehydration")
            self.hints["cholera"] = 1

    def addDefTrenchExpiration(self, num):
        """set 'num' deftrenches to expire in the designated number of turns"""
        num = int(num[0])
        self.camp.defTrenchExpiration.append([self.camp.defTrenchLifespan,
                                              num])

    def revealLatrineInfo(self):
        """put latrine info in the infoStore. Happens when building latrines"""
        dummyAssessment = AssessLatrinesOnly(self.sim)  # create a fake task...
        dummyAssessment.do()  # and then execute it immediately

    def treatSickHelper(self, diseaseTuple):
        """distributes treatment among symptomatic sick people"""
        # this treats in the order they were infected... not entirely realistic
        # the number of people who can be treated in one turn by one person
        number = 2000
        dName = diseaseTuple[0]
        refugeesRef = self.refugees
        index = 0
        for r in refugeesRef.pop:
            if number > 0:
                if dName in r.symptoms and g.random() <= 0.70:
                    # 70% chance of successful removal
                    for d in r.diseases:
                        if d.name == dName:
                            refugeesRef.removeDisease(r, index, d)
                    number -= 1
            else:
                break  # we have treated the maximum number
            index += 1

    def treatWater(self):
        """treat the water quality. Effect wears off after a few turns"""
        self.sim.camp.treatments[0] += 1

    def vaccinate(self, diseaseTuple):
        """vaccinates some refugees against a disease"""
        dName = diseaseTuple[0]
        delay = diseaseTuple[1]  # immunity delay of this vaccine
        howMany = 2500
        remaining = howMany

        if dName == "measles":
            # measles vaccine treats as well as immunizes (permanent immunity)
            # kidsFirst ensures that children under 15 get their
            # measles vaccine before anyone else.
            kidsFirst = 1
            while (1):
                index = -1
                for r in self.refugees.pop:
                    index += 1
                    if ((r.age < 15 or kidsFirst == 0)
                            and "measles" not in r.immunized):
                        # give them permanent immunity:
                        r.immunized.append("measles")
                        remaining -= 1
                        #### TREATMENT ####
                        for d in r.diseases:
                            if d.name == "measles":
                                self.refugees.removeDisease(r, index, d)
                    if remaining <= 0:
                        break
                # if, after checking each child, we still have vaccines,
                # do this loop one more time and vaccinate adults
                if remaining > 0 and kidsFirst == 1:
                    kidsFirst = 0
                else:
                    break
        else:
            # not measles...
            for r in self.refugees.pop:
                if dName not in r.immunized:
                    # check for existing immunity
                    for x in r.immunityCountdown:
                        if x[1] == dName:
                            break  # check for pending immunity
                    else:
                        # if they are not immune and not pending immunity,
                        # vaccinate
                        r.immunityCountdown.append([delay, dName])
                        remaining -= 1
                if remaining <= 0:
                    break

        if remaining < howMany:
            # increment the vaccine counters
            statKey = "imm" + string.upper(dName[0]) + dName[1:]
            self.sim.refugees.data[statKey] += howMany - remaining

###### BEGIN SCRIPT-ONLY COMMANDS (take 1 string parameter) ######

    def addFood(self, num):
        """increases the daily food supply by the specified amount"""
        self.camp.data["foodQuantity"] += int(num)

    def addPersonnel(self, num):
        """add Personnel to your staff"""
        numExisting = len(self.resource.personnel)
        max = self.resource.maxPersonnel
        num = int(num)
        if numExisting + num > max:
            # are we going to go over the limit?
            if max - numExisting > 0:
                # if we can add some but not all of the requested staff...
                num = max - numExisting
            else:
                return  # can't add any more
        if num == 1:
            sentenceStarting = ""
            sentenceEnding = " person has joined your staff!"
        else:
            sentenceStarting = "Use your "
            sentenceEnding = (
                " staff members to protect and stabilize "
                "this camp population in as few turns as "
                "possible. Each turn is 3 days.<span "
                "class='welcomeMessage'>Select either an "
                "assessment or an intervention by clicking on it. Then click "
                "the \"ASSIGN\" button next to a member of your staff. "
                "When you have finished assigning tasks, have your team "
                "perform them by hitting the \"END TURN\" button.</span>")
        self.infoStore.messages.append(
            sentenceStarting + str(num) + sentenceEnding)
        for x in range(num):
            p = Personnel()
            self.resource.personnel.append(p)
            if self.probability.turn > 0:
                # append their name to the history header list
                self.infoStore.history[0][2].append(p.name)

    def addRefugees(self, num):
        """add refugees to the camp"""
        self.refugees.addRandomizedRefugees(num)  # pass along the task
        if num == 1:
            self.infoStore.messages.append(
                "New Refugees have joined your camp!")

    def addWater(self, num):
        """increases the daily water supply by the specified amount"""
        self.camp.data["waterQuantity"] += int(num)

    def feedingCenterMeaslesOutbreak(self):
        """ if this is our first feeding center, schedule a measles
        outbreak in two turns"""
        # +1 will make it happen at the END of the next turn.
        turn = self.sim.probability.turn + 1
        script = self.sim.scenario.script
        self.sim.camp.measlesOutbreak = 1
        if turn in script.keys():
            script[turn].append("measlesOutbreak 10")
        else:
            script[turn] = ["measlesOutbreak 10"]

    def measlesOutbreak(self, numCases):
        """cause an outbreak of measles in the lowest age bracket"""
        numCases = int(numCases)
        lenRef = len(self.refugees.pop)
        vector = Measles()
        # starting at the beginning, infect only those under 5,
        # stopping after numCases.
        for i in range(lenRef):
            person = self.refugees.pop[i]
            if person.age < 5:
                self.refugees.infect(i, vector)
                if numCases > 1:
                    numCases -= 1
                else:
                    break


############# END NON-TASK COMMANDS #############

class Task:
    """Something that occupies a person's time"""
    def __init__(self, sim, daysToComplete, statusText):
        self.daysToComplete = daysToComplete
        self.statusText = statusText
        self.daysRemaining = self.daysToComplete
        self.sim = sim
        self.beforeFunc = []  # a list of function names to call first
        self.afterFunc = []  # a list of function names to call last

    def do(self):
        pass  # override this method when inheriting!

    def timePass(self):
        """subtract a day from the days remaining counter"""
        self.daysRemaining -= 1


class Assessment(Task):
    """an assessment of the conditions of the camp/refugees"""
    def __init__(self, sim, daysToComplete, statusText, properties):
        Task.__init__(self, sim, daysToComplete, statusText)
        self.properties = properties
        self.isa = "assessment"

    def do(self):
        for (func, arg) in self.beforeFunc:
            # calls each designated function
            getattr(self.sim.action, func)(arg)
        for x in self.properties:
            (c, a) = x.split(".")
            if c == "refugees":
                self.sim.action.infoStore.refugees[a] = copy.deepcopy(
                    self.sim.probability.getRefugees(a))
            elif c == "camp":
                self.sim.action.infoStore.camp[a] = copy.deepcopy(
                    self.sim.probability.getCamp(a))
        for stuff in self.afterFunc:
            if len(stuff) == 1:
                # calls the designated function
                getattr(self.sim.action, stuff[0])()
            else:
                # calls it with a tuple of arguments
                getattr(self.sim.action, stuff[0])(stuff[1:])


class Intervention(Task):
    """an action meant to change a condition of the camp or the refugees"""
    def __init__(self, sim, daysToComplete, statusText, propertyPairs):
        Task.__init__(self, sim, daysToComplete, statusText)
        # a list of doubles in the form ("area.property", amount)
        self.propertyPairs = propertyPairs
        self.isa = "intervention"

    def do(self):
        for stuff in self.beforeFunc:
            if len(stuff) == 1:
                # calls the designated function
                getattr(self.sim.action, stuff[0])()
            else:
                # calls it with a tuple of arguments
                getattr(self.sim.action, stuff[0])(stuff[1:])
        for (x, y) in self.propertyPairs:
            self.sim.probability.adjustProperty(x, y)
        for stuff in self.afterFunc:
            if len(stuff) == 1:
                # calls the designated function
                getattr(self.sim.action, stuff[0])()
            else:
                # calls it with a tuple of arguments
                getattr(self.sim.action, stuff[0])(stuff[1:])

######### BEGIN SPECIFIC COMMMAND TYPES ####


class AssessRefugeeMedicalProfile(Assessment):
    """an assessment of the medical profile of the refugees"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 3, "assessing refugee medical profile",
            ["refugees.population", "refugees.dead", "refugees.cholera",
             "refugees.diarrhea", "refugees.measles", "refugees.malaria",
             "refugees.malnourished", "refugees.malaria",
             "refugees.meningitis"])


class AssessRefugeePopulation(Assessment):
    """an assessment of the number of refugees in your camp"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing refugee population",
            ["refugees.population", "refugees.dead"])


class AssessRefugeeFoodSupplyDemand(Assessment):
    """an assessment of how many calories per day the average
    refugee is not getting AND how many calories are being
    delivered to the camp."""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing refugee food supply/demand",
            ["refugees.nutritionalDemand", "camp.foodQuantity"])


class AssessRefugeeCholera(Assessment):
    """an assessment of how many people are showing symptoms of cholera"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for cholera symptoms",
            ["refugees.cholera", "refugees.population", "refugees.dead"])


class AssessRefugeeDiarrhea(Assessment):
    """an assessment of how many people are showing symptoms of diarrhea"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for diarrhea symptoms",
            ["refugees.diarrhea", "refugees.population", "refugees.dead"])


class AssessRefugeeMeasles(Assessment):
    """an assessment of how many people are showing symptoms of measles"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for measles symptoms",
            ["refugees.measles", "refugees.population", "refugees.dead"])


class AssessRefugeeMalaria(Assessment):
    """an assessment of how many people are showing symptoms of malaria"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for malaria symptoms",
            ["refugees.malaria", "refugees.population", "refugees.dead"])


class AssessRefugeeMalnourished(Assessment):
    """an assessment of how many people are malnourished"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for malnutrition",
            ["refugees.malnourished", "refugees.population", "refugees.dead"])


class AssessRefugeeMeningitis(Assessment):
    """an assessment of how many people are showing symptoms of Meningitis"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing for meningitis symptoms",
            ["refugees.meningitis", "refugees.population", "refugees.dead"])


class AssessLatrinesOnly(Assessment):
    """an assessment of the number of each type of latrine in your camp"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "you should not be reading this",
            ["camp.latrinesDefTrench", "camp.latrinesCommPit"])


class AssessCampLatrines(Assessment):
    """an assessment of the number of each type of latrine
    in your camp and the number of unserviced refugees"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing sanitation facilities",
            ["camp.latrinesDefTrench", "camp.latrinesCommPit",
             "camp.solidWaste"])
        self.afterFunc = [("choleraHint",)]


class AssessCampWaterQuality(Assessment):
    """an assessment of the water quality in your camp"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing camp water quality",
            ["camp.waterQuality"])


class AssessCampWaterSupplyDemand(Assessment):
    """an assessment of how many liters of water is being
    delivered daily to camp and how much the avg
    refugee isn't getting"""
    def __init__(self, sim):
        Assessment.__init__(
            self, sim, 1, "assessing camp water supply and demand",
            ["camp.waterQuantity", "refugees.waterDemand"])

###### END ASSESSMENTS / BEGIN INTERVENTIONS #######


class AddCampFoodQuantity(Intervention):
    """Increase the daily food supply at the camp"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "arranging for daily food supply increase",
            [("camp.foodQuantity", 2000000)])


class AddCampLatrineDefTrench(Intervention):
    """Dig some defecation trenches at the camp"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "digging 100 new defecation trenches",
            [("camp.latrinesDefTrench", 100)])
        self.afterFunc = [("revealLatrineInfo",),
                          ("addDefTrenchExpiration", "100")]


class AddCampLatrineCommPit(Intervention):
    """Build some community pits at the camp"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "building 60 new community pits",
            [("camp.latrinesCommPit", 60)])
        self.afterFunc = [("revealLatrineInfo",)]


class AddCampWaterQuality(Intervention):
    """Improve the quality of the water at the camp"""
    def __init__(self, sim):
        Intervention.__init__(self, sim, 1, "improving water quality", [])
        self.afterFunc = [("treatWater",)]


class AddCampWaterQuantity(Intervention):
    """Increase the daily water delivery amount"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "arranging for more water",
            [("camp.waterQuantity", 10000)])


class SetUpSuppFeedingCenter(Intervention):
    """Set up a supplimentary feeding center for malnourished
    children age 5 and under"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 2, "setting up a supplimentary feeding center",
            [("camp.suppFeedingCenters", 1)])


class TreatMeasles(Intervention):
    """Treat refugees who are showing symptoms of measles"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "treating refugees showing measles symptoms",
            [])
        self.beforeFunc = [("treatSickHelper", "measles")]


class TreatCholeraAndDiarrhea(Intervention):
    """Treat refugees who are showing symptoms of cholera or diarrhea"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1,
            "treating refugees with cholera or diarrhea symptoms",
            [])
        self.beforeFunc = [("treatSickHelper", "cholera")]
        self.afterFunc = [("treatSickHelper", "diarrhea")]


class TreatMeningitis(Intervention):
    """Treat refugees who are showing symptoms of meningitis"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "treating refugees showing meningitis symptoms", [])
        self.beforeFunc = [("treatSickHelper", "meningitis")]


class TreatMalaria(Intervention):
    """Treat refugees who are showing symptoms of malaria"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "treating refugees showing malaria symptoms", [])
        self.beforeFunc = [("treatSickHelper", "malaria")]


class VaccinateMeasles(Intervention):
    """Vaccinate some refugees against measles"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "vaccinating some refugees against measles", [])
        self.beforeFunc = [("vaccinate", "measles", 2)]


class VaccinateCholera(Intervention):
    """Vaccinate some refugees against cholera"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "vaccinating some refugees against cholera", [])
        self.beforeFunc = [("vaccinate", "cholera", 14)]


class VaccinateMeningitis(Intervention):
    """Vaccinate some refugees against meningitis"""
    def __init__(self, sim):
        Intervention.__init__(
            self, sim, 1, "vaccinating some refugees against meningitis", [])
        self.beforeFunc = [("vaccinate", "meningitis", 5)]

############ END COMMAND TYPES ###########


class Resource:
    """resources for the user to manage"""
    def __init__(self):
        self.personnel = []
        self.maxPersonnel = 5

    def findFreePersonnel(self):
        """return the first non-busy person on staff,
        or 'None' if everyone is busy"""
        for x in self.personnel:
            if x.getDaysBusy() == 0:
                return x

    def nextDay(self):
        """decrement all personnel task daysRemaining counters."""
        for x in self.personnel:
            if x.task is not None:
                x.task.timePass()

    # pass either "assessment" or "intervention"
    def doTasks(self, taskType):
        """do all tasks of the indicated type that are to be done today"""
        for x in self.personnel:
            if (x.task is not None
                    and x.task.isa == taskType
                    and x.task.daysRemaining == 0):
                x.task.do()
                x.task = None


class Personnel:
    names = ["Juan", "Alexis", "Eric", "Marilyn", "Ryan"]
    nameCount = 0
    taskId = ""

    def __init__(self):
        self.name = Personnel.names[Personnel.nameCount]
        Personnel.nameCount += 1
        if Personnel.nameCount >= len(Personnel.names):
            Personnel.nameCount = 0
        self.task = None

    def assign(self, task):
        """assign a task to this person"""
        self.task = task

    def getDaysBusy(self):
        """return the number of days this person will be busy
        doing their current task"""
        if self.task is not None:
            return self.task.daysRemaining
        else:
            return 0


class InfoStore:
    """contains known data about the camp and the refugees"""
    def __init__(self):
        self.camp = {}  # currently perceived view of the camp facilities
        self.refugees = {}  # currently perceived view of the refugees
        self.messages = []  # contains messages about the news for the turn
        self.history = []  # a list containing the real stats for every turn


class Scenario:
    """contains data and scripted events for the scenario"""
    def __init__(self, action):
        """sets up the scenario"""
        self.script = {}
        self.data = {}
        # for regularly repeating events.
        #  Format: ("functionname arg", startturn, repeatfreq)
        self.repeating = []
        self.data["title"] = "Relief Simulation"  # the scenario title
        # a very brief description
        self.data["briefDescription"] = "(no description)"
        self.data["description"] = "(no description)"  # a lengthy description.
        self.data["location"] = "(unspecified location)"  # example: "Sudan"
        self.data["days"] = "0"  # the number of days in the scenario
        self.action = action
        # events in script[X] will happen at the END of turn X

        # the following lines would normally be read from a file
        self.script[0] = ["addPersonnel 3", "addRefugees 10000",
                          "addFood 15000000", "addWater 100000"]
        self.repeating.append(("addRefugees 2000", 15, 15))
        self.repeating.append(("addPersonnel 1", 12, 12))
        self.data["title"] = "Demo Scenario"
        self.data["briefDescription"] = "The Prototype ReliefSim Scenario"
        self.data["description"] = """\
You are the manager of a refugee camp in Sudan. You have \
10 days. Try to keep as many people alive and healthy as you can!"""
        self.data["location"] = "Sudan"

    def parseEvent(self, eventString):
        """parse the string for an action name and arguments"""
        if ' ' in eventString:
            (a, b) = eventString.split()
            # calls the scripted function
            # with the provided argument as a string
            getattr(self.action, a)(b)
        else:
            # calls the scripted function with no argument
            getattr(self.action, eventString)()

    def fireEvents(self, turnNum):
        """perform the commands listed in the scenario script
        for the indicated turn and any repeating events"""
        if turnNum in self.script.keys():
            for eventString in self.script[turnNum]:
                self.parseEvent(eventString)
        for event in self.repeating:
            if turnNum >= event[1] and (turnNum - event[1]) % event[2] == 0:
                # if it is time for this event to fire
                self.parseEvent(event[0])


class Camp:
    """represents the facilities of the camp"""
    def __init__(self, sim):
        self.sim = sim
        self.data = {}
        self.data["waterQuality"] = 0
        self.data["waterQuantity"] = 0
        self.data["foodQuantity"] = 0
        self.data["suppFeedingCenters"] = 0
        self.data["solidWaste"] = 0
        self.data["latrinesDefTrench"] = 0
        self.data["latrinesCommPit"] = 0
        # list of [turns remaining, number of dts to expire]
        self.defTrenchExpiration = []
        # number of turns a def trench will last
        self.defTrenchLifespan = 5
        # number of consecutive turns of insufficient
        # latrine coverage until cholera breaks out.
        self.choleraTurnsReq = 5
        # dynamic counter of consecutive turns
        # with cholera-inducing conditions.
        self.choleraCountdown = self.choleraTurnsReq
        # number of consecutive turns of insufficient
        # latrine coverage until diarrhea breaks out.
        self.diarrheaTurnsReq = 3
        # dynamic counter of consecutive turns
        # with diarrhea-inducing conditions.
        self.diarrheaCountdown = self.diarrheaTurnsReq
        # how many people can each feeding center service
        self.foodPerFeedingCenter = 500
        self.measlesOutbreak = 0  # has a measles outbreak ever occurred?
        self.treatmentTurns = 3  # how many turns water treatment lasts
        # how effective is treatment on the first turn?
        self.treatmentMaxEffect = 0.6
        # a list of currently active water treatments:
        # [turn1treatments, turn2treatments, ...]
        self.treatments = []
        for i in range(self.treatmentTurns):
            self.treatments.append(0)

    def calculateWasteAndWater(self):
        """this performs calculation of solid waste and water quality"""

        # calculate solidWaste a.k.a Refugees w/o latrines:
        pop = self.sim.refugees.data["population"][0]
        dt = self.data["latrinesDefTrench"]
        cp = self.data["latrinesCommPit"]
        solidWaste = max(0, pop - (50 * dt + 30 * cp))
        self.data["solidWaste"] = int(solidWaste)

        # calculate waste / water (lower is better):
        wQuant = float(self.data["waterQuantity"])
        if wQuant != 0:
            wQual = (solidWaste / wQuant)
        else:
            wQual = 0.0
        # now map that ratio to a scale of acceptability:
        lowerBound = 0.0  # the best quality water
        upperBound = 0.1  # the worst quality water
        if wQual < lowerBound:
            wQual = lowerBound
        if wQual > upperBound:
            wQual = upperBound
        # scale and invert (so higher is better):
        wQual = 1 - ((wQual - lowerBound) / (upperBound - lowerBound))

        # water treatments wear off gradually:
        for i in range(self.treatmentTurns):
            factor = ((float(self.treatmentTurns) - i)
                      / float(self.treatmentTurns)) * self.treatmentMaxEffect
            wQual += self.treatments[i] * factor
        wQual = min(1.0, wQual)
        self.data["waterQuality"] = wQual

    def evolveWasteAndWater(self):
        """simulation of sanitation and water quality"""
        self.calculateWasteAndWater()
        ###### AGE THE WATER TREATMENTS
        tRange = range(self.treatmentTurns)
        tRange.reverse()
        for i in tRange:
            if i > 0:
                self.treatments[i] = self.treatments[i - 1]
        self.treatments[0] = 0
        ###### EXPIRE DEFECATION TRENCHES
        offset = 0
        for i in range(len(self.defTrenchExpiration)):
            i -= offset
            self.defTrenchExpiration[i][0] -= 1  # 'age' the def trench
            if self.defTrenchExpiration[i][0] == 0:
                # expire the defecation trench
                self.data[
                    "latrinesDefTrench"] -= self.defTrenchExpiration[i][1]
                del self.defTrenchExpiration[i:i + 1]
                offset += 1
        if offset > 0:
            self.sim.action.infoStore.messages.append(
                "Some of your defecation trenches have become unusable!")

####### BEGIN DISEASES #######


class Disease:
    """a disease"""
    def __init__(self, name, commutability, severity, avgDuration,
                 turnsUntilSymptomatic):
        self.name = name
        # scale from 0 to 1: how easily does it spread? 0 = not contagious
        self.commutability = commutability
        # scale from 0 to 1: how severe is this disease?
        # This is totally arbitrary.
        self.severity = severity
        # on average, how many turns does this disease last?
        self.avgDuration = avgDuration
        # on average, how many turns until symptoms show?
        self.turnsUntilSymptomatic = turnsUntilSymptomatic
        # these next three are assigned at infection-time
        self.healthDamage = 0.0  # how much health is removed each turn
        # how many turns more this disease will be around
        self.turnsRemaining = 0.0
        # tricky: how many turns are between the symptom
        # start-date and the end of the disease
        self.symptomaticTurn = 0


class Cholera(Disease):
    """A severe contagious disease acquired from
    water contaminated with feces"""
    def __init__(self):
        Disease.__init__(self, "cholera", 0.3, 0.18, 5, 1)


class Diarrhea(Disease):
    """A mild contagious disease acquired from water contaminated with feces"""
    def __init__(self):
        Disease.__init__(self, "diarrhea", 0.32, 0.04, 5, 1)


class Measles(Disease):
    """A severe highly-contagious disease that is
    transmitted through the air"""
    def __init__(self):
        Disease.__init__(self, "measles", 0.5, 0.18, 6, 1)

######## END DISEASES #######


class Refugee:
    """a refugee at the camp"""
    def __init__(self, dh=1.0, nh=1.0, age=0,
                 gender="random", immunized=[], diseases=[]):
        if age == 0:  # random age
            self.age = int(g.random() * 69) + 1
        else:
            self.age = age
        if gender == "random":  # random gender
            if g.random() < 0.5:
                self.gender = "male"
            else:
                self.gender = "female"
        else:
            self.gender = gender

        # a dictionary of diseases and the refugee's resistances to them:
        self.diseaseResistance = {}
        self.diseaseResistance["measles"] = g.random()
        self.diseaseResistance["cholera"] = g.random()
        self.diseaseResistance["diarrhea"] = g.random()
        self.diseaseResistance["meningitis"] = g.random()
        self.diseaseResistance["malaria"] = g.random()

        # make younger people weaker against disease:
        if self.age < 15 and self.age >= 5:
            for d in self.diseaseResistance.keys():
                self.diseaseResistance[d] *= 0.5 + (0.5 * (self.age / 15.0))
        elif self.age < 5:
            for d in self.diseaseResistance.keys():
                self.diseaseResistance[d] *= 0.2 + (0.8 * (self.age / 5.0))

        # a factor that determines how sensitive to food this person is
        self.hungerFactor = g.random() * 0.14 + 0.93
        # make younger people more sensitive to malnutrition:
        if self.age < 15 and self.age >= 5:
            self.hungerFactor *= 0.5 + (0.5 * (self.age / 15.0))
        elif self.age < 5:
            self.hungerFactor *= 0.3 + (0.7 * (self.age / 5.0))

        ##### STATS BELOW ARE MUTABLE AND DYNAMIC. STATS ABOVE ARE PERMANENT.
        self.diseaseHealth = dh
        self.nutritionalHealth = nh
        self.generalHealth = dh * nh
        # a list of diseases (objects, not strings) this refugee is carrying
        self.diseases = []
        for d in diseases:
            self.diseases.append(d)
        # a list of diseases this refugee has been immunized against.
        self.immunized = []
        # a list of diseases which this refugee will soon be
        # immune: [[delay, diseaseName],...]
        self.immunityCountdown = []
        # a list of diseases this refugee is temporarily immune to.
        self.tempImmunity = []
        for i in immunized:
            self.immunized.append(i)
        # how many turns of disease recovery this person has remaining
        self.recoveryTurnsRemaining = 0
        # how much health is left to be recovered
        self.recoveryHealthRemaining = 0
        self.healthState = "healthy"
        if self.diseases != []:
            self.healthState = "sick"
        # a list of disease names of which symptoms are showing
        self.symptoms = []
        if self.diseases != []:
            self.symptoms = self.calculateSymptoms()

    def calculateSymptoms(self):
        """calculates the symptoms list, sets it and returns it"""
        self.symptoms = []
        for d in self.diseases:
            if d.symptomaticTurn > d.turnsRemaining:
                self.symptoms.append(d.name)
        return self.symptoms


class Refugees:
    """represents the refugees at the camp"""
    def __init__(self, sim):
        self.sim = sim
        self.pop = []  # this is the array of refugee objects
        self.bdKeys = ["population", "dead", "diarrhea",
                       "malnourished", "measles", "cholera",
                       "meningitis", "malaria"]
        self.data = {}
        self.data["population"] = [0, 0, 0, 0]
        self.data["dead"] = [0, 0, 0, 0]

        # how many people fall below the malnourishment threshold
        self.data["malnourished"] = [0, 0, 0, 0]

        self.data["cholera"] = [0, 0, 0, 0]  # symptomatic for cholera
        self.data["diarrhea"] = [0, 0, 0, 0]  # symptomatic for diarrhea
        self.data["measles"] = [0, 0, 0, 0]  # symptomatic for measles
        self.data["meningitis"] = [0, 0, 0, 0]  # symptomatic for meningitis
        self.data["malaria"] = [0, 0, 0, 0]  # symptomatic for malaria

        # number of refugees who died with Cholera
        self.data["diedWithCholera"] = [0, 0, 0, 0]
        # number of refugees who died with Diarrhea
        self.data["diedWithDiarrhea"] = [0, 0, 0, 0]
        # number of refugees who died with both Cholera and Diarrhea
        self.data["diedWithBothCDD"] = [0, 0, 0, 0]

        # this is only used for the end-of-game graph
        self.data["symptomatic"] = 0
        self.data["sick"] = 0  # this is only used for the end-of-game graph

        self.data["generalHealth"] = 1.0  # average general health at the camp.
        # average nutritional health at the camp.
        self.data["nutritionalHealth"] = 1.0
        # average disease health at the camp.
        self.data["diseaseHealth"] = 1.0

        self.data["waterDemand"] = 0
        self.data["nutritionalDemand"] = 0
        self.data["immMeasles"] = 0  # number of measles vaccinations completed
        self.data["immCholera"] = 0  # number of cholera vaccinations completed
        # number of meningitis vaccinations completed
        self.data["immMeningitis"] = 0

        # calories per day each person needs
        self.reqFoodIntakePerPerson = 2100
        # liters per day required for healthy living
        self.reqWaterPerPerson = 15
        # a list of people who have been infected on this turn.
        self.justInfectedIndex = []
        # the indices of people who are dead and waiting to
        # be 'reaped' off the list.
        self.deadPeople = []
        # how many people can be served by the feeding centers
        self.feedingCenterFoodSupply = 0
        # to be added to the nutritionalHealth rating.
        self.feedingCenterFoodRation = 0.1
        # under this level, you are malnourished
        self.malnourishmentThreshold = 0.5

    def addRandomizedRefugees(self, num):
        """adds the specified number of refugees to the camp.
        Uses weighted probability to determine age/gender"""
        num = int(num)
        # weighted probability distribution for age groups
        upperBounds = [20, 50, 90, 100]
        ageGroups = [0, 5, 15, 50, 70]  # age group boundaries (years)
        for i in range(num):
            # randomly pick an age group (using weighted probability)
            x = g.random() * 100
            for group in range(len(upperBounds)):
                if x < upperBounds[group]:
                    # randomly pick an age in between the boundaries
                    # of that age group.
                    rAge = (ageGroups[group]
                            + int(
                            g.random()
                            * (ageGroups[group + 1] - ageGroups[group])
                            ) + 1)
                    break
            # randomly pick a gender based on the weighted
            # probability of that age range
            if rAge < 15:
                x = 0.5
            else:
                x = 0.35
            if g.random() < x:
                rGender = "male"
            else:
                rGender = "female"
            # random nutritionalHealth in the range 0.2 - 1.0
            randomNH = 0.2 + (g.random() * 0.8)
            r = Refugee(age=rAge, gender=rGender, nh=randomNH)
            # add the customized refugee to the camp
            self.pop.append(r)
            self.adjustBDStat(r, "population", 1)

    def addRefugees(self, num):
        """adds the specified number of refugees to the camp.
        Each refugee is given the default configuration"""
        num = int(num)
        for i in range(num):
            r = Refugee()
            # add a default refugee to the camp
            self.pop.append(r)
            # this is not an optimized way of doing this
            self.adjustBDStat(r, "population", 1)

    def adjustBDStat(self, r, statName, amount):
        """adjusts a breakdown statistic"""
        self.data[statName][0] += amount  # adjust the 'total' stat
        if r.age < 5:
            index = 1
        elif r.age < 15:
            index = 2
        else:
            index = 3
        # adjust the specific age-group stat
        self.data[statName][index] += amount

    # used during turn 0 to provide correct stats
    # for the initial history state.
    def calculateHealthStats(self):
        """calculates and updates nutritionalHealth,
        diseaseHealth, and generalHealth"""
        pop = self.data["population"][0]
        if pop == 0:
            self.data["generalHealth"] == 0
            self.data["nutritionalHealth"] == 0
            self.data["diseaseHealth"] == 0
            return
        else:
            (gh, nh, dh) = (0.0, 0.0, 0.0)
            for r in self.pop:
                gh += r.generalHealth
                nh += r.nutritionalHealth
                dh += r.diseaseHealth
            gh /= pop
            dh /= pop
            nh /= pop
            self.data["nutritionalHealth"] = nh
            self.data["diseaseHealth"] = dh
            self.data["generalHealth"] = gh

    # assumes food is equally distributed and
    # everyone requires the same amount
    def calculateNutritionalDemand(self):
        """calculates the avg num of calories (and water liters)
        under the req amount for each refugee"""
        pop = float(self.data["population"][0])
        if pop <= 0:
            self.data["nutritionalDemand"] = 0
            self.data["waterDemand"] = 0
            return
        self.data["nutritionalDemand"] = (
            pop * float(self.reqFoodIntakePerPerson)
            - float(self.sim.camp.data["foodQuantity"])) / pop
        self.data["waterDemand"] = (
            pop * float(self.reqWaterPerPerson)
            - float(self.sim.camp.data["waterQuantity"])) / pop

    def changeState(self, newState, index):
        """changes between states: healthy, sick, recovering, and dead"""
        # This should only affect the 'dead', 'population',
        # and 'sick' stats. NOT symptomatic or symptoms
        r = self.pop[index]

        if newState == "dead":  # always do this stuff if they're dead:
            self.adjustBDStat(r, "population", -1)
            self.adjustBDStat(r, "dead", 1)

        if r.healthState == "healthy":
            if newState == "sick":
                self.data["sick"] += 1
        elif r.healthState == "sick":
            self.data["sick"] -= 1
        elif r.healthState == "recovering":
            if newState == "sick":
                self.data["sick"] += 1
        r.healthState = newState

    def infect(self, index, sourceDisease):
        """infects somebody with the disease of your choice!"""
        # "sourceDisease" is the disease instance
        # carried by the spreader/vector

        dName = sourceDisease.name
        person = self.pop[index]
        if (person.healthState == "dead"
                or dName in person.immunized
                or dName in person.tempImmunity):
            return
        if (person.healthState == "healthy"
                or person.healthState == "recovering"):
            self.changeState("sick", index)

        # create a new instance based on the name of the source disease:
        if dName == "cholera":
            disease = Cholera()
        elif dName == "diarrhea":
            disease = Diarrhea()
        elif dName == "measles":
            disease = Measles()

        disease.turnsRemaining = int(
            1.8 * disease.avgDuration
            * (1 - (0.7 * person.diseaseResistance[dName]
                    + 0.3 * person.nutritionalHealth)))
        disease.symptomaticTurn = (disease.turnsRemaining
                                   - disease.turnsUntilSymptomatic)
        disease.healthDamage = (disease.severity
                                * (1 - person.diseaseResistance[dName]))
        recoveryTime = int(disease.turnsRemaining * 0.5)
        if recoveryTime == 0:
            recoveryTime = 1  # this prevents a zero-length recovery period
        # add to any pre-existing recovery time
        person.recoveryTurnsRemaining += recoveryTime
        person.diseases.append(disease)
        person.tempImmunity.append(dName)

    def reap(self):  # get those pesky dead people out of the list
        """removes dead refugees from the population array"""
        offset = 0
        for x in self.deadPeople:
            person = self.pop[x - offset]
            diseaseCounter = 0
            for disease in person.diseases:
                if disease.name == "diarrhea":
                    self.adjustBDStat(person, "diedWithDiarrhea", 1)
                    diseaseCounter += 1
                if disease.name == "cholera":
                    self.adjustBDStat(person, "diedWithCholera", 1)
                    diseaseCounter += 1
            if diseaseCounter == 2:
                self.adjustBDStat(person, "diedWithBothCDD", 1)
            # splice them out of the list:
            del self.pop[x - offset:x - offset + 1]
            offset += 1

    def removeDisease(self, refugee, index, disease):
        """ Will handle state change and stat adjustment
        for when diseases are removed."""
        # Takes care of diseases, symptoms, bdstats,
        # and changestate. "disease" must be an instance, not a string!
        refugee.diseases.remove(disease)
        if disease.symptomaticTurn >= disease.turnsRemaining:
            # remove symptoms:
            refugee.symptoms.remove(disease.name)
            self.adjustBDStat(refugee, disease.name, -1)
            if refugee.symptoms == []:
                self.data["symptomatic"] -= 1
        if refugee.diseases == []:
            self.changeState("recovering", index)

    def simulate(self):
        """this is the do-everything function
        that handles the automatic stuff"""
        camp = self.sim.camp
        ##### OVERHEAD CALCULATIONS FOR THE WHOLE CAMP ###############
        self.calculateNutritionalDemand()
        if self.data["population"][0] > 0:
            # IMPORTANT: this assumes food is equally
            # distributed and everyone requires the same amount
            nutD = self.data["nutritionalDemand"]
            watD = self.data["waterDemand"]
            reqF = float(self.reqFoodIntakePerPerson)
            reqW = float(self.reqWaterPerPerson)

            foodFactor = nutD  # average nutritional demand
            if foodFactor < -700:
                # cut off any nutritional benefit after 700 cal more
                # than their required intake
                foodFactor = -700
            # percent of requirement
            foodFactor = (reqF - foodFactor) / reqF

            waterFactor = watD  # average water demand
            if waterFactor < -2:
                # cut off any nutritional benefit after 2 liters
                # more than their required intake
                waterFactor = -2
            # percent of requirement
            waterFactor = (reqW - waterFactor) / reqW

            # weighted average food and water benefits, then multiply
            # by an arbitrary conversion factor to get the base
            # benefit/loss amount.  that will later be tweaked by
            # everyone's hungerFactor and then added/subtracted from
            # their NH rating

            nutFactor = (0.4 * foodFactor + 0.6 * waterFactor)
            if nutFactor > 0.9:
                # nutritional Health should go up more easily than go down.
                nutHealthGain = 0.5 * (nutFactor - 0.9)  # gain
            else:
                nutHealthGain = -0.3 * (0.9 - nutFactor)  # loss

            self.feedingCenterFoodSupply = (
                camp.foodPerFeedingCenter
                * camp.data["suppFeedingCenters"])
            # compare the foodsupply to this to see how crowded
            self.measlesFCFS = int(self.feedingCenterFoodSupply / 2)
            self.justInfectedIndex = []  # reset the index.
            self.deadPeople = []

            # CHOLERA AND DIARRHEA CHECK:

            # (waste/pop) ranges from 0 to 1, smaller is better.
            fecesFactor = (float(camp.data["solidWaste"])
                           / float(self.sim.refugees.data["population"][0]))
            # do a weighted average of water quality and inverted
            # fecesFactor, so now larger is better.
            fecesFactor = ((0.8 * (1.0 - fecesFactor))
                           + (0.2 * camp.data["waterQuality"]))

            # fecesFactor values for various sanitation
            # improvements (10/23/2006):
            # nothing = 0.03
            # 1 water quality = 0.153
            # 1 commpit = 0.2
            # 2 commpits = 0.38
            # 1 deftrench = 0.516
            # 3 commpits = 0.555
            # 1 deftrench + 1 commpit = 0.691

            if fecesFactor < 0.3:
                camp.choleraCountdown -= 1
                if camp.choleraCountdown <= 0:  # it's cholera time...
                    for i in range(int(len(self.pop) * 0.02) + 1):
                        # expose 2% of the population:
                        self.justInfectedIndex.append(
                            (int(g.random() * len(self.pop)), Cholera()))
            # reset counter if a healthy solidwaste turn elapsed.
            # DON'T reset if the outbreak was triggered.
            elif (camp.choleraCountdown > 0
                  and camp.choleraCountdown < camp.choleraTurnsReq):
                camp.choleraCountdown = camp.choleraTurnsReq

            if fecesFactor < 0.8:
                camp.diarrheaCountdown -= 1
                if camp.diarrheaCountdown <= 0:  # it's diarrhea time...
                    for i in range(int(len(self.pop) * 0.04) + 1):
                        # expose 4% of the population:
                        self.justInfectedIndex.append(
                            (int(g.random() * len(self.pop)), Diarrhea()))
            # reset counter if a healthy solidwaste turn elapsed.
            # DON'T reset if the outbreak was triggered.
            elif (camp.diarrheaCountdown > 0
                  and camp.diarrheaCountdown < camp.diarrheaTurnsReq):
                camp.diarrheaCountdown = camp.diarrheaTurnsReq

        # sums for averaging later
        generalHealth = 0
        nutritionalHealth = 0
        diseaseHealth = 0

        # reset the malnourishment count
        for i in range(len(self.data["malnourished"])):
            self.data["malnourished"][i] = 0
        index = 0

        ############ FOR EACH REFUGEE ##############
        for r in self.pop:
            ######### CONDITION CHECK
            disease = 0
            recovery = 0
            dead = 0
            if r.healthState == "sick":
                disease = 1
            elif r.healthState == "recovering":
                recovery = 1

            ######### NUTRITION #####################
            z = r.nutritionalHealth + nutHealthGain * r.hungerFactor
            if z < self.malnourishmentThreshold:
                if r.age <= 5 and self.feedingCenterFoodSupply > 0:
                    # supplimentary feeding centers ONLY for 5 and under
                    z += self.feedingCenterFoodRation
                    self.feedingCenterFoodSupply -= 1
                    if (self.feedingCenterFoodSupply <= self.measlesFCFS
                            and self.sim.camp.measlesOutbreak == 0):
                        # will set camp.measlesOB to 1
                        self.sim.action.feedingCenterMeaslesOutbreak()
            if z > 1.0:
                z = 1.0
            r.nutritionalHealth = z
            r.generalHealth = z
            # starving to death:
            if z < 0.1:
                dead = 1

            if dead == 0:
                ####### DELAYED IMMUNITY ###############
                for packet in r.immunityCountdown:
                    packet[0] -= 1  # decrement the countdown timer
                    if packet[0] == 0:  # it's immunity time...
                        r.immunized.append(packet[1])
                        r.immunityCountdown.remove(packet)

                ######################### DISEASE ############
                if disease == 1:
                    for d in r.diseases:
                        dName = d.name
                        if d.turnsRemaining > 0:
                            # still sick... take some damage and
                            #  decrement turnsRemaining
                            r.diseaseHealth -= d.healthDamage
                            r.recoveryHealthRemaining += d.healthDamage
                            d.turnsRemaining -= 1
                            if d.symptomaticTurn == d.turnsRemaining:
                                # become symptomatic:
                                if r.symptoms == []:
                                    self.data["symptomatic"] += 1
                                r.symptoms.append(dName)
                                self.adjustBDStat(r, dName, 1)
                            if g.random() < d.commutability:
                                # spread the disease...
                                lenJII = len(self.justInfectedIndex)
                                #set an upper bound on infections
                                if lenJII > self.data["population"][0]:
                                    break
                                # choose a person to expose to the disease.
                                # Infection may or may not happen
                                #  (after the loop)...
                                self.justInfectedIndex.append(
                                    (int(g.random()
                                         * self.data["population"][0]),
                                     d))
                        else:
                            # this disease is done...
                            self.removeDisease(r, index, d)

                    r.generalHealth *= r.diseaseHealth
                    if r.diseaseHealth < 0.1 or r.generalHealth < 0.1:
                        dead = 1

                #################### RECOVERY #################
                elif recovery == 1:
                    if r.recoveryTurnsRemaining <= 0:
                        # finish recovery (become healthy) and
                        # revoke temporary immunity:
                        self.changeState("healthy", index)
                        r.tempImmunity = []
                    else:
                        # recover some health:
                        x = (r.recoveryHealthRemaining
                             / r.recoveryTurnsRemaining)
                        r.diseaseHealth += x
                        r.recoveryHealthRemaining -= x
                        r.recoveryTurnsRemaining -= 1
                    r.generalHealth *= r.diseaseHealth
                    # you might die during recovery if your generalHealth
                    # dropped due to malnutrition:
                    if r.diseaseHealth < 0.1 or r.generalHealth < 0.1:
                        dead = 1

            if dead == 1:
                # this is the only place where refugees changeState to dead
                self.changeState("dead", index)
                # add them to the reaper list:
                self.deadPeople.append(index)
                # adjust stats for diseases and symptomatic:
                if r.symptoms != []:
                    self.data["symptomatic"] -= 1
                    for dName in r.symptoms:
                        self.adjustBDStat(r, dName, -1)
            else:
                # mandatory python joke: "I'm not dead!"
                if r.nutritionalHealth < self.malnourishmentThreshold:
                    self.adjustBDStat(r, "malnourished", 1)
                generalHealth += r.generalHealth
                diseaseHealth += r.diseaseHealth
                nutritionalHealth += r.nutritionalHealth
            index += 1
        ########## END FOR EACH REFUGEE ##############
        ######## HANDLE THE PEOPLE EXPOSED TO THE DISEASE #######
        for (ref, d) in self.justInfectedIndex:
            # we didn't infect them before to prevent the extra turn of damage
            self.infect(ref, d)

        ############ REAP THE DEAD PEOPLE #############
        self.reap()

        #### CALCULATE AVERAGES AND STUFF ####
        pop = self.data["population"][0]
        if pop > 0:
            self.data["nutritionalHealth"] = nutritionalHealth / pop
            self.data["diseaseHealth"] = diseaseHealth / pop
            self.data["generalHealth"] = generalHealth / pop
        else:
            self.data["nutritionalHealth"] = 0
            self.data["diseaseHealth"] = 0
            self.data["generalHealth"] = 0


class Probability:
    """controls the success of actions and events;
    also contains info about the game state."""
    def __init__(self, sim):
        self.sim = sim
        self.camp = self.sim.camp
        self.refugees = self.sim.refugees
        self.gameOver = 0  # this will be set to 1 when the game ends
        self.turn = 0  # the current turn number

    def getRefugees(self, attribute):
        """get a property of the refugees"""
        return self.refugees.data[attribute]

    def getCamp(self, attribute):
        """get a property of the camp"""
        return self.camp.data[attribute]

    def getProperty(self, qualifiedAttribute):
        """get a property of something"""
        (c, a) = qualifiedAttribute.split(".")
        if c == "refugees":
            return self.getRefugees(a)
        elif c == "camp":
            return self.getCamp(a)

    def adjustProperty(self, qualifiedAttribute, amount):
        """adjust a property of something (used by interventions)"""
        (c, a) = qualifiedAttribute.split(".")
        if c == "camp":
            target = self.camp
        else:
            target = self.refugees
        target.data[a] += amount  # adjust the value
        # here comes a terribly inelegant way to enforce
        #  0-10 boundaries: (I don't think this is even important any more
        if a == "nutritionalHealth" or a == "diseaseHealth":
            if target.data[a] < 0:
                target.data[a] = 0
            elif target.data[a] > 10:
                target.data[a] = 10

    def beginGame(self):
        """do the necessary preparations for beginning the game"""
        self.sim.scenario.fireEvents(0)
        self.camp.calculateWasteAndWater()
        self.refugees.calculateNutritionalDemand()
        self.sim.action.updateInfoStore()
        self.sim.action.initHistory()
        self.sim.refugees.calculateHealthStats()
        self.turn = 1

    def endTurn(self):
        """do the automatic stuff and tell the scenario to
        fire the events for the next turn"""
        self.sim.action.storeHistory(self.camp, self.refugees)
        self.sim.scenario.fireEvents(self.turn)
        self.turn += 1  # advance to the next turn
        # this causes task timers to decrement
        self.sim.action.resource.nextDay()
        self.sim.action.resource.doTasks("intervention")  # do interventions
        self.camp.calculateWasteAndWater()
        self.refugees.simulate()
        # age sanitation facilities and update stats
        self.camp.evolveWasteAndWater()
        self.sim.action.resource.doTasks("assessment")  # do assessments
        self.sim.action.updateInfoStore()
        if self.refugees.data["population"][0] <= 0:
            # The end-of-game condition
            self.endGame()

    def endGame(self):
        """carry out any end-of-game actions"""
        self.gameOver = 1
