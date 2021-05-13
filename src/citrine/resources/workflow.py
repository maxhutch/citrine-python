"""Resources that represent collections of Workflows."""
from itertools import chain
from uuid import UUID
from typing import TypeVar, Optional, Callable, Tuple
from warnings import warn

from citrine.informatics.workflows import Workflow
from citrine.resources.design_workflow import DesignWorkflowCollection
from citrine.resources.predictor_evaluation_workflow import PredictorEvaluationWorkflowCollection
from typing import Iterable

from citrine._rest.collection import Collection
from citrine._session import Session

CreationType = TypeVar('CreationType', bound=Workflow)
ResourceType = TypeVar('ResourceType', bound='Resource')


class WorkflowCollection(Collection[Workflow]):
    """[DEPRECATED] Represents the collection of all legacy Workflows.

    Parameters
    ----------
    project_id: UUID
        the UUID of the project

    """

    _path_template = '/projects/{project_id}/modules'
    _individual_key = None
    _resource = Workflow

    def __init__(self, project_id: UUID, session: Session):
        msg = "{this_class} is deprecated. Please use {dw_replacement} instead for " \
            "Design Workflows and {pew_replacement} for Predictor Evaluation Workflows".format(
                this_class=self.__class__.__name__,
                dw_replacement=DesignWorkflowCollection.__name__,
                pew_replacement=PredictorEvaluationWorkflowCollection.__name__)
        warn(msg, category=DeprecationWarning)
        self.project_id = project_id
        self.session: Session = session

    def register(self, model: CreationType) -> CreationType:
        """Legacy workflows are deprecated and can not be registered."""
        msg = "Legacy Workflows are deprecated and can not be registered. " \
              "Use project.design_workflows instead"
        raise NotImplementedError(msg)

    def update(self, model: CreationType) -> CreationType:
        """Legacy workflows are deprecated and can not be updated."""
        msg = "Legacy Workflows are deprecated and can not be updated. " \
              "Use project.design_workflows instead"
        raise NotImplementedError(msg)

    def list(self,
             page: Optional[int] = None,
             per_page: int = 100) -> Iterable[Workflow]:
        """
        Paginate over the Design Workflows and Performance Workflows.

        Leaving page and per_page as default values will yield all workflows,
        paginating over all available pages.

        Parameters
        ---------
        page: int, optional
            The "page" of results to list. Default is to read all pages and yield
            all results.  This option is deprecated.
        per_page: int, optional
            Max number of results to return per page. Default is 100.  This parameter
            is used when making requests to the backend service.  If the page parameter
            is specified it limits the maximum number of elements in the response.

        Returns
        -------
        Iterable[ResourceType]
            Resources in this collection.

        """
        # List all Design Workflows
        design_workflows = self._paginator.paginate(
            page_fetcher=self._fetch_design_page,
            collection_builder=self._build_collection_elements,
            page=page,
            per_page=per_page
        )

        # List all Performance Workflows
        performance_workflows = self._paginator.paginate(
            page_fetcher=self._fetch_performance_page,
            collection_builder=self._build_collection_elements,
            page=page,
            per_page=per_page
        )

        return chain(design_workflows, performance_workflows)

    def build(self, data: dict) -> Workflow:
        """Build an individual Workflow."""
        workflow = Workflow.build(data)
        workflow.session = self.session
        workflow.project_id = self.project_id
        return workflow

    def _fetch_design_page(self,
                           path: Optional[str] = None,
                           fetch_func: Optional[Callable[..., dict]] = None,
                           page: Optional[int] = None,
                           per_page: Optional[int] = None,
                           json_body: Optional[dict] = None,
                           additional_params: Optional[dict] = None
                           ) -> Tuple[Iterable[dict], str]:

        additional_params = {"module_type": "DESIGN_WORKFLOW"}
        return self._fetch_page(path, fetch_func, page, per_page, json_body, additional_params)

    def _fetch_performance_page(self,
                                path: Optional[str] = None,
                                fetch_func: Optional[Callable[..., dict]] = None,
                                page: Optional[int] = None,
                                per_page: Optional[int] = None,
                                json_body: Optional[dict] = None,
                                additional_params: Optional[dict] = None,
                                ) -> Tuple[Iterable[dict], str]:

        additional_params = {"module_type": "PERFORMANCE_WORKFLOW"}
        return self._fetch_page(path, fetch_func, page, per_page, json_body, additional_params)
