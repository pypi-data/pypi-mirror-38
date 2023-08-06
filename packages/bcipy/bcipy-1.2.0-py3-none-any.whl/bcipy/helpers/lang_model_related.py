"""Helper functions for language model use."""
import math
from typing import List, Tuple
from bcipy.language_model.lm_modes import LangModel, LmType


def init_language_model(parameters):
    """
    Init Language Model.

    Function to Initialize remote language model and get an instance of
        LangModel wrapper. Assumes a docker image is already loaded.

    See language_model/demo/ for more information of how it works.

    Parameters
    ----------
        parameters : dict
            configuration details and path locations

    Returns
    -------
        lmodel: instance
            instance of lmodel wrapper with connections to docker server
    """
    lmtype = LmType[parameters.get("lang_model_type", "PRELM")]

    port = int(parameters['lang_model_server_port'])
    lmodel = LangModel(lmtype, logfile="lmwrap.log", port=port)
    lmodel.init()
    return lmodel


def norm_domain(priors: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """Convert a list of (symbol, likelihood) values from negative log
    likelihood to the probability domain (between 0 and 1)

    Parameters:
        priors - list of (symbol, likelihood) values.
            assumes that the units are in the negative log likelihood where
            the lowest value is the most likely.
    Returns:
        list of values in the probability domain (between 0 and 1),
            where the highest value is the most likely.
    """
    return [(sym, math.exp(-prob)) for sym, prob in priors]
