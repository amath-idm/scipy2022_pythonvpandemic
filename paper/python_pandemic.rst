:author: Cliff Kerr 
:email: cliff@covasim.org
:institution: Institute for Disease Modeling, Bill & Melinda Gates Foundation
:institution: School of Physics, University of Sydney

:author: Robyn Stuart 
:email: robyn@math.ku.dk
:institution: Department of Mathematical Sciences, University of Copenhagen
:institution: Burnet Institute

:author: Dina Mistry 
:email: dina.c.mistry@gmail.com
:institution: Twitter

:author: Romesh Abeysuriya 
:email: romesh.abeysuriya@burnet.edu.au
:institution: Burnet Institute

:author: Jamie Cohen 
:email: jamie.cohen@gatesfoundation.org
:institution: Institute for Disease Modeling, Bill & Melinda Gates Foundation

:author: Lauren George 
:email: lauren.george@live.com
:institution: Microsoft

:author: Michał Jastrzębski 
:email: inc007@gmail.com
:institution: GitHub

:author: Michael Famulare 
:email: mike.famulare@gatesfoundation.org
:institution: Institute for Disease Modeling, Bill & Melinda Gates Foundation

:author: Edward Wenger 
:email: edward.wenger@gatesfoundation.org
:institution: Institute for Disease Modeling, Bill & Melinda Gates Foundation

:author: Daniel Klein 
:email: daniel.klein@gatesfoundation.org
:institution: Institute for Disease Modeling, Bill & Melinda Gates Foundation




:bibliography: python_pandemic


-------------------------------------------------------------------------
Python vs. the pandemic: a case study in high-stakes software development
-------------------------------------------------------------------------

.. class:: abstract

   When it became clear in early 2020 that COVID-19 was going to be a major public health threat, politicians and public health officials turned to academic disease modelers like us for urgent guidance. Academic software development is typically a slow and haphazard process, and we realized that business-as-usual would not suffice for dealing with this crisis. Here we describe the case study of how we built Covasim (covasim.org), an agent-based model of COVID-19 epidemiology and public health interventions, by using standard Python libraries like NumPy, Numba, and SciPy along with less common ones like Sciris (sciris.org). Covasim was created in a few weeks, an order of magnitude faster than the typical model development process, and achieves performance comparable to C++ despite being written in pure Python. It has become one of the most widely adopted COVID models, and is used by researchers and policymakers in dozens of countries. Covasim's rapid development was enabled not only by leveraging the Python scientific computing ecosystem, but also by adopting coding practices and workflows that lowered the barriers to entry for scientific contributors without sacrificing either performance or rigor.

.. class:: keywords

   COVID-19, SARS-CoV-2, Epidemiology, Mathematical modeling, NumPy, Numba, Sciris



Background
----------

For decades, scientists have been concerned about the possibility of another global pandemic on the scale of the 1918 flu [REF:pandemic]. Despite a number of "close calls", including outbreaks of SARS in 2002 [REF:sars], Ebola in 2014-2016 [REF:ebola], and flu outbreaks including 1957, 1968, and H1N1 in 2009 [REF:flu] – some of which led to 1 million or more deaths – the world had avoided experiencing a planetary-scale emergent pathogen since the HIV in the 1980s [REF:hiv]. 

In 2015, Bill Gates gave a TED talk stating that the world was not ready to deal with another pandemic [REF:bill]. While the Bill and Melinda Gates Foundation (BMGF) has not historically focused on pandemic preparedness, its expertise in disease surveillance, modeling, and drug discovery made it well placed to contribute to a global pandemic response plan. Founded in 2008, the Institute for Disease Modeling (IDM) has provided analytical support for BMGF and other global health partners, including efforts to eradicate malaria and polio. Since its founding, IDM has built up a portfolio of computational tools to understand, analyze, and predict the dynamics of different diseases.

When "coronavirus disease 2019" (COVID-19) and the virus that causes it (SARS-CoV-2) were first identified in late 2019, our team began summarizing what was known about the virus  [REF:mike-reports]. By early February 2020, even though it was more than a month before the WHO would declare a pandemic [REF:who], it had become clear that COVID-19 was emerging as a major public health threat. The outbreak on the Diamond Princess cruise ship [REF:diamond] was the impetus for us to start modeling COVID in detail. Specifically,  we needed a tool to (a) incorporate new data as soon as it became available, (b) explore policy scenarios, and (c) predict likely future epidemic trajectories.

The first step was to identify which software tool would form the best starting point for our new COVID model. The richest modeling framework used by IDM at the time was EMOD, which is a multi-disease agent-based model written in C++ and based on JSON configuration files [REF:emod]. We also considered Atomica, a multi-disease compartmental model written in Python and based on Excel input files [REF:atomica]. However, both options had significant drawbacks: as a compartmental model, Atomica was unable to capture the individual level detail necessary for modeling the Diamond Princess outbreak (such as passenger-crew interactions); EMOD had sufficient flexibility, but developing new disease modules had historically required months rather than days. 

As a result, we instead started developing Covasim ("COVID-19 Agent-based Simulator") from a nascent agent-based model written in Python, LEMOD-FP ("Light"-EMOD for Family Planning). LEMOD-FP was used to model reproductive health choices of women in Senegal, and this model had in turn been based on an even simpler agent-based model of measles vaccination programs in Nigeria ("Value-of-information simulator" or VoISim). The timeline and interrelations between IDM's software ecosystem are shown in Fig. :ref:`ecosystem`.


.. figure:: fig_ecosystem.png

   IDM's software ecosystem. :label:`ecosystem`


Parallel to the development of Covasim, other research teams at IDM developed their own COVID models, including one based on the EMOD framework [REF:emod], and one based on an earlier influenza model [REF:corvid]. However, while both of these models saw use in academic contexts [REF:emod-rural] [REF:corvid-lancet], neither was able to incorporate new features quickly enough, or was easy enough to use, for widespread adoption in a policy context.

Covasim, by contrast, had immediate real-world impact. The first version was released on 10 March 2020, and on 12 March 2020, its output was presented by Governor Jay Inslee of Washington State as justification for school closures and social distancing measures [REF:inslee]. Since the early days of the pandemic, Covasim releases have coincided with major events in the pandemic, especially the identification of new variants of concern (Fig. :ref:`releases`). Covasim was quickly adopted globally, including applications in the UK regarding school closures [REF:jasmina], Australia regarding outbreak control [REF:robyn], and Vietnam regarding lockdown measures [REF:quang]. 


.. figure:: fig_releases.png

   Covasim releases since the start of the pandemic. :label:`releases`


To date, Covasim has been downloaded from PyPI over 100,000 times [REF:pypi], used in dozens of academic studies [REF:natcomms], and informed decision-making on every continent (Fig. :ref:`worldmap`). We believe key elements of its success include (a) the simplicity of its architecture, such as using a relatively small number of classes; (b) high performance, enabled by the use of NumPy arrays and Numba decorators; (c) our emphasis on prioritizing usability, including flexible type handling and careful choices of default settings. In the remainder of this paper, we outline these principles in more detail. Our aim is to provide a roadmap for how to quickly develop high-performance scientific computing libraries.


.. figure:: fig_worldmap.png
   :align: center
   :scale: 20%
   :figclass: w

   Covasim releases since the start of the pandemic. :label:`worldmap`



Software architecture and implementation
----------------------------------------

Covasim conceptual design and usage
+++++++++++++++++++++++++++++++++++

Covasim is a standard susceptible-infected-exposed-recovered (SEIR) model (Fig. :ref:`seir`). It is an agent-based model, meaning that individual people and their interactions with one another are simulated. The fundamental calculation that Covasim performs is to calculate the probability that a given person, on a given time step, will change from one state to another, such as from susceptible to infected (i.e., they were infected), from undiagnosed to diagnosed, or from critically ill to dead. Covasim is fully open-source and available on GitHub (http://covasim.org) or PyPI (``pip install covasim``), and comes with comprehensive documentation (http://docs.covasim.org).


.. figure:: fig_seir.png

   Basic Covasim disease model. The blue arrow shows the process of reinfection. :label:`seir`


The first principle of Covasim's design philosophy is that "Common tasks should be simple" – for example, defining parameters, running a simulation, and plotting results. The following example illustrates this principle: it creates a simulation with a custom parameter value, runs it, and plots the results:


.. code-block:: python

   import covasim as cv
   cv.Sim(pop_size=100e3).run().plot()


The second principle of the design philosophy is "Uncommon tasks can't always be simple, but they still should be possible". Examples include writing a custom goodness-of-fit function or defining a new population structure. To some extent, the second principle is at odds with the first, since the more flexibility an interface has, typically the more complex it is as well.

For example, the following code and Fig. :ref:`example` shows the result of running two simulations to determine the impact of a custom intervention aimed at protecting the elderly:


.. code-block:: python

   import covasim as cv

   # Custom intervention
   def elderly(sim):
       if sim.t == sim.day('2020-04-01'):
           elderly = sim.people.age>70
           sim.people.rel_sus[elderly] = 0.0

   pars = dict(
       pop_type = 'hybrid', # More realistic population
       location = 'japan', # Japan characteristics
       pop_size = 50e3, # Have 50,000 people total
       pop_infected = 100, # 100 infected people
       n_days = 90, # Run for 90 days
       verbose = 0, # Do not print output
   )

   # Running in parallel
   label = 'Protect the elderly'
   s1 = cv.Sim(pars, label='Default')
   s2 = cv.Sim(pars, interventions=elderly, label=label)
   msim = cv.parallel(s1, s2)
   fig = msim.plot(['cum_deaths', 'cum_infections'])


.. figure:: fig_example.png

   Running a custom intervention in Covasim, illustrating the tradeoff between simplicity and flexibility. :label:`example`



Simplifications using Sciris
++++++++++++++++++++++++++++

A key component of Covasim's architecture is heavy reliance on Sciris [REF:sciris], a library of functions for scientific computing that provide additional flexibility and ease-of-use on top of NumPy, SciPy, and Matplotlib, including parallel computing, array operations, and high-performance container datatypes. 

As shown in Fig. :ref:`sciris`, Sciris significantly reduces the number of lines of code required to perform common scientific tasks, allowing the user to focus on the code's scientific logic rather than the low-level implementation. Key Covasim features that rely on Sciris include: ensuring consistent list, dictionary, array types; referencing ordered dictionary elements by index; handling and interconverting dates; saving and loading files; and running simulations in parallel.


.. figure:: fig_sciris.png

   Comparison of functionally identical code implemented with (left) and without (right) Sciris. :label:`sciris`



Array-based architecture
++++++++++++++++++++++++

In a typical agent-based simulation, the outermost loop is over time, while the inner loops iterate over different agents and agent states. For a simulation like Covasim, with roughly 700 (daily) timesteps, tens or hundreds of thousands of agents, and several dozen states, this requires on the order of one billion update steps.

However, we can take advantage of the fact that each state (such as agent age or their infection status) has the same data type, and thus we can avoid an explicit loop over agents by instead representing agents as entries in NumPy vectors, and performing operations on these vectors. These two architectures are shown in Fig. :ref:`array`. Compared to the explicitly object-oriented implementation of an agent-based model, the array-based version is 1-2 orders of magnitude faster for population sizes larger than 10,000 agents (Fig. :ref:`perf`). Example code implementations of the two approaches (for FPsim) are shown below.


.. figure:: fig_array.png

   The standard object-oriented approach for implementing agent-based models (top), compared to the array-based approach used in Covasim (bottom). :label:`array`


.. figure:: fig_perf.png

   Performance comparison for FPsim from an explicit loop-based approach compared to an array-based approach. :label:`perf`


TODO: fix long lines


.. code-block:: python
   
   #%% Loop-based agent simulation

   if self.alive:  # Do not move through step if not alive

    self.age_person()  # Age person in units of the timestep
    self.check_mortality()  # Decide if person dies
    if not self.alive:
        return self.step_results

    if self.sex == 0 and self.age < self.pars['age_limit_fecundity']:

        if self.pregnant:
            self.check_delivery()  # Deliver with birth outcomes
            self.update_pregnancy()  # Advance gestation in timestep
            if not self.alive:
                return self.step_results

        if not self.pregnant:
            self.check_sexually_active()
            if self.pars['method_age']<=self.age<self.pars['age_lim_fecund']:
                self.update_contraception(t, y)
            self.check_lam()
            if self.sexually_active:
                self.check_conception()  # Decide if conceives
            if self.postpartum:
                self.update_postpartum() # Updates postpartum counter

        if self.lactating:
            self.update_breastfeeding()


.. code-block:: python

   #%% Array-based agent simulation
   
   alive_inds = sc.findinds(self.alive)
   self.age_person(inds=alive_inds)  # Age person in units of the timestep
   self.check_mortality(inds=alive_inds)  # Decide if person dies

   fbool = self.alive*(self.sex==0)*(self.age<self.pars['age_lim_fecund'])
   fecund_inds  = sc.findinds(fbool)
   preg_inds    = fecund_inds[sc.findinds(self.pregnant[fecund_inds])]
   nonpreg_inds = np.setdiff1d(fecund_inds, preg_inds)
   lact_inds    = fecund_inds[sc.findinds(self.lactating[fecund_inds])]

   # Update everything
   self.check_delivery(preg_inds)  # Deliver with birth outcomes
   self.update_pregnancy(preg_inds)  # Advance gestation in timestep
   self.check_sexually_active(nonpreg_inds)
   self.update_contraception(nonpreg_inds)
   self.check_lam(nonpreg_inds)
   self.update_postpartum(nonpreg_inds) # Updates postpartum counter
   self.update_breastfeeding(lact_inds)
   self.check_conception(nonpreg_inds)  # Decide if conceives



Numba optimization
++++++++++++++++++

Numba is a compiler that translates subsets of Python and NumPy into machine code [REF:numba]. Each low-level numerical function was tested with and without Numba decoration; in some cases speed improvements were negligible, wile in other cases they were considerable. For example, the following function is roughly 10 times faster with the Numba decorator than without:


.. code-block:: python

   @nb.njit((nb.int32, nb.int32), cache=True)
   def choose_r(max_n, n):
       return np.random.choice(max_n, n, replace=True)


Since Covasim is stochastic, calculations rarely need to be exact; as a result, most numerical operations are performed as 32-bit operations.

Together, these speed optimizations allow Covasim to run at speeds comparable to agent-based models implemented in C\+\+. Practically, this means that most users can run Covasim analyses on their laptops without needing to use cloud-based HPC resources.



Lessons for scientific software development
-------------------------------------------

Accessible coding and design
++++++++++++++++++++++++++++

Since Covasim was designed to be used by scientists and health officials, not developers, we made a number of design decisions that were aimed to improve accessibility to our audience, rather than follow common principles of good software design.

First, Covasim is designed to have as flexible of user inputs as possible. For example, a date can be specified as an integer number of days from the start of the simulation, as a string (e.g. ``'2020-04-04'``), or as a ``datetime.datetime`` object. Similarly, numeric inputs that can have either one or multiple values (such as the change in transmission rate following one or multiple lockdowns) can be provided as a scalar, list, or NumPy array. As long as the input is unambiguous, we prioritized ease-of-use and simplicity of the interface over rigorous type checking. Since Covasim is a top-level library (i.e., it does not perform low-level functions as part of other libraries), this prioritization has been welcomed by its users.

Second, "advanced" Python programming paradigms – such as method and function decorators, lambda functions, multiple inheritance, and "dunder" methods – have been avoided where possible, even when they would otherwise be good coding practice. This is because a relatively large fraction of Covasim users, including those with relatively limited Python backgrounds, need to inspect and modify the source code. A Covasim user coming from an R programming background, for example, is unlikely to have encountered the NumPy function ``intersect1d()`` before, they can quickly look it up and relate it to R's ``intersect()`` function. In contrast, an R user who has not encountered decorators before is unlikely to be able to look them up and understand their meaning (indeed, they may not even know what terms to search for). While Covasim indeed does use all of the advanced methods listed above, they have been kept to a minimum and sequestered in particular files the user is less likely to interact with.

Third, testing for Covasim presented a major challenge. Given that Covasim was being used to make decisions that affected tens of millions of people, even the smallest errors could have potentially catastrophic consequences. Furthermore, errors could be not only in the software logic but also in an incorrect parameter value or a misinterpreted study. Compounding these challenges, features often had to be developed and used within hours to days to be of use to policymakers, a speed which was incompatible with typical software testing approaches. In addition, the rapidly evolving codebase made it difficult to write even simple regression tests. Our solution was to use a hierarchical testing approach: low-level functions were tested through a standard software unit test approach, while new features and higher-level outputs were tested extensively by epidemiologists who varied inputs corresponding to realistic scenarios, and checked the outputs (predominantly in the form or graphs) against their intuition. We found that these high-level "sanity checks" were far more effective in catching bugs than formal software tests, and shifted the emphasis of our test suite to prioritize the former. Despite extensive scrutiny, both by our external collaborators and by "COVID skeptics" [REF:skeptics], to our knowledge, no bug that had a qualitative effect on the results ever made it through to production.


Workflow and team management
++++++++++++++++++++++++++++

Covasim was developed by a team of roughly 75 people with widely disparate backgrounds: from those with 20+ years of enterprise-level software development experience and no public health background, through to public health experts with virtually no prior experience in Python. Roughly 45% of Covasim contributors had significant Python expertise, while 60% had public health experience; only about half a dozen contributors (<10%) had significant experience in both areas. 

These half-dozen contributors formed a core group (including the authors of this paper) that oversaw overall Covasim development. Using GitHub for both software and project management, we created issues and assigned them to other contributors based on urgency and skillset match. At least one person from this group would also review all pull requests prior to merge. While the dangers of accepting changes from contributors with limited Python experience is obvious, considerable risks were also posed by contributors who lacked epidemiological insight. For example, several tests were written based on assumptions that were true for a given time and place, but not valid for other geographical contexts.

One surprising outcome was that even though Covasim is largely a software project, after the initial phase of development (i.e., the first 4-8 weeks), we found that relatively few tasks could be assigned to the developers as opposed to the epidemiologists on the project. We believe there are several reasons for this. First, epidemiologists tended to be much more aware of knowledge they were missing (e.g., what a particular NumPy function did), and were more readily able to fill that gap (e.g., look it up in the documentation or on Stack Overflow). By contrast, developers were less able to identify gaps in their knowledge and address them (e.g., by finding a study on Google Scholar). As a consequence, many of the epidemiologists' software skills improved markedly over the first few months, while the developers' epidemiology knowledge increased more slowly. Second, and more importantly, we found that once transparent and performant software engineering practices had been implemented, epidemiologists were able to successfully adapt them to new contexts even without complete understanding of the code. Thus, for developing a scientific software tool, it appears that optimal staffing would consist of a roughly equal ratio of developers and domain experts during the early development phase, followed by a rapid (on a timescale of weeks) ramp-down of developer resources.

Acknowledging that Covasim's potential user base includes many people who have limited coding skills, we developed a three-tiered support model to maximize Covasim's real-world policy impact (Fig. :ref:`modes`). For "mode 1" engagements, we perform the work using Covasim ourselves; while this mode typically ensures high quality and efficiency, it is highly resource-constrained and thus used only for our highest-profile engagements, such as with Washington State [REF:natcomms]. For "mode 2" engagements, we offer our partners training on how to use Covasim, and let them lead analyses with our feedback; this is our most common and most impactful mode of engagement [REF:quang] [REF:jasmina] [REF:qld]. Finally, "mode 3" partnerships, in which we provide a tool that others download and use without our input, are the most common in the broader Python ecosystem. While this mode is by far the most scalable, in practice, relatively few (such as state health departments or ministries of health) have the time and internal technical capacity to use this mode.


.. figure:: fig_modes.png

   The three pathways to impact with Covasim, from high bandwidth/small scale to low bandwidth/large scale. IDM: Institute for Disease Modeling; OSS: open-source software; GPG: global public good; PyPI: Python Package Index. :label:`modes`



Future directions
-----------------

While the need for COVID modeling is hopefully starting to decrease, we and our collaborators are continuing development of Covasim by updating parameters with the latest scientific evidence, implementing new immune dynamics [REF:jamie], and providing other usability and bugfix updates. We also continue to provide support and training workshops (including, for the first time, in person).

We are using what we learned during the development of Covasim to build a broader suite of Python-based disease modeling tools (tentatively named "\*-sim" or "Starsim"). The suite of Starsim tools under development includes models for family planning [REF:fp-poster], polio, respiratory syncytial virus (RSV), and human papillomavirus (HPV). To date, each tool in this suite uses an independent codebase, and is related to Covasim only through the shared design principles described above, and by having used the Covasim codebase as the starting point for development. 

A major open question is whether the disease dynamics implemented in Covasim and these related models have sufficient overlap to be refactored into a single disease-agnostic modeling library, which the disease-specific modeling libraries would then import. This "core and specialization" approach was adopted by EMOD and Atomica, and while both frameworks continue to be used, neither has been broadly adapted within the disease modeling community. The alternative approach, currently used by the Starsim suite, is for each disease model to be a self-contained library. A shared library would reduce code duplication, and allow new features and bugfixes to be immediately rolled out to multiple models simultaneously. However, it would also increase interdependencies that would have the effect of increasing code complexity, increasing the risk of introducing subtle bugs. Which of these two options is preferable likely depends on the speed with which new disease models need to be implemented. We hope that for the foreseeable future, none will need to be implemented as quickly as COVID.





Bibliographies, citations and block quotes
------------------------------------------

If you want to include a ``.bib`` file, do so above by placing  :code:`:bibliography: yourFilenameWithoutExtension` as above (replacing ``mybib``) for a file named :code:`yourFilenameWithoutExtension.bib` after removing the ``.bib`` extension. 

**Do not include any special characters that need to be escaped or any spaces in the bib-file's name**. Doing so makes bibTeX cranky, & the rst to LaTeX+bibTeX transform won't work. 

To reference citations contained in that bibliography use the :code:`:cite:`citation-key`` role, as in :cite:`hume48` (which literally is :code:`:cite:`hume48`` in accordance with the ``hume48`` cite-key in the associated ``mybib.bib`` file).

However, if you use a bibtex file, this will overwrite any manually written references. 

So what would previously have registered as a in text reference ``[Atr03]_`` for 

:: 

     [Atr03] P. Atreides. *How to catch a sandworm*,
           Transactions on Terraforming, 21(3):261-300, August 2003.

what you actually see will be an empty reference rendered as **[?]**.

E.g., [Atr03]_.


If you wish to have a block quote, you can just indent the text, as in 

    When it is asked, What is the nature of all our reasonings concerning matter of fact? the proper answer seems to be, that they are founded on the relation of cause and effect. When again it is asked, What is the foundation of all our reasonings and conclusions concerning that relation? it may be replied in one word, experience. But if we still carry on our sifting humor, and ask, What is the foundation of all conclusions from experience? this implies a new question, which may be of more difficult solution and explication. :cite:`hume48`

Dois in bibliographies
++++++++++++++++++++++

In order to include a doi in your bibliography, add the doi to your bibliography
entry as a string. For example:

.. code-block:: bibtex

   @Book{hume48,
     author =  "David Hume",
     year =    "1748",
     title =   "An enquiry concerning human understanding",
     address =     "Indianapolis, IN",
     publisher =   "Hackett",
     doi = "10.1017/CBO9780511808432",
   }


If there are errors when adding it due to non-alphanumeric characters, see if
wrapping the doi in ``\detokenize`` works to solve the issue.

.. code-block:: bibtex

   @Book{hume48,
     author =  "David Hume",
     year =    "1748",
     title =   "An enquiry concerning human understanding",
     address =     "Indianapolis, IN",
     publisher =   "Hackett",
     doi = \detokenize{10.1017/CBO9780511808432},
   }

Source code examples
--------------------

Of course, no paper would be complete without some source code.  Without
highlighting, it would look like this::

   def sum(a, b):
       """Sum two numbers."""

       return a + b

With code-highlighting:

.. code-block:: python

   def sum(a, b):
       """Sum two numbers."""

       return a + b

Maybe also in another language, and with line numbers:

.. code-block:: c
   :linenos:

   int main() {
       for (int i = 0; i < 10; i++) {
           /* do something */
       }
       return 0;
   }

Or a snippet from the above code, starting at the correct line number:

.. code-block:: c
   :linenos:
   :linenostart: 2

   for (int i = 0; i < 10; i++) {
       /* do something */
   }
 
Important Part
--------------

It is well known [Atr03]_ that Spice grows on the planet Dune.  Test
some maths, for example :math:`e^{\pi i} + 3 \delta`.  Or maybe an
equation on a separate line:

.. math::

   g(x) = \int_0^\infty f(x) dx

or on multiple, aligned lines:

.. math::
   :type: eqnarray

   g(x) &=& \int_0^\infty f(x) dx \\
        &=& \ldots

The area of a circle and volume of a sphere are given as

.. math::
   :label: circarea

   A(r) = \pi r^2.

.. math::
   :label: spherevol

   V(r) = \frac{4}{3} \pi r^3

We can then refer back to Equation (:ref:`circarea`) or
(:ref:`spherevol`) later.

Mauris purus enim, volutpat non dapibus et, gravida sit amet sapien. In at
consectetur lacus. Praesent orci nulla, blandit eu egestas nec, facilisis vel
lacus. Fusce non ante vitae justo faucibus facilisis. Nam venenatis lacinia
turpis. Donec eu ultrices mauris. Ut pulvinar viverra rhoncus. Vivamus
adipiscing faucibus ligula, in porta orci vehicula in. Suspendisse quis augue
arcu, sit amet accumsan diam. Vestibulum lacinia luctus dui. Aliquam odio arcu,
faucibus non laoreet ac, condimentum eu quam. Quisque et nunc non diam
consequat iaculis ut quis leo. Integer suscipit accumsan ligula. Sed nec eros a
orci aliquam dictum sed ac felis. Suspendisse sit amet dui ut ligula iaculis
sollicitudin vel id velit. Pellentesque hendrerit sapien ac ante facilisis
lacinia. Nunc sit amet sem sem. In tellus metus, elementum vitae tincidunt ac,
volutpat sit amet mauris. Maecenas [#]_ diam turpis, placerat [#]_ at adipiscing ac,
pulvinar id metus.

.. [#] On the one hand, a footnote.
.. [#] On the other hand, another footnote.

.. figure:: fig_ecosystem.png

   This is the caption. :label:`egfig`

.. figure:: fig_ecosystem.png
   :align: center
   :figclass: w

   This is a wide figure, specified by adding "w" to the figclass.  It is also
   center aligned, by setting the align keyword (can be left, right or center).

.. figure:: fig_ecosystem.png
   :scale: 20%
   :figclass: bht

   This is the caption on a smaller figure that will be placed by default at the
   bottom of the page, and failing that it will be placed inline or at the top.
   Note that for now, scale is relative to a completely arbitrary original
   reference size which might be the original size of your image - you probably
   have to play with it. :label:`egfig2`

As you can see in Figures :ref:`egfig` and :ref:`egfig2`, this is how you reference auto-numbered
figures.

.. table:: This is the caption for the materials table. :label:`mtable`

   +------------+----------------+
   | Material   | Units          |
   +============+================+
   | Stone      | 3              |
   +------------+----------------+
   | Water      | 12             |
   +------------+----------------+
   | Cement     | :math:`\alpha` |
   +------------+----------------+


We show the different quantities of materials required in Table
:ref:`mtable`.


.. The statement below shows how to adjust the width of a table.

.. raw:: latex

   \setlength{\tablewidth}{0.8\linewidth}


.. table:: This is the caption for the wide table.
   :class: w

   +--------+----+------+------+------+------+--------+
   | This   | is |  a   | very | very | wide | table  |
   +--------+----+------+------+------+------+--------+

Unfortunately, restructuredtext can be picky about tables, so if it simply
won't work try raw LaTeX:


.. raw:: latex

   \begin{table*}

     \begin{longtable*}{|l|r|r|r|}
     \hline
     \multirow{2}{*}{Projection} & \multicolumn{3}{c|}{Area in square miles}\tabularnewline
     \cline{2-4}
      & Large Horizontal Area & Large Vertical Area & Smaller Square Area\tabularnewline
     \hline
     Albers Equal Area  & 7,498.7 & 10,847.3 & 35.8\tabularnewline
     \hline
     Web Mercator & 13,410.0 & 18,271.4 & 63.0\tabularnewline
     \hline
     Difference & 5,911.3 & 7,424.1 & 27.2\tabularnewline
     \hline
     Percent Difference & 44\% & 41\% & 43\%\tabularnewline
     \hline
     \end{longtable*}

     \caption{Area Comparisons \DUrole{label}{quanitities-table}}

   \end{table*}

Perhaps we want to end off with a quote by Lao Tse [#]_:

  *Muddy water, let stand, becomes clear.*

.. [#] :math:`\mathrm{e^{-i\pi}}`

.. Customised LaTeX packages
.. -------------------------

.. Please avoid using this feature, unless agreed upon with the
.. proceedings editors.

.. ::

..   .. latex::
..      :usepackage: somepackage

..      Some custom LaTeX source here.

References
----------
.. [Atr03] P. Atreides. *How to catch a sandworm*,
           Transactions on Terraforming, 21(3):261-300, August 2003.


