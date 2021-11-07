# Thomeer-Used-to-Model-High-Pressure-Mercury-Injection-Data
In this repository we provide the python code used to Closure correct and model High Pressure Mercury Injection (HPMI) data using the Thomeer hyperbola.

This is the GitHub repository for the python code used to model High Pressure Mercury Injection (HPMI) Core data employing the Thomeer hyperbola to model the Thomeer Capillary Pressure parameters as shown below. We use this software to develop our own Core Characterization Reservoir-Specific calibration database for your next reservoir characterization project.

![HPMI_Image](HPMI.png)

The following animated image illustrates how this software operates. We start with the original HPMI data. The first step is to locate the point on the HPMI curve that represents the point where real data begins and not the HPMI data representing surface conformance around the plug sample. We also select the Initial Displacement Pressure (Pd1) for the sample for the first pore system. We find that most carbonate rock has bi-modal pore throat distributions representing two pore systems as shown in this example. The selection of this point is done with a click on the Graphical User Interface (GUI) where this occurs. The second step pick the point for the Bulk Volume for the first pore system (BV1) and the Initial Displacement Pressure for the second pore system (Pd2).

The second step pick the point for the Bulk Volume for the first pore system (BV1) and the Initial Displacement Pressure for the second pore system (Pd2).

The third step is to select the Total porosity for the HPMI data called BVtotal where:

      BV2 = BVtotal - BV1

![HPMI_Image](Thomeer_Parameter_fitting.gif)

The program then uses Scipy Optimize Curve_fit to estimate the appropriate Thomeer parameters to model the HPMI data using these Thomeer Capillary Pressure parameters. The points selected from the GUIs are used to estimate boundary conditions for the estimations. 

At this point we are using the data from one HPMI sample for our example. Our objective will be to employ this program as a Geolog python loglan and read the Pc data from the SCAL data stored in a well and write the results for each sample back to Geolog to build our core calibration database. We would then use the carbonate characterization workflow as employed in our following repository but alter the workflow to use our own reservoir specific data for our own reservoir characterization.

https://github.com/Philliec459/Geolog-Used-to-Automate-the-Characterization-Workflow-using-Clerkes-Rosetta-Stone-calibration-data


