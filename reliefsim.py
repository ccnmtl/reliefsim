from google.appengine.ext import db
import webapp2
import jinja2
import os
from simulation import Simulation, WebUI
import zlib
import cPickle
import xml.dom.minidom
import random
import string
import time


def zdumps(obj):
    return zlib.compress(cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL), 9)


def zloads(zstr):
    return cPickle.loads(zlib.decompress(zstr))


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(
            os.path.dirname(__file__),
            "templates")))

random.seed(time.time())


def gen_id():
    source = string.lowercase + string.uppercase + string.digits
    return "".join([random.choice(source) for x in range(20)])


class UserState(db.Model):
    ui = db.BlobProperty(default=None)
    data = db.BlobProperty(default=None)
    date = db.DateTimeProperty(auto_now_add=True)


class IndexPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('welcome.html')
        template_values = dict()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))


class NewPage(webapp2.RequestHandler):
    def post(self):
        game = Simulation()
        ui = WebUI(game)
        game.probability.beginGame()
        session_key = gen_id()
        userstate = UserState(key_name=session_key)
        userstate.ui = db.Blob(zdumps(ui))
        userstate.put()
        self.response.set_cookie('reliefsim_session_key',
                                 session_key,
                                 max_age=360, path='/')
        self.redirect("/turn")


def get_state(request):
        session_key = request.cookies.get('reliefsim_session_key', None)
        k = db.Key.from_path('UserState', session_key)
        state = db.get(k)
        return state


class TurnPage(webapp2.RequestHandler):
    def get(self):
        state = get_state(self.request)
        ui = zloads(state.ui)
        game = ui.sim

        template = jinja_environment.get_template('turn.html')
        template_values = dict()
        if game.probability.gameOver != 0:
            template_values['game'] = game
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))


class ExecutePage(webapp2.RequestHandler):
    def post(self):
        state = get_state(self.request)
        ui = zloads(state.ui)
        game = ui.sim
        input = self.request.POST.get('input', '')
        if game.probability.gameOver == 0:
            ui.assembleMenuString()
            if input == "newGame":
                menu = ui.newMenu
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write(menu)
                return
            if input == "quit":
                self.redirect("/quit")
                return
            else:
                ui.process(input)
                ui.assembleMenuString()
                menu = ui.newMenu
                state.ui = zdumps(ui)
                state.put()
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write(menu)
                return
        else:
            self.redirect("/game_over")


class GameOverPage(webapp2.RequestHandler):
    def get(self):
        state = get_state(self.request)
        ui = zloads(state.ui)
        (dead, data) = ui.doEndGame()
        state.data = zdumps(data)
        state.put()
        template = jinja_environment.get_template('game_over.html')
        template_values = dict(dead=dead)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))


class DataPage(webapp2.RequestHandler):
    def get(self):
        state = get_state(self.request)

        data = zloads(state.data)
        if not data:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(
                "no data. are you sure you've finished the game?")
        else:
            self.response.headers[
                'Content-Disposition'] = "attachment;filename=history.csv"
            self.response.out.write(data)


class LoadDataPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        data = xml.dom.minidom.parseString(HELP_XML)
        # Get a list of the info
        assessments = data.documentElement.getElementsByTagName('info')
        # Go through each info
        for info in assessments:
            infoId = info.attributes['id'].nodeValue
            if infoId == self.request.GET['senddata']:
                self.response.write(info.childNodes[0].nodeValue)
                return
        self.response.write(
            "Failed to get information data for requested topic.")


app = webapp2.WSGIApplication(
        [
            ('/', IndexPage),
            ('/new', NewPage),
            ('/turn', TurnPage),
            ('/execute', ExecutePage),
            ('/quit', GameOverPage),
            ('/game_over', GameOverPage),
            ('/data', DataPage),
            ('/loadData', LoadDataPage),
        ],
        debug=True)


HELP_XML = """
<root>
	<info id="ass1">&lt;b&gt;Daily Water Supply &amp; Demand&lt;/b&gt;&lt;br/&gt;
Water is essential for life, health and human dignity. In extreme situations, there may not be sufficient water available to meet basic needs, and in these cases supplying a survival level of drinking water is of critical importance. In most cases, the main health problems are caused by poor hygiene due to insufficient water and by the consumption of contaminated water.&lt;br/&gt;
Water and sanitation are critical determinants for survival in the initial stags of a disaster. People affected by disasters are generally much more susceptible to illness and death from disease, which are related to a large extent to inadequate sanitation, inadequate water supplies and poor hygiene.
</info>

	<info id="ass2">&lt;b&gt;Water Quality&lt;/b&gt;&lt;br/&gt;
In many emergency situations, water-related disease transmission is due as much to insufficient water for personal and domestic hygiene as to contaminated water supplies. Until minimum standards for both quantity and quality are met, the priority should be to provide equitable access to an adequate quantity of water even if it is of intermediate quality, rather than to provide an inadequate quantity of water that meets the minimum quality standard.
</info>

	<info id="ass3">&lt;b&gt;Food Supply &amp; Demand&lt;/b&gt;&lt;br/&gt;
The goal of food aid management is to deliver food to those people who need it most. Generally speaking, this involves delivering the right goods, to the right location, in the right condition, at the right time with minimal handling loss. Equity in distribution process is of primary importance and the involvement of people from the disaster-affected population in decision-making and implementation is essential. The method of food distribution must be responsive, transparent, equitable and appropriate to the local conditions.
</info>
	
	<info id="ass4">&lt;b&gt;Sanitation Facilities&lt;/b&gt;&lt;br/&gt;
Water and sanitation are critical determinants for survival in the initial stages of a disaster. People affected by disasters are generally much more susceptible to illness and death from disease, which are related to a large extent to inadequate sanitation, inadequate water supplies and poor hygiene.
</info>
	
	<info id="ass5">&lt;b&gt;Population&lt;/b&gt;&lt;br/&gt;
Assessments provide an understanding of the disaster situation and a clear analysis of threats to life, dignity, health, and livelihoods to determine, in consultation with the relevant authorities, whether an external response is required and, if so, the nature of the response. Estimates of population numbers are cross-checked and validated with as many sources as possible, and the basis for the estimate made know.
</info>
	
	<info id="ass6">&lt;b&gt;Full Medical Profile&lt;/b&gt;&lt;br/&gt;
The design and development of health services are guided by the ongoing, coordinated collection, analysis and utilization of relevant public health data. Data should be disaggregated by age and sex as far as is practical in order to guide decision-making. Detailed disaggregation may be difficult during early stages of disaster. However, mortality and morbidity for children  under five years old should be documented from the outset, as this group is usually at special risk.
</info>
	
	<info id="ass7">&lt;b&gt;Malnutrition&lt;/b&gt;&lt;br/&gt;
Malnutrition, including micronutrient deficiency, is associated with increased risk of morbidity and mortality for affected individuals. Therefore, when rates of malnutrition are high, it is necessary to ensure access to services which correct as well as prevent malnutrition.
</info>
	
	<info id="ass8">&lt;b&gt;Cholera Symptoms&lt;/b&gt;&lt;br/&gt;
The spread of cholera is one of the main dangers following a natural disaster. &lt;br/&gt;
Cholera is an acute infection of the gut which causes chronic diarrhoea and vomiting.  Cholera is spread by contaminated water and food. Sudden outbreaks, such as those which follow a disaster, are usually caused by a contaminated water supply. In communities which are unprepared for a cholera outbreak, up to 50% of people who become seriously ill may die. &lt;br/&gt;
Approximately 1 in 20 infected persons has severe disease characterized by:
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;profuse watery diarrhea, 
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;vomiting, and 
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;leg cramps. 
&lt;br/&gt;
In these persons, rapid loss of body fluids leads to dehydration and shock. Without treatment, death can occur within hours.
</info>
	
	<info id="ass9">&lt;b&gt;Diarrheal Diseases&lt;/b&gt;&lt;br/&gt;
Intensive fly control is carried out in high-density settlements when there is a risk or the presence of diarrhoea epidemic. For water supplies with presence of diarrhoea epidemic, water is treated with disinfectant so that there is a free chlorine residual at the tap of 0.5mg per litre and turbidity is below 5 NTU.
</info>
	
	<info id="ass10">&lt;b&gt;Malaria Symptoms&lt;/b&gt;&lt;br/&gt;
Malaria incidence is likely to rise within a few days/weeks of mass population movements in endemic areas primarily due to mosquitoes. Because of widespread and increasing resistance to chloroquine and sulphadoxine-pyrimethamine (Fansider), more efficacious anti-malarial drugs may be required. This will be especially important for non-immune and vulnerable populations exposed to falciparam malaria. 
</info>
	
	<info id="ass11">&lt;b&gt;Measles Symptoms&lt;/b&gt;&lt;br/&gt;
Measles, also known as rubeola, is a viral infection of your respiratory system. Although mainly a disease of children, measles can affect all age groups. Rubella, also known as German measles or three-day measles, is an infection caused by a virus different from rubeola (measles). In children, rubella infection is much like a mild case of rubeola. But in adults and teenagers, it can be more severe. The striking feature of rubella infection is the marked enlargement and tenderness of your lymph nodes, which is more severe than with rubeola. Rubella is well known for causing birth defects if a pregnant woman gets this form of measles. For that reason, pregnant women should avoid anyone who may have rubella or rubeola. If exposed, you may talk with your doctor about being immunized with immune globulin after exposure. The rubella vaccine is given as part of the MMR vaccine (measles, mumps, rubella). 
</info>
	
	<info id="ass12">&lt;b&gt;Meningitis Symptoms&lt;/b&gt;&lt;br/&gt;
Meningitis is an inflammation of the meninges, the membranes that cover the brain and spinal cord. It is usually caused by bacteria or viruses, but it can also be caused by certain medications or illnesses. Meningitis can be caused by a variety of things, including bacteria (the most serious), viruses, fungi, reactions to medications, and environmental toxins such as heavy metals.&lt;br/&gt;
Bacteria and viruses that infect the skin, urinary system, gastrointestinal or respiratory tract can spread by the bloodstream to the meningitis through cerebrospinal fluid, the fluid that circulates in and around the spinal cord.
</info>

	
	<info id="intervention1">&lt;b&gt;Increase Daily Water Supply&lt;/b&gt;&lt;br/&gt;
Having enough clean drinking water is a top priority during any emergency! A normally active person needs at least two quarts of water each day. However, needs vary depending on the weather and an individual's age and health status. Interruptions of the water supply and sewage spills are situations which require immediate recovery and remediation measures to assure the health and safety of patients and staff.
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;In an area that has been devastated by an earthquake, the water supply may be disrupted or contaminated. 
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;Consider all water from wells, cisterns and other delivery systems in the disaster area unsafe until tested. 
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;Drink only water you have stored or water that has been treated. To improve the taste of water stored for a long time, pour it from one clean container to another clean container several times.
&lt;br/&gt;
</info>

	<info id="intervention2">&lt;b&gt;Improve Water Quality&lt;/b&gt;&lt;br/&gt;
Water quality is key to water avail-ability. If a water is naturally low-quality (high in minerals, for example) or has been impaired by industrial or municipal use (such as sewage effluent or plant wastewater), it typically is not re-usable for potable purposes unless it's treated.
</info>

	<info id="intervention3">&lt;b&gt;Build Community Pits&lt;/b&gt;&lt;br/&gt;
In some situations on-site, community pits may be a suitable medium-term solution, whilst in others it will be necessary to devise ways of removing and disposing of waste. This will usually involve the following: storage in the house; deposition at intermediate storage point; and collection and transport to final disposal.
</info>

	<info id="intervention4">&lt;b&gt;Dig Defecation Trenches&lt;/b&gt;&lt;br/&gt;
Open defecation should be restricted to agreed areas outside the emergency settlement, away from where local people live, and at least 50 metres from drinking water sources. Trenches can be dug for people to defecate in. Trenches need to be kept clean and covered over with soil each day.
</info>

	<info id="intervention5">&lt;b&gt;Increase Daily Food Supply&lt;/b&gt;&lt;br/&gt;
Food shortages are often an immediate health consequence of disasters. Existing food stocks may be destroyed or disruptions to distribution systems may prevent the delivery of food. In these situations, food relief programs should include the following elements: &lt;br/&gt;
(1) assessment of food supplies available after the disaster, &lt;br/&gt;
(2) determination of the nutritional needs of victims, &lt;br/&gt;
(3) calculation of daily food needs, and &lt;br/&gt;
(4) surveillance of victims' nutritional status.&lt;br/&gt;
An increased demand on water and food supplies, elevated risk of contamination, and disruption of sanitation services all contribute to the risk of a disease outbreak.
</info>

	<info id="intervention6">&lt;b&gt;Treat Cholera &amp; Diarrheal Diseases&lt;/b&gt;&lt;br/&gt;
Cholera can be effectively treated with oral rehydration salts and antibiotics. &lt;br/&gt;
Containing a cholera outbreak involves ensuring there are proper sanitation methods for disposing of sewage, an adequate drinking water supply and good food hygiene. &lt;br/&gt;
Food should be cooked thoroughly and should not be contaminated by contact with raw foods, flies or dirty surfaces. 
</info>

	<info id="intervention7">&lt;b&gt;Treat Malaria&lt;/b&gt;&lt;br/&gt;
The objective of treating uncomplicated malaria is to cure the infection. This is important as it will help prevent progression to severe disease and prevent additional morbidity associated with treatment failure. Cure of the infection means eradication from the body of the infection that caused the illness.&lt;br/&gt;
The primary objective of antimalarial treatment in severe malaria is to prevent death. Prevention of recrudescence and avoidance of minor adverse effects are secondary. In treating cerebral malaria, prevention of neurological deficit is also an important objective. In the treatment of severe malaria in pregnancy, saving the life of the mother is the primary objective.</info>

	<info id="intervention8">&lt;b&gt;Treat Measles&lt;/b&gt;&lt;br/&gt;
After a disaster the threat of disease often increased due to the close living conditions and poor hygiene that result from people being displaced from their homes. Nonimmunized infants may be given the measles vaccination within 72 hours of exposure to the measles virus, to provide protection against the disease. Pregnant women, infants and people with weakened immune systems who are exposed to the virus may receive an injection of proteins (antibodies) that can fight off infection, called immune serum globulin. When given within six days of exposure to the virus, these antibodies can prevent measles or make symptoms less severe. &lt;br/&gt;
Isolation is another element of treatment. Because measles is highly contagious from about four days before to four days after the rash breaks out, people with measles shouldn't return to activities in which they interact with other people during this period.
</info>

	<info id="intervention9">&lt;b&gt;Treat Meningitis&lt;/b&gt;&lt;br/&gt;
Treatment for meningitis depends on the organism causing the infection, your age, the extent of the infection, and the presence of other medical conditions or complications of meningitis.&lt;br/&gt;
Most people with viral meningitis usually start getting better within 3 days of feeling sick and recover within 2 weeks. However, it is important to see your health professional if symptoms of meningitis develop so that he or she can rule out bacterial meningitis, which is more serious. With mild cases of viral meningitis, you may only need home treatment, including fluids to prevent dehydration and medicine to control pain and fever. If you do not get better or if symptoms get worse, you may need further testing to check for other causes of illness. 
</info>

	<info id="intervention10">&lt;b&gt;Open Supplementary Feeding Center&lt;/b&gt;&lt;br/&gt;
Supplementary feeding is a short-term, remedial measure in disaster relief and should be quickly incorporated into a broader plan for relief assistance so that resources can be used most efficiently. The supplementary feeding program must fulfill the minimum standards in disaster response for death during treatment, and the numbers of recovered and abandoned must be nearly adequate.
</info>

	<info id="intervention11">&lt;b&gt;Vaccinate against cholera&lt;/b&gt;&lt;br/&gt;
Cholera vaccine is a suspension of two strains of killed cholera bacteria in saline solution. Phenol is added as a preservative. Cholera vaccine is about 50% effective in preventing disease. The indications for cholera vaccine are travel to or from and residence in countries with cholera. Cholera vaccine is not recommended for infants under six (6) months of age. &lt;br/&gt;The best protection is to avoid contaminated food and water. Vaccination for cholera is not a substitute for careful food and water consumption. Some countries require cholera immunization for persons entering the country, especially when arriving from another country where cholera occurs. 
</info>

	<info id="intervention12">&lt;b&gt;Vaccinate against measles&lt;/b&gt;&lt;br/&gt;
To prevent measles outbreaks. all persons 6 months-35 years of age who are living in displaced persons camps should receive measles-containing vaccine. Vaccine should be administered as soon as they enter an organized camp or settlement. Having previously been vaccinated or having a history of measles disease are not contraindications receiving the vaccine. The vaccine of choice is either measles-rubella (MR) vaccine or measles-mumps-rubella (M-M-R) vaccine. If neither of the above vaccines are available then single-antigen measles vaccine may be administered.
</info>

	<info id="intervention13">&lt;b&gt;Vaccinate against meningitis&lt;/b&gt;&lt;br/&gt;
The purpose of Interim Immunization Recommendations for Individuals Displaced by a Disaster is two-fold: 
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;To ensure that children, adolescents, and adults are protected against vaccine-preventable diseases in accordance with current recommendations.
&lt;br/&gt;
&lt;span style='font-family: verdana; font-size:14px;'&gt;&#8226;&lt;/span&gt;To reduce the likelihood of outbreaks of vaccine-preventable diseases in large crowded group settings. 

</info>
	
</root>"""
