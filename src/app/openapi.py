"""Module with openapi settings."""

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse


async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
    """Endpoint to support static swagger.

    Returns:
        HTTP response.
    """
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='TG_ANALYTICS',
        # oauth2_redirect_url=request.app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
    )


async def custom_swagger_ui_html_dark(request: Request) -> HTMLResponse:
    """Endpoint to support static swagger.

    Returns:
        HTTP response.
    """
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='AUTH',
        oauth2_redirect_url=request.app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger_ui_dark.css',
    )


async def redoc_html() -> HTMLResponse:
    """Endpoint to support static ReDoc.

    Returns:
        HTTP response.
    """
    return get_redoc_html(
        openapi_url='/openapi.json',
        title='AUTH',
        redoc_js_url='/static/redoc.standalone.js',
    )


def custom_openapi(app: FastAPI):
    """Customize OpenAPI schema for the application.

    Returns:
        dict: The OpenAPI schema for the application.
    """
    if app.openapi_schema:
        return lambda: app.openapi_schema
    openapi_schema = get_openapi(
        title='AUTH TEST',
        version='1.0.0',
        description='for dev',
        routes=app.routes,
    )
    for path in openapi_schema['paths'].values():
        for method in path.values():
            responses = method.get('responses', {})
            for response in responses.values():
                headers = response.get('headers', {})
                headers['X-Process-Time'] = {
                    'description': 'Time taken to process the request',
                    'schema': {'type': 'string'},
                }
                response['headers'] = headers
    app.openapi_schema = openapi_schema

    return lambda: app.openapi_schema
