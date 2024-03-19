from typing import TYPE_CHECKING

from bgpy.simulation_engine.policies import BGP

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann


class RouteFlapDampening(BGP):
    """An Policy that employs Route Flap Dampening Technique"""

    name: str = "RouteFlapDampening"

    # mypy doesn't understand that this func is valid
    def _valid_ann(self, ann: "Ann", *args, **kwargs) -> bool:  # type: ignore
        """Returns announcement validity

        Returns false if the announcement has been made more than the threshold value,
        otherwise uses standard BGP (such as no loops, etc)
        to determine validity
        """
        
        # Not valid if it crosses the threshold
        if not ann.below_threshold:
            return False
        # Otherwise use the standard validity check
        else:
            # Mypy doesn't map superclasses properly
            return super(RouteFlapDampening, self)._valid_ann(
                ann, *args, **kwargs)  # type: ignore
