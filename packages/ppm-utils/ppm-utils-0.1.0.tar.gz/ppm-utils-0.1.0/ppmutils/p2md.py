from ppmutils.ppm import PPM

import logging
logger = logging.getLogger(__name__)


class P2MD(PPM.Service):

    @classmethod
    def _p2md_auth_url(cls, request):

        # Check if specified
        if hasattr(settings, 'P2MD_AUTH_URL') and settings.P2MD_AUTH_URL:
            url = furl(settings.P2MD_AUTH_URL)

        else:
            # The same URL, different path
            url = furl(request.build_absolute_uri())

            # Clear everything
            url.path.segments.clear()
            url.query.params.clear()

        # Add the sources path
        url.path.segments.append('sources')

        return url

    @classmethod
    def _p2md_api_url(cls, request):

        # Check if specified
        if hasattr(settings, 'P2MD_API_URL') and settings.P2MD_API_URL:
            url = furl(settings.P2MD_API_URL)

        else:
            # The same URL, different path
            url = furl(request.build_absolute_uri())

            # Clear everything
            url.path.segments.clear()
            url.query.params.clear()

        # Add the sources path
        url.path.segments.append('sources')

        return url

    @classmethod
    def get_authorizations(cls, request, ppm_ids):
        """
        Make a request to P2MD to determine what providers all participants have authorized.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['auths'])
        url.query.params.add('ppm_ids', ','.join(ppm_ids))

        # Make the request
        response = requests.get(url.url, headers=P2MD._headers(request))
        data = response.json()

        return data

    @classmethod
    def has_smart_authorization(cls, request, ppm_id):
        """
        Make a request to P2MD to determine if a participant has authorized any SMART provider.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['smart', ppm_id, 'auths'])

        # Make the request
        response = requests.head(url.url, headers=P2MD._headers(request))

        # Return True if no errors
        return response.ok

    @classmethod
    def get_smart_authorizations(cls, request, ppm_id):
        """
        Make a request to P2MD to get a list of SMART providers authorized by the participant.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['smart', ppm_id, 'auths'])

        # Make the request
        response = requests.get(url.url, headers=P2MD._headers(request))
        data = response.json()
        smart_authorizations = data.get("smart_authorizations", [])

        return smart_authorizations

    @classmethod
    def get_operations(cls, request, ppm_id):
        """
        Make a request to P2MD to get a full history of all data operations conducted
        for the participant.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'ppm', ppm_id])

        try:
            # Make the request
            response = requests.get(url.url, headers=P2MD._headers(request))
            content = response.json()
            response.raise_for_status()

            return content
        except requests.HTTPError as e:
            logger.exception('Operations fetch error: {}'.format(e), exc_info=True,
                             extra={'ppm_id': ppm_id, 'url': url.url, 'response': content})

    @classmethod
    def get_twitter_data(cls, request, ppm_id, handle):
        """
        Make a request to P2MD to fetch Twitter data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'twitter', ppm_id])

        # prepare data for request
        data = {
            'handle': handle
        }

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json=data)

        # Return True if no errors
        return response.ok

    @classmethod
    def get_fitbit_data(cls, request, ppm_id):
        """
        Make a request to P2MD to fetch Fitbit data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'fitbit', ppm_id])

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json={})

        # Return True if no errors
        return response.ok

    @classmethod
    def get_gencove_data(cls, request, ppm_id, gencove_id):
        """
        Make a request to P2MD to fetch Gencove data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'gencove', ppm_id])

        # prepare data for request
        data = {
            'gencove_id': gencove_id
        }

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json=data)

        # Return True if no errors
        return response.ok

    @classmethod
    def get_facebook_data(cls, request, ppm_id):
        """
        Make a request to P2MD to fetch Facebook data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'facebook', ppm_id])

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json={})

        # Return True if no errors
        return response.ok

    @classmethod
    def get_smart_data(cls, request, ppm_id, provider):
        """
        Make a request to P2MD to fetch SMART on FHIR EHR data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'smart', provider, ppm_id])

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json={})

        # Return True if no errors
        return response.ok

    @classmethod
    def add_document(cls, request, ppm_id, document_type, uuid):
        """
        Make a request to P2MD to fetch SMART on FHIR EHR data and store it in PPM.
        """

        # Build the URL
        url = P2MD._p2md_api_url(request)
        url.path.segments.extend(['api', 'document', ppm_id])

        # Set data
        data = {'type': document_type, 'uuid': uuid}

        # Make the resquest
        response = requests.post(url.url, headers=P2MD._headers(request), json=data)
        response.raise_for_status()

        # Return True if no errors
        return response.ok

    @classmethod
    def get_files(cls, request, ppm_id):
        """
        Queries P2MD for all uploaded files related to this participant.
        """
        return cls.get(request, '/api/file/{}'.format(ppm_id))

    @classmethod
    def create_file(cls, request, ppm_id, document_type, filename, metadata={}, tags=[]):
        """
        Make a request to P2MD to create a file upload
        """
        # Set data
        data = {'type': document_type, 'filename': filename, 'metadata': metadata, 'tags': tags}

        # Get the file data
        upload = cls.post(request, '/api/file/{}'.format(ppm_id), data)

        # Get the UUID
        uuid = upload.get('uuid')

        # Return True if no errors
        return uuid, upload

    @classmethod
    def uploaded_file(cls, request, ppm_id, document_type, uuid, location):
        """
        Make a request to P2MD to create a file upload
        """
        # Set data
        data = {'uuid': uuid, 'location': location, 'type': document_type}

        # Return True if no errors
        return cls.patch(request, '/api/file/{}'.format(ppm_id), data)

    @classmethod
    def get_smart_endpoints(cls, request):
        """
        Return a list of all registered SMART endpoints
        :param request: The current HttpRequest
        :return: list
        """
        return cls.get(request, '/smart')
