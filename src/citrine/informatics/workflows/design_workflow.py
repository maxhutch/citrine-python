from typing import Optional
from uuid import UUID

from citrine._rest.resource import Resource
from citrine._serialization import properties
from citrine._session import Session
from citrine.informatics.workflows.workflow import Workflow
from citrine.resources.workflow_executions import WorkflowExecutionCollection
from citrine.resources.design_execution import DesignExecutionCollection

__all__ = ['DesignWorkflow', 'NewDesignWorkflow']


class DesignWorkflow(Resource['DesignWorkflow'], Workflow):
    """[ALPHA] Object that generates scored materials that may approach higher values of the score.

    Parameters
    ----------
    name: str
        the name of the workflow
    design_space_id: UUID
        the UUID corresponding to the design space to use
    processor_id: Optional[UUID]
        the UUID corresponding to the processor to use
        if none is provided, one matching your design space will be automatically generated
    predictor_id: UUID
        the UUID corresponding to the predictor to use
    project_id: UUID
        the UUID corresponding to the project to use

    """

    uid = properties.Optional(properties.UUID, 'id', serializable=False)
    name = properties.String('display_name')
    status = properties.String('status', serializable=False)
    status_info = properties.Optional(
        properties.List(properties.String()),
        'status_info',
        serializable=False
    )
    experimental = properties.Boolean("experimental", serializable=False, default=True)
    experimental_reasons = properties.Optional(
        properties.List(properties.String()),
        'experimental_reasons',
        serializable=False
    )
    archived = properties.Boolean('archived', default=False)
    created_by = properties.Optional(properties.UUID, 'created_by', serializable=False)
    create_time = properties.Optional(properties.Datetime, 'create_time', serializable=False)
    design_space_id = properties.UUID('config.design_space_id')
    processor_id = properties.Optional(properties.UUID, 'config.processor_id')
    predictor_id = properties.UUID('config.predictor_id')
    module_type = properties.String('module_type', default='DESIGN_WORKFLOW')
    typ = properties.String('config.type', default='DesignWorkflow', deserializable=False)

    def __init__(self,
                 name: str,
                 design_space_id: UUID,
                 processor_id: Optional[UUID],
                 predictor_id: UUID,
                 project_id: Optional[UUID] = None,
                 session: Session = Session()):
        self.name = name
        self.design_space_id = design_space_id
        self.processor_id = processor_id
        self.predictor_id = predictor_id
        self.project_id = project_id
        self.session = session

    def __str__(self):
        return '<DesignWorkflow {!r}>'.format(self.name)

    @property
    def executions(self) -> WorkflowExecutionCollection:
        """Return a resource representing all visible executions of this workflow."""
        if getattr(self, 'project_id', None) is None:
            raise AttributeError('Cannot initialize execution without project reference!')
        return WorkflowExecutionCollection(self.project_id, self.uid, self.session)

    @property
    def design_executions(self) -> DesignExecutionCollection:
        """Return a resource representing all visible executions of this workflow."""
        if getattr(self, 'project_id', None) is None:
            raise AttributeError('Cannot initialize execution without project reference!')
        return DesignExecutionCollection(
            project_id=self.project_id, session=self.session, workflow_id=self.uid)



class NewDesignWorkflow(Resource['NewDesignWorkflow'], Workflow):
    """[ALPHA] Object that generates scored materials that may approach higher values of the score.

    Parameters
    ----------
    name: str
        the name of the workflow
    design_space_id: UUID
        the UUID corresponding to the design space to use
    processor_id: Optional[UUID]
        the UUID corresponding to the processor to use
        if none is provided, one matching your design space will be automatically generated
    predictor_id: UUID
        the UUID corresponding to the predictor to use
    project_id: UUID
        the UUID corresponding to the project to use

    """

    uid = properties.Optional(properties.UUID, 'id', serializable=False)
    name = properties.String('name')
    status = properties.String('status', serializable=False)
    status_info = properties.Optional(
        properties.List(properties.String()),
        'status_info',
        serializable=False
    )
    experimental = properties.Boolean("experimental", serializable=False, default=True)
    experimental_reasons = properties.Optional(
        properties.List(properties.String()),
        'experimental_reasons',
        serializable=False
    )
    archived = properties.Boolean('archived', serializable=False, default=False)
    created_by = properties.Optional(properties.UUID, 'created_by', serializable=False)
    create_time = properties.Optional(properties.Datetime, 'create_time', serializable=False)
    design_space_id = properties.UUID('design_space_id')
    processor_id = properties.Optional(properties.UUID, 'processor_id')
    predictor_id = properties.UUID('predictor_id')

    def __init__(self,
                 name: str,
                 design_space_id: UUID,
                 processor_id: Optional[UUID],
                 predictor_id: UUID,
                 project_id: Optional[UUID] = None,
                 session: Session = Session()):
        self.name = name
        self.design_space_id = design_space_id
        self.processor_id = processor_id
        self.predictor_id = predictor_id
        self.project_id = project_id
        self.session = session

    def __str__(self):
        return '<NewDesignWorkflow {!r}>'.format(self.name)

    @property
    def design_executions(self) -> DesignExecutionCollection:
        """Return a resource representing all visible executions of this workflow."""
        if getattr(self, 'project_id', None) is None:
            raise AttributeError('Cannot initialize execution without project reference!')
        return DesignExecutionCollection(
            project_id=self.project_id, session=self.session, workflow_id=self.uid)