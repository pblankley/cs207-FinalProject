### Motivate and describe the feature
Currently the user can use chemkin to calculate reaction rates and produce final numerical output for a given temperature.  However, we expect that the user will often need to translate the reaction rates into a form that can be more easily distributed and disseminated.  
For example, one of the common uses of this package will be to publish findings in journals.  For each iteration of the journal writing, the user will need to invest time in producing results, pasting them into the appropriate output, and visualizing them to a high quality standard.
We propose an additional chemkin feature that would automate these outputs.  Other anticipated “use cases” that we would prepare solution for include:
The user may wish to export the results to more portable output format, such as a .csv, txt., .json or HDF5.
The user may be interested in tabulating their data in a repeatable format
The user may need to visualize outputs at a range of temperatures rather than a single temperature, and repeatedly across a number of reactions
The user may be interested in finding local or global maxima/minima across the output temperature range
Our package would support three new output methodologies:
1. Automated graphing,
2. Multiple common output formats, and
3. Tabulation and “pretty print” presentation of numerical findings

##### Explain how the feature will fit into your code base (and package)
To achieve this, we would create a “wrapper” class around the ReactionSet() class with its own set of methods, built for more 
The rationale behind this approach is that it would leave the basic ReactionSet() class available for python-level calculations for the user, but more repeatable “range level” scripts could be written to produce outputs for direct export to final documents.
Discuss the modules that you will write to realize your feature/ Map out the methods you plan on implementing
We would encompass all of the necessary methods into a single class, called PrettyReaction().  Pretty reaction would include the following methods:
	a) prettyReaction.tables(ReactionSet, columns, species, comparison_basis)
	Runs comparison tables for reaction rates and progress rates for each specie.  Can compare between species or between multiple reactions.
	b) prettyReaction.prettyOutput(ReactionSet, columns, species, consolidate, format)
	Computes reaction rates for multiple reactions and exports formatted outputs into any of .txt, .csv, .json, or HDF5 format.  Text outputs will be “pretty printed” for readability and transportability into final documents
	c) prettyReaction.plot(ReactionSet, species, tmin, tmax)
	Calculates each reaction and outputs into a repeatable format.  Would also use internal settings to format the chart – these include automatically adding chart elements such as positioning lines for local and global temperature maxima, thresholds indicating minimum acceptable reaction rate, and so on.
	d) prettyReaction.ExportPlotConfig(*args)
	Exports a .json with chart format args to be repeated for future reactions (or sets of reactions)
	d) prettyReaction.ImportPlotConfig(*args)
	Imports a .json with chart format args to from previous reactions.

##### Overview how you envision the user to use your new feature
If a user desired formatted outputs, they would declare an arbitrary number of reactions using the existing ReactionSet class.  They would then instantiate a prettyReaction class instance with the reaction module as an argument.  
At that point, the user would all call all outputs directly from the prettyReaction class.  It would handle the inputs and manage the ReactionSet class to obtain the necessary outputs.

##### Discuss any external dependencies that your feature will require
We will build the plotting functionality on top of MatplotLib.  The HDF5 outputs will use H5py.  	Each of these libraries is open source, well documented, and accepted as a de facto standard for Python.
JSON, txt, and CSV outputs will all use native functions from python 3.5.  
