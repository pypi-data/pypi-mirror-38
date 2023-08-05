""" all methods of GETting data for Eloqua.Bulk """

from copy import deepcopy
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

EXPORT_JOB_DEF = {
    "name": "test name",
    "fields": {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    "dataRetentionDuration": "PT12H",
    "uri": "/contacts/exports/1",
    "createdBy": "testuser",
    "createdAt": "2017-02-13T16:32:31.7020994Z",
    "updatedBy": "testuser",
    "updatedAt": "2017-02-13T16:32:31.7020994Z"
}

IMPORT_JOB_DEF = {
    "name": "test name",
    "fields": {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    "identifierFieldName": "contactID",
    "isSyncTriggeredOnImport": False,
    "dataRetentionDuration": "P7D",
    "isUpdatingMultipleMatchedRecords": False,
    "uri": "/contacts/imports/1",
    "createdBy": "testuser",
    "createdAt": "2017-02-13T16:38:13.3442894Z",
    "updatedBy": "testuser",
    "updatedAt": "2017-02-13T16:38:13.3442894Z"
}

RETURN_DATA = {
    "items": [
        {
            "contactID": "12345",
            "createdAt": "2017-01-01 00:00:00",
            "updatedAt": "2017-01-01 00:00:00"
        }
    ],
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

RETURN_NORESULTS = {
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

RETURN_SYNC_REJECTS = {
    "items": [
        {
            "fieldValues": {
                "contactID": "12345",
                "createdAt": "2017-01-01 00:00:00",
                "updatedAt": "2017-01-01 00:00:00"
            },
            "message": "Multiple matches.",
            "statusCode": "ELQ-00026",
            "recordIndex": 111,
            "invalidFields": [
                "emailAddress"
            ]
        },
    ],
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

RETURN_SYNC_LOGS = {
    "items": [
        {
            "syncUri": "/syncs/845824",
            "count": 30000,
            "severity": "information",
            "statusCode": "ELQ-00130",
            "message": "Total records staged for import.",
            "createdAt": "2016-11-12T00:02:37.0770000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 0,
            "severity": "information",
            "statusCode": "ELQ-00137",
            "message": "Ready for data import processing.",
            "createdAt": "2016-11-12T00:02:37.0770000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 0,
            "severity": "information",
            "statusCode": "ELQ-00101",
            "message": "Sync processed for sync , resulting in Warning status.",
            "createdAt": "2016-11-12T00:02:52.0870000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 30000,
            "severity": "information",
            "statusCode": "ELQ-00001",
            "message": "Total records processed.",
            "createdAt": "2016-11-12T00:02:37.7000000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 21000,
            "severity": "warning",
            "statusCode": "ELQ-00026",
            "message": "Duplicate identifier.",
            "createdAt": "2016-11-12T00:02:46.2700000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 9000,
            "severity": "information",
            "statusCode": "ELQ-00003",
            "message": "Total records remaining after duplicates are rejected.",
            "createdAt": "2016-11-12T00:02:46.2700000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 0,
            "severity": "information",
            "statusCode": "ELQ-00004",
            "message": "Contacts created.",
            "createdAt": "2016-11-12T00:02:46.2700000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 9000,
            "severity": "information",
            "statusCode": "ELQ-00022",
            "message": "Contacts updated.",
            "createdAt": "2016-11-12T00:02:46.2700000Z"
        },
        {
            "syncUri": "/syncs/845824",
            "count": 0,
            "severity": "information",
            "statusCode": "ELQ-00071",
            "createdAt": "2016-11-12T00:02:46.2700000Z"
        }
    ],
    "totalResults": 9,
    "limit": 1000,
    "offset": 0,
    "count": 9,
    "hasMore": False
}

SYNC_RESPONSE_SUCCESS = {
    "syncStartedAt": "2013-07-22T22:17:59.6730000Z",
    "syncEndedAt": "2013-07-22T22:18:07.6430000Z",
    "status": "success",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}

###############################################################################
# grab some datas
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_get_data_call(mock_get):
    """ get data from an endpoint - api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(RETURN_DATA)
    bulk.get_data(endpoint='/dummyurl')
    mock_get.assert_called_with(url=bulk.bulk_base + '/dummyurl?limit=1000&offset=0',
                                auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_data_return(mock_get):
    """ get data from an endpoint - return data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(RETURN_DATA)
    return_data = bulk.get_data(endpoint='/dummyurl')
    assert return_data == RETURN_DATA['items']


@patch('pyeloqua.bulk.requests.get')
def test_get_data_nodata(mock_get):
    """ get data from an endpoint - no results data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(RETURN_NORESULTS)
    return_data = bulk.get_data(endpoint='/dummyurl')
    assert return_data == []

###############################################################################
# get sunk'd export data
###############################################################################


@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_export_data_call(mock_data):
    """ get data from a synced export - method call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_data.return_value = RETURN_DATA['items']
    bulk.get_export_data()
    mock_data.assert_called_with(endpoint='/contacts/exports/1/data',
                                 max_recs=None,
                                 offset=0)


@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_export_data_rt(mock_data):
    """ get data from a synced export - return data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_data.return_value = RETURN_DATA['items']
    data = bulk.get_export_data()
    assert data == RETURN_DATA['items']


@patch('pyeloqua.bulk.Bulk.get_data')
@raises(Exception)
def test_get_export_data_notexp(mock_data):
    """ get data from a synced export - exception """
    bulk = Bulk(test=True)
    bulk.imports('contacts')
    bulk.job_def = IMPORT_JOB_DEF
    mock_data.return_value = RETURN_DATA['items']
    bulk.get_export_data()


###############################################################################
# get sync logs
###############################################################################

@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_sync_logs_call(mock_data):
    """ get logs from a sync - method call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE_SUCCESS
    mock_data.return_value = RETURN_SYNC_LOGS['items']
    bulk.get_sync_logs()
    mock_data.assert_called_with(endpoint='/syncs/1/logs')


@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_sync_logs_rt(mock_data):
    """ get logs from a sync - return data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE_SUCCESS
    mock_data.return_value = RETURN_SYNC_LOGS['items']
    data = bulk.get_sync_logs()
    assert data == RETURN_SYNC_LOGS['items']


@patch('pyeloqua.bulk.Bulk.get_data')
@raises(Exception)
def test_get_sync_logs_notexp(mock_data):
    """ get logs from a sync - exception """
    bulk = Bulk(test=True)
    bulk.imports('contacts')
    mock_data.return_value = RETURN_SYNC_LOGS['items']
    bulk.get_sync_logs()


###############################################################################
# get sync rejects
###############################################################################

@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_sync_rejects_call(mock_data):
    """ get logs from a sync - method call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE_SUCCESS
    mock_data.return_value = RETURN_SYNC_REJECTS['items']
    bulk.get_sync_rejects()
    mock_data.assert_called_with(endpoint='/syncs/1/rejects')


@patch('pyeloqua.bulk.Bulk.get_data')
def test_get_sync_rejects_rt(mock_data):
    """ get logs from a sync - return data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE_SUCCESS
    mock_data.return_value = RETURN_SYNC_REJECTS['items']
    data = bulk.get_sync_rejects()
    assert data == RETURN_SYNC_REJECTS['items']


@patch('pyeloqua.bulk.Bulk.get_data')
@raises(Exception)
def test_get_sync_rejects_notexp(mock_data):
    """ get logs from a sync - exception """
    bulk = Bulk(test=True)
    bulk.imports('contacts')
    mock_data.return_value = RETURN_SYNC_REJECTS['items']
    bulk.get_sync_rejects()
