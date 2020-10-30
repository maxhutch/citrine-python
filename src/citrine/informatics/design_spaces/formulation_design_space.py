from typing import Mapping, Set

from citrine._rest.resource import Resource
from citrine._serialization import properties
from citrine._session import Session
from citrine.informatics.constraints import Constraint
from citrine.informatics.descriptors import FormulationDescriptor
from citrine.informatics.design_spaces.design_space import DesignSpace

__all__ = ['FormulationDesignSpace']


class FormulationDesignSpace(Resource['FormulationDesignSpace'], DesignSpace):
    """[ALPHA] Design space composed of mixtures of ingredients.

    Parameters
    ----------
    name: str
        the name of the design space
    description: str
        the description of the design space
    descriptor: FormulationDescriptor
        descriptor used to store formulations sampled from the design space
    ingredients: Set[str]
        set of ingredients that can be used in a formulation
    labels: Mapping[str, Set[str]]
        Map from a label to each ingredient that should given that label
        when it's included in a formulation, e.g., ``{'solvent': {'water', 'alcohol'}}``
    constraints: Set[IngredientConstraint]
        Set of constraints that restricts formulations sampled from the space
    resolution: float, optional
        Minimum increment used to specify ingredient quantities.
        Default is 0.01.

    """

    _response_key = None

    uid = properties.Optional(properties.UUID, 'id', serializable=False)
    name = properties.String('config.name')
    description = properties.Optional(properties.String(), 'config.description')
    descriptor = properties.Object(FormulationDescriptor, 'config.descriptor')
    ingredients = properties.Set(properties.String, 'config.ingredients')
    labels = properties.Mapping(properties.String, properties.Set(properties.String), 'config.labels')
    constraints = properties.Set(properties.Object(Constraint), 'config.constraints')
    resolution = properties.Float('config.resolution')
    typ = properties.String('config.type', default='FormulationDesignSpace', deserializable=False)
    status = properties.String('status', serializable=False)
    status_info = properties.Optional(
        properties.List(properties.String()),
        'status_info',
        serializable=False
    )
    archived = properties.Boolean('archived', default=False)
    experimental = properties.Boolean("experimental", serializable=False, default=True)
    experimental_reasons = properties.Optional(
        properties.List(properties.String()),
        'experimental_reasons',
        serializable=False
    )

    def __init__(self,
                 name: str,
                 description: str,
                 descriptor: FormulationDescriptor,
                 ingredients: Set[str],
                 labels: Mapping[str, Set[str]],
                 constraints: Set[Constraint],
                 resolution: float = 0.01,
                 session: Session = Session()):
        self.name: str = name
        self.description: str = description
        self.descriptor: FormulationDescriptor = descriptor
        self.ingredients: Set[str] = ingredients
        self.labels: Mapping[str, Set[str]] = labels
        self.constraints: Set[Constraint] = constraints
        self.resolution: float = resolution
        self.session: Session = session

    def _post_dump(self, data: dict) -> dict:
        data['display_name'] = data['config']['name']
        return data

    def __str__(self):
        return '<FormulationDesignSpace {!r}>'.format(self.name)
