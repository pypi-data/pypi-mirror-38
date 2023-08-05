# zope.interface convenience imports
from .behaviors import IAsyncBehavior  # noqa
from .behaviors import IBehavior  # noqa
from .behaviors import IBehaviorAdapterFactory  # noqa
from .behaviors import IBehaviorSchemaAwareFactory  # noqa
from .behaviors import IContentBehavior  # noqa
from .catalog import ICatalogDataAdapter  # noqa
from .catalog import ICatalogUtility  # noqa
from .catalog import ISecurityInfo  # noqa
from .configuration import IDatabaseConfigurationFactory  # noqa
from .content import IAnnotationData  # noqa
from .content import IAnnotations  # noqa
from .content import IApplication  # noqa
from .content import IAsyncContainer  # noqa
from .content import IContainer  # noqa
from .content import IContentNegotiation  # noqa
from .content import IDatabase  # noqa
from .content import IFolder  # noqa
from .content import IGetOwner  # noqa
from .content import IGroupFolder  # noqa
from .content import IItem  # noqa
from .content import IJavaScriptApplication  # noqa
from .content import ILocation  # noqa
from .content import IRegistry  # noqa
from .content import IResource  # noqa
from .content import IResourceFactory  # noqa
from .content import IStaticDirectory  # noqa
from .content import IStaticFile  # noqa
from .content import ITraversable  # noqa
from .events import IBeforeObjectAddedEvent  # noqa
from .events import IBeforeObjectMovedEvent  # noqa
from .events import IBeforeObjectRemovedEvent  # noqa
from .events import IFileBeforeFinishUploaded  # noqa
from .events import IFileFinishUploaded  # noqa
from .events import IFileStartedUpload  # noqa
from .events import IFileUploadEvent  # noqa
from .events import INewUserAdded  # noqa
from .events import IObjectAddedEvent  # noqa
from .events import IObjectDuplicatedEvent  # noqa
from .events import IObjectLoadedEvent  # noqa
from .events import IObjectLocationEvent  # noqa
from .events import IObjectModifiedEvent  # noqa
from .events import IObjectMovedEvent  # noqa
from .events import IObjectPermissionsModifiedEvent  # noqa
from .events import IObjectPermissionsViewEvent  # noqa
from .events import IObjectRemovedEvent  # noqa
from .events import IObjectVisitedEvent  # noqa
from .exceptions import IErrorResponseException  # noqa
from .exceptions import IForbidden  # noqa
from .exceptions import IForbiddenAttribute  # noqa
from .exceptions import ISerializableException  # noqa
from .exceptions import IUnauthorized  # noqa
from .files import ICloudFileField  # noqa
from .files import IDBFile  # noqa
from .files import IDBFileField  # noqa
from .files import IFile  # noqa
from .files import IFileCleanup  # noqa
from .files import IFileField  # noqa
from .files import IFileManager  # noqa
from .files import IFileStorageManager  # noqa
from .files import IUploadDataManager  # noqa
from .json import IFactorySerializeToJson  # noqa
from .json import IJSONToValue  # noqa
from .json import IResourceDeserializeFromJson  # noqa
from .json import IResourceSerializeToJson  # noqa
from .json import IResourceSerializeToJsonSummary  # noqa
from .json import ISchemaFieldSerializeToJson  # noqa
from .json import ISchemaSerializeToJson  # noqa
from .json import IValueToJson  # noqa
from .layer import IDefaultLayer  # noqa
from .registry import IAddons  # noqa
from .registry import ILayers  # noqa
from .renderers import IRendererFormatHtml  # noqa
from .renderers import IRendererFormatJson  # noqa
from .renderers import IRendererFormatPlain  # noqa
from .renderers import IRendererFormatRaw  # noqa
from .renderers import IRenderFormats  # noqa
from .security import Allow  # noqa
from .security import AllowSingle  # noqa
from .security import Deny  # noqa
from .security import IGroups  # noqa
from .security import IInteraction  # noqa
from .security import IParticipation  # noqa
from .security import IPermission  # noqa
from .security import IPrincipal  # noqa
from .security import IPrincipalPermissionManager  # noqa
from .security import IPrincipalPermissionMap  # noqa
from .security import IPrincipalRoleManager  # noqa
from .security import IPrincipalRoleMap  # noqa
from .security import IRole  # noqa
from .security import IRolePermissionManager  # noqa
from .security import IRolePermissionMap  # noqa
from .security import ISecurityPolicy  # noqa
from .security import Public  # noqa
from .security import Unset  # noqa
from .types import IConstrainTypes  # noqa
from .views import ICONNECT  # noqa
from .views import IDELETE  # noqa
from .views import IDownloadView  # noqa
from .views import IGET  # noqa
from .views import IHEAD  # noqa
from .views import IOPTIONS  # noqa
from .views import IPATCH  # noqa
from .views import IPOST  # noqa
from .views import IPROPFIND  # noqa
from .views import IPUT  # noqa
from .views import IView  # noqa
from guillotina.i18n import MessageFactory
from zope.interface import Interface


_ = MessageFactory('guillotina')

DEFAULT_ADD_PERMISSION = 'guillotina.AddContent'
DEFAULT_READ_PERMISSION = 'guillotina.ViewContent'
DEFAULT_WRITE_PERMISSION = 'guillotina.ManageContent'

WRITING_VERBS = ['POST', 'PUT', 'PATCH', 'DELETE']

ACTIVE_LAYERS_KEY = 'guillotina.registry.ILayers.active_layers'
ADDONS_KEY = 'guillotina.registry.IAddons.enabled'

# Attributes not allowed in deserialization payloads
RESERVED_ATTRS = (
    '__name__',
    '__behaviors__',
    '__parent__',
    '__acl__',
    'id',
    'parent',
    'uuid',
    'type_name'
)

class IRequest(Interface):
    pass


class IResponse(Interface):

    def __init__(context, request):  # noqa: N805
        '''
        '''


class IFrameFormats(Interface):
    pass


class IFrameFormatsJson(IFrameFormats):
    pass


class ILanguage(Interface):
    pass


# Target interfaces on resolving

class IRendered(Interface):
    pass


class ITranslated(Interface):
    pass


# Get Absolute URL


class IAbsoluteURL(Interface):
    pass


# Addon interface

class IAddOn(Interface):

    def install(cls, container, request):  # noqa: N805
        '''
        '''

    def uninstall(cls, container, request):  # noqa: N805
        '''
        '''
