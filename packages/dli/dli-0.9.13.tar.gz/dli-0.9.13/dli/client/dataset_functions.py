
import logging
import os
import six

from dli.client.exceptions import (
    CatalogueEntityNotFoundException,
    MissingMandatoryArgumentException,
)
from dli.siren import siren_to_entity, siren_to_dict
from dli.client.utils import ensure_count_is_valid

logger = logging.getLogger(__name__)


class DatasetFunctions(object):

    @property
    def __root(self):
        return self.get_root_siren().datasets_root()

    def get_s3_access_keys_for_dataset(self, *dataset_ids):
        """
        Retrieve S3 access keys for the specified account to access the
        specified package. The retrieved keys and session token will be stored
        in the client context.

        :param str dataset_id: The id of the dataset.
        :param bool use_cached: Optional. Flag to use token cached from previous call. Defaults to False.
        
        :returns: A namedtuple containing the AWS keys, dataset id and session token.
        :rtype: collections.namedtuple
        
        - **Sample**
        
        .. code-block:: python

                s3_access_keys = client.get_s3_access_keys_for_dataset(dataset_id)
                # print(s3_access_keys)
                # access_key(access_key_id='39D19A440AFE452B9', secret_access_key='F426A93CDECE45C9BFF8F4F19DA5CB81', session_token='C0CC405803F244CA99999')

        """
        if not dataset_ids:
            raise MissingMandatoryArgumentException('dataset_ids')

        # validate that all datasets exist
        for dataset_id in dataset_ids:
            self._get_dataset(dataset_id=dataset_id)

        payload = {"datasetIds": list(dataset_ids)}
        response = self.get_root_siren().request_access_keys(__json=payload)
        keys = siren_to_entity(response)
        return keys

    def get_dataset(self, id=None, name=None, package_id=None, package_name=None):
        """
        Retrieves a dataset (or `None` if it doesn't exist).

        :param str id: The id of the dataset.
        :param str name: The name of the dataset.
        :param str package_id: The id of the package to which this dataset belongs. 
                            Either this or package name is required if dataset is being looked up by name.
        :param str package_name: The name of the package to which this dataset belongs.
                            Either this or package id is required if dataset is being looked up by name.

        :returns: The dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Look up by dataset id
                dataset = client.get_dataset('my_dataset_id')
                # or equivalent
                dataset = client.get_dataset(id='my_dataset_id')

                # Look up by dataset name 

                # If package id is known
                dataset = client.get_dataset(name='my_dataset', package_id='my_package_id')

                # if package name is known
                dataset = client.get_dataset(name='my_dataset', package_name='my_package')
        """

        if id is not None:
            return siren_to_entity(self._get_dataset(dataset_id=id))

        if name is not None:
            return siren_to_entity(self._get_dataset(name=name, package_id=package_id, package_name=package_name))

        raise ValueError("Either dataset id or name (along with package id or package name) must be specified to look up dataset")

    def _get_dataset(self, **kwargs):

        dataset = self.__root.get_dataset(**kwargs)

        if not dataset:
            raise CatalogueEntityNotFoundException('Dataset', params=kwargs)

        return dataset   

    def register_dataset(self, builder):
        """
        Submit a request to create a new dataset under a specified package in the Data Catalogue.

        :param dli.client.builders.DatasetBuilder builder: An instance of DatasetBuilder. This builder object sets sensible defaults and exposes
                                                           helper methods on how to configure its storage options.

        :returns: A newly created Dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Please refer to builder docs for examples on
                # how to creata an instance of DatasetBuilder.

                dataset = client.register_dataset(builder)
        """
        payload = builder.build()

        result = self.__root.create_dataset(__json=payload)
        return siren_to_entity(result)

    def edit_dataset(
        self,
        dataset_id,
        name=None,
        description=None,
        content_type=None,
        data_format=None,
        publishing_frequency=None,
        keywords=None,
        naming_convention=None,
        documentation=None
    ):
        """
        Updates information on a dataset, returning the updated instance.
        Fields that are left as ``None`` will not be changed.

        :param str dataset_id: Id of the dataset being updated.
        :param str name: A descriptive name of a dataset. It should be unique within the package.
        :param str description: A short description of a package.
        :param str content_type: A way for the data steward to classify the type of data in the dataset (e.g. pricing).
        :param str data_format: The format of the data: csv, parquet, etc.
        :param str publishing_frequency: The internal on which data is published (e.g. daily, monthly, etc.).
        :param list[str] keywords: User-defined list of keywords that can be used to find this dataset through the search interface.
        :param str naming_convention: Key for how to read the dataset name.
        :param str documentation: Documentation about this dataset in markdown format.

        :returns: Updated Dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                updated_dataset = client.edit_dataset(
                    "my-dataset-id",
                    description="Updated my dataset description"
                )
        """
        if not dataset_id:
            raise MissingMandatoryArgumentException('dataset_id')

        dataset = self._get_dataset(dataset_id=dataset_id)

        fields = {
            "packageId": dataset.packageId,
            "name": name,
            "description": description,
            "keywords": keywords,
            "contentType": content_type,
            "location": dataset.location,
            "dataFormat": {"type": data_format} if data_format else None,
            "publishingFrequency": publishing_frequency,
            "namingConvention": naming_convention,
            "documentation": documentation
        }

        # clean up any unknown fields, and update the entity
        dataset_as_dict = siren_to_dict(dataset)
        for key in list(dataset_as_dict.keys()):
            if key not in fields:
                del dataset_as_dict[key]

        payload = {k: v for k, v in fields.items() if v is not None}
        dataset_as_dict.update(payload)

        # perform the update and return the resulting entity
        return siren_to_entity(dataset.edit_dataset(__json=dataset_as_dict))

    def delete_dataset(self, dataset_id):
        """
        Marks a particular dataset (and all its datafiles) as deleted.
        This dataset will no longer be accessible by consumers.

        :param str dataset_id: The id of the dataset to be deleted.

        :returns:

        - **Sample**

        .. code-block:: python

                client.delete_dataset(dataset_id)

        """
        if not dataset_id:
            raise MissingMandatoryArgumentException('dataset_id')

        dataset = self._get_dataset(dataset_id=dataset_id)

        dataset.delete_dataset()


    def get_datafiles(self, dataset_id, name_contains=None, as_of_date_start=None, as_of_date_end=None, count=100):
        """
        Returns a list of all datafiles registered under a dataset.

        :param str dataset_id: The id of the dataset.
        :param str name_contains: Optional. Look up only those datafiles for the dataset where name contains this string.
        :param str as_of_date_start: Optional. Datafiles having data_as_of date greater than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param str as_of_date_end: Optional. Datafiles having data_as_of date less than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param int count: Optional count of datafiles to be returned. Defaulted to 100.

        :returns: List of all datafiles registered under the dataset.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                datafiles = client.get_datafiles(
                    dataset_id,
                    name_contains='My Test Data',
                    as_of_date_start='2018-10-11',
                    as_of_date_end='2018-10-15',                    
                    count=10
                )
        """
        if not dataset_id:
            raise MissingMandatoryArgumentException('dataset_id')

        ensure_count_is_valid(count)

        params = {
            'name': name_contains,
            'as_of_date_start': as_of_date_start,
            'as_of_date_end': as_of_date_end,
            'page_size': count
        }

        query_params = {k: v for k, v in six.iteritems(params) if v is not None}

        dataset = self._get_dataset(dataset_id=dataset_id)
            
        datafiles = dataset.get_datafiles(**query_params).get_entities(rel="datafile")

        return [siren_to_entity(df) for df in datafiles]
