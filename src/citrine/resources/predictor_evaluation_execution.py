"""Resources that represent both individual and collections of predictor evaluation executions."""
from functools import partial
from typing import Optional, Union, Iterator
from uuid import UUID
import sys

from citrine._rest.collection import Collection
from citrine._session import Session
from citrine.informatics.modules import ModuleRef
from citrine.resources.response import Response
import citrine.informatics.executions
from citrine.informatics.executions import PredictorEvaluationExecution

from citrine._utils.functions import shadow_classes_in_module


shadow_classes_in_module(citrine.informatics.executions, sys.modules[__name__])


class PredictorEvaluationExecutionCollection(Collection["PredictorEvaluationExecution"]):
    """A collection of PredictorEvaluationExecutions."""

    _path_template = '/projects/{project_id}/predictor-evaluation-executions'  # noqa
    _individual_key = None
    _collection_key = 'response'
    _resource = PredictorEvaluationExecution

    def __init__(self,
                 project_id: UUID,
                 session: Session,
                 workflow_id: Optional[UUID] = None):
        self.project_id: UUID = project_id
        self.session: Session = session
        self.workflow_id: Optional[UUID] = workflow_id

    def build(self, data: dict) -> PredictorEvaluationExecution:
        """Build an individual PredictorEvaluationExecution."""
        execution = PredictorEvaluationExecution.build(data)
        execution._session = self.session
        execution.project_id = self.project_id
        return execution

    def trigger(self, predictor_id: UUID):
        """Trigger a predictor evaluation execution against a predictor, by id."""
        if self.workflow_id is None:
            msg = "Cannot trigger a predictor evaluation execution without knowing the " \
                  "predictor evaluation workflow. Use workflow.executions.trigger instead of " \
                  "project.predictor_evaluation_executions.trigger"
            raise RuntimeError(msg)
        path = '/projects/{project_id}/predictor-evaluation-workflows/{workflow_id}/executions' \
            .format(project_id=self.project_id, workflow_id=self.workflow_id)
        data = self.session.post_resource(path, ModuleRef(str(predictor_id)).dump())
        self._check_experimental(data)
        return self.build(data)

    def register(self, model: PredictorEvaluationExecution) -> PredictorEvaluationExecution:
        """Cannot register an execution."""
        raise NotImplementedError("Cannot register a PredictorEvaluationExecution.")

    def update(self, model: PredictorEvaluationExecution) -> PredictorEvaluationExecution:
        """Cannot update an execution."""
        raise NotImplementedError("Cannot update a PredictorEvaluationExecution.")

    def archive(self, execution_id: UUID):
        """Archive a predictor evaluation execution.

        Parameters
        ----------
        execution_id: UUID
            Unique identifier of the execution to archive

        """
        self._put_module_ref('archive', execution_id)

    def restore(self, execution_id: UUID):
        """Restore an archived predictor evaluation execution.

        Parameters
        ----------
        execution_id: UUID
            Unique identifier of the execution to restore

        """
        self._put_module_ref('restore', execution_id)

    def list(self,
             *,
             page: Optional[int] = None,
             per_page: int = 100,
             predictor_id: Optional[UUID] = None
             ) -> Iterator[PredictorEvaluationExecution]:
        """
        Paginate over the elements of the collection.

        Leaving page and per_page as default values will yield all elements in the
        collection, paginating over all available pages.

        Parameters
        ---------
        page: int, optional
            The "page" of results to list. Default is to read all pages and yield
            all results.  This option is deprecated.
        per_page: int, optional
            Max number of results to return per page. Default is 100.  This parameter
            is used when making requests to the backend service.  If the page parameter
            is specified it limits the maximum number of elements in the response.
        predictor_id: uuid, optional
            list executions that targeted the predictor with this id

        Returns
        -------
        Iterator[ResourceType]
            Resources in this collection.

        """
        params = {}
        if predictor_id is not None:
            params["predictor_id"] = str(predictor_id)
        if self.workflow_id is not None:
            params["workflow_id"] = str(self.workflow_id)

        fetcher = partial(self._fetch_page, additional_params=params)
        return self._paginator.paginate(page_fetcher=fetcher,
                                        collection_builder=self._build_collection_elements,
                                        page=page,
                                        per_page=per_page)

    def delete(self, uid: Union[UUID, str]) -> Response:
        """Predictor Evaluation Executions cannot be deleted; they can be archived instead."""
        raise NotImplementedError(
            "Predictor Evaluation Executions cannot be deleted; they can be archived instead.")
