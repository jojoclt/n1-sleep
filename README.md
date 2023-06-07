# **Sleep Stage NREM1 Detection Using Machine Learning Models**

# Introduction
- Overview
    
    This is a model that can detect the N1 stage of sleep, and it improves the accuracy of the N1 sleep stage by modifying the training dataset.
    
- Purpose
    
    This model aims to collect labeled data through EEG for the development of a nap-related mobile application.
    
- Functionality
    
    The function of this model is to detect the N1 sleep stage.
    
- Key Features
    
    The model we trained performs better in the detection of N1 compared to existing models.
- Overview
- Purpose
- Functionality
- Key Features

# Dataset

- Data Description
    - Experimental Design / Paradigm
    - Procedure for Collecting Data
    - Hardware and Software Used
    - Data Size
    - Number of Channels
    - Sampling Rate
    - Website
    - Owner
    - Source
- Quality Evaluation: Justify the reliability and credibility of the data source
    - Survey and analyzing existing literature
    - Analyzing the hidden independent conponent within EEG using ICA with
        1. Apply ICA to your EEG data
        2. use ICLabel to automatically label the ICs and estimate the probability of each IC being either non-brain artifactual or Brain ICs.
        3. Investigate and analyze the change in the number of recognized ICs for the
        following EEG datasets: 
            1. Raw EEG data 
            2. Filtered EEG data
            3. EEG data corrected using ASR. 

# Model Framework

- Architecture and Component of BCI System
    - Input / Output Mechanisms
    - Signal Preprocessing Techniques
    - Data Segmentation Methods
    - Artitfact removal Strategies
    - Feature Extraction Approached
    - Machine Learning Model Utilized

# Validation

- Methods used to validate the effectiveness and reliability

# Usage

- Explain the required environment and dependencies needed to run the code
- Describe any comfigurable options or parameters within the code
- Provide instructions on how to execute the code

# Result

- Compare and contrast your BCI system with existing competing methods.
    - Accuracy
    - Precision
    - Recall
    - F1-score
- Highlight the advantages and unique aspects of your system.

# References
1. S. Lee, Y. Yu, S. Back, H. Seo, and K. Lee, “Sleepyco: Automatic sleep scoring with feature pyramid and contrastive learning,” arXiv preprint arXiv:2209.09452, 2022.
2. Van Der Donckt, J. et al. (2022) “Do not sleep on linear models: Simple and interpretable techniques outperform deep learning for sleep scoring,” SSRN Electronic Journal [Preprint]. Available at: https://doi.org/10.2139/ssrn.4170465. 
3. B Kemp, AH Zwinderman, B Tuk, HAC Kamphuisen, JJL Oberyé. Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. IEEE-BME 47(9):1185-1194 (2000).
https://www.physionet.org/content/sleep-edfx/1.0.0/
4. Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.
https://www.physionet.org/content/sleep-edfx/1.0.0/
5. Suni, E. (2023, March 2). Stages of Sleep (Dr. nilong vyas, Ed.). Sleep Foundation. https://www.sleepfoundation.org/stages-of-sleep
6. Célia Lacaux et al. (2021) “Sleep onset is a creative sweet spot”.Sci. Adv.7, eabj5866. DOI:10.1126/sciadv.abj5866
7. Meta AI. Sleep Stage Detection on Sleep-EDF. Paperswithcode. https://paperswithcode.com/sota/sleep-stage-detection-on-sleep-edf