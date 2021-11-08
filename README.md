# Thomeer-Used-to-Model-High-Pressure-Mercury-Injection-Data
In this repository we provide the python code used to Closure correct and model High Pressure Mercury Injection (HPMI) data using the Thomeer hyperbola.

This GitHub repository uses python code used to input High Pressure Mercury Injection (HPMI) Core data and then employ the Thomeer hyperbola to model the Thomeer Capillary Pressure parameters as shown below. Ed Clerke used a similar method in Excel with Solver to estimate his Thomeer parameters for each HPMI sample that went into the Rosetta Stone Arab D Carbonate Thomeer database. We use these types of software to establish our own Core Characterization Reservoir-Specific calibration database for a reservoir-specific reservoir characterization project.

![HPMI_Image](HPMI.png)

The following animated image illustrates how this software operates. We start with the original HPMI data. The first step is to locate the point on the HPMI curve that represents the point where real data begins and not the HPMI data representing surface conformance around the plug sample. We also select the Initial Displacement Pressure (Pd1) for the sample for the first pore system too. We find that most carbonate rocks have bi-modal pore throat distributions representing two pore systems as shown in the example below. The selection of this point is performed with just a click on the Graphical User Interface (GUI) where this occurs. 

For the second step we pick the point for the Bulk Volume porosity of the first pore system (BV1) as well as the Initial Displacement Pressure for the second pore system (Pd2).

The third step is to select the Total porosity for the HPMI data called BVtotal where the porosity of the second pore system is called BV2:

      BV2 = BVtotal - BV1

![HPMI_Image](Thomeer_Parameter_fitting.gif)

This program uses Scipy Optimize Curve_fit to estimate the appropriate Thomeer parameters necessary to model the HPMI data. The points selected from the GUIs are used to estimate boundary conditions for these estimations, and the estimations for this example are shown below:

            Thomeer Parameters Estimated from Example 1 HPMI Data:
            Pd1 = 9.05 ,  G1 = 0.51 , BV1 = 9.97
            Pd2 = 374.4 , G2 = 0.25 , BV2 = 3.63

We are using the HPMI data from just one sample for this example. Our objective will be to employ this program in Geolog as a python loglan. In Geolog we will read the Pc data in from the SCAL data stored in a well and write the results for each sample back to Geolog to build our sample-by-sample core calibration database. We would then use the carbonate characterization workflow as employed in our following GitHub repository but alter the workflow to employ our own new reservoir-specific calibration data for our reservoir characterization.

https://github.com/Philliec459/Geolog-Used-to-Automate-the-Characterization-Workflow-using-Clerkes-Rosetta-Stone-calibration-data

In the above workflows we have used hundreds of HPMI samples as calibration. In the image below we are showing the Porosity vs. Permeability cross plot in the upper left for all the calibration samples used for the Arab D reservoir; all colored by Petrophysical Rock Type. We select a small group of poro-perm samples, and the Pc curves from this small group of selected samples is then shown in the lower left. The black Pc curve is the upscaled Pc curve from the selected samples. We would be using upscaled Pc curves that varies level by level in the well to model saturations because of the changing reservoir quality along the wellbore.

![HPMI_Image](geolog_altair_thomeer.gif)

Also, the following image shows one example from our modeling of saturations from Capillary Pressure vs. log analysis. The match is very good. I personally have performed this type of characterization on at least 30 huge carbonate oil fields in Saudi, and the results shown below are very typical.

![HPMI_Image](logsats.gif)
