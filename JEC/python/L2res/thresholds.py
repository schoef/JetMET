
#abs_eta_bins = [ (0, 5.2), (0, 0.8), (0, 1.3), (0.8, 1.3), (1.3, 1.9), (1.9, 2.5), (2.5, 3), (3, 3.2), (3.2, 5.2) ]
coarse_abs_eta_bins = [ (0, 1.3), ( 1.3, 2.5 ), (2.5, 3), (3, 3.2), (3.2, 5.2) ]

# L2res
abs_eta_thresholds = [0.000, 0.261, 0.522, 0.783, 1.044, 1.305, 1.479, 1.653, 1.930, 2.172, 2.322, 2.500, 2.650, 2.853, 2.964, 3.139, 3.489, 3.839, 5.191]
abs_eta_bins       = [(abs_eta_thresholds[i], abs_eta_thresholds[i+1]) for i in range( len( abs_eta_thresholds ) -1 ) ]

eta_thresholds_neg = [-x for x in abs_eta_thresholds[1:]]
eta_thresholds_neg.reverse()
eta_thresholds = eta_thresholds_neg + abs_eta_thresholds 

#pt_avg_thresholds = [51,73,129,163,230,299,365,435,566,1000]
pt_avg_thresholds = [50,80,130,170,230,300,370,440,550,1000]
pt_avg_bins       = [(pt_avg_thresholds[i], pt_avg_thresholds[i+1]) for i in range( len( pt_avg_thresholds ) -1 ) ]
