from JetMET.JetCorrector.JetCorrector import JetCorrector 
from JetMET.JetCorrector.JetCorrector import correction_levels_data
from JetMET.JetCorrector.JetCorrector import correction_levels_mc

# config
config_Fall17_17Nov17_V11_MC = [(1, 'Fall17_17Nov2017_V11_MC') ]
config_Fall17_17Nov17_V24_MC = [(1, 'Fall17_17Nov2017_V24_MC') ]

if __name__ == "__main__":

    # Logging
    import JetMET.tools.logger as logger
    logger  = logger.get_logger('DEBUG', logFile = None)

Fall17_17Nov17_V11_MC = JetCorrector.fromTarBalls( config_Fall17_17Nov17_V11_MC, correctionLevels = correction_levels_mc ) 
Fall17_17Nov17_V24_MC = JetCorrector.fromTarBalls( config_Fall17_17Nov17_V24_MC, correctionLevels = correction_levels_mc )
