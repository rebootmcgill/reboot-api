from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from machinerequests.models import CPU, OperatingSystem, Preset, Request, Machine
from django.contrib.auth.models import User
from rest_framework.decorators import list_route

# Data Serializers


class CPUSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CPU
        fields = ('url', 'name', 'cores', 'x64', 'clock')


class OperatingSystemSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ('url', 'name', 'version', 'experimental')


class PresetSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preset
        fields = ('url', 'cpu', 'ram', 'hdd')


class RequestSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = ('url', 'family_name', 'given_name', 'requester_type', 'faculty_and_dept', 'organization', 'preset',
            'os', 'machine_use', 'need_display', 'need_keyboard', 'need_mouse', 'need_ethernet', 'extra_information',
            'amount', 'filled', 'filled_at', 'requested_at')


class MachineSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ('url', 'request', 'fulfiller', 'cpu', 'ram', 'hdd', 'pickedup_at', 'notes', 'picked_up')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'is_staff')

# View Sets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer


class OperatingSystemViewSet(viewsets.ModelViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer


class PresetViewSet(viewsets.ModelViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @list_route
    def pending(self, request):
        queryset = Request.objects.filter(filled=False)
        page = self.paginate_queryset(queryset)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    @list_route
    def pending(self, request):
        Machine.objects.filter(picked_up=False)
        page = self.paginate_queryset(queryset)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

# The router routes all the routes

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cpus', CPUViewSet)
router.register(r'os', OperatingSystemViewSet)
router.register(r'presets', PresetViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'machines', MachineViewSet)



def get_router():
    return router