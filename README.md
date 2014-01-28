poser-hand-generator
====================

Poser scripts for generate hand images together with ground truth pose, as used in ["Non-parametric hand pose estimation with object context"](http://www.sciencedirect.com/science/article/pii/S0262885613000656) by Romero et al. They are heavily based on the fantastic poser scripts from [Gregory Shakhnarovich](http://ttic.uchicago.edu/~gregory/download.html).

The script can be used for generating large amounts of images of a hand grasping different sets of simple objects, according to the taxonomy defined in "A comprehensive grasp taxonomy" by Feix et al. Images are generated together with some joint angle representation of the pose.

In order to run the script you should have installed some version of [Poser](http://poser.smithmicro.com/poser.html). The original version of the software was tested on Poser 7 in 2009, and this version has been tested on PoserPro 2012. In order to run it, select "File" > "Run Python Script" and select the location of the file "createGraspICRA09.py". You will also be asked for the location of the ligth file light1.lt2, which is in the lights subfolder.

The best way to let me know that you're using the scripts is to fork the code and modify your version in github. If you use this script or modify it for your research, please include the following citation in your paper:

    @article{Romero_IVC_2013,
        title = "Non-parametric hand pose estimation with object context ",
        journal = "Image and Vision Computing ",
        volume = "31",
        number = "8",
        pages = "555 - 564",
        year = "2013",
        note = "",
        issn = "0262-8856",
        doi = "http://dx.doi.org/10.1016/j.imavis.2013.04.002",
        url = "http://www.sciencedirect.com/science/article/pii/S0262885613000656",
        author = "Javier Romero and Hedvig Kjellstr\:om and Carl Henrik Ek and Danica Kragic",
    }
