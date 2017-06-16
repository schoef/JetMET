from JetMET.JetCorrector.JetSmearer import JetSmearer 

if __name__ == "__main__":
    # Logging
    import JetMET.tools.logger as logger
    logger  = logger.get_logger('DEBUG', logFile = None)

    smearer_mc = JetSmearer("Spring16_25nsV10_MC", "AK4PFchs")

    # Logging
    args = (400, 420, 2.4, 24 )
    logger.info( "Hybrid pt: '%r' -> '%r'" , args, smearer_mc.hybrid_correction(*args) )

    # Segfault otherwise (no, destructor doesn't work)
    smearer_mc.delete()
