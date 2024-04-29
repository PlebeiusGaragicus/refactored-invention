if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    import logging
    from graph_builder.logger import setup_logging
    setup_logging()
    # streamlit_root_logger = logging.getLogger(streamlit.__name__)
    # streamlit_root_logger = logging.getLogger()
    # logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
    logging.getLogger("fsevents").setLevel(logging.INFO)
    # logging.info("RERUN:\n\n\n\n\n")
    logger = logging.getLogger(__name__)
    logger.info("RERUN:\n\n\n\n\n")

    from graph_builder.main import main
    main()

